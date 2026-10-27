#!/usr/bin/env python3
"""Voz en off local con Kokoro (kokoro-onnx, español: em_alex, em_santa, ef_dora). Sin servicios externos.

  python3 tools/tts_kokoro.py guion.txt salida_dir [--voice em_alex] [--speed 0.9]

Una línea del guion = una frase = un WAV (frase_01.wav…), más frases.json con la duración de cada una.
Modelos en models/kokoro/ (los baja .claude/hooks/setup.sh desde GitHub).
"""
import argparse, json
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

M = Path(__file__).resolve().parent.parent / "models" / "kokoro"
ap = argparse.ArgumentParser()
ap.add_argument("guion"); ap.add_argument("out")
ap.add_argument("--voice", default="em_alex"); ap.add_argument("--speed", type=float, default=0.9)
a = ap.parse_args()
k = Kokoro(str(M / "kokoro-v1.0.onnx"), str(M / "voices-v1.0.bin"))
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
frases = []
for i, line in enumerate([l.strip() for l in Path(a.guion).read_text().splitlines() if l.strip()], 1):
    s, sr = k.create(line, voice=a.voice, speed=a.speed, lang="es")
    f = out / f"frase_{i:02d}.wav"
    sf.write(f, s, sr)
    frases.append({"n": i, "texto": line, "archivo": f.name, "dur": round(len(s) / sr, 3)})
(out / "frases.json").write_text(json.dumps(frases, ensure_ascii=False, indent=1))
print(f"{len(frases)} frases, {sum(x['dur'] for x in frases):.1f} s de voz")
