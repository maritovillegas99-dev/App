#!/usr/bin/env python3
"""Transcriptor local de respaldo para IT Reelsmaker cuando Hugging Face está bloqueado (sin faster-whisper).

Usa Parakeet TDT 0.6B v3 (sherpa-onnx, 25 idiomas europeos, español incluido), descargado desde GitHub.
Entrega el formato de `transcribe.py check`: {"language_code", "text", "words": [{text, start, end, type}]}.

  python3 tools/transcribe_parakeet.py edit/<id>/audio.wav edit/<id>/transcripts/<stem>.json [--language es]

El WAV debe salir de `transcribe.py audio edit/<id> <fuente>` (mismo timeline que el video). Cualquier WAV/video
también sirve: se convierte a 16 kHz mono con ffmpeg. El audio largo se parte en trozos de <= 25 s, cortando en
el punto más silencioso cerca del límite, para no partir palabras.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

MODEL = Path(__file__).resolve().parent.parent / "models" / "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
SR = 16000
CHUNK = 25.0   # segundos por trozo como máximo
SEARCH = 4.0   # ventana antes del límite donde se busca el silencio para cortar


def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def split_points(x):
    """Inicios de trozo (en muestras): cortes en el mínimo de energía (ventanas de 20 ms) antes de cada límite."""
    starts, pos, n = [0], 0, len(x)
    win = SR // 50
    while n - pos > CHUNK * SR:
        lo, hi = pos + int((CHUNK - SEARCH) * SR), pos + int(CHUNK * SR)
        seg = x[lo:hi]
        frames = seg[: len(seg) // win * win].reshape(-1, win)
        cut = lo + int(np.argmin((frames ** 2).mean(axis=1))) * win + win // 2
        starts.append(cut)
        pos = cut
    return starts


def recognizer():
    import sherpa_onnx
    if not (MODEL / "encoder.int8.onnx").exists():
        sys.exit(f"falta el modelo en {MODEL}: corre bash .claude/hooks/setup.sh")
    return sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(MODEL / "encoder.int8.onnx"), decoder=str(MODEL / "decoder.int8.onnx"),
        joiner=str(MODEL / "joiner.int8.onnx"), tokens=str(MODEL / "tokens.txt"),
        model_type="nemo_transducer", num_threads=4)


def words_of(rec, x):
    starts = split_points(x)
    bounds = starts[1:] + [len(x)]
    words = []
    for a, b in zip(starts, bounds):
        stream = rec.create_stream()
        stream.accept_waveform(SR, x[a:b])
        rec.decode_stream(stream)
        r = stream.result
        off, end_chunk = a / SR, b / SR
        durs = list(getattr(r, "durations", []) or [])
        cur = None
        for k, (tok, ts) in enumerate(zip(r.tokens, r.timestamps)):
            t = off + float(ts)
            tok_end = t + (float(durs[k]) if k < len(durs) and durs[k] > 0 else 0.08)
            if tok.startswith("▁") or tok.startswith(" ") or cur is None:
                if cur:
                    words.append(cur)
                cur = {"text": tok.lstrip("▁ "), "start": t, "end": tok_end, "type": "word"}
            else:
                cur["text"] += tok
                if any(c.isalnum() for c in tok):  # la puntuación llega al final de la pausa: no alarga la palabra
                    cur["end"] = tok_end
        if cur:
            words.append(cur)
        for w in words:
            w["end"] = min(w["end"], end_chunk)
    words = [w for w in words if w["text"].strip()]
    for w, nxt in zip(words, words[1:]):  # una palabra no termina después de que empieza la siguiente
        w["end"] = min(w["end"], nxt["start"])
    for w in words:
        w["start"], w["end"] = round(w["start"], 3), round(max(w["end"], w["start"] + 0.02), 3)
    return words


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--language", default="es", help="solo se anota en el JSON; el modelo detecta el idioma")
    a = ap.parse_args()
    words = words_of(recognizer(), load_audio(a.audio))
    doc = {"language_code": a.language, "text": " ".join(w["text"] for w in words), "words": words,
           "transcriber": "parakeet-tdt-0.6b-v3 (sherpa-onnx)"}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1))
    print(f"{a.out}: {len(words)} palabras")


if __name__ == "__main__":
    main()
