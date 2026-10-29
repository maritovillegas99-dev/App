#!/usr/bin/env python3
"""Recorte vertical 9:16 de un corte horizontal (1920×1080) siguiendo la cara, un encuadre fijo por plano.

Para clips de podcast ya editados (una persona por plano): detecta los cambios de plano (ffmpeg scdet + uniones del
corte), mide la cara con YuNet cada 0.2 s, y en cada plano fija el recorte en la mediana del centro de la cara.
Sale un MP4 1080×1920 con el mismo timeline y el mismo audio, que reemplaza a final.mp4 (el horizontal queda como
final_h.mp4), para que faces.py, visual_plan.py y el render lo traten como un video vertical normal.

  python3 tools/reframe_vertical.py edit/<id>            # escribe final.mp4 (vertical) y final_h.mp4
  python3 tools/reframe_vertical.py edit/<id> --dry      # solo imprime los planos y el recorte
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "models" / "face_detection_yunet_2023mar.onnx"
CW = 608          # ancho del recorte en el original (1080 · 1080/1920 ≈ 607.5, par)
STEP = 0.2        # s entre muestras de cara
SCENE = 0.25      # umbral de scdet (0–1) para un cambio de plano
MIN_SHOT = 0.6    # s: un "plano" más corto se une al anterior


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"]["duration"])


def scene_cuts(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", f"scale=480:-2,scdet=threshold={SCENE * 100}:sc_pass=0",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(m) for m in re.findall(r"lavfi\.scd\.time:\s*([0-9.]+)", err)]


def face_track(path, dur, w, h):
    det = cv2.FaceDetectorYN.create(str(MODEL), "", (640, int(640 * h / w)), 0.6, 0.3, 50)
    cap = cv2.VideoCapture(str(path))
    out = []
    t = 0.0
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, img = cap.read()
        if not ok:
            break
        small = cv2.resize(img, (640, int(640 * h / w)))
        _, faces = det.detect(small)
        best = None
        if faces is not None and len(faces):
            f = max(faces, key=lambda f: f[2] * f[3])  # la cara más grande
            s = w / 640
            best = ((f[0] + f[2] / 2) * s, (f[1] + f[3] / 2) * s, f[2] * s, f[3] * s)
        out.append((t, best))
        t += STEP
    return out


def shots(cuts, joins, dur):
    pts = sorted(set([0.0] + [c for c in cuts + joins if 0 < c < dur] + [dur]))
    merged = [pts[0]]
    for p in pts[1:]:
        if p - merged[-1] < MIN_SHOT and p != dur:
            continue
        merged.append(p)
    if merged[-1] != dur:
        merged.append(dur)
    if len(merged) > 2 and merged[-1] - merged[-2] < MIN_SHOT:
        merged.pop(-2)
    return list(zip(merged[:-1], merged[1:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edit")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    d = (ROOT / a.edit).resolve()
    src = d / "final_h.mp4" if (d / "final_h.mp4").exists() else d / "final.mp4"
    w, h, dur = probe(src)
    if w < h:
        raise SystemExit(f"{src} ya es vertical")
    caps = json.loads((d / "captions.json").read_text())
    joins = [s["out_start"] for s in caps["segments"][1:]]
    cuts = scene_cuts(src)
    track = face_track(src, dur, w, h)
    plan = []
    last_x = w / 2
    for a0, b0 in shots(cuts, joins, dur):
        xs = [f[0] for t, f in track if f and a0 + 0.05 <= t < b0 - 0.05]
        if not xs:  # plano muy corto: la muestra más cercana
            near = [f[0] for t, f in track if f and a0 - 0.3 <= t < b0 + 0.3]
            xs = near or [last_x]
        cx = float(np.median(xs))
        last_x = cx
        x = int(round(min(max(cx - CW / 2, 0), w - CW)))
        x -= x % 2
        if plan and abs(x - plan[-1][2]) < 30:  # mismo plano tras un corte: sin saltitos de pocos píxeles
            x = plan[-1][2]
        plan.append((round(a0, 3), round(b0, 3), x, len(xs)))
    for p in plan:
        print(f"  {p[0]:7.2f}–{p[1]:7.2f}  x={p[2]:4d}  ({p[3]} muestras)")
    (d / "reframe.json").write_text(json.dumps({"source": src.name, "crop_w": CW, "shots": plan}, indent=1))
    if a.dry:
        return
    expr = str(plan[-1][2])
    for a0, b0, x, _ in reversed(plan[:-1]):
        expr = f"if(lt(t,{b0}),{x},{expr})"
    vf = (f"crop={CW}:{h}:'{expr}':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0,setsar=1")
    tmp = d / "final_v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
    if src.name == "final.mp4":
        shutil.move(str(src), str(d / "final_h.mp4"))
    shutil.move(str(tmp), str(d / "final.mp4"))
    print(f"{d / 'final.mp4'}: 1080x1920, {len(plan)} planos")


if __name__ == "__main__":
    main()
