// "Blanco minimalista" (serie podcast péptidos): the kit's ReelKit for the footage and checks, with the subtitles and the
// hook drawn here instead: bold white Montserrat with a soft shadow, no plate and no accent color; words come up as they
// are spoken (the line keeps its place, no jumps); key words (props.emphasis) are drawn larger instead of in color.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { measureText } from "@remotion/layout-utils";
import { KIT_FPS, ReelKit, ReelKitProps, reelKitDefaults, Sampled } from "./ReelKit";
import { brandFont, BrandFont } from "./kit/brand";
import { useFontsReady } from "./kit/Phrase";
import { buildChunks, Word } from "./kit/Subtitles";

export type ReelMinimalProps = ReelKitProps & {
  emphasis?: string[]; // words (any case, no punctuation) drawn ×EMPH larger
  minimalHook?: { text: string; until: number; top?: number } | null; // headline in the same white style; top: under the measured chin
};

const FONT: BrandFont = { family: "Montserrat", weights: [700, 800, 900], source: "google" };
const SIZE = 76;
const EMPH = 1.38;
const MAX_W = 900;
const BOTTOM = 1500; // nothing below: the app's UI
const HOOK_UP = 100; // the hook starts this far above the subtitle top (still under the chin: export puts that top at chin + 30 or lower)
const HOOK_H = 2 * 64 * 1.08 + 26; // two hook lines + the gap to the subtitles
const SHADOW = "0 3px 14px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.6)";
const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ%-]/g, "");

type Line = { words: Word[]; width: number; height: number };

const layout = (ws: Word[], font: string, emph: Set<string>, ready: boolean): Line[] => {
  const size = (w: Word) => (emph.has(norm(w.text)) ? SIZE * EMPH : SIZE);
  const wordW = (w: Word) => (ready ? measureText({ text: w.text, fontFamily: font, fontSize: size(w), fontWeight: 800 }).width : w.text.length * size(w) * 0.6);
  const space = SIZE * 0.28;
  const lines: Line[] = [];
  let cur: Word[] = [];
  let curW = 0;
  ws.forEach((w) => {
    const ww = wordW(w);
    if (cur.length && curW + space + ww > MAX_W) {
      lines.push({ words: cur, width: curW, height: Math.max(...cur.map(size)) * 1.12 });
      cur = [];
      curW = 0;
    }
    curW += (cur.length ? space : 0) + ww;
    cur.push(w);
  });
  if (cur.length) lines.push({ words: cur, width: curW, height: Math.max(...cur.map(size)) * 1.12 });
  return lines;
};

const MinimalSubs: React.FC<{ words: Word[]; top: number; emphasis: string[]; hide: [number, number][]; font: string }> = (
  { words, top, emphasis, hide, font },
) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ready = useFontsReady([font]);
  const emph = React.useMemo(() => new Set(emphasis.map(norm)), [emphasis]);
  const chunks = React.useMemo(() => buildChunks(words, 3, 18), [words]);
  const t = frame / fps;
  if (hide.some(([a, b]) => t >= a && t < b)) return null;
  const c = chunks.find((x) => t >= x.start - 0.05 && t < x.end);
  if (!c) return null;
  const lines = layout(c.words, font, emph, ready);
  const total = lines.reduce((n, l) => n + l.height, 0);
  const y0 = Math.min(top, BOTTOM - total);
  return (
    <div data-rk="sub" style={{ position: "absolute", left: (1080 - MAX_W) / 2, width: MAX_W, top: y0, display: "flex", flexDirection: "column", alignItems: "center" }}>
      {lines.map((l, i) => (
        <div key={i} style={{ display: "flex", alignItems: "baseline", justifyContent: "center", gap: SIZE * 0.28, height: l.height, whiteSpace: "pre" }}>
          {/* only the words already said: each line stays centered on what is on screen (line breaks fixed per chunk) */}
          {l.words.filter((w) => w === c.words[0] || t >= w.start - 0.03).map((w, k) => {
            const big = emph.has(norm(w.text));
            const since = t - (w.start - 0.03);
            const p = interpolate(since * fps, [0, 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
            return (
              <span key={k} style={{ fontFamily: font, fontWeight: big ? 900 : 800, fontSize: big ? SIZE * EMPH : SIZE, lineHeight: 1.05, color: "#FFFFFF",
                textShadow: SHADOW, opacity: w === c.words[0] ? 1 : p, transform: `translateY(${(1 - p) * 10}px) scale(${0.92 + 0.08 * p})`,
                display: "inline-block", transformOrigin: "50% 80%" }}>
                {w.text}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const MinimalHook: React.FC<{ hook: { text: string; until: number }; top: number; font: string }> = ({ hook, top, font }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  if (t >= hook.until) return null;
  const a = interpolate(frame, [0, 6, hook.until * fps - 6, hook.until * fps], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const y = interpolate(frame, [0, 8], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <div data-rk="hook" style={{ position: "absolute", left: (1080 - MAX_W) / 2, width: MAX_W, top, textAlign: "center", fontFamily: font, fontWeight: 900, fontSize: 64,
      lineHeight: 1.08, color: "#FFFFFF", textShadow: SHADOW, opacity: a, transform: `translateY(${y}px)`, textTransform: "uppercase", letterSpacing: 0.5 }}>
      {hook.text}
    </div>
  );
};

const Frame: React.FC<ReelMinimalProps> = (p) => {
  const font = brandFont(FONT);
  const hook = p.minimalHook ?? null;
  const top = p.subtitlesTop ?? 1290;
  const frame = useCurrentFrame();
  // the hook sits where the subtitles start (under the chin: the headroom above the head is too small in these shots);
  // while it shows, the subtitles move down under it
  const hookOn = !!hook && frame / KIT_FPS < hook.until;
  const hookTop = hook?.top ?? top - HOOK_UP;
  return (
    <AbsoluteFill>
      <ReelKit {...p} subtitles="none" hook={null} sample={null} />
      {hook ? <MinimalHook hook={hook} top={hookTop} font={font} /> : null}
      <MinimalSubs words={(p.subtitleCaptions ?? p.captions).words} top={hookOn ? Math.max(top, hookTop + HOOK_H) : top} emphasis={p.emphasis ?? []}
        hide={p.hideSubtitles ?? []} font={font} />
    </AbsoluteFill>
  );
};

export const ReelMinimal: React.FC<ReelMinimalProps> = (p) =>
  p.sample?.frames?.length ? <Sampled sample={p.sample}><Frame {...p} /></Sampled> : <Frame {...p} />;

export const reelMinimalDefaults: ReelMinimalProps = { ...reelKitDefaults, emphasis: [], minimalHook: null };
