"""Weight of Evidence 3D scenes, built and rendered entirely from Python (Blender 5 bpy + Cycles).

    python scenes.py <scene> <out_dir> [--frames A:B] [--res 1920x1080] [--samples 32] [k=v ...]

Scenes:
  scale     The Scale: brass balance in a black void. k=v: tilt (deg, + tips right pan
            down), left/right (cards on each pan), anim=tip|settle|none, orbit (deg)
  brain     Stylized glass brain with the right orbitofrontal tumor. k=v: tumor (0..1
            size), glow (0..1), orbit (deg over the clip), view=front|side|three_q
  tower     Stylized tower silhouette at dawn (reconstruction, simplified massing).
            k=v: push (0..1 dolly over the clip)
  corridor  Hospital corridor at night, one failing light. k=v: flicker=1
  road      (Case 02) A divided arterial at night, simplified. k=v: view=push|top|median,
            dist (m, push), orbit (deg, top), exposure
  car       (Case 02) A generic test SUV with a roof lidar, black void. k=v: orbit (deg)
  sea       (Case 03) The South Atlantic with an empty 13-ft dinghy. k=v: view=dinghy|swell|
            storm|close|above, mood=dawn|dusk|grey|storm, sea=swell|calm|storm, speed, sun_az, flash
  book      (Case 04) A thick, closed, untitled book on a dark table under one key light. No
            pages are ever opened. k=v: mood=day|night, push (0..1 dolly over the clip)
  or        (Case 04) An empty operating room in near-darkness; the surgical lamp warms up
            over an empty table. k=v: warm (seconds for the lamp to come up), push (0..1)
  lot       (Case 05) A generic sedan alone in a store car park at dusk, one sodium lamp. No badge
            or plate. k=v: view=push|wide, push (0..1 dolly toward the driver's door handle)
  shelf     (Case 05) Steel shelving of plain archive boxes in a cold store, one box lit. No
            labels. k=v: push (0..1 dolly along the aisle)
  room      (Case 06) An empty precinct interview room at night, a 1980s video camera on a
            tripod aimed at an empty chair. No figures. k=v: view=push|camera, push (0..1)
  park      (Case 06) A park footpath at night under one old lamp, bare trees, a bench. No
            landmarks. k=v: push (0..1 drift along the path)
Each frame is written as <out_dir>/<scene>_####.png. Single stills: --frames 0:0.
Everything here is a reconstruction or a symbol and is tagged as such in the edit.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

FPS = 24


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    scene, out = a[0], a[1]
    opts = {"frames": "0:0", "res": "1920x1080", "samples": "32"}
    kv = {}
    i = 2
    while i < len(a):
        if a[i].startswith("--"):
            opts[a[i][2:]] = a[i + 1]
            i += 2
        else:
            k, v = a[i].split("=", 1)
            kv[k] = v
            i += 1
    return scene, out, opts, kv


# ---------------------------------------------------------------- common setup

def reset(res, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    w, h = (int(v) for v in res.split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.fps = FPS
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.0, 0.0, 0.0, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.0
    sc.world = world
    return sc


def mat_principled(name, color, metallic=0.0, rough=0.5, emission=None, strength=0.0,
                   alpha=1.0, transmission=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    b.inputs["Alpha"].default_value = alpha
    b.inputs["Transmission Weight"].default_value = transmission
    b.inputs["Coat Weight"].default_value = coat
    if emission:
        b.inputs["Emission Color"].default_value = (*emission, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def camera(loc, target, lens=50, name="Cam"):
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
    bpy.context.scene.collection.objects.link(cam)
    cam.location = loc
    cam.data.lens = lens
    cam.data.clip_end = 2000
    look_at(cam, target)
    bpy.context.scene.camera = cam
    return cam


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def area_light(loc, target, power, size=2.0, color=(1, 1, 1), name="Key"):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    look_at(obj, target)
    return obj


def spot(loc, target, power, angle=30, blend=0.4, color=(1, 1, 1), name="Spot"):
    data = bpy.data.lights.new(name, "SPOT")
    data.energy = power
    data.spot_size = math.radians(angle)
    data.spot_blend = blend
    data.color = color
    data.shadow_soft_size = 0.3
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    look_at(obj, target)
    return obj


def add(prim, name, **kw):
    getattr(bpy.ops.mesh, f"primitive_{prim}_add")(**kw)
    o = bpy.context.active_object
    o.name = name
    return o


def floor(color=(0.012, 0.012, 0.014), rough=0.22, size=60):
    f = add("plane", "Floor", size=size)
    assign(f, mat_principled("FloorMat", color, rough=rough, coat=0.3))
    return f


# ---------------------------------------------------------------- THE SCALE

def build_scale(kv):
    brass = mat_principled("Brass", (0.80, 0.58, 0.28), metallic=1.0, rough=0.28)
    dark = mat_principled("DarkBrass", (0.35, 0.24, 0.12), metallic=1.0, rough=0.4)
    paper = mat_principled("Card", (0.86, 0.82, 0.74), rough=0.75)
    floor()

    # Base: stepped round plinth, column, finial.
    b1 = smooth(add("cylinder", "Base1", radius=0.55, depth=0.06, location=(0, 0, 0.03), vertices=96))
    b2 = smooth(add("cylinder", "Base2", radius=0.40, depth=0.06, location=(0, 0, 0.09), vertices=96))
    col = smooth(add("cylinder", "Column", radius=0.045, depth=1.5, location=(0, 0, 0.87), vertices=48))
    fin = smooth(add("uv_sphere", "Finial", radius=0.07, location=(0, 0, 1.74), segments=48, ring_count=24))
    for o in (b1, b2, fin):
        assign(o, brass)
    assign(col, dark)

    # Beam rig: everything that tips is parented to an empty at the pivot.
    pivot = bpy.data.objects.new("Pivot", None)
    bpy.context.scene.collection.objects.link(pivot)
    pivot.location = (0, 0, 1.62)
    beam = smooth(add("cylinder", "Beam", radius=0.022, depth=1.6, location=(0, 0, 1.62), vertices=32,
                      rotation=(0, math.radians(90), 0)))
    hub = smooth(add("cylinder", "Hub", radius=0.06, depth=0.08, location=(0, 0, 1.62), vertices=48,
                     rotation=(math.radians(90), 0, 0)))
    needle = add("cone", "Needle", radius1=0.018, depth=0.32, location=(0, 0, 1.45), vertices=24,
                 rotation=(math.radians(180), 0, 0))
    for o in (beam, hub, needle):
        assign(o, brass)
        o.parent = pivot
        o.matrix_parent_inverse = pivot.matrix_world.inverted()

    pans = []
    for side, x in (("L", -0.78), ("R", 0.78)):
        tip = smooth(add("uv_sphere", f"Tip{side}", radius=0.035, location=(x, 0, 1.62)))
        assign(tip, brass)
        tip.parent = pivot
        tip.matrix_parent_inverse = pivot.matrix_world.inverted()
        # The hanger stays vertical while the beam tips: parent to an empty at the beam tip
        # whose rotation counters the pivot's (done per frame below).
        hang = bpy.data.objects.new(f"Hang{side}", None)
        bpy.context.scene.collection.objects.link(hang)
        hang.location = (x, 0, 1.62)
        hang.parent = pivot
        hang.matrix_parent_inverse = pivot.matrix_world.inverted()
        pan = smooth(add("uv_sphere", f"Pan{side}", radius=0.30, location=(x, 0, 0.92),
                         segments=96, ring_count=48))
        # flatten into a shallow dish: keep the lower cap only
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        for v in pan.data.vertices:
            v.select = v.co.z > -0.12
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.delete(type="VERT")
        bpy.ops.object.mode_set(mode="OBJECT")
        pan.scale = (1, 1, 0.55)
        sol = pan.modifiers.new("Thick", "SOLIDIFY")
        sol.thickness = 0.008
        assign(pan, brass)
        parts = [pan]
        for k in range(3):  # three suspension rods
            ang = k * 2 * math.pi / 3 + math.pi / 2
            px, py = x + 0.27 * math.cos(ang), 0.27 * math.sin(ang)
            top, bot = Vector((x, 0, 1.6)), Vector((px, py, 0.92 - 0.12 * 0.55 + 0.05))
            mid = (top + bot) / 2
            length = (top - bot).length
            rod = smooth(add("cylinder", f"Rod{side}{k}", radius=0.004, depth=length, location=mid, vertices=12))
            rod.rotation_euler = (top - bot).to_track_quat("Z", "Y").to_euler()
            assign(rod, dark)
            parts.append(rod)
        n = int(kv.get("left" if side == "L" else "right", 0))
        for c in range(n):  # stacked evidence cards
            card = add("cube", f"Card{side}{c}", size=1, location=(x + 0.01 * ((c * 7) % 3 - 1),
                                                                    0.012 * ((c * 5) % 3 - 1),
                                                                    0.92 - 0.12 * 0.55 + 0.012 + c * 0.012))
            card.scale = (0.30, 0.20, 0.004)
            card.rotation_euler = (0, 0, math.radians((c * 37) % 40 - 20))
            assign(card, paper)
            parts.append(card)
        for p in parts:
            p.parent = hang
            p.matrix_parent_inverse = hang.matrix_world.inverted()
        pans.append(hang)

    return pivot, pans


def animate_scale(pivot, pans, kv, f0, f1):
    """Tilt in degrees (+ tips the right pan down)."""
    tilt = float(kv.get("tilt", 0))
    mode = kv.get("anim", "none")
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        if mode == "tip":  # level -> tilt with a small overshoot
            e = 1 - math.exp(-5 * u) * math.cos(7 * u)
            a = tilt * e
        elif mode == "settle":  # swinging, damping to tilt
            a = tilt + 9 * math.exp(-4 * u) * math.cos(10 * u)
        else:
            a = tilt
        pivot.rotation_euler = (0, math.radians(a), 0)
        pivot.keyframe_insert("rotation_euler", frame=f)
        for h in pans:
            h.rotation_euler = (0, -math.radians(a), 0)
            h.keyframe_insert("rotation_euler", frame=f)


def scene_scale(kv, f0, f1):
    pivot, pans = build_scale(kv)
    orbit = float(kv.get("orbit", 0))
    cam = camera((0, -4.2, 1.35), (0, 0, 1.15), lens=50)
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        ang = math.radians(-orbit / 2 + orbit * u)
        cam.location = (4.2 * math.sin(ang), -4.2 * math.cos(ang), 1.35)
        look_at(cam, (0, 0, 1.15))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    animate_scale(pivot, pans, kv, f0, f1)
    spot((0.0, -0.4, 5.5), (0, 0, 1.1), 900, angle=34, blend=0.6, color=(1.0, 0.93, 0.82))
    area_light((-3, -2, 2.5), (0, 0, 1.2), 60, size=3, color=(0.55, 0.75, 1.0), name="Rim")
    area_light((3, 2.5, 2.0), (0, 0, 1.4), 90, size=2, color=(1, 0.85, 0.7), name="Back")


# ---------------------------------------------------------------- THE BRAIN

def scene_brain(kv, f0, f1):
    """Stylized brain: two displaced hemispheres, cerebellum, stem, in a cyan 'glass' look.
    The tumor sits in the right orbitofrontal region (front, low, the patient's right)."""
    glass = bpy.data.materials.new("Glass")
    glass.use_nodes = True
    nt = glass.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    emis = nt.nodes.new("ShaderNodeEmission")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    lw.inputs["Blend"].default_value = 0.35
    ramp.color_ramp.elements[0].position = 0.15
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.95
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    emis.inputs["Color"].default_value = (0.25, 0.75, 0.85, 1)
    emis.inputs["Strength"].default_value = 3.0
    nt.links.new(lw.outputs["Facing"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs["Fac"])
    nt.links.new(transp.outputs[0], mix.inputs[1])
    nt.links.new(emis.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])

    # Gyri: Voronoi distance-to-edge gives a network of ridges and furrows.
    tex = bpy.data.textures.new("Gyri", "VORONOI")
    tex.distance_metric = "DISTANCE"
    tex.color_mode = "INTENSITY"
    tex.noise_scale = 0.16
    tex.weight_1, tex.weight_2 = -1.0, 1.0  # F2 - F1: ridges along cell edges

    root = bpy.data.objects.new("BrainRoot", None)
    bpy.context.scene.collection.objects.link(root)
    for side, x in (("L", -0.36), ("R", 0.36)):
        h = add("uv_sphere", f"Hemi{side}", radius=1.0, location=(x, 0, 0), segments=128, ring_count=96)
        h.scale = (0.36, 0.86, 0.62)
        bpy.ops.object.transform_apply(scale=True)
        sub = h.modifiers.new("Sub", "SUBSURF")
        sub.levels = sub.render_levels = 1
        disp = h.modifiers.new("Gyri", "DISPLACE")
        disp.texture = tex
        disp.strength = 0.07
        disp.mid_level = 0.5
        smooth(h)
        assign(h, glass)
        h.parent = root
    cb = smooth(add("uv_sphere", "Cerebellum", radius=1.0, location=(0, 0.52, -0.42), segments=64, ring_count=32))
    cb.scale = (0.5, 0.3, 0.24)
    assign(cb, glass)
    cb.parent = root
    st = smooth(add("cylinder", "Stem", radius=0.11, depth=0.7, location=(0, 0.25, -0.75), vertices=32))
    st.rotation_euler = (math.radians(-20), 0, 0)
    assign(st, glass)
    st.parent = root

    size = float(kv.get("tumor", 1.0))
    glow = float(kv.get("glow", 1.0))
    if size > 0:
        tm = mat_principled("Tumor", (0.9, 0.35, 0.12), rough=0.6, emission=(1.0, 0.45, 0.15),
                            strength=1.6 * glow)
        # Front (-Y), low (-Z), the patient's right (+X when facing the camera at -Y... the
        # camera sits in front, so the patient's right appears on screen left: x < 0).
        site = (0.03, 0.05, -0.12) if kv.get("site") == "deep" else (-0.24, -0.58, -0.22)
        t = smooth(add("uv_sphere", "Tumor", radius=0.17 * size, location=site,
                       segments=48, ring_count=24))
        d = t.modifiers.new("Lumpy", "DISPLACE")
        d.texture = bpy.data.textures.new("Lump", "CLOUDS")
        d.texture.noise_scale = 0.12
        d.strength = 0.04
        assign(t, tm)
        t.parent = root
        pl = bpy.data.lights.new("TumorGlow", "POINT")
        pl.energy = 12 * glow * size
        pl.color = (1.0, 0.5, 0.2)
        pl.shadow_soft_size = 0.2
        po = bpy.data.objects.new("TumorGlow", pl)
        bpy.context.scene.collection.objects.link(po)
        po.location = site
        po.parent = root

    view = kv.get("view", "three_q")
    base = {"front": 0, "three_q": 50, "side": 90}[view]
    orbit = float(kv.get("orbit", 30))
    cam = camera((0, -4.6, 0.6), (0, 0, -0.05), lens=55)
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        ang = math.radians(base - orbit / 2 + orbit * u)
        cam.location = (-4.6 * math.sin(ang), -4.6 * math.cos(ang), 1.3)
        look_at(cam, (0, 0, -0.05))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    sc = bpy.context.scene
    sc.cycles.transparent_max_bounces = 24


# ---------------------------------------------------------------- THE TOWER

def scene_tower(kv, f0, f1):
    """Simplified massing of a campus tower at dawn: a long base block, a tall square shaft,
    an open colonnade level, a stepped crown and cupola. Approximate proportions only
    (overall ~94 m); it is a symbol, tagged RECONSTRUCTION. No people, no event depicted."""
    stone = mat_principled("Limestone", (0.78, 0.70, 0.58), rough=0.85)
    roof = mat_principled("Roof", (0.30, 0.20, 0.16), rough=0.7)
    win = mat_principled("Window", (0.02, 0.02, 0.025), rough=0.15, metallic=0.2)
    ground = add("plane", "Ground", size=1200)
    assign(ground, mat_principled("Lawn", (0.05, 0.06, 0.045), rough=0.95))

    def box(name, cx, cy, z0, sx, sy, sz, m=stone):
        o = add("cube", name, size=1, location=(cx, cy, z0 + sz / 2))
        o.scale = (sx, sy, sz)
        assign(o, m)
        return o

    box("Main", 0, 0, 0, 90, 26, 18)
    box("MainRoof", 0, 0, 18, 92, 28, 1.2, roof)
    box("Shaft", 0, 0, 0, 18, 18, 66)
    for i in range(14):  # vertical window slots on the two visible faces
        for j in range(3):
            box(f"WinF{i}{j}", -5 + j * 5, -9.05, 20 + i * 3.1, 1.6, 0.2, 2.0, win)
            box(f"WinS{i}{j}", -9.05, -5 + j * 5, 20 + i * 3.1, 0.2, 1.6, 2.0, win)
    box("Cornice", 0, 0, 66, 20, 20, 1.2)
    for k in range(4):  # colonnade: corner piers + columns, open between
        for c in range(5):
            t = -8 + c * 4
            pos = [(t, -8.6), (t, 8.6), (-8.6, t), (8.6, t)][k]
            col = smooth(add("cylinder", f"Col{k}{c}", radius=0.55, depth=9, location=(pos[0], pos[1], 67.2 + 4.5), vertices=24))
            assign(col, stone)
    box("Core", 0, 0, 67.2, 12, 12, 9, win)
    box("Entab", 0, 0, 76.2, 20, 20, 2.0)
    box("Crown1", 0, 0, 78.2, 15, 15, 5)
    box("Crown2", 0, 0, 83.2, 10, 10, 4)
    cup = smooth(add("cylinder", "Cupola", radius=3.6, depth=4.5, location=(0, 0, 89.4), vertices=8))
    assign(cup, stone)
    dome = smooth(add("cone", "Lantern", radius1=3.8, depth=3.6, location=(0, 0, 93.4), vertices=8))
    assign(dome, roof)
    for k in range(4):  # clock faces, one per side, unlit discs
        ang = k * math.pi / 2
        x, y = 10.15 * math.sin(ang), -10.15 * math.cos(ang)
        cl = add("cylinder", f"Clock{k}", radius=3.0, depth=0.3, location=(x, y, 80.7), vertices=48)
        cl.rotation_euler = (math.radians(90), 0, ang)
        assign(cl, mat_principled("ClockFace", (0.75, 0.72, 0.62), rough=0.4))

    sc = bpy.context.scene
    sky = sc.world.node_tree
    sky.nodes.clear()
    tc = sky.nodes.new("ShaderNodeTexCoord")
    sep = sky.nodes.new("ShaderNodeSeparateXYZ")
    rmp = sky.nodes.new("ShaderNodeValToRGB")
    bg = sky.nodes.new("ShaderNodeBackground")
    o = sky.nodes.new("ShaderNodeOutputWorld")
    el = rmp.color_ramp.elements
    el[0].position, el[0].color = 0.0, (0.55, 0.22, 0.08, 1)   # horizon ember
    el[1].position, el[1].color = 0.35, (0.012, 0.02, 0.06, 1)  # high, still night
    mid = el.new(0.08)
    mid.color = (0.22, 0.12, 0.14, 1)
    sky.links.new(tc.outputs["Generated"], sep.inputs[0])  # world: view direction
    sky.links.new(sep.outputs["Z"], rmp.inputs["Fac"])
    sky.links.new(rmp.outputs["Color"], bg.inputs[0])
    bg.inputs["Strength"].default_value = 1.0
    sky.links.new(bg.outputs[0], o.inputs[0])
    sun = bpy.data.lights.new("Sun", "SUN")
    sun.energy = 0.9
    sun.color = (1.0, 0.55, 0.32)
    sun.angle = math.radians(1.5)
    so = bpy.data.objects.new("Sun", sun)
    sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(87), 0, math.radians(110))
    push = float(kv.get("push", 0.15))
    cam = camera((-70, -190, 6), (0, 0, 52), lens=42)
    start = Vector((-70, -190, 6))
    end = start.lerp(Vector((0, 0, 52)), push)
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        u = u * u * (3 - 2 * u)
        cam.location = start.lerp(end, u)
        look_at(cam, (0, 0, 52))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = -0.3


