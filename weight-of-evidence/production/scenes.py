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


# ---------------------------------------------------------------- main

def main():
    scene, out, opts, kv = args()
    f0, f1 = (int(v) for v in opts["frames"].split(":"))
    sc = reset(opts["res"], int(opts["samples"]))
    {"scale": scene_scale, "brain": scene_brain, "tower": scene_tower,
     "corridor": scene_corridor}[scene](kv, f0, f1)
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
