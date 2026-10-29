#!/usr/bin/env python3
"""Props del estilo "blanco minimalista" (src/ReelMinimal.tsx) para un clip de la serie del podcast.

Lee edit/podcast/serie.json (gancho y palabras clave por clip) y faces.json del clip, y agrega a
edit/podcast-<id>/reelkit-props.json: minimalHook {text, until, top} con el gancho bajo el mentón medido en sus
segundos, y emphasis. Correr después de `visual_plan.py export … --props`.

  python3 tools/serie_props.py 01 02 …
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK_H = 2 * 64 * 1.08 + 26   # igual que ReelMinimal.tsx
SUB_BLOCK = 2 * 76 * 1.38 * 1.12  # dos líneas de subtítulo con una palabra clave
BOTTOM = 1500


def main():
    serie = json.loads((ROOT / "edit/podcast/serie.json").read_text())
    for cid in sys.argv[1:]:
        d = ROOT / f"edit/podcast-{cid}"
        cfg = serie["clips"][cid]
        props_path = d / "reelkit-props.json"
        props = json.loads(props_path.read_text())
        faces = json.loads((d / "faces.json").read_text())
        until = serie["hook_seconds"]
        chins = [f[1] + f[3] for s in faces["samples"] if s["t"] <= until + 0.25 for f in s["faces"]]
        chin = max(chins) if chins else 1000
        top = int(chin + 40)
        top = min(top, int(BOTTOM - SUB_BLOCK - HOOK_H))  # gancho + subtítulos caben sobre y 1500
        if top < chin + 20:
            print(f"{cid}: ojo, el gancho queda a {top - chin} px del mentón")
        props["minimalHook"] = {"text": cfg["hook"], "until": until, "top": top}
        props["emphasis"] = cfg["emphasis"]
        props_path.write_text(json.dumps(props, ensure_ascii=False, indent=1))
        print(f"{cid}: gancho «{cfg['hook']}» en y {top} (mentón {chin}), subtítulos en y {props.get('subtitlesTop')}")


if __name__ == "__main__":
    main()
