import cv2, json, sys
src = sys.argv[1]
cap = cv2.VideoCapture(src)
W, H = int(cap.get(3)), int(cap.get(4))
det = cv2.FaceDetectorYN.create("models/face_detection_yunet_2023mar.onnx", "", (W, H), 0.2)
out = []
last = None
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    _, faces = det.detect(f)
    # cara con buena confianza, o (cuando mira hacia abajo) candidata débil cerca de la última posición
    cand = []
    for fc in (faces if faces is not None else []):
        x, y, w, h = fc[:4]; sc = float(fc[14]); fx, fy = float(x + w/2), float(y + h/2)
        if sc >= 0.6 or (fy < 230 and last is not None and abs(fx - last) < 60):
            cand.append((sc, fx, fy, float(w), float(h)))
    if cand:
        sc, fx, fy, w, h = max(cand)
        last = fx
        out.append([i, fx, fy, w, h])
    else:
        out.append([i, None, None, None, None])
    i += 1
json.dump({"W": W, "H": H, "n": i, "faces": out}, open("edit/zen1/faces_src.json", "w"))
hits = [o for o in out if o[1] is not None]
print(i, "frames,", len(hits), "with face")
for o in out[::30]: print(o)