# ---------------------------------------------------------------- THE CORRIDOR

def scene_corridor(kv, f0, f1):
    """A hospital corridor at night: glossy floor, ceiling panels, doors; one panel failing."""
    wall = mat_principled("Wall", (0.55, 0.60, 0.58), rough=0.6)
    flo = mat_principled("Vinyl", (0.18, 0.22, 0.21), rough=0.18, coat=0.5)
    door = mat_principled("Door", (0.30, 0.36, 0.38), rough=0.5)
    L = 40.0

    def box(name, cx, cy, cz, sx, sy, sz, m):
        o = add("cube", name, size=1, location=(cx, cy, cz))
        o.scale = (sx, sy, sz)
        assign(o, m)
        return o

    box("Floor", 0, L / 2, -0.05, 3.2, L, 0.1, flo)
    box("Ceil", 0, L / 2, 2.85, 3.2, L, 0.1, wall)
    box("WallL", -1.6, L / 2, 1.4, 0.1, L, 2.9, wall)
    box("WallR", 1.6, L / 2, 1.4, 0.1, L, 2.9, wall)
    box("End", 0, L, 1.4, 3.2, 0.1, 2.9, door)
    for i in range(10):
        y = 2 + i * 4
        for side in (-1.53, 1.53):
            if (i + (side > 0)) % 2 == 0:
                box(f"Door{i}{side}", side, y + 1.2, 1.05, 0.08, 1.1, 2.1, door)
        box(f"Rail{i}", -1.52, y, 0.95, 0.06, 3.6, 0.05, mat_principled("Rail", (0.7, 0.7, 0.68), metallic=0.8, rough=0.3))
    flicker = kv.get("flicker", "1") == "1"
    lights = []
    for i in range(9):
        y = 3 + i * 4.3
        m = mat_principled(f"Panel{i}", (1, 1, 1), emission=(0.85, 0.95, 1.0), strength=6.0)
        p = box(f"Panel{i}", 0, y, 2.79, 0.7, 1.4, 0.02, m)
        l = area_light((0, y, 2.75), (0, y, 0), 70, size=1.0, color=(0.85, 0.95, 1.0), name=f"PanelLight{i}")
        lights.append((m, l))
    cam = camera((0, -0.5, 1.55), (0, 30, 1.25), lens=32)
    bad_m, bad_l = lights[3]
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        cam.location = (0.05 * math.sin(f / 13.0), -0.5 + 3.0 * u, 1.55 + 0.012 * math.sin(f / 5.0))
        cam.keyframe_insert("location", frame=f)
        on = 1.0
        if flicker:
            on = 0.15 if ((f * 7) % 23 < 4 or (f * 3) % 31 < 2) else 1.0
        bad_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 6.0 * on
        bad_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
        bad_l.data.energy = 70 * on
        bad_l.data.keyframe_insert("energy", frame=f)


