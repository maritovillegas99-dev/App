#!/usr/bin/env python3
"""Música épica generada por código (sin muestras ni servicios externos), para reels motivacionales.

  python3 tools/music_epic.py salida.wav --dur 30 --drums 10.6 --riser 17.5 --climax 23.0 --hit 24.8 --outro 26.0

Re menor a 90 bpm: zumbido grave desde el inicio, colchón de acordes (Dm Bb F C) y ostinato desde --pulse,
tambores desde --drums, riser y redoble hacia --climax (braam + percusión al doble), golpe en --hit y cierre en
re mayor que se apaga desde --outro. Los tiempos van en segundos del video final.
"""
import argparse

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, lfilter

SR = 48000
BEAT = 60 / 90
rng = np.random.default_rng(7)


def t_(n):
    return np.arange(n) / SR


def saw(f, n, detune=0.0):
    ph = (t_(n) * f * (1 + detune)) % 1.0
    return 2 * ph - 1


def lowpass(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2))
    return lfilter(b, a, x)


def highpass(x, fc):
    b, a = butter(2, fc / (SR / 2), btype="high")
    return lfilter(b, a, x)


def env(n, a=0.01, d=0.3):
    t = t_(n)
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    m = min(len(x), len(buf) - i)
    buf[i:i + m] += x[:m]


def note(name):
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "Bb": 1}
    p, octv = name[:-1], int(name[-1])
    return 440 * 2 ** ((names[p] + 12 * (octv - 4)) / 12)


def pad_chord(notes, n):
    x = sum(saw(note(k), n, d) for k in notes for d in (-0.004, 0.0, 0.005))
    return lowpass(x / (3 * len(notes)), 1400)


def kick(n=int(0.5 * SR)):
    t = t_(n)
    f = 45 + 80 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28)


def tom(f0=90, d=0.45):
    n = int(1.0 * SR)
    t = t_(n)
    body = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.6 * np.exp(-t / 0.05))) / SR) * np.exp(-t / d)
    skin = lowpass(rng.standard_normal(n), 2500) * np.exp(-t / 0.06) * 0.5
    return body + skin


def snare():
    n = int(0.3 * SR)
    t = t_(n)
    return highpass(rng.standard_normal(n), 1200) * np.exp(-t / 0.08) * 0.6 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4


def braam(n):
    t = t_(n)
    x = sum(saw(note(k), n, d) for k in ("D1", "D2", "A2", "D3") for d in (-0.006, 0.006))
    cutoff = 300 + 2500 * np.minimum(1, t / 0.25) * np.exp(-t / 1.2)
    # filtro variable por bloques
    out = np.zeros(n)
    blk = 2048
    for i in range(0, n, blk):
        out[i:i + blk] = lowpass(x[i:i + blk], max(120, cutoff[i]), 1)
    return out / 8 * np.minimum(1, t / 0.02) * np.exp(-t / 2.2)


