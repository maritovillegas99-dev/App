# Música zen generada localmente: pad ambiental + cuencos tibetanos. Sin samples ajenos.
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000
DUR = 18.6
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def env(start, length, att, rel):
    e = np.zeros(N)
    s, l = int(start * SR), int(length * SR)
    l = min(l, N - s)
    x = np.arange(l) / SR
    a = np.clip(x / att, 0, 1) ** 2
    r = np.clip((length - x) / rel, 0, 1) ** 2
    e[s:s + l] = a * r
    return e

def pad_note(f):
    out = np.zeros(N)
    for d in (-0.07, 0.0, 0.06):  # detuned voices
        ff = f * 2 ** (d / 12)
        ph = rng.uniform(0, 2 * np.pi)
        out += np.sin(2 * np.pi * ff * t + ph) + 0.25 * np.sin(4 * np.pi * ff * t + ph) + 0.08 * np.sin(6 * np.pi * ff * t)
    return out / 3

# D mayor modal: Dmaj9 - Bm(add11) - Gmaj7 - Aadd9 (sus)
chords = [
    (0.0, [50, 57, 62, 64, 66, 69]),
    (4.6, [47, 54, 59, 62, 64, 66]),
    (9.2, [43, 50, 59, 62, 66, 69]),
    (13.8, [45, 52, 57, 59, 64, 69]),
]
pad = np.zeros(N)
for i, (st, notes) in enumerate(chords):
    ln = (chords[i + 1][0] if i + 1 < len(chords) else DUR) - st + 2.0
    e = env(max(st - 0.8, 0), ln, 2.2, 2.5)
    for m in notes:
        pad += pad_note(hz(m)) * e * (0.9 if m < 52 else 0.5)
pad *= 1 + 0.15 * np.sin(2 * np.pi * 0.11 * t)  # respiración lenta
pad = sosfilt(butter(2, 1800, 'low', fs=SR, output='sos'), pad)

def bowl(start, f0, amp):
    out = np.zeros(N)
    s = int(start * SR)
    x = np.arange(N - s) / SR
    for ratio, a, dec in ((1, 1.0, 6.0), (2.71, 0.5, 4.0), (5.15, 0.25, 2.5), (8.21, 0.1, 1.5)):
        f = f0 * ratio
        beat = 1 + 0.3 * np.sin(2 * np.pi * (1.3 + ratio * 0.4) * x)
        out[s:] += a * np.sin(2 * np.pi * f * x) * np.exp(-x / dec) * beat
    out[s:s + 200] *= np.linspace(0, 1, 200)
    return out * amp

bowls = bowl(0.5, hz(62) / 2 * 2, 0.35) + bowl(6.4, hz(69) / 2 * 2, 0.28) + bowl(12.4, hz(66), 0.3) + bowl(16.9, hz(62) / 2 * 2, 0.18)

# brisa suave (ruido filtrado)
air = sosfilt(butter(2, [300, 1200], 'band', fs=SR, output='sos'), rng.standard_normal(N)) * 0.04

dry = pad * 0.22 + bowls + air

# reverb: IR sintética estéreo
ir_len = int(3.5 * SR)
xi = np.arange(ir_len) / SR
irs = [sosfilt(butter(1, 5000, 'low', fs=SR, output='sos'), rng.standard_normal(ir_len)) * np.exp(-xi / 0.9) for _ in range(2)]
L = dry * 0.6 + fftconvolve(dry, irs[0])[:N] * 0.025
R = dry * 0.6 + fftconvolve(dry, irs[1])[:N] * 0.025
st = np.stack([L, R], 1)
fade = np.ones(N); fi = int(1.0 * SR); fo = int(2.5 * SR)
fade[:fi] = np.linspace(0, 1, fi) ** 2; fade[-fo:] = np.linspace(1, 0, fo) ** 2
st *= fade[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write("edit/zen1/music_raw.wav", SR, (st * 32767).astype(np.int16))
print("ok")