# ---------------------------------------------------------------- THE ROAD (Case 02)

def night_sky(sc, low=(0.035, 0.03, 0.05), high=(0.002, 0.003, 0.008)):
    sky = sc.world.node_tree
    sky.nodes.clear()
    tc = sky.nodes.new("ShaderNodeTexCoord")
    sep = sky.nodes.new("ShaderNodeSeparateXYZ")
    rmp = sky.nodes.new("ShaderNodeValToRGB")
    bg = sky.nodes.new("ShaderNodeBackground")
    o = sky.nodes.new("ShaderNodeOutputWorld")
    el = rmp.color_ramp.elements
    el[0].position, el[0].color = 0.0, (*low, 1)   # city glow at the horizon
    el[1].position, el[1].color = 0.25, (*high, 1)
    sky.links.new(tc.outputs["Generated"], sep.inputs[0])
    sky.links.new(sep.outputs["Z"], rmp.inputs["Fac"])
    sky.links.new(rmp.outputs["Color"], bg.inputs[0])
    bg.inputs["Strength"].default_value = 1.0
    sky.links.new(bg.outputs[0], o.inputs[0])


def build_road():
    """A divided four-lane arterial at night, simplified: two lanes each way, a bike lane,
    a raised landscaped median with an X-shaped paved path and a sign pointing pedestrians to
    the crosswalk, LED streetlights on the median. Generic massing; tagged RECONSTRUCTION.
    +Y is the direction of travel; northbound lanes are x in [0.5, 8.5]."""
    asphalt = mat_principled("Asphalt", (0.035, 0.035, 0.038), rough=0.55, coat=0.15)
    paint = mat_principled("Paint", (0.75, 0.74, 0.70), rough=0.6)
    yellow = mat_principled("Yellow", (0.75, 0.55, 0.12), rough=0.6)
    curb = mat_principled("Curb", (0.32, 0.31, 0.29), rough=0.8)
    brick = mat_principled("Brick", (0.34, 0.13, 0.08), rough=0.85)
    gravel = mat_principled("Gravel", (0.20, 0.17, 0.13), rough=0.95)
    shrub = mat_principled("Shrub", (0.03, 0.05, 0.03), rough=0.9)
    pole = mat_principled("Pole", (0.25, 0.26, 0.27), metallic=0.7, rough=0.4)
    L0, L1 = -120, 260

    def box(name, cx, cy, cz, sx, sy, sz, m):
        o = add("cube", name, size=1, location=(cx, cy, cz))
        o.scale = (sx, sy, sz)
        assign(o, m)
        return o

    MX0, MX1 = -21.1, 0.5  # median edges: 71 ft (21.6 m) wide
    MC = (MX0 + MX1) / 2
    box("Road", -11, (L0 + L1) / 2, -0.05, 44, L1 - L0, 0.1, asphalt)
    box("Verge", 0, (L0 + L1) / 2, -0.12, 220, L1 - L0, 0.1, mat_principled("Dirt", (0.05, 0.045, 0.04), rough=0.95))
    # median: raised 15 cm, decorative rock with shrubs; an X of brick paving around y=40
    box("Median", MC, (L0 + L1) / 2, 0.075, MX1 - MX0, L1 - L0, 0.15, gravel)
    for k, ang in enumerate((35.8, -35.8)):
        p = box(f"Path{k}", MC, 40, 0.16, 2.4, 36.5, 0.02, brick)
        p.rotation_euler = (0, 0, math.radians(ang))
    for k in range(70):
        y = L0 + 5 + (k * 37) % (L1 - L0 - 10)
        x = MX0 + 1.5 + ((k * 53) % 100) / 100 * (MX1 - MX0 - 3)
        if 18 < y < 62:
            continue
        sz = 0.5 + ((k * 17) % 10) / 20
        sh = smooth(add("uv_sphere", f"Shrub{k}", radius=sz, location=(x, y, 0.15 + sz * 0.5), segments=12, ring_count=8))
        sh.scale = (1, 1.2, 0.65)
        assign(sh, shrub)
    # curbs and lane paint (northbound side gets full detail; it is what the camera sees)
    box("CurbE", 9.0, (L0 + L1) / 2, 0.08, 0.3, L1 - L0, 0.16, curb)
    box("Edge", 8.4, (L0 + L1) / 2, 0.005, 0.12, L1 - L0, 0.01, paint)       # bike lane line
    box("YellowN", MX1 + 0.15, (L0 + L1) / 2, 0.005, 0.1, L1 - L0, 0.01, yellow)
    box("YellowS", MX0 - 0.15, (L0 + L1) / 2, 0.005, 0.1, L1 - L0, 0.01, yellow)
    for y in range(L0, L1, 12):
        box(f"Dash{y}", 4.5, y, 0.005, 0.12, 3.0, 0.01, paint)
        box(f"DashS{y}", MX0 - 4.2, y, 0.005, 0.12, 3.0, 0.01, paint)
    # sign at the path, facing the northbound lanes: "USE CROSSWALK" and an arrow
    SX, SY = -0.9, 33.0
    box("SignPost", SX - 0.06, SY, 1.1, 0.06, 0.06, 2.2, pole)  # behind the plate, away from the lanes
    box("SignPlate", SX, SY, 2.0, 0.04, 1.15, 0.8, mat_principled("SignWhite", (0.85, 0.85, 0.82), rough=0.5))
    ink = mat_principled("SignInk", (0.02, 0.02, 0.02), rough=0.6)
    for txt, z, size in (("USE", 2.2, 0.17), ("CROSSWALK", 1.98, 0.17), ("\u2192", 1.74, 0.26)):
        bpy.ops.object.text_add(location=(SX + 0.03, SY, z))
        t = bpy.context.active_object
        t.data.body = txt
        t.data.align_x = "CENTER"
        t.data.align_y = "CENTER"
        t.data.size = size
        t.rotation_euler = (math.radians(90), 0, math.radians(90))
        assign(t, ink)
    # streetlights along both median edges, each arm over its own carriageway
    lamp_m = mat_principled("Lamp", (1, 1, 1), emission=(1.0, 0.86, 0.62), strength=40)
    for i, y in enumerate(range(L0 + 10, L1, 38)):
        for side, px in ((1, MX1 - 0.8), (-1, MX0 + 0.8)):
            box(f"Pole{i}{side}", px, y, 4.5, 0.18, 0.18, 9.0, pole)
            box(f"Arm{i}{side}", px + side * 2.0, y, 8.9, 4.0, 0.12, 0.12, pole)
            box(f"Head{i}{side}", px + side * 3.8, y, 8.82, 0.7, 0.35, 0.08, lamp_m)
            data = bpy.data.lights.new(f"SL{i}{side}", "SPOT")
            data.energy = 9000
            data.spot_size = math.radians(115)
            data.spot_blend = 0.6
            data.color = (1.0, 0.82, 0.58)
            data.shadow_soft_size = 0.4
            o = bpy.data.objects.new(f"SL{i}{side}", data)
            bpy.context.scene.collection.objects.link(o)
            o.location = (px + side * 3.8, y, 8.6)
    # distant blocks on both sides, a few lit windows: reads as city, not as any real building
    for k in range(18):
        side = 1 if k % 2 else -1
        x = (12 if side > 0 else -34) + side * (28 + (k * 13) % 30)
        y = L0 + 30 + k * 24
        h = 6 + (k * 7) % 14
        box(f"Bldg{k}", x, y, h / 2, 14, 18, h, mat_principled(f"B{k}", (0.02, 0.02, 0.022), rough=0.9))
        if k % 3 == 0:
            box(f"BW{k}", x - side * 7.05, y, h * 0.6, 0.05, 3, 1.2, mat_principled(f"BW{k}", (1, 1, 1), emission=(1.0, 0.75, 0.45), strength=3))


def scene_road(kv, f0, f1):
    """Mill Avenue at night, simplified. view=push (driver's-eye dolly up the right lane, hood
    and A-pillars framing), top (high slow orbit over the median crossing), median (the sign
    and the paved path, slow push). Nothing moving on the road; no person, no car ahead."""
    sc = bpy.context.scene
    night_sky(sc)
    build_road()
    view = kv.get("view", "push")
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = float(kv.get("exposure", 0.4))
    if view == "push":
        start, end = Vector((6.6, -60, 1.3)), Vector((6.6, -60 + float(kv.get("dist", 70)), 1.3))
        cam = camera(start, (6.2, 60, 1.0), lens=28)
        # hood edge and A-pillars as black silhouettes parented to the camera
        blk = mat_principled("Cabin", (0.0, 0.0, 0.0), rough=1.0)
        hood = add("cube", "Hood", size=1, location=(0, -0.62, -0.95))
        hood.scale = (3.0, 0.5, 1.0)
        assign(hood, blk)
        hood.parent = cam
        for side in (-1, 1):
            p = add("cube", f"Pillar{side}", size=1, location=(side * 1.05, 0.0, -1.0))
            p.scale = (0.12, 2.5, 0.12)
            p.rotation_euler = (math.radians(-25), 0, math.radians(side * 30))
            assign(p, blk)
            p.parent = cam
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            cam.location = start.lerp(end, u)
            cam.location.z = 1.3 + 0.006 * math.sin(f / 4.0)
            cam.keyframe_insert("location", frame=f)
    elif view == "top":
        sc.view_settings.exposure = float(kv.get("exposure", 1.3))
        tgt = Vector((-6.0, 40, 0))
        cam = camera((40, -20, 50), tgt, lens=32)
        orbit = math.radians(float(kv.get("orbit", 25)))
        r = math.hypot(46, 60)
        a0 = math.atan2(-60, 46)
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            a = a0 + orbit * u
            cam.location = (tgt.x + r * math.cos(a), tgt.y + r * math.sin(a), 50 - 8 * u)
            look_at(cam, tgt)
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    else:  # median: low push toward the sign, across the paved X
        start, end = Vector((5.0, 27.0, 1.2)), Vector((2.6, 31.0, 1.4))
        cam = camera(start, (-0.9, 33.0, 1.7), lens=35)
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            u = u * u * (3 - 2 * u)
            cam.location = start.lerp(end, u)
            look_at(cam, (-0.9, 33.0, 1.8))
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE TEST CAR (Case 02)

