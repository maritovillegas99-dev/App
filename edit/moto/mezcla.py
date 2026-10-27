import json, subprocess, sys
X = "/home/user/App/.claude/skills/media-use/audio/assets/sfx"
mus_vol, ratio, thr, riser, vozg = [float(a) for a in sys.argv[1:6]]
NOVOZ = len(sys.argv) > 6
tl = json.load(open('timeline.json'))
inp, f = [], []
for i, l in enumerate(tl):
    inp += ['-i', 'voz/' + l['archivo']]
    # frases que caen sobre tambores, riser o clímax: un poco más arriba para no perderse
    g = {5: 2.8, 9: 1.3, 10: 5.0, 11: 3.6, 12: 1.4}.get(l['n'], 1.0)
    f.append(f"[{i}]aresample=48000,volume={g},adelay={int(l['start']*1000)}:all=1[v{i}]")
n = len(tl)
f.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,highpass=f=80,asetrate=46080,aresample=48000,atempo=1.04167,lowpass=f=8500,equalizer=f=220:t=q:w=1:g=3,equalizer=f=3000:t=q:w=1.2:g=1,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=150:makeup=2,chorus=0.7:0.9:35:0.25:0.3:1.8,aecho=0.8:0.75:70|140|230:0.24|0.16|0.10,volume={vozg},pan=stereo|c0=c0|c1=c0,apad=whole_dur=30[voz]")
sfx = [("whoosh-cinematic.mp3", 0.0, 1.9, 0.45), ("riser.mp3", 19.98, 0.0, riser), ("whoosh.mp3", 22.85, 0.0, 0.8),
       ("impact-bass-1.mp3", 10.25, 0.0, 0.6), ("impact-bass-1.mp3", 22.85, 0.0, 0.7), ("impact-bass-1.mp3", 24.62, 0.0, 0.6)]
inp += ['-i', 'audio/musica.wav']; m = n; base = n + 1
for j, (s, at, ss, g) in enumerate(sfx):
    inp += ['-ss', str(ss), '-i', f"{X}/{s}"]
    f.append(f"[{base+j}]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={int(at*1000)}:all=1[s{j}]")
f.append("".join(f"[s{j}]" for j in range(len(sfx))) + f"amix=inputs={len(sfx)}:normalize=0[fx0]")
f.append(f"[{m}]volume={mus_vol}[mus0]")
f.append("[voz]asplit=3[voz1][key][key2]")
f.append(f"[mus0][key]sidechaincompress=threshold={thr}:ratio={ratio}:attack=15:release=350[mus]")
f.append(f"[fx0][key2]sidechaincompress=threshold={thr}:ratio={ratio}:attack=15:release=350[fx]")
f.append(f"[voz1]volume={0 if NOVOZ else 1}[vz]")
f.append("[vz][mus][fx]amix=inputs=3:normalize=0,atrim=0:30,afade=t=out:st=28.6:d=1.4[mix]")
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ";".join(f), '-map', '[mix]', '-ar', '48000', '-c:a', 'pcm_f32le', ('tmp/fondo.wav' if NOVOZ else 'audio/premix.wav')], check=True)
if NOVOZ: sys.exit()
r = subprocess.run(['ffmpeg', '-i', 'audio/premix.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
d = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/premix.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true,aresample=48000",
                'audio/mezcla_final.wav'], check=True)