def reverb(x, secs=2.2, mix=0.25):
    n = int(secs * SR)
    ir = rng.standard_normal(n) * np.exp(-t_(n) / (secs / 5))
    ir = lowpass(ir, 6000)
    wet = fftconvolve(x, ir)[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return (1 - mix) * x + mix * wet * np.max(np.abs(x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--dur", type=float, default=30.0)
    ap.add_argument("--pulse", type=float, default=4.4)
    ap.add_argument("--drums", type=float, default=10.6)
    ap.add_argument("--riser", type=float, default=17.5)
    ap.add_argument("--climax", type=float, default=23.0)
    ap.add_argument("--hit", type=float, default=24.8)
    ap.add_argument("--outro", type=float, default=26.0)
    a = ap.parse_args()
    N = int(a.dur * SR)
    T = t_(N)
    mus = np.zeros(N)

    # zumbido grave: entra en 3 s, crece hacia el clímax, se apaga al final
    drone = lowpass(saw(note("D2"), N) + 0.6 * saw(note("A2"), N, 0.003), 260)
    g = np.clip(T / 3, 0, 1) * (0.5 + 0.5 * np.clip((T - a.riser) / (a.climax - a.riser), 0, 1))
    g *= np.clip((a.dur - T) / 3, 0, 1)
    mus += 0.35 * drone * g

    # colchón de acordes, un acorde por compás
    prog = [("D3", "F3", "A3", "D4"), ("Bb2", "D3", "F3", "Bb3"), ("F2", "C3", "F3", "A3"), ("C3", "E3", "G3", "C4")]
    bar = 4 * BEAT
    k, t0 = 0, a.pulse - bar / 2
    while t0 < a.outro:
        n = int(bar * 1.05 * SR)
        c = pad_chord(prog[k % 4], n) * np.minimum(1, t_(n) / 0.4) * np.clip((bar * 1.05 - t_(n)) / 0.3, 0, 1)
        lvl = 0.22 if t0 < a.climax else 0.32
        place(mus, c * lvl, max(0, t0))
        t0 += bar
        k += 1
    # final en re mayor
    nf = int((a.dur - a.outro) * SR)
    fsharp = note("F3") * 2 ** (1 / 12)  # la tercera mayor (fa#) cierra en re mayor
    fin = pad_chord(("D3", "A3", "D4"), nf) + 0.25 * lowpass(saw(fsharp, nf) + saw(fsharp, nf, 0.004), 1400)
    fin *= np.minimum(1, t_(len(fin)) / 0.5) * np.clip((a.dur - a.outro - t_(len(fin))) / 2.5, 0, 1)
    place(mus, fin * 0.3, a.outro)

    # ostinato en corcheas
    t0 = a.pulse
    while t0 < a.outro:
        n = int(0.3 * SR)
        p = lowpass(saw(note("D3"), n), 1800) * env(n, 0.005, 0.12)
        if t0 >= a.drums:
            p += 0.6 * lowpass(saw(note("D4"), n), 2500) * env(n, 0.005, 0.1)
        place(mus, p * (0.18 if t0 < a.climax else 0.26), t0)
        t0 += BEAT / 2

    # percusión
    drums = np.zeros(N)
    t0 = a.drums
    b = 0
    while t0 < a.outro:
        step = BEAT / 2 if t0 >= a.climax else BEAT
        if t0 >= a.climax or b % 2 == 0:
            place(drums, kick() * 0.9, t0)
        if t0 < a.climax and b % 4 == 3:
            place(drums, tom(80) * 0.7, t0)
        if t0 >= a.climax and b % 2 == 1:
            place(drums, tom(110, 0.3) * 0.6, t0)
        t0 += step
        b += 1
    # redoble que crece antes del clímax
    roll0 = a.climax - 1.6
    t0, i = roll0, 0
    while t0 < a.climax - 0.02:
        place(drums, snare() * (0.15 + 0.6 * (t0 - roll0) / 1.6), t0)
        t0 += max(0.05, 0.16 - 0.11 * (t0 - roll0) / 1.6)
    # golpes
    for at, lvl in ((a.drums, 0.9), (a.climax, 1.2), (a.hit, 1.0)):
        place(drums, kick() * lvl, at)
        place(drums, tom(55, 0.8) * lvl, at)
    place(mus, braam(int(3.0 * SR)) * 0.55, a.climax)
    place(mus, braam(int(2.0 * SR)) * 0.3, a.hit)

    # riser de ruido filtrado hacia el clímax
    n = int((a.climax - a.riser) * SR)
    tr = t_(n) / (n / SR)
    noise = rng.standard_normal(n)
    rise = np.zeros(n)
    for i in range(0, n, 2048):
        rise[i:i + 2048] = lowpass(noise[i:i + 2048], 300 + 7000 * tr[i] ** 2, 1)
    place(mus, rise * tr ** 2 * 0.25, a.riser)

    mix = 1.7 * reverb(mus, 2.5, 0.3) + 0.6 * reverb(drums, 1.2, 0.15)
    mix = np.tanh(mix * 0.8) / np.tanh(0.8)  # saturación suave: más cuerpo, sin picos sueltos
    mix = highpass(mix, 30)
    mix /= np.max(np.abs(mix)) + 1e-9
    mix *= 0.89
    sf.write(a.out, np.stack([mix, np.roll(mix, int(0.012 * SR))], axis=1), SR)
    print(a.out, f"{a.dur:.1f} s")


if __name__ == "__main__":
    main()
