#!/usr/bin/env bash
# Render every 3D clip Case 01 and the trailer use, then encode each to 1080p24.
#   render_ep01.sh <prod_dir> [clip ...]     (no clips = all)
# Renders at 960x540, every 2nd frame (12 fps), Cycles CPU with denoising; ffmpeg upscales
# with Lanczos and blends to 24 fps. Slow camera moves hide the half rate.
# The tumor fading out and back is a crossfade between brain_clean and brain_tumor, which
# share an identical camera path.
set -euo pipefail
PROD=${1:?prod dir}; shift || true
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$PROD/anim
mkdir -p "$OUT"

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "tower_push|tower|288|16|push=0.25"
  "scale_empty|scale|192|16|tilt=0 orbit=12"
  "scale_tip_left|scale|120|16|tilt=-9 anim=tip left=1"
  "scale_swing|scale|240|16|tilt=-2 anim=settle left=1 right=1"
  "scale_tip_right|scale|192|16|tilt=9 anim=tip left=1 right=5"
  "scale_bottom_left|scale|144|16|tilt=-16 anim=tip left=9 right=5"
  "scale_level_loaded|scale|288|16|tilt=0 left=8 right=7 orbit=30"
  "brain_clean|brain|384|12|tumor=0 orbit=40"
  "brain_tumor|brain|384|12|tumor=1 orbit=40"
  "corridor|corridor|360|10|flicker=1"
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