# ---------------------------------------------------------------- car bodies (Cases 02, 05)

def rounded_box(name, loc, scale, m, bevel=0.15):
    o = add("cube", name, size=1, location=loc)
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    mod = o.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = 4
    assign(o, m)
    smooth(o)
    return o


def extruded_profile(name, pts, width, m, bevel=0.04):
    """Extrude a side profile [(y, z), ...] across x in [-width/2, width/2]."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    L = [bm.verts.new((-width / 2, y, z)) for y, z in pts]
    R = [bm.verts.new((width / 2, y, z)) for y, z in pts]
    bm.faces.new(L[::-1])
    bm.faces.new(R)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((L[i], L[j], R[j], R[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    mod = o.modifiers.new("Bevel", "BEVEL")
    mod.width = bevel
    mod.segments = 3
    mod.limit_method = "ANGLE"
    assign(o, m)
    return o


def scene_car(kv, f0, f1):
    """A generic test SUV, simplified (not a model of the actual vehicle): body, glasshouse,
    wheels, roof sensor rack with a spinning lidar puck. Black void, rim lights, slow orbit."""
    paint = mat_principled("Paint", (0.10, 0.105, 0.11), metallic=0.6, rough=0.25, coat=1.0)
    glass = mat_principled("Glass", (0.01, 0.01, 0.012), rough=0.05, metallic=0.3)
    rubber = mat_principled("Tyre", (0.02, 0.02, 0.02), rough=0.8)
    rack = mat_principled("Rack", (0.05, 0.05, 0.05), metallic=0.8, rough=0.3)
    floor(color=(0.008, 0.008, 0.01), rough=0.15)

    rbox, profile = rounded_box, extruded_profile

    # side profile of a generic mid-size SUV, metres; +Y is the front
    profile("Body", [(-2.45, 0.42), (2.42, 0.42), (2.48, 0.72), (2.35, 1.02), (1.30, 1.16),
                     (0.55, 1.74), (-1.95, 1.78), (-2.35, 1.40), (-2.48, 1.02)], 1.95, paint, 0.06)
    profile("Glass", [(-2.22, 1.18), (1.22, 1.18), (0.52, 1.70), (-1.92, 1.73), (-2.28, 1.38)], 1.97, glass, 0.02)
    for x in (-0.86, 0.86):
        for y in (-1.5, 1.45):
            w = add("cylinder", f"W{x}{y}", radius=0.38, depth=0.26, location=(x, y, 0.38), vertices=48)
            w.rotation_euler = (0, math.radians(90), 0)
            assign(w, rubber)
            hub = add("cylinder", f"H{x}{y}", radius=0.22, depth=0.27, location=(x, y, 0.38), vertices=32)
            hub.rotation_euler = (0, math.radians(90), 0)
            assign(hub, mat_principled("Rim", (0.5, 0.5, 0.52), metallic=1.0, rough=0.3))
    rbox("RackBase", (0, -0.5, 1.86), (1.3, 1.6, 0.12), rack, 0.04)
    puck = smooth(add("cylinder", "Lidar", radius=0.22, depth=0.28, location=(0, -0.3, 2.06), vertices=32))
    assign(puck, mat_principled("LidarMat", (0.05, 0.05, 0.06), metallic=0.5, rough=0.2,
                                emission=(0.25, 0.6, 1.0), strength=0.12))
    for k in range(6):  # side cameras on the rack
        c = add("cube", f"Cam{k}", size=1, location=((-0.6 + 0.24 * k), 0.32, 1.95))
        c.scale = (0.12, 0.1, 0.08)
        assign(c, rack)
    area_light((5, -6, 4), (0, 0, 1), 900, size=4, color=(0.75, 0.85, 1.0), name="Rim1")
    area_light((-6, 5, 3), (0, 0, 1), 700, size=4, color=(1.0, 0.85, 0.65), name="Rim2")
    area_light((0, 0, 7), (0, 0, 0), 150, size=6, name="Top")
    tgt = (0, 0, 1.0)
    cam = camera((7.5, -7.5, 2.4), tgt, lens=50)
    orbit = math.radians(float(kv.get("orbit", 30)))
    r = math.hypot(7.5, 7.5)
    a0 = math.atan2(-7.5, 7.5)
    for f in range(f0, f1 + 1):
        u = (f - f0) / max(1, f1 - f0)
        a = a0 + orbit * u
        cam.location = (r * math.cos(a), r * math.sin(a), 2.4)
        look_at(cam, tgt)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        puck.rotation_euler = (0, 0, f * 0.6)  # the lidar spins
        puck.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE SEA (Case 03)

MOODS = {  # horizon, low sky, zenith, sun (elevation deg, strength, colour, glow), exposure
    "dawn": ((0.36, 0.19, 0.085), (0.035, 0.027, 0.035), (0.004, 0.006, 0.014), (3.0, 3.0, (1.0, 0.66, 0.40), 1.0), -0.5),
    "dusk": ((0.28, 0.10, 0.06), (0.025, 0.017, 0.025), (0.003, 0.004, 0.010), (1.0, 1.6, (1.0, 0.46, 0.26), 0.9), -0.6),
    "grey": ((0.16, 0.17, 0.18), (0.08, 0.085, 0.095), (0.035, 0.04, 0.048), (25.0, 0.8, (0.85, 0.9, 1.0), 0.0), -0.7),
    "storm": ((0.016, 0.019, 0.026), (0.006, 0.008, 0.011), (0.002, 0.003, 0.004), (35.0, 0.35, (0.62, 0.72, 0.95), 0.0), 1.1),
    "day": ((0.42, 0.40, 0.36), (0.20, 0.21, 0.22), (0.06, 0.08, 0.13), (42.0, 3.2, (1.0, 0.88, 0.70), 0.5), -1.1),
}
SEAS = {  # wind m/s, wave scale, choppiness, alignment, foam coverage
    "swell": (16.0, 0.55, 0.6, 0.85, 0.0),
    "calm": (11.0, 0.4, 0.5, 0.8, 0.0),
    "storm": (26.0, 1.6, 1.4, 0.35, 0.45),
}
# The dinghy: 13 ft (3.96 m), beam and depth assumed for a ship's boat of that length.
BOAT_L, BOAT_B, BOAT_D = 3.96, 1.45, 0.55
SHEER = 0.22  # rise of the gunwale toward the bow


def sea_sky(sc, mood, sun_az):
    """Graded sky with a soft glow round the sun, and the sun itself as the single key."""
    hz, low, zen, (el, power, col, glow), exposure = MOODS[mood]
    nt = sc.world.node_tree
    nt.nodes.clear()
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    rmp = nt.nodes.new("ShaderNodeValToRGB")
    el_ = rmp.color_ramp.elements
    el_[0].position, el_[0].color = 0.0, (*hz, 1)
    el_[1].position, el_[1].color = 0.22, (*zen, 1)
    mid = el_.new(0.035)
    mid.color = (*low, 1)
    L(tc.outputs["Generated"], sep.inputs[0])
    L(sep.outputs["Z"], rmp.inputs["Fac"])
    sd = Vector((math.cos(math.radians(el)) * math.sin(sun_az), math.cos(math.radians(el)) * math.cos(sun_az),
                 math.sin(math.radians(el))))
    dot = nt.nodes.new("ShaderNodeVectorMath")
    dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = sd
    L(tc.outputs["Generated"], dot.inputs[0])
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = 90.0
    L(dot.outputs["Value"], pw.inputs[0])
    gl = nt.nodes.new("ShaderNodeMix")
    gl.data_type = "RGBA"
    gl.blend_type = "ADD"
    L(pw.outputs[0], gl.inputs["Factor"])
    L(rmp.outputs["Color"], gl.inputs["A"])
    gl.inputs["B"].default_value = (col[0] * glow, col[1] * glow, col[2] * glow, 1)
    bg = nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    L(gl.outputs["Result"], bg.inputs[0])
    L(bg.outputs[0], out.inputs[0])
    data = bpy.data.lights.new("Sun", "SUN")
    data.energy = power
    data.color = col
    data.angle = math.radians(1.2 if el < 10 else (8 if mood == "day" else 50))
    sun = bpy.data.objects.new("Sun", data)
    sc.collection.objects.link(sun)
    sun.rotation_euler = (-sd).to_track_quat("-Z", "Y").to_euler()
    sc.view_settings.exposure = exposure
    return bg, data


class NodeMath:
    """Tiny expression helper for shader math chains."""

    def __init__(self, nt):
        self.nt = nt

    def op(self, operation, a, b=None):
        n = self.nt.nodes.new("ShaderNodeMath")
        n.operation = operation
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                self.nt.links.new(v, n.inputs[i])
        return n.outputs[0]


def hull_halfwidth(s, z):
    """Hull half-width (m) at station s (0 stern .. 1 bow) and height z (boat coords)."""
    b = BOAT_B / 2 * math.sin(math.pi * (0.15 + 0.85 * s))
    sheer = SHEER * s * s
    k = (sheer - z) / BOAT_D
    return b * math.sqrt(max(0.0, 1 - k * k)), sheer


def water_material(name, rough, boat=None, foam=False, haze=None):
    """Dark sea water. haze=(colour, metres) fades it toward the horizon colour with distance,
    which is also what hides the seam where the swell tiles meet the flat far sea. With a
    boat, the surface is cut away inside the hull section, so the swell never shows through
    the floor of the boat."""
    m = mat_principled(name, (0.004, 0.010, 0.014), rough=rough)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["IOR"].default_value = 1.333
    # small ripples on top of the swell
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.12
    bump.inputs["Distance"].default_value = 0.03
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    if foam:
        at = nt.nodes.new("ShaderNodeAttribute")
        at.attribute_name = "foam"
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        mx.inputs["A"].default_value = (0.004, 0.010, 0.014, 1)
        mx.inputs["B"].default_value = (0.32, 0.36, 0.40, 1)
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.35
        nt.links.new(at.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], mx.inputs["Factor"])
        nt.links.new(mx.outputs["Result"], b.inputs["Base Color"])
    out = nt.nodes["Material Output"]
    surface = b.outputs["BSDF"]
    if haze is not None:
        M = NodeMath(nt)
        cd = nt.nodes.new("ShaderNodeCameraData")
        k = M.op("SUBTRACT", 1.0, M.op("EXPONENT", M.op("DIVIDE", M.op("MULTIPLY", cd.outputs["View Distance"], -1.0), haze[1])))
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (*haze[0], 1)
        hm = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(k, hm.inputs["Fac"])
        nt.links.new(surface, hm.inputs[1])
        nt.links.new(em.outputs["Emission"], hm.inputs[2])
        surface = hm.outputs["Shader"]
    if boat is not None:
        M = NodeMath(nt)
        bc = nt.nodes.new("ShaderNodeTexCoord")
        bc.object = boat
        sp = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(bc.outputs["Object"], sp.inputs[0])
        x, y, z = sp.outputs["X"], sp.outputs["Y"], sp.outputs["Z"]
        s = M.op("ADD", M.op("DIVIDE", y, BOAT_L), 0.5)
        bw = M.op("MULTIPLY", M.op("SINE", M.op("MULTIPLY", M.op("ADD", M.op("MULTIPLY", s, 0.85), 0.15), math.pi)), BOAT_B / 2)
        sheer = M.op("MULTIPLY", M.op("MULTIPLY", s, s), SHEER)
        k = M.op("DIVIDE", M.op("SUBTRACT", sheer, z), BOAT_D)
        hw = M.op("MULTIPLY", bw, M.op("SQRT", M.op("MAXIMUM", M.op("SUBTRACT", 1.0, M.op("MULTIPLY", k, k)), 0.0)))
        inside_x = M.op("LESS_THAN", M.op("ABSOLUTE", x), M.op("SUBTRACT", hw, 0.004))
        inside_s = M.op("MULTIPLY", M.op("GREATER_THAN", s, 0.0), M.op("LESS_THAN", s, 1.0))
        under = M.op("LESS_THAN", z, sheer)
        inside = M.op("MULTIPLY", M.op("MULTIPLY", inside_x, inside_s), under)
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(inside, mix.inputs["Fac"])
        nt.links.new(surface, mix.inputs[1])
        nt.links.new(tr.outputs["BSDF"], mix.inputs[2])
        surface = mix.outputs["Shader"]
    nt.links.new(surface, out.inputs["Surface"])
    return m, nz


def build_ocean(kv, f0, f1, boat=None, res=12, haze=None):
    sea = kv.get("sea", "swell")
    wind, scale, chop, align, foam = SEAS[sea]
    speed = float(kv.get("speed", 1.0))
    bpy.ops.mesh.primitive_plane_add(size=2)
    ocean = bpy.context.active_object
    ocean.name = "Ocean"
    o = ocean.modifiers.new("Ocean", "OCEAN")
    o.geometry_mode = "GENERATE"
    o.spatial_size = 60
    o.repeat_x = o.repeat_y = int(kv.get("tiles", 9))
    off = -(o.repeat_x - 1) / 2 * o.spatial_size  # repeats grow toward +x/+y; centre them
    ocean.location = (off, off, 0)
    o.resolution = o.viewport_resolution = res
    o.wind_velocity = wind
    o.wave_scale = scale
    o.choppiness = chop
    o.wave_alignment = align
    o.wave_direction = math.radians(float(kv.get("wave_dir", 20)))
    o.random_seed = int(kv.get("seed", 7))
    o.use_normals = True
    if foam:
        o.use_foam = True
        o.foam_coverage = foam
        o.foam_layer_name = "foam"
    rough = 0.05 if sea != "storm" else 0.12
    mat, nz = water_material("Water", rough, boat=boat, foam=bool(foam), haze=haze)
    assign(ocean, mat)
    smooth(ocean)
    for f in range(f0, f1 + 1):
        o.time = 10.0 + f / FPS * speed
        o.keyframe_insert("time", frame=f)
        nz.inputs["W"].default_value = f / FPS * 0.35 * speed
        nz.inputs["W"].keyframe_insert("default_value", frame=f)
    # flat sea from the edge of the tiles to the horizon: a square hole that meets the tiles
    # exactly, so the two never overlap
    import bmesh
    me = bpy.data.meshes.new("FarSea")
    bm = bmesh.new()
    a, z = o.spatial_size * o.repeat_x / 2, 0.0
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    inner = [bm.verts.new((a * cx, a * cy, z)) for cx, cy in corners]
    outer = [bm.verts.new((4000 * cx, 4000 * cy, z)) for cx, cy in corners]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((inner[i], inner[j], outer[j], outer[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    far = bpy.data.objects.new("FarSea", me)
    bpy.context.scene.collection.objects.link(far)
    far_mat, fnz = water_material("FarWater", rough + 0.22, haze=haze)  # rougher: averages the waves it stands in for
    assign(far, far_mat)
    return ocean


def build_dinghy(props=False):
    """An open 13-ft ship's boat, simplified: lofted round-bilge hull with a small transom,
    gunwale rail, two thwarts and bottom boards. Generic; nothing here is from a plan."""
    import bmesh
    wood = mat_principled("Wood", (0.15, 0.095, 0.055), rough=0.7)
    nt = wood.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave")  # clinker plank lines along the hull
    wv.wave_type = "BANDS"
    wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 9.0
    wv.inputs["Distortion"].default_value = 0.0
    wv.inputs["Detail"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    mp = nt.nodes.new("ShaderNodeMapping")  # grain: noise stretched along the boat
    mp.inputs["Scale"].default_value = (30.0, 0.6, 30.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    gr = nt.nodes.new("ShaderNodeTexNoise")
    gr.inputs["Scale"].default_value = 3.0
    gr.inputs["Detail"].default_value = 8.0
    nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
    col = nt.nodes.new("ShaderNodeValToRGB")
    col.color_ramp.elements[0].color = (0.07, 0.045, 0.028, 1)
    col.color_ramp.elements[1].color = (0.24, 0.17, 0.105, 1)
    nt.links.new(gr.outputs["Fac"], col.inputs["Fac"])
    nt.links.new(col.outputs["Color"], bsdf.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.4
    bump.inputs["Distance"].default_value = 0.003
    nt.links.new(wv.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    rail_m = mat_principled("Rail", (0.07, 0.045, 0.03), rough=0.5)
    me = bpy.data.meshes.new("Hull")
    bm = bmesh.new()
    NS, NT = 28, 18
    rows = []
    for i in range(NS + 1):
        s = i / NS
        b = BOAT_B / 2 * math.sin(math.pi * (0.15 + 0.85 * s))
        sheer = SHEER * s * s
        y = (s - 0.5) * BOAT_L
        row = []
        for j in range(NT + 1):
            th = -math.pi / 2 + math.pi * j / NT
            row.append(bm.verts.new((b * math.sin(th), y, sheer - BOAT_D * math.cos(th))))
        rows.append(row)
    for i in range(NS):
        for j in range(NT):
            bm.faces.new((rows[i][j], rows[i + 1][j], rows[i + 1][j + 1], rows[i][j + 1]))
    bm.faces.new(rows[0])  # transom
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    hull = bpy.data.objects.new("Dinghy", me)
    bpy.context.scene.collection.objects.link(hull)
    sol = hull.modifiers.new("Solid", "SOLIDIFY")
    sol.thickness = 0.016
    sol.offset = -1
    assign(hull, wood)
    smooth(hull)
    # gunwale rail along the sheer, both sides
    cu = bpy.data.curves.new("Gunwale", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.024
    cu.bevel_resolution = 2
    for side in (-1, 1):
        sp = cu.splines.new("POLY")
        pts = []
        for i in range(NS + 1):
            s = i / NS
            hw, sheer = hull_halfwidth(s, SHEER * s * s)
            pts.append((side * hw, (s - 0.5) * BOAT_L, sheer))
        sp.points.add(len(pts) - 1)
        for p, c in zip(sp.points, pts):
            p.co = (*c, 1)
    rail = bpy.data.objects.new("Gunwale", cu)
    bpy.context.scene.collection.objects.link(rail)
    rail.data.materials.append(rail_m)
    rail.parent = hull
    parts = [rail]

    def box(name, loc, size, m):
        o = add("cube", name, size=1, location=loc)
        o.scale = size
        bpy.ops.object.transform_apply(scale=True)
        bv = o.modifiers.new("Bevel", "BEVEL")
        bv.width = 0.006
        bv.segments = 2
        assign(o, m)
        o.parent = hull
        parts.append(o)
        return o

    for s in (0.28, 0.62):  # thwarts
        z = SHEER * s * s - 0.2
        hw, _ = hull_halfwidth(s, z)
        box(f"Thwart{s}", (0, (s - 0.5) * BOAT_L, z), (2 * hw - 0.02, 0.2, 0.03), wood)
    for k in range(5):  # bottom boards
        s = 0.18 + 0.13 * k
        z = SHEER * s * s - BOAT_D + 0.07
        hw, _ = hull_halfwidth(s, z)
        box(f"Board{k}", (0, (s - 0.5) * BOAT_L, z), (2 * hw - 0.03, 0.42, 0.02), wood)
    if props:
        # a sodden oilskin left on the stern sheets, aft of the thwart
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=40, size=1, location=(-0.12, (0.16 - 0.5) * BOAT_L, -0.30))
        sk = bpy.context.active_object
        sk.name = "Oilskin"
        sk.scale = (0.7, 0.55, 1)
        sk.rotation_euler = (math.radians(4), math.radians(10), math.radians(-18))
        tex = bpy.data.textures.new("Folds", "CLOUDS")
        tex.noise_scale = 0.32  # a few broad folds, not bubbles
        tex.noise_depth = 1
        d = sk.modifiers.new("Folds", "DISPLACE")
        d.texture = tex
        d.strength = 0.15
        sk.modifiers.new("Thick", "SOLIDIFY").thickness = 0.004
        assign(sk, mat_principled("OilskinMat", (0.13, 0.095, 0.03), rough=0.38, coat=0.5))
        smooth(sk)
        sk.parent = hull
        parts.append(sk)
    return hull


def float_boat(hull, ocean, f0, f1, at=(0.0, 0.0), heading=0.0, damp=1.0, freeboard=0.30):
    """Sit the boat on the swell: sample the evaluated ocean under bow, stern and both sides
    every frame, then pitch, roll and heave to match (lightly smoothed)."""
    import numpy as np
    sc = bpy.context.scene
    ch, sh = math.cos(heading), math.sin(heading)

    def local(dx, dy):
        return (at[0] + dx * ch - dy * sh, at[1] + dx * sh + dy * ch)

    probes = {"c": local(0, 0), "bow": local(0, 1.6), "stern": local(0, -1.6),
              "port": local(-0.6, 0), "stb": local(0.6, 0)}
    raw = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        me = ocean.evaluated_get(dg).to_mesh()
        co = np.empty(len(me.vertices) * 3, np.float32)
        me.vertices.foreach_get("co", co)
        ocean.evaluated_get(dg).to_mesh_clear()
        co = co.reshape(-1, 3) + np.array([ocean.location.x, ocean.location.y, 0.0], np.float32)
        pts = co[(np.abs(co[:, 0] - at[0]) < 5) & (np.abs(co[:, 1] - at[1]) < 5)]
        h = {}
        for k, (x, y) in probes.items():  # mean height of the 4 nearest displaced vertices
            d2 = (pts[:, 0] - x) ** 2 + (pts[:, 1] - y) ** 2
            h[k] = float(pts[np.argpartition(d2, 4)[:4], 2].mean())
        raw.append(h)
    n = len(raw)
    for idx, f in enumerate(range(f0, f1 + 1)):
        win = raw[max(0, idx - 3): min(n, idx + 4)]
        avg = {k: sum(w[k] for w in win) / len(win) for k in raw[0]}
        pitch = math.atan2(avg["bow"] - avg["stern"], 3.2) * damp
        roll = math.atan2(avg["port"] - avg["stb"], 1.2) * damp
        hull.location = (at[0], at[1], avg["c"] * damp + freeboard)
        hull.rotation_euler = (pitch, -roll, heading)
        hull.keyframe_insert("location", frame=f)
        hull.keyframe_insert("rotation_euler", frame=f)


def scene_sea(kv, f0, f1):
    """The South Atlantic, a reconstruction. view=dinghy (the empty boat, small, riding a long
    swell into a low sun), swell (open ocean, no boat), storm (night, heavy breaking sea),
    close (low over the gunwale, inside the empty boat), above (thumbnail: from high above). k=v: mood=dawn|dusk|grey|storm,
    sea=swell|calm|storm, speed (wave time scale), seed."""
    sc = bpy.context.scene
    view = kv.get("view", "dinghy")
    mood = kv.get("mood", {"storm": "storm", "swell": "grey", "close": "day"}.get(view, "dawn"))
    if view == "storm":
        kv.setdefault("sea", "storm")
    sc.cycles.max_bounces = 4
    # sun azimuth from +Y: ahead of the camera for the glint path; behind it when overcast
    sun_az = math.radians(float(kv.get("sun_az", 200 if mood == "grey" else 8)))
    bg, sun = sea_sky(sc, mood, sun_az)
    haze = (MOODS[mood][0], float(kv.get("haze", 1100)))
    boat = None
    if view in ("dinghy", "close", "above"):
        boat = build_dinghy(props=view != "dinghy")
    ocean = build_ocean(kv, f0, f1, boat=boat, res=16 if view == "close" else 12, haze=haze)
    if "exposure" in kv:
        sc.view_settings.exposure = float(kv["exposure"])
    if boat is not None:
        float_boat(boat, ocean, f0, f1, heading=math.radians(float(kv.get("heading", 35))),
                   damp=0.75 if view == "close" else 1.0)
    if view == "dinghy":
        tgt = Vector((0, 0, 0.4))
        # boat in the lower right third, the sun's path to its left, horizon high in frame
        start, end = Vector((-12.0, -30.0, 6.0)), Vector((-9.0, -27.5, 5.6))
        aim = Vector((10.4, 48.9, -3.06))
        cam = camera(start, tgt, lens=40)
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            u = u * u * (3 - 2 * u)
            cam.location = start.lerp(end, u)
            look_at(cam, cam.location + aim)
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    elif view == "close":
        cam = camera((0, 0, 0), (0, 1, 0), lens=26)
        cam.parent = boat
        cam.rotation_euler = (math.radians(62), 0, math.radians(16))  # down into the boat, toward the bow
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            cam.location = (0.62 - 0.08 * u, -2.2 + 0.3 * u, 0.62)  # boat coords: off the starboard quarter
            cam.keyframe_insert("location", frame=f)
        tin = smooth(add("cylinder", "Tin", radius=0.055, depth=0.11, vertices=32))
        assign(tin, mat_principled("TinMat", (0.55, 0.51, 0.46), metallic=1.0, rough=0.35))
        tin.parent = boat
        s_tin = 0.44  # on the bottom boards, between the thwarts
        z_tin = SHEER * s_tin * s_tin - BOAT_D + 0.08 + 0.055
        for f in range(f0, f1 + 1):  # rolls across the bottom boards as the boat rolls
            x = 0.16 * math.sin(2 * math.pi * f / 120.0)
            tin.location = (x, (s_tin - 0.5) * BOAT_L, z_tin)
            tin.rotation_euler = (0, math.radians(90), x / 0.055)
            tin.keyframe_insert("location", frame=f)
            tin.keyframe_insert("rotation_euler", frame=f)
    elif view == "above":  # thumbnail: the boat from high above, small, lower left
        camera((-3.0, -12.0, 24.0), (2.6, 0.6, 0.0), lens=50)
    else:  # swell / storm: open water, slow pan along the horizon
        h = 2.2 if view == "storm" else 4.0
        lens = 28 if view == "storm" else 35
        cam = camera((0, -30, h), (0, 60, h - 6), lens=lens)
        pan = math.radians(float(kv.get("pan", 10)))
        for f in range(f0, f1 + 1):
            u = (f - f0) / max(1, f1 - f0)
            a = -pan / 2 + pan * u
            cam.location = (0, -30, h + (0.25 * math.sin(f / 30.0) if view == "storm" else 0))
            look_at(cam, (60 * math.sin(a), -30 + 60 * math.cos(a), h - (4.0 if view == "storm" else 5.0)))
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
    if view == "storm" and "flash" in kv:  # one distant lightning flash
        fl = int(kv["flash"])
        for f, k in ((fl - 1, 1.0), (fl, 9.0), (fl + 1, 3.0), (fl + 3, 6.0), (fl + 6, 1.0)):
            bg.inputs["Strength"].default_value = k
            bg.inputs["Strength"].keyframe_insert("default_value", frame=f)


# ---------------------------------------------------------------- THE BOOK (Case 04)

def scene_book(kv, f0, f1):
    """A thick closed book, untitled, on a dark table. Never opened: no plate is ever shown."""
    night = kv.get("mood", "day") == "night"
    push = float(kv.get("push", "0.25"))
    wood = mat_principled("Table", (0.035, 0.022, 0.015), rough=0.38, coat=0.25)
    cloth = mat_principled("Cloth", (0.055, 0.05, 0.048), rough=0.75)
    pages = mat_principled("Pages", (0.62, 0.57, 0.47), rough=0.9)
    spine_band = mat_principled("Band", (0.80, 0.58, 0.28), metallic=1.0, rough=0.35)
    t = add("cube", "Table", size=1, location=(0, 0, -0.03))
    t.scale = (3.2, 2.0, 0.06)
    assign(t, wood)
    # the book: page block inside two boards and a rounded spine
    W, D, H = 0.30, 0.40, 0.085
    rot = math.radians(-14)

    def part(name, loc, scale, m):
        o = add("cube", name, size=1, location=loc)
        o.scale = scale
        assign(o, m)
        bpy.ops.object.modifier_add(type="BEVEL")
        o.modifiers["Bevel"].width = 0.003
        o.modifiers["Bevel"].segments = 2
        return o

    parts = [part("Block", (0.006, 0, H / 2), (W - 0.012, D - 0.012, H - 0.012), pages),
             part("BoardBot", (0, 0, 0.003), (W, D, 0.006), cloth),
             part("BoardTop", (0, 0, H - 0.003), (W, D, 0.006), cloth)]
    sp = add("cylinder", "Spine", radius=H / 2, depth=D, location=(-W / 2, 0, H / 2),
             rotation=(math.radians(90), 0, 0), vertices=32)
    assign(sp, cloth)
    smooth(sp)
    parts.append(sp)
    for i, y in enumerate((-0.13, 0.13)):  # two dull brass bands on the spine, no lettering
        b = add("cylinder", f"Band{i}", radius=H / 2 + 0.0015, depth=0.008, location=(-W / 2, y, H / 2),
                rotation=(math.radians(90), 0, 0), vertices=32)
        assign(b, spine_band)
        parts.append(b)
    pivot = bpy.data.objects.new("BookPivot", None)
    bpy.context.scene.collection.objects.link(pivot)
    for o in parts:
        o.parent = pivot
    pivot.rotation_euler = (0, 0, rot)
    if night:
        spot((-0.9, -0.5, 1.1), (0, 0, 0.02), 220, angle=34, blend=0.7, color=(1.0, 0.72, 0.45), name="Key")
        area_light((1.2, 1.4, 0.8), (0, 0, 0), 4, size=2.0, color=(0.45, 0.55, 0.75), name="Fill")
    else:
        spot((-0.5, -0.3, 1.5), (0, 0, 0.02), 340, angle=30, blend=0.6, color=(1.0, 0.86, 0.68), name="Key")
        area_light((1.0, 1.2, 1.0), (0, 0, 0), 8, size=2.0, color=(0.6, 0.7, 0.85), name="Fill")
    cam = camera((0.0, -1.15, 0.62), (0.0, 0.0, 0.03), lens=55)
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        k = 1.0 - push * u
        cam.location = (0.08 * math.sin(u * 0.8), -1.15 * k, 0.15 + 0.47 * k)
        look_at(cam, (0.0, 0.0, 0.03))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


def G_ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ---------------------------------------------------------------- THE OPERATING ROOM (Case 04)

def scene_or(kv, f0, f1):
    """An empty operating room in near-darkness; the lamp over the table warms up."""
    warm = float(kv.get("warm", "2.5")) * FPS
    push = float(kv.get("push", "0.2"))
    flo = mat_principled("ORFloor", (0.10, 0.13, 0.13), rough=0.45, coat=0.1)
    wall = mat_principled("ORWall", (0.16, 0.22, 0.22), rough=0.6)
    steel = mat_principled("Steel", (0.62, 0.64, 0.66), metallic=1.0, rough=0.25)
    pad = mat_principled("Pad", (0.06, 0.09, 0.10), rough=0.55)

    def box(name, loc, scale, m):
        o = add("cube", name, size=1, location=loc)
        o.scale = scale
        assign(o, m)
        return o

    box("Floor", (0, 0, -0.05), (9, 9, 0.1), flo)
    box("WallB", (0, 3.5, 1.6), (9, 0.1, 3.4), wall)
    box("WallL", (-3.5, 0, 1.6), (0.1, 9, 3.4), wall)
    box("WallR", (3.5, 0, 1.6), (0.1, 9, 3.4), wall)
    box("Ceil", (0, 0, 3.2), (9, 9, 0.1), wall)
    # table: column, base, slab, pad
    box("Base", (0, 0, 0.05), (0.7, 0.45, 0.1), steel)
    col = add("cylinder", "Column", radius=0.11, depth=0.7, location=(0, 0, 0.45))
    assign(col, steel)
    box("Slab", (0, 0, 0.83), (0.6, 2.0, 0.06), steel)
    p = box("TablePad", (0, 0, 0.89), (0.56, 1.96, 0.06), pad)
    bpy.ops.object.modifier_add(type="BEVEL")
    p.modifiers["Bevel"].width = 0.02
    # lamp: ceiling mount, arm, dish head with an emissive ring
    box("Mount", (0.0, 0.6, 3.1), (0.25, 0.25, 0.12), steel)
    box("Arm", (0.0, 0.3, 2.75), (0.06, 0.06, 0.7), steel)
    head = add("cylinder", "Head", radius=0.38, depth=0.12, location=(0.0, 0.0, 2.35), vertices=48)
    assign(head, steel)
    smooth(head)
    glow = mat_principled("LampGlow", (1, 1, 1), emission=(1.0, 0.96, 0.88), strength=0.0)
    lens = add("cylinder", "Lens", radius=0.33, depth=0.02, location=(0.0, 0.0, 2.285), vertices=48)
    assign(lens, glow)
    key = spot((0.0, 0.0, 2.27), (0.0, 0.0, 0.9), 0.0, angle=34, blend=0.5, color=(1.0, 0.96, 0.88), name="Lamp")
    # one dim cyan monitor at the back, off-axis
    mon = mat_principled("Monitor", (0.02, 0.02, 0.02), emission=(0.38, 0.78, 0.84), strength=0.6)
    box("Screen", (-2.2, 3.42, 1.7), (0.7, 0.04, 0.45), mon)
    # cool fill so the room reads before the lamp comes up; a wash on the back wall for depth
    area_light((0, -3, 2.6), (0, 0, 0.8), 70, size=3.0, color=(0.5, 0.65, 0.75), name="Ambient")
    area_light((0, 1.6, 3.0), (0, 3.5, 1.2), 45, size=4.0, color=(0.45, 0.62, 0.70), name="Wash")
    area_light((0, 2.4, 1.6), (0, 0, 0.9), 25, size=1.2, color=(0.55, 0.70, 0.80), name="Rim")
    cam = camera((1.9, -3.1, 1.35), (0.0, 0.1, 1.55), lens=30)
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        on = 1.0 if warm <= 0 else G_ease((f - f0) / warm)
        b = glow.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        b.default_value = 30.0 * on
        b.keyframe_insert("default_value", frame=f)
        key.data.energy = 2600 * on
        key.data.keyframe_insert("energy", frame=f)
        k = 1.0 - push * u
        cam.location = (1.9 * k, -3.1 * k, 1.35 - 0.05 * u)
        look_at(cam, (0.0, 0.1, 1.55))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE CAR PARK (Case 05)

def scene_lot(kv, f0, f1):
    """A generic sedan, alone in a store car park at dusk under one sodium lamp. Not a model of
    any real car: no badge, no plate. view=push (slow dolly toward the driver's door handle) or
    wide (static, high three-quarter)."""
    sc = bpy.context.scene
    night_sky(sc, low=(0.16, 0.07, 0.035), high=(0.004, 0.006, 0.016))
    asphalt = mat_principled("Asphalt", (0.035, 0.035, 0.038), rough=0.55, coat=0.15)
    paintline = mat_principled("Line", (0.55, 0.53, 0.48), rough=0.6)
    paint = mat_principled("Paint", (0.05, 0.065, 0.09), metallic=0.6, rough=0.3, coat=1.0)
    glass = mat_principled("Glass", (0.01, 0.01, 0.012), rough=0.05, metallic=0.3)
    rubber = mat_principled("Tyre", (0.02, 0.02, 0.02), rough=0.8)
    chrome = mat_principled("Handle", (0.55, 0.55, 0.57), metallic=1.0, rough=0.2)
    pole = mat_principled("Pole", (0.25, 0.25, 0.26), metallic=0.7, rough=0.4)
    g = add("plane", "Lot", size=80)
    assign(g, asphalt)
    for k in range(-4, 6):  # parking bay lines
        ln = add("cube", f"Bay{k}", size=1, location=(k * 2.7 - 1.35, 0.0, 0.003))
        ln.scale = (0.1, 5.2, 0.005)
        assign(ln, paintline)
    # a low sedan side profile, metres; +Y is the front
    extruded_profile("Body", [(-2.35, 0.36), (2.30, 0.36), (2.38, 0.62), (2.20, 0.82), (0.95, 0.92),
                              (0.35, 1.38), (-1.15, 1.40), (-1.90, 1.00), (-2.38, 0.86)], 1.82, paint, 0.06)
    extruded_profile("Glass", [(-1.80, 0.98), (0.90, 0.95), (0.33, 1.34), (-1.12, 1.36)], 1.84, glass, 0.02)
    for x in (-0.80, 0.80):
        for y in (-1.45, 1.40):
            w = add("cylinder", f"W{x}{y}", radius=0.33, depth=0.24, location=(x, y, 0.33), vertices=48)
            w.rotation_euler = (0, math.radians(90), 0)
            assign(w, rubber)
            hub = add("cylinder", f"H{x}{y}", radius=0.2, depth=0.25, location=(x, y, 0.33), vertices=32)
            hub.rotation_euler = (0, math.radians(90), 0)
            assign(hub, mat_principled("Rim", (0.5, 0.5, 0.52), metallic=1.0, rough=0.3))
    handle = rounded_box("DoorHandle", (0.925, 0.05, 0.86), (0.04, 0.26, 0.05), chrome, 0.015)
    # lamp post with a sodium head, behind and to the left
    post = add("cylinder", "Post", radius=0.09, depth=7.0, location=(5.5, 4.0, 3.5), vertices=16)
    assign(post, pole)
    head = rounded_box("LampHead", (5.0, 4.0, 7.0), (1.2, 0.5, 0.18), pole, 0.05)
    spot((4.6, 4.0, 6.85), (0.4, 0.0, 0.3), 9000, angle=80, blend=0.6, color=(1.0, 0.62, 0.28), name="Sodium")
    glow = mat_principled("SodiumGlow", (1, 1, 1), emission=(1.0, 0.62, 0.28), strength=8.0)
    lens = add("cube", "LampLens", size=1, location=(5.0, 4.0, 6.9))
    lens.scale = (1.0, 0.4, 0.02)
    assign(lens, glow)
    area_light((8, -10, 6), (0, 0, 1), 300, size=8, color=(0.45, 0.55, 0.75), name="SkyFill")
    area_light((6, -2, 1.5), (0.9, 0.05, 0.8), 120, size=3, color=(1.0, 0.75, 0.5), name="DoorFill")
    view = kv.get("view", "push")
    push = float(kv.get("push", "0.45"))
    tgt = (0.9, 0.05, 0.8)
    if view == "wide":
        cam = camera((9.5, -8.0, 4.2), (0.0, 0.5, 0.6), lens=35)
        for f in range(f0, f1 + 1):  # slow sideways drift
            u = G_ease((f - f0) / max(1, f1 - f0))
            cam.location = (9.5 - 2.0 * u, -8.0 - 1.0 * u, 4.2)
            look_at(cam, (0.0, 0.5, 0.6))
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
        return
    cam = camera((6.5, -3.5, 1.3), tgt, lens=45)
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        k = 1.0 - push * u
        cam.location = (0.9 + 5.6 * k, 0.05 - 3.55 * k, 0.95 + 0.35 * k)
        look_at(cam, tgt)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE EVIDENCE STORE (Case 05)

def scene_shelf(kv, f0, f1):
    """Steel shelving of plain archive boxes in a cold store; one box picked out by a light.
    No labels or case numbers. Slow dolly along the aisle."""
    sc = bpy.context.scene
    night_sky(sc, low=(0.004, 0.005, 0.007), high=(0.002, 0.002, 0.003))
    steel = mat_principled("Shelf", (0.30, 0.32, 0.33), metallic=0.8, rough=0.45)
    floor(color=(0.05, 0.055, 0.06), rough=0.35)
    import random
    rng = random.Random(1980)
    boxes = [mat_principled(f"Box{i}", c, rough=0.85) for i, c in
             enumerate([(0.42, 0.33, 0.22), (0.38, 0.30, 0.20), (0.46, 0.37, 0.25)])]
    hero = None
    for side in (-1.4, 1.4):
        for bay in range(6):
            y0 = bay * 1.9
            for x in (side - 0.42, side + 0.42):
                for z in (0.0, 2.4):
                    up = add("cube", f"Up{side}{bay}{x}{z}", size=1, location=(x, y0 + (0.9 if z else -0.9), 1.2))
                    up.scale = (0.04, 0.04, 2.4)
                    assign(up, steel)
            for lvl in range(5):
                z = 0.15 + lvl * 0.55
                sh = add("cube", f"Sh{side}{bay}{lvl}", size=1, location=(side, y0, z))
                sh.scale = (0.9, 1.85, 0.025)
                assign(sh, steel)
                for b in range(3):
                    is_hero = side < 0 and bay == 3 and lvl == 2 and b == 1
                    if rng.random() < 0.18 and not is_hero:
                        continue
                    bx = add("cube", f"B{side}{bay}{lvl}{b}", size=1,
                             location=(side + rng.uniform(-0.04, 0.04), y0 - 0.58 + b * 0.58, z + 0.19))
                    bx.scale = (0.75, 0.5, 0.36)
                    bx.rotation_euler = (0, 0, math.radians(rng.uniform(-2, 2)))
                    assign(bx, boxes[rng.randrange(3)])
                    if is_hero:
                        hero = bx
    hx, hy, hz = hero.location
    spot((hx + 1.6, hy - 0.6, hz + 1.8), (hx, hy, hz), 1600, angle=12, blend=0.4, color=(1.0, 0.9, 0.75), name="Key")
    for k in range(4):  # cold tube lights down the aisle
        area_light((0, k * 3.2, 3.2), (0, k * 3.2, 0), 18, size=1.2, color=(0.65, 0.78, 0.9), name=f"Tube{k}")
    cam = camera((0.3, -2.5, 1.55), (hx, hy, hz), lens=35)
    push = float(kv.get("push", "0.35"))
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        cam.location = (0.3, -2.5 + 3.2 * push * u, 1.55)
        look_at(cam, (hx, hy, hz))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE INTERVIEW ROOM (Case 06)

def scene_room(kv, f0, f1):
    """An empty precinct interview room at night: metal table, two chairs, a 1980s shoulder video
    camera on a tripod facing the empty far chair, one fluorescent fixture. No figures, no papers.
    view=push (slow dolly from the door toward the table) | camera (close on the camera, its red
    tally light on, the empty chair beyond)."""
    wall = mat_principled("RoomWall", (0.075, 0.085, 0.07), rough=0.75)
    flo = mat_principled("RoomFloor", (0.035, 0.035, 0.032), rough=0.35, coat=0.2)
    steel = mat_principled("TableSteel", (0.30, 0.31, 0.30), metallic=0.6, rough=0.45)
    top = mat_principled("TableTop", (0.045, 0.042, 0.038), rough=0.35, coat=0.25)
    seat = mat_principled("Seat", (0.05, 0.05, 0.055), rough=0.6)
    body = mat_principled("CamBody", (0.03, 0.03, 0.032), rough=0.4)
    lensm = mat_principled("CamLens", (0.01, 0.01, 0.012), metallic=0.4, rough=0.15)
    tally = mat_principled("Tally", (1, 0, 0), emission=(1.0, 0.08, 0.05), strength=0.0)
    tube = mat_principled("Tube", (1, 1, 1), emission=(0.82, 0.93, 0.88), strength=6.0)

    def box(name, loc, scale, m, rot=(0, 0, 0)):
        o = add("cube", name, size=1, location=loc)
        o.scale = scale
        o.rotation_euler = rot
        assign(o, m)
        return o

    def rod(name, a, b, r, m):
        a, b = Vector(a), Vector(b)
        o = add("cylinder", name, radius=r, depth=(b - a).length, location=(a + b) / 2, vertices=12)
        o.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
        assign(o, m)
        return o

    box("Floor", (0, 0, -0.05), (5.0, 5.0, 0.1), flo)
    box("WallB", (0, 2.2, 1.5), (5.0, 0.1, 3.2), wall)
    box("WallL", (-2.0, 0, 1.5), (0.1, 5.0, 3.2), wall)
    box("WallR", (2.0, 0, 1.5), (0.1, 5.0, 3.2), wall)
    box("Ceil", (0, 0, 2.9), (5.0, 5.0, 0.1), wall)
    # table, legs, two chairs facing each other across it
    box("TableTop", (0, 0.3, 0.74), (1.5, 0.8, 0.04), top)
    for x in (-0.68, 0.68):
        for y in (-0.05, 0.65):
            rod(f"TLeg{x}{y}", (x, 0.3 + (y - 0.3), 0.0), (x, 0.3 + (y - 0.3), 0.72), 0.02, steel)

    def chair(name, y, facing):
        box(f"{name}Seat", (0, y, 0.45), (0.44, 0.42, 0.04), seat)
        box(f"{name}Back", (0, y + 0.2 * facing, 0.72), (0.42, 0.03, 0.42), seat)
        for dx in (-0.19, 0.19):
            for dy in (-0.18, 0.18):
                rod(f"{name}Leg{dx}{dy}", (dx, y + dy, 0.0), (dx, y + dy, 0.43), 0.012, steel)

    chair("Far", 1.0, 1)   # the empty chair the camera points at
    chair("Near", -0.4, -1)
    # a 1980s shoulder camera on a tripod, in the near-right corner, aimed at the far chair
    cx, cy, cz = 1.15, -0.85, 1.35
    aim = Vector((0.0, 1.0, 0.9)) - Vector((cx, cy, cz))
    yaw = math.atan2(aim.y, aim.x) - math.pi / 2
    cam_body = box("CamBody", (cx, cy, cz), (0.14, 0.42, 0.2), body, rot=(0, 0, yaw))
    fwd = Vector((math.cos(yaw + math.pi / 2), math.sin(yaw + math.pi / 2), 0))
    lens_c = Vector((cx, cy, cz)) + fwd * 0.27
    rod("CamLens", lens_c - fwd * 0.07, lens_c + fwd * 0.07, 0.055, lensm)
    vf = Vector((cx, cy, cz + 0.13)) + fwd * 0.08
    box("Viewfinder", tuple(vf), (0.05, 0.14, 0.05), body, rot=(0, 0, yaw))
    tl = Vector((cx, cy, cz + 0.07)) + fwd * 0.215
    led = add("uv_sphere", "TallyLight", radius=0.012, location=tuple(tl))
    assign(led, tally)
    rod("TripodHead", (cx, cy, cz - 0.1), (cx, cy, cz - 0.22), 0.03, steel)
    for k in range(3):
        a = math.radians(90 + k * 120)
        rod(f"TripodLeg{k}", (cx, cy, cz - 0.22), (cx + 0.38 * math.cos(a), cy + 0.38 * math.sin(a), 0.0),
            0.012, steel)
    # one fluorescent fixture over the table; a hard key under it; dim cool fill
    box("Fixture", (0, 0.3, 2.82), (0.35, 1.25, 0.06), steel)
    box("TubeA", (-0.08, 0.3, 2.785), (0.04, 1.15, 0.025), tube)
    box("TubeB", (0.08, 0.3, 2.785), (0.04, 1.15, 0.025), tube)
    area_light((0, 0.3, 2.74), (0, 0.3, 0), 70, size=0.8, color=(0.85, 0.95, 0.9), name="Fluor")
    area_light((-1.6, -1.6, 2.2), (0.3, 0.6, 0.8), 4, size=1.5, color=(0.5, 0.6, 0.7), name="Fill")
    view = kv.get("view", "push")
    push = float(kv.get("push", "0.3"))
    if view == "camera":
        side = Vector((fwd.y, -fwd.x, 0))
        start = Vector((cx, cy, cz + 0.22)) - fwd * 0.7 + side * 0.5
        chair_c = Vector((0.0, 1.0, 0.7))
        cam = camera(tuple(start), tuple(chair_c), lens=35)
        for f in range(f0, f1 + 1):
            u = G_ease((f - f0) / max(1, f1 - f0))
            t_on = (f - f0) / FPS
            s = tally.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
            s.default_value = 12.0 if (t_on > 0.8 or kv.get("tally")) else 0.0  # the light comes on: recording
            s.keyframe_insert("default_value", frame=f)
            cam.location = tuple(start + fwd * (0.3 * push * u))
            look_at(cam, tuple(chair_c))
            cam.keyframe_insert("location", frame=f)
            cam.keyframe_insert("rotation_euler", frame=f)
        return
    s = tally.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    s.default_value = 12.0
    tgt = (0.2, 0.6, 0.75)
    cam = camera((-1.4, -1.9, 1.6), tgt, lens=24)
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        k = 1.0 - push * u
        cam.location = (0.2 + (-1.6) * k, 0.6 + (-2.5) * k, 0.75 + 0.85 * k)
        look_at(cam, tgt)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- THE PARK PATH (Case 06)

def scene_park(kv, f0, f1):
    """A park footpath at night under one old lamp post: bare trees, a bench, wet asphalt.
    Generic, no landmarks. Slow drift along the path."""
    sc = bpy.context.scene
    night_sky(sc, low=(0.02, 0.025, 0.04), high=(0.002, 0.003, 0.008))
    grass = mat_principled("Grass", (0.03, 0.04, 0.028), rough=0.9)
    path = mat_principled("Path", (0.03, 0.03, 0.033), rough=0.25, coat=0.6)
    bark = mat_principled("Bark", (0.03, 0.025, 0.022), rough=0.9)
    iron = mat_principled("Iron", (0.03, 0.035, 0.03), metallic=0.6, rough=0.5)
    slat = mat_principled("Slat", (0.06, 0.04, 0.025), rough=0.7)
    glow = mat_principled("Lantern", (1, 1, 1), emission=(1.0, 0.78, 0.5), strength=18.0)
    g = add("plane", "Ground", size=120)
    assign(g, grass)
    import random
    rng = random.Random(1989)
    # a gently curving path along +Y
    pts = [(1.2 * math.sin(i * 0.12), i * 1.0) for i in range(-10, 45)]
    verts, faces = [], []
    for i, (x, y) in enumerate(pts):  # one continuous strip, 2.6 m wide
        verts += [(x - 1.3, y, 0.01), (x + 1.3, y, 0.01)]
        if i:
            faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
    me = bpy.data.meshes.new("PathMesh")
    me.from_pydata(verts, [], faces)
    strip = bpy.data.objects.new("Path", me)
    sc.collection.objects.link(strip)
    assign(strip, path)

    def rod(name, a, b, r, m):
        a, b = Vector(a), Vector(b)
        o = add("cylinder", name, radius=r, depth=(b - a).length, location=(a + b) / 2, vertices=8)
        o.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
        assign(o, m)
        return o

    def tree(n, x, y):
        h = rng.uniform(5.5, 8.0)
        rod(f"Trunk{n}", (x, y, 0), (x, y, h), rng.uniform(0.14, 0.22), bark)
        for b in range(rng.randint(5, 8)):
            z = rng.uniform(h * 0.45, h * 0.95)
            a = rng.uniform(0, 2 * math.pi)
            ln = rng.uniform(1.2, 2.8)
            end = (x + ln * math.cos(a), y + ln * math.sin(a), z + rng.uniform(0.6, 1.8))
            rod(f"Br{n}_{b}", (x, y, z), end, 0.05, bark)
            for t in range(2):
                a2 = a + rng.uniform(-0.9, 0.9)
                rod(f"Tw{n}_{b}_{t}", end, (end[0] + 0.9 * math.cos(a2), end[1] + 0.9 * math.sin(a2),
                                             end[2] + rng.uniform(0.2, 0.8)), 0.02, bark)

    n = 0
    for y in range(-6, 44, 4):
        for side in (-1, 1):
            if rng.random() < 0.75:
                tree(n, 1.2 * math.sin(y * 0.12) + side * rng.uniform(3.5, 7.5), y + rng.uniform(-1.5, 1.5))
                n += 1
    # one lamp post beside the path, a bench under it
    lx, ly = 1.2 * math.sin(14 * 0.12) + 1.9, 14.0
    rod("Post", (lx, ly, 0), (lx, ly, 3.6), 0.07, iron)
    lan = add("cylinder", "LanternGlass", radius=0.2, depth=0.4, location=(lx, ly, 3.8), vertices=6)
    assign(lan, glow)
    cap = add("cone", "LanternCap", radius1=0.3, depth=0.25, location=(lx, ly, 4.1), vertices=6)
    assign(cap, iron)
    spot((lx, ly, 3.7), (lx - 1.2, ly, 0), 900, angle=110, blend=0.8, color=(1.0, 0.78, 0.5), name="Lamp")
    for k, dz in enumerate((0.45, 0.62, 0.79)):
        sl = add("cube", f"Slat{k}", size=1, location=(lx + 0.55, ly - 1.6, dz if k == 0 else 0.5 + 0.12 * k))
        sl.scale = (0.45 if k == 0 else 0.05, 1.6, 0.04 if k == 0 else 0.12)
        assign(sl, slat)
    for dy in (-0.7, 0.7):
        rod(f"BenchLeg{dy}", (lx + 0.55, ly - 1.6 + dy, 0), (lx + 0.55, ly - 1.6 + dy, 0.45), 0.03, iron)
    area_light((0, 60, 25), (0, 10, 0), 900, size=40, color=(0.35, 0.45, 0.7), name="SkyGlow")
    push = float(kv.get("push", "0.35"))
    cam = camera((0.3, -2.0, 1.6), (1.2, 16.0, 1.4), lens=32)
    for f in range(f0, f1 + 1):
        u = G_ease((f - f0) / max(1, f1 - f0))
        y = -2.0 + 9.0 * push * u
        cam.location = (1.2 * math.sin(y * 0.12) - 0.4, y, 1.6)
        look_at(cam, (1.2 * math.sin((y + 16) * 0.12) + 0.6, y + 16, 1.3))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


# ---------------------------------------------------------------- main

def main():
    scene, out, opts, kv = args()
    f0, f1 = (int(v) for v in opts["frames"].split(":"))
    sc = reset(opts["res"], int(opts["samples"]))
    {"scale": scene_scale, "brain": scene_brain, "tower": scene_tower,
     "corridor": scene_corridor, "road": scene_road, "car": scene_car, "sea": scene_sea,
     "book": scene_book, "or": scene_or, "lot": scene_lot, "shelf": scene_shelf,
     "room": scene_room, "park": scene_park}[scene](kv, f0, f1)
    os.makedirs(out, exist_ok=True)
    tag = kv.get("name", scene)
    for f in range(f0, f1 + 1, int(opts.get("step", 1))):
        path = os.path.join(out, f"{tag}_{f:04d}.png")
        if os.path.exists(path) and os.path.getsize(path) > 0:  # resume an interrupted clip
            continue
        sc.frame_set(f)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("frame", f, flush=True)


if __name__ == "__main__":
    main()
