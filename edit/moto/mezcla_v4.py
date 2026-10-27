import json, subprocess, sys
X = "/home/user/App/.claude/skills/media-use/audio/assets/sfx"
mus_vol, ratio, thr, riser, vozg = [float(a) for a in sys.argv[1:6]]
NOVOZ = len(sys.argv) > 6
tl = json.load(open('timeline_v4.json'))
inp, f = [], []
for i, l in enumerate(tl):
    inp += ['-i', 'voz_propia/' + l['archivo']]
    # frases que caen sobre tambores, riser o clímax: un poco más arriba para no perderse
    g = {2: 1.1, 3: 1.1, 4: 1.2, 5: 2.0, 6: 1.25, 7: 1.3, 8: 1.4, 9: 1.7, 10: 1.8, 11: 1.5, 12: 1.4}.get(l['n'], 1.0)
    f.append(f"[{i}]aresample=48000,highpass=f=90,afftdn=nr=8:nf=-45,deesser=i=0.4,equalizer=f=200:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-22dB:ratio=3:attack=6:release=150:makeup=3,aecho=0.8:0.7:60|120|200:0.18|0.12|0.07,volume={vozg},volume={g},adelay={int(l['start']*1000)}:all=1[v{i}]")
n = len(tl)
f.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,pan=stereo|c0=c0|c1=c0,apad=whole_dur=30[voz]")
sfx = [("whoosh-cinematic.mp3", 0.0, 1.9, 0.45), ("riser.mp3", 20.58, 0.0, riser), ("whoosh.mp3", 23.45, 0.0, 0.4),
       ("impact-bass-1.mp3", 10.25, 0.0, 0.6), ("impact-bass-1.mp3", 23.5, 0.0, 0.35), ("impact-bass-1.mp3", 24.68, 0.0, 0.3)]
inp += ['-i', 'audio/musica_v4.wav']; m = n; base = n + 1
for j, (s, at, ss, g) in enumerate(sfx):
    inp += ['-ss', str(ss), '-i', f"{X}/{s}"]
    f.append(f"[{base+j}]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(at*1000)}:all=1[s{j}]")
f.append("".join(f"[s{j}]" for j in range(len(sfx))) + f"amix=inputs={len(sfx)}:normalize=0[fx0]")
# la música abre un hueco solo mientras dices "Acelera" y "Vive" (el golpe pega justo antes)
holes = "+".join(f"between(t,{l['words'][0]['start']-0.05:.2f},{l['words'][-1]['end']+0.1:.2f})" for l in tl if l['n'] in (10, 11))
f.append(f"[{m}]volume={mus_vol},volume='if({holes},0.4,1)':eval=frame[mus0]")
f.append("[voz]asplit=3[voz1][key][key2]")
f.append(f"[mus0][key]sidechaincompress=threshold={thr}:ratio={ratio}:attack=15:release=350[mus]")
f.append(f"[fx0]volume='if({holes},0.5,1)':eval=frame[fx1]")
f.append(f"[fx1][key2]sidechaincompress=threshold={thr}:ratio={ratio}:attack=15:release=350[fx]")
f.append(f"[voz1]volume={0 if NOVOZ else 1}[vz]")
f.append("[vz][mus][fx]amix=inputs=3:normalize=0,atrim=0:30,afade=t=out:st=28.6:d=1.4[mix]")
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ";".join(f), '-map', '[mix]', '-ar', '48000', '-c:a', 'pcm_f32le', ('tmp/fondo_v4.wav' if NOVOZ else 'audio/premix_v4.wav')], check=True)
if NOVOZ: sys.exit()
r = subprocess.run(['ffmpeg', '-i', 'audio/premix_v4.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
d = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/premix_v4.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,aresample=48000",
                'audio/mezcla_v4.wav'], check=True)
