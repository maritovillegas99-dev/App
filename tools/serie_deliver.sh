#!/usr/bin/env bash
# Serie podcast péptidos: del render (kit.py render --comp ReelMinimal) al MP4 que se entrega en Resultados/.
#   auditoría de caras del render → portada (cuadro con el gancho) → master −14 LUFS con portada → Resultados/
#   bash tools/serie_deliver.sh 01 [v1]
set -euo pipefail
cd "$(dirname "$0")/.."
S=.claude/skills/it-reelsmaker/scripts
i=$1; v=${2:-v1}
d=edit/podcast-$i
render=reels/out/podcast-$i.mp4
python3 $S/check.py $d --render $render 2>&1 | tail -4 || echo "check: revisar $d/verify/sheet.png"
python3 $S/poster.py pick $d --render $render --t 1.4 -o $d/cover.jpg 2>&1 | tail -1
# la portada va como carátula (attach), no en el cuadro 0: el gancho entra con fundido y bake rechaza el cuadro 0
python3 $S/master_audio.py $render -o reels/out/podcast-$i-master.mp4 2>&1 | grep -E "output|LUFS" | tail -1
python3 $S/poster.py attach reels/out/podcast-$i-master.mp4 --cover $d/cover.jpg -o reels/out/podcast-$i-final.mp4 2>&1 | tail -1
mkdir -p Resultados
cp reels/out/podcast-$i-final.mp4 "Resultados/podcast-peptidos_${i}_editado_${v}.mp4"
cp $d/cover.jpg "Resultados/podcast-peptidos_${i}_portada_${v}.jpg"
ffprobe -v error -show_entries stream=width,height:format=duration -of compact "Resultados/podcast-peptidos_${i}_editado_${v}.mp4"
ffmpeg -nostats -i "Resultados/podcast-peptidos_${i}_editado_${v}.mp4" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
