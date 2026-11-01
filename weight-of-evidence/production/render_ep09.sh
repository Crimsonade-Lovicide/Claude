#!/usr/bin/env bash
# Render the new 3D clips Case 09 uses (the fax, the flashover test room, the desk documents) and link
# the ones it reuses (the Scale, the courtroom, generic places from Cases 07 and 08, the Case 08 tier).
#   render_ep09.sh <prod_dir> [clip ...]     (no clips = all)
# Same recipe as render_ep01.sh: 960x540, every 2nd frame, Cycles CPU + denoise, ffmpeg
# upscales (Lanczos) and blends to 24 fps. Interrupted clips resume from their frames.
set -euo pipefail
PROD=${1:?prod dir}; shift || true
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$PROD/anim
mkdir -p "$OUT"
# clips reused from earlier cases (name in this case = case/clip)
for pair in scale_empty=ep01/scale_empty scale_tip_left=ep01/scale_tip_left \
            scale_tip_right=ep01/scale_tip_right scale_level_loaded=ep01/scale_level_loaded \
            court_push=ep07v2/court_push court_bench=ep07v2/court_bench \
            court_witness=ep07v2/court_witness court_gallery=ep07v2/court_gallery \
            courtroom_push=ep07/courtroom_push courtroom_bench=ep07/courtroom_bench \
            desk_blank_pen=ep07v2/desk_blank_pen evidence_shelf=ep05/evidence_shelf \
            ai_archive=ep07v2/ai_archive ai_papers=ep07v2/ai_papers ai_lights=ep07v2/ai_lights \
            ai_rain_window=ep07v2/ai_rain_window ai_scotus=ep07v2/ai_scotus \
            ai_westminster=ep07v2/ai_westminster ai_razor_wire=ep08/ai_razor_wire \
            ai_clock=ep08/ai_clock ai_court_corridor=ep08/ai_court_corridor \
            tier_corridor=ep08/tier_corridor cell_door=ep08/cell_door; do
  c=${pair%%=*}; p=${pair#*=}; src=$PROD/../${p%%/*}/anim/${p#*/}.mp4
  [ -e "$OUT/$c.mp4" ] || ln -s "$(cd "$(dirname "$src")" && pwd -P)/$(basename "$src")" "$OUT/$c.mp4"
done

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "fax_push|fax|240|12|view=push"
  "fax_page|fax|200|12|view=page"
  "fire_push|fireroom|240|10|view=push"
  "fire_floor|fireroom|200|10|view=floor"
  "desk_hurst|desk|200|12|doc=hurst view=push push=0.3"
  "desk_vasquez|desk|160|12|doc=vasquez view=push push=0.3"
  "desk_beyler|desk|200|12|doc=beyler view=stack push=0.3"
  "desk_herrera|desk|160|12|doc=herrera view=push push=0.3"
)

want() { [ $# -eq 0 ] && return 0; for w in "${@:2}"; do [ "$w" = "$1" ] && return 0; done; return 1; }

for spec in "${CLIPS[@]}"; do
  IFS='|' read -r name scene last samples kv <<<"$spec"
  if [ $# -gt 0 ] && ! want "$name" "$@"; then continue; fi
  dir=$OUT/$name
  if [ -f "$OUT/$name.mp4" ]; then echo "skip $name"; continue; fi
  mkdir -p "$dir"
  echo "render $name ($scene 0..$last step 2, $samples spp)"
  # shellcheck disable=SC2086
  nice -n 5 "$PY" "$HERE/scenes.py" "$scene" "$dir" --frames "0:$last" --step 2 \
      --res 960x540 --samples "$samples" name="$name" $kv >"$dir.log" 2>&1
  ffmpeg -y -loglevel error -framerate 12 -pattern_type glob -i "$dir/${name}_*.png" \
      -vf "scale=1920:1080:flags=lanczos,framerate=fps=24" \
      -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p "$OUT/$name.mp4"
  echo "done $name"
done
