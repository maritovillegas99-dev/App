#!/usr/bin/env python3
"""Corrige el texto de los subtítulos (captions.json) de un clip sin tocar el audio ni los tiempos de corte.

La transcripción local (Parakeet) se equivoca en términos médicos y nombres ("pépidos", "Lili", "asiática"). Las
correcciones viven en edit/podcast/fixes.json, por clip, como pares ["texto como quedó", "texto correcto"]: una
secuencia exacta de palabras se reemplaza por otra, y sus tiempos se reparten por largo entre las palabras nuevas.
Se aplica sobre captions.json recién salido de cut.py (guarda el original como captions.raw.json y siempre parte de
él, así se puede correr de nuevo).

  python3 tools/fix_captions.py 01 02 …
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace(words, old, new):
    o = old.split()
    n = len(o)
    for i in range(len(words) - n + 1):
        if [w["text"] for w in words[i:i + n]] == o:
            first, last = words[i], words[i + n - 1]
            toks = new.split()
            if not toks:
                return words[:i] + words[i + n:]
            a, b = first["start"], last["end"]
            total = sum(len(t) + 1 for t in toks)
            out, t = [], a
            for tok in toks:
                dur = (b - a) * (len(tok) + 1) / total
                w = {k: v for k, v in first.items() if k not in ("text", "start", "end")}
                w.update(text=tok, start=round(t, 3), end=round(t + dur, 3))
                out.append(w)
                t += dur
            return words[:i] + out + words[i + n:]
    raise SystemExit(f"no encontré «{old}»")


def main():
    fixes = json.loads((ROOT / "edit/podcast/fixes.json").read_text())
    for cid in sys.argv[1:]:
        d = ROOT / f"edit/podcast-{cid}"
        raw = d / "captions.raw.json"
        cap_path = d / "captions.json"
        cap = json.loads(cap_path.read_text())
        if raw.exists() and json.loads(raw.read_text())["duration"] == cap["duration"] and "fixed" in cap:
            cap = json.loads(raw.read_text())
        else:
            raw.write_text(json.dumps(cap, ensure_ascii=False, indent=1))
        words = cap["words"]
        for old, new in fixes.get(cid, []):
            words = replace(words, old, new)
        cap["words"] = words
        cap["fixed"] = len(fixes.get(cid, []))
        cap_path.write_text(json.dumps(cap, ensure_ascii=False, indent=1))
        print(f"== {cid}: {cap['fixed']} correcciones\n" + " ".join(w["text"] for w in words))


if __name__ == "__main__":
    main()
