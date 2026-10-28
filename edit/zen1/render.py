import cv2, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import gaussian_filter1d

SRC = "Material crudo/video_2026-10-28.mp4"
OUT = sys.argv[1]
FPS = 30
OW, OH = 1080, 1920
fj = json.load(open("edit/zen1/faces_src.json"))
W, H, n = fj["W"], fj["H"], fj["n"]
CW = int(round(H * 9 / 16))  # 270

# centro x: cara interpolada en huecos, suavizado lento (~1.2 s)
xs = np.array([f[1] if f[1] is not None else np.nan for f in fj["faces"]])
idx = np.arange(n); ok = ~np.isnan(xs)
xs = np.interp(idx, idx[ok], xs[ok])
# descartar saltos espurios
med = np.array([np.median(xs[max(0, i - 15):i + 16]) for i in range(n)])
xs = gaussian_filter1d(med, 36, mode="nearest")
cx = np.clip(xs - 10, CW / 2, W - CW / 2)  # leve sesgo hacia las manos
json.dump({"cx": cx.tolist(), "cw": CW}, open("edit/zen1/camera.json", "w"))

FONT = "edit/zen1/fonts/InstrumentSerif-Regular.ttf"
FONT_I = "edit/zen1/fonts/InstrumentSerif-Italic.ttf"
# (inicio, fin, línea 1, línea 2 en cursiva)
PHRASES = [
    (0.3, 5.5, "Cada día,", "con calma"),
    (6.5, 11.4, "Dedicación", "en cada detalle"),
    (12.5, 17.6, "Tu bienestar", "empieza aquí"),
]
TEXT_CY = 1480  # bajo la cara (cabeza entre y≈150 y 700 en salida)

def text_layer(l1, l2):
    img = Image.new("RGBA", (OW, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(FONT, 118); f2 = ImageFont.truetype(FONT_I, 118)
    for txt, f, y in ((l1, f1, 150), (l2, f2, 285)):
        w = d.textlength(txt, font=f)
        d.text(((OW - w) / 2, y), txt, font=f, fill=(255, 255, 255, 255), anchor="ls")
    # línea fina decorativa
    d.line([(OW / 2 - 60, 345), (OW / 2 + 60, 345)], fill=(255, 255, 255, 200), width=3)
    return img

layers = [text_layer(a, b) for _, _, a, b in PHRASES]

def shadow(img):
    a = img.split()[3].filter(ImageFilter.GaussianBlur(14))
    s = Image.new("RGBA", img.size, (20, 18, 15, 0)); s.putalpha(a.point(lambda v: int(v * 0.7)))
    return s

shadows = [shadow(l) for l in layers]

def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

def text_state(tm, a, b):
    fin, fout = 1.4, 1.2
    if tm < a or tm > b: return 0, 0, 0
    p = ease((tm - a) / fin) if tm < a + fin else (ease((b - tm) / fout) if tm > b - fout else 1)
    blur = (1 - p) * 14
    dy = (1 - p) * 30 * (1 if tm < a + fin else -1)
    return p, blur, dy

# viñeta + degradado inferior suave para leer el texto
yy, xx = np.mgrid[0:OH, 0:OW]
vig = 1 - 0.28 * (((xx - OW / 2) / (OW / 2)) ** 2 + ((yy - OH / 2) / (OH / 1.6)) ** 2)
grad = 1 - 0.32 * np.clip((yy - 1150) / 600, 0, 1) * np.clip((1950 - yy) / 300, 0, 1)
mult = np.clip(vig * grad, 0, 1)[..., None].astype(np.float32)

cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                       "-i", "edit/zen1/music.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p",
                       "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
TOT = n / FPS
for i in range(n):
    ok, fr = cap.read()
    if not ok: break
    tm = i / FPS
    x0 = int(round(cx[i] - CW / 2))
    crop = fr[:, x0:x0 + CW]
    up = cv2.resize(crop, (OW, OH), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(up, (0, 0), 3)
    up = cv2.addWeighted(up, 1.45, bl, -0.45, 0)  # nitidez suave tras el escalado
    rgb = cv2.cvtColor(up, cv2.COLOR_BGR2RGB).astype(np.float32)
    # grade cálido y suave
    rgb[..., 0] *= 1.04; rgb[..., 2] *= 0.95
    rgb = rgb * 0.94 + 10
    rgb *= mult
    g = min(1, tm / 0.9, (TOT - tm) / 1.0)  # fundido de entrada y salida
    rgb *= max(g, 0)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    for (a, b, _, _), L, Sh in zip(PHRASES, layers, shadows):
        p, blur, dy = text_state(tm, a, b)
        if p <= 0: continue
        for lay in (Sh, L):
            l = lay.filter(ImageFilter.GaussianBlur(blur)) if blur > 0.3 else lay
            al = l.split()[3].point(lambda v: int(v * p))
            l = l.copy(); l.putalpha(al)
            img.alpha_composite(l, (0, int(TEXT_CY - 260 + dy)))
    ff.stdin.write(img.convert("RGB").tobytes())
ff.stdin.close(); ff.wait()
print("rendered", OUT)
