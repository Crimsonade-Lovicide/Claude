#!/usr/bin/env bash
# Render the new 3D clips Case 08 uses and link the ones it reuses (the Scale from Case 01, the
# courtroom, static TV and generic AI places from Case 07, the archive shelf from Case 05).
#   render_ep08.sh <prod_dir> [clip ...]     (no clips = all)
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
            tv_static=ep07v2/tv_static desk_blank_pen=ep07v2/desk_blank_pen \
            evidence_shelf=ep05/evidence_shelf park_path=ep06/park_path room_push=ep06/room_push \
            ai_archive=ep07v2/ai_archive ai_papers=ep07v2/ai_papers ai_lights=ep07v2/ai_lights \
            ai_rain_window=ep07v2/ai_rain_window ai_scotus=ep07v2/ai_scotus \
            ai_westminster=ep07v2/ai_westminster ai_philly=ep07v2/ai_philly; do
  c=${pair%%=*}; p=${pair#*=}; src=$PROD/../${p%%/*}/anim/${p#*/}.mp4
  [ -e "$OUT/$c.mp4" ] || ln -s "$(cd "$(dirname "$src")" && pwd -P)/$(basename "$src")" "$OUT/$c.mp4"
done

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "cell_push|cell|240|14|view=push push=0.35"
  "cell_slot|cell|200|14|view=slot push=0.35"
  "cell_window|cell|200|14|view=window"
  "cell_door|cell|160|14|view=door"
  "tier_corridor|tier|240|14|view=corridor push=1.0"
  "tier_phone|tier|160|14|view=phone"
  "tier_dorm|tier|200|14|view=dorm"
  "desk_cpl3030|desk|200|14|doc=cpl3030 view=push push=0.3"
  "desk_docket|desk|160|14|doc=docket view=push push=0.3"
  "desk_sdny|desk|160|14|doc=sdny view=stack push=0.3"
  "desk_stack|desk|200|14|doc=stack view=push push=0.3"
  "desk_salerno|desk|200|14|doc=salerno view=stack push=0.3"
  "desk_bailact|desk|160|14|doc=bailact view=push push=0.3"
  "desk_dgy|desk|160|14|doc=dgy view=stack push=0.3"
  "desk_bjs|desk|160|14|doc=bjs view=push push=0.3"
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
