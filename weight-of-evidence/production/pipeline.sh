#!/usr/bin/env bash
# Build an episode end to end, resuming wherever it stopped (the cloud container restarts often).
#   pipeline.sh <prod_dir> <render_script> <episode.py> [jobs]
# 1. the render script (its clips resume frame by frame and skip finished clips);
# 2. every shot that has no shots/<id>.mp4 yet (shots are written whole or not at all);
# 3. --remux: concat, mix, master, captions, chapters.
# Writes <prod_dir>/pipeline.done when finished. Safe to run again at any point.
set -euo pipefail
PROD=${1:?prod dir}; RENDER=${2:?render script}; EP=${3:?episode.py}; JOBS=${4:-2}
PY=${WOE_PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -f "$PROD/pipeline.done"
"$RENDER" "$PROD"
find "$PROD/shots" -name '*.part.mp4' -delete 2>/dev/null || true
missing=$("$PY" - "$PROD" <<'EOF'
import json, os, sys
prod = sys.argv[1]
ids = [s["id"] for s in json.load(open(os.path.join(prod, "narration.json")))["shots"]]
print(",".join(i for i in ids if not os.path.exists(os.path.join(prod, "shots", f"{i}.mp4"))))
EOF
)
if [ -n "$missing" ]; then
  echo "shots: $missing"
  (cd "$HERE" && nice -n 5 "$PY" "$EP" "$PROD" --only "$missing" -j "$JOBS")
fi
(cd "$HERE" && "$PY" "$EP" "$PROD" --remux)
touch "$PROD/pipeline.done"
echo "pipeline done"
