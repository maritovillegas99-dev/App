#!/usr/bin/env bash
# Reinstala lo que no se guarda en git (dependencias y modelos) en una sesión nueva.
set -u
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg) >/dev/null 2>&1
python3 -c "import yt_dlp, PIL, cv2, faster_whisper, rembg" 2>/dev/null || \
  pip install -q --root-user-action=ignore yt-dlp Pillow opencv-python-headless faster-whisper "rembg[cpu,cli]" >/dev/null 2>&1
[ -d reels/node_modules ] || (cd reels && npm install --no-audit --no-fund >/dev/null 2>&1)
# rembg nuevo guarda el modelo en ~/.rembg/models; IT Reelsmaker lo busca en ~/.u2net
( [ -f "$HOME/.rembg/models/u2net_human_seg/u2net_human_seg.onnx" ] || rembg d u2net_human_seg >/dev/null 2>&1
  mkdir -p "$HOME/.u2net" && ln -sf "$HOME/.rembg/models/u2net_human_seg/u2net_human_seg.onnx" "$HOME/.u2net/u2net_human_seg.onnx" ) &
python3 -c "from faster_whisper import download_model; download_model('medium')" >/dev/null 2>&1 &
wait
python3 .claude/skills/it-reelsmaker/scripts/doctor.py --remotion reels 2>&1 | tail -1
exit 0
