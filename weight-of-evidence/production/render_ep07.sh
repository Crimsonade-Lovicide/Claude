#!/usr/bin/env bash
# Render the new 3D clips Case 07 uses (the Scale clips are linked from Case 01's anim/).
#   render_ep07.sh <prod_dir> [clip ...]     (no clips = all)
# Same recipe as render_ep01.sh: 960x540, every 2nd frame, Cycles CPU + denoise, ffmpeg
# upscales (Lanczos) and blends to 24 fps.
set -euo pipefail
PROD=${1:?prod dir}; shift || true
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$PROD/anim
mkdir -p "$OUT"
for c in scale_empty scale_tip_left scale_tip_right scale_level_loaded; do
  [ -e "$OUT/$c.mp4" ] || ln -s "${EP01_ANIM:-$PROD/../ep01/anim}/$c.mp4" "$OUT/$c.mp4"
done
# clips reused from earlier cases (name in this case = case/clip)
for pair in brain_clean=ep01/brain_clean tower_push=ep01/tower_push corridor_b=ep01/corridor \
            corridor=ep04/corridor book_closed=ep04/book_closed book_night=ep04/book_night \
            or_lamp=ep04/or_lamp evidence_shelf=ep05/evidence_shelf park_path=ep06/park_path; do
  c=${pair%%=*}; p=${pair#*=}; src=$PROD/../${p%%/*}/anim/${p#*/}.mp4
  [ -e "$OUT/$c.mp4" ] || ln -s "$(cd "$(dirname "$src")" && pwd)/$(basename "$src")" "$OUT/$c.mp4"
done

# name | scene | last frame (24 fps) | samples | key=value ...
CLIPS=(
  "dome_push|dome|400|14|push=0.25"
  "courtroom_push|courtroom|540|14|view=push push=0.4"
  "courtroom_bench|courtroom|440|14|view=bench"
  "desk_act_push|desk|260|14|doc=pl109_3 view=push push=0.3"
  "desk_blank_pen|desk|200|14|doc=blank view=pen push=0.25"
  "desk_directive|desk|280|14|doc=directive view=stack push=0.3"
  "desk_act_stack|desk|160|14|doc=pl109_3 view=stack push=0.3"
  "court_push|courtroom|200|14|view=push push=0.35"
  "court_witness|courtroom|200|14|view=witness"
  "court_bench|courtroom|200|14|view=bench"
  "court_gallery|courtroom|200|14|view=gallery"
  "ward_push|ward|200|14|view=push"
  "ward_window|ward|200|14|view=window"
  "tv_static|tv|200|14|push=0.3"
  "desk_petition|desk|160|14|doc=petition view=push push=0.3"
  "desk_greer|desk|160|14|doc=greer view=push push=0.3"
  "desk_dca2003|desk|200|14|doc=dca2003 view=stack push=0.3"
  "desk_wolfson|desk|160|14|doc=wolfson view=push push=0.3"
  "desk_pariente|desk|160|14|doc=pariente view=stack push=0.3"
  "desk_birch|desk|160|14|doc=birch view=push push=0.3"
  "desk_examiner|desk|200|14|doc=examiner view=push push=0.3"
  "desk_cruzan|desk|200|14|doc=cruzan view=stack push=0.3"
  "desk_mca|desk|160|14|doc=mca view=push push=0.3"
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
