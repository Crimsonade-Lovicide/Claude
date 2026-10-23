#!/usr/bin/env bash
# Render the new 3D clips Case 03 uses (the Scale clips are linked from Case 01's anim/).
#   render_ep03.sh <prod_dir> [clip ...]     (no clips = all)
# Same recipe as render_ep01.sh: 960x540, every 2nd frame, Cycles CPU + denoise, ffmpeg
# upscales (Lanczos) and blends to 24 fps.
set -euo pipefail
PROD=${1:?prod dir}; shift || true
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$PROD/anim
mkdir -p "$OUT"
for c in scale_empty scale_tip_left scale_swing scale_tip_right scale_bottom_left scale_level_loaded; do
  [ -e "$OUT/$c.mp4" ] || ln -s "${EP01_ANIM:-$PROD/../ep01/anim}/$c.mp4" "$OUT/$c.mp4"
done

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "sea_dawn|sea|408|14|view=dinghy mood=dawn"
  "dinghy_close|sea|336|14|view=close tiles=5"
  "sea_storm|sea|408|14|view=storm flash=200"
  "sea_swell|sea|504|12|view=swell"
  "sea_dusk|sea|408|14|view=dinghy mood=dusk sun_az=14"
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
