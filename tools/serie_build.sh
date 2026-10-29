#!/usr/bin/env bash
# Serie podcast péptidos: de un corte listo (cut.py) a los props del render, por clip.
#   recorte vertical → corrección de subtítulos → caras → export a Remotion → props "blanco minimalista"
#   bash tools/serie_build.sh 01 02 …
set -euo pipefail
cd "$(dirname "$0")/.."
S=.claude/skills/it-reelsmaker/scripts
for i in "$@"; do
  d=edit/podcast-$i
  echo "=== $i"
  if [ "$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 $d/final.mp4)" != "1080" ]; then
    python3 tools/reframe_vertical.py $d 2>&1 | grep -vE "WARN|partial file" | tail -2
  fi
  python3 tools/fix_captions.py $i | head -1
  python3 $S/faces.py scan $d 2>&1 | tail -1
  python3 $S/faces.py zones $d > /dev/null 2>&1
  python3 $S/visual_plan.py export $d --remotion reels --props $d/reelkit-props.json --subtitles none --no-hook --no-end --no-corner 2>&1 | grep -E "subtitles:|error|ERROR" || true
  python3 tools/serie_props.py $i
done
