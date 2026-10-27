// Reel motivacional de moto (Resultados/moto_plan_v1.md): placa de video ya graduada y en cámara lenta
// (public/moto/plate.mp4), mezcla final (public/moto/mezcla.wav) y subtítulos cinemáticos palabra por palabra.
import { CameraMotionBlur } from "@remotion/motion-blur";
import { loadFont } from "@remotion/google-fonts/Anton";
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { LINES, Line, W } from "./timeline";

const { fontFamily } = loadFont("normal", { weights: ["400"], subsets: ["latin", "latin-ext"] });

export const FPS = 30;
export const DURATION = 30 * FPS;
const AMBER = "#F5B83D";
const CLIMAX = 22.85; // golpe de "Acelera"
const HIT = 24.62; // golpe de "Vive al máximo"
const FADE_OUT = [25.9, 26.5]; // el video se va a negro antes de la frase final
const BAND_Y = 1385; // centro de la franja de subtítulos (y 1290–1490, fuera de la UI de las apps)

// Un bloque = las palabras que se ven juntas: corta en coma o al pasar ~18 caracteres.
type Chunk = { words: W[]; start: number; end: number; line: Line };
const chunks: Chunk[] = [];
for (const line of LINES) {
  let cur: W[] = [];
  const flush = () => {
    if (cur.length) chunks.push({ words: cur, start: cur[0].s, end: 0, line });
    cur = [];
  };
  for (const w of line.words) {
    const len = cur.map((x) => x.t).join(" ").length;
    const whole = line.n === 1 || line.n === 12; // el gancho y el cierre se leen enteros
    if (!whole && cur.length && len + 1 + w.t.length > 18) flush();
    cur.push(w);
    if (!whole && w.t.endsWith(",")) flush();
  }
  flush();
}
chunks.forEach((c, i) => {
  const next = chunks[i + 1];
  const lastWord = c.words[c.words.length - 1];
  c.end = next ? Math.min(next.start, Math.max(lastWord.e + 0.5, next.start - 0.05)) : 30;
  if (next && next.line.n !== c.line.n) c.end = Math.min(next.start, lastWord.e + 0.9);
});

const big = (n: number) => n === 10 || n === 11;

const Word: React.FC<{ w: W; chunkStart: number; hook: boolean; size: number }> = ({ w, chunkStart, hook, size }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // el gancho se ve completo desde el cuadro 1 (funciona sin sonido); el resto entra con la voz
  const at = hook ? chunkStart - 0.4 : w.s - 0.03;
  const p = spring({ frame: frame - at * fps, fps, config: { damping: 14, stiffness: 170, mass: 0.6 } });
  const t = hook ? 1 : p;
  return (
    <span
      style={{
        display: "inline-block",
        marginRight: size * 0.22,
        color: w.k ? AMBER : "white",
        opacity: interpolate(t, [0, 0.6], [0, 1], { extrapolateRight: "clamp" }),
        filter: `blur(${interpolate(t, [0, 1], [14, 0])}px)`,
        transform: `translateY(${interpolate(t, [0, 1], [28, 0])}px) scale(${interpolate(t, [0, 1], [1.25, 1])})`,
      }}
    >
      {w.t}
    </span>
  );
};

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  const c = chunks.find((x) => sec >= x.start - (x.line.n === 1 ? 0.4 : 0.05) && sec < x.end);
  if (!c) return null;
  const n = c.line.n;
  const final = n === 12;
  const size = big(n) ? 170 : final ? 130 : 118;
  const out = interpolate(sec, [c.end - 0.15, c.end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        top: final ? 0 : BAND_Y - 960,
        opacity: out,
        filter: `blur(${(1 - out) * 10}px)`,
      }}
    >
      <div
        style={{
          fontFamily,
          fontSize: size,
          lineHeight: 1.0,
          letterSpacing: 2,
          textAlign: "center",
          width: final ? 860 : 980,
          textShadow: "0 6px 30px rgba(0,0,0,0.45)",
        }}
      >
        {c.words.map((w, i) => (
          <Word key={i} w={w} chunkStart={c.start} hook={n === 1} size={size} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Plate: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  // golpe de zoom y sacudida en "Acelera"; golpe más corto en "Vive al máximo"
  const punch = (t0: number, amp: number, dur: number) =>
    sec >= t0 && sec < t0 + dur ? amp * Math.exp(-(sec - t0) / (dur / 4)) : 0;
  const shake = punch(CLIMAX, 14, 1.6) + punch(HIT, 8, 0.8);
  const scale = 1 + punch(CLIMAX, 0.06, 1.6) + punch(HIT, 0.035, 0.8);
  const dx = (random(`x${frame}`) - 0.5) * 2 * shake;
  const dy = (random(`y${frame}`) - 0.5) * 2 * shake;
  const fade = interpolate(sec, FADE_OUT, [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill style={{ opacity: fade, transform: `translate(${dx}px, ${dy}px) scale(${scale})` }}>
        <OffthreadVideo src={staticFile("moto/plate.mp4")} muted />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  const f = (t0: number, a: number) => (sec >= t0 && sec < t0 + 0.25 ? a * (1 - (sec - t0) / 0.25) : 0);
  return <AbsoluteFill style={{ backgroundColor: "white", opacity: f(CLIMAX, 0.45) + f(HIT, 0.3) }} />;
};

export const MotoReel: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Plate />
    <Flash />
    <CameraMotionBlur shutterAngle={180} samples={6}>
      <Captions />
    </CameraMotionBlur>
    <Audio src={staticFile("moto/mezcla.wav")} />
  </AbsoluteFill>
);

// Portada: la foto del usuario a pantalla completa, con el gancho en el cielo (lejos de las caras).
export const MotoCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Img
      src={staticFile("moto/portada.jpg")}
      style={{ width: 1080, height: 1920, objectFit: "cover", filter: "contrast(1.08) saturate(1.1)" }}
    />
    <AbsoluteFill
      style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.45) 26%, rgba(0,0,0,0) 40%)" }}
    />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%)" }} />
    <div
      style={{
        position: "absolute",
        top: 250,
        width: 1080,
        textAlign: "center",
        fontFamily,
        lineHeight: 0.95,
        letterSpacing: 3,
        textShadow: "0 8px 36px rgba(0,0,0,0.5)",
      }}
    >
      <div style={{ fontSize: 150, color: "white" }}>LA VIDA</div>
      <div style={{ fontSize: 150, color: AMBER }}>NO TE ESPERA</div>
    </div>
  </AbsoluteFill>
);
