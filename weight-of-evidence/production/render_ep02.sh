#!/usr/bin/env bash
# Render the new 3D clips Case 02 uses (the Scale clips come from Case 01's anim/).
#   render_ep02.sh <prod_dir> [clip ...]     (no clips = all)
# Same recipe as render_ep01.sh: 960x540, every 2nd frame, Cycles CPU + denoise, ffmpeg
# upscales (Lanczos) and blends to 24 fps.
set -euo pipefail
PROD=${1:?prod dir}; shift || true
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$PROD/anim
mkdir -p "$OUT"

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "road_push|road|336|10|view=push dist=60"
  "road_top|road|288|10|view=top orbit=20"
  "road_median|road|240|10|view=median"
  "car_orbit|car|288|12|orbit=35"
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
