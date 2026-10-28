# video-zen · plan por escenas v1

Fuente: `Material crudo/video_2026-10-28.mp4` (848×480 horizontal, 18.6 s, sin audio).
Decisiones del usuario: frases de calma · recorte vertical a la persona · pad ambiental + cuencos · serif blanca elegante.

| Tiempo | Qué se ve | Texto en pantalla | Efecto | Sonido | Herramienta |
|---|---|---|---|---|---|
| 0.0–0.9 | Fundido desde negro; ella escribe en su escritorio | — | Fade in | Entra el pad (Re mayor) | ffmpeg/OpenCV |
| 0.3–5.5 | Plano vertical que sigue su cara | "Cada día, / *con calma*" | Aparición lenta con desenfoque y leve subida | Cuenco a 0.5 s | Python (PIL) |
| 6.5–11.4 | Ella se inclina a escribir; la cámara la acompaña | "Dedicación / *en cada detalle*" | Igual | Cuenco a 6.4 s; acorde Si menor → Sol | Python (PIL) |
| 12.5–17.6 | Levanta la vista, plano medio | "Tu bienestar / *empieza aquí*" | Igual | Cuenco a 12.4 s; acorde La sus | Python (PIL) |
| 17.5–18.5 | Cierre | — | Fundido a negro | Cuenco final + fade out | ffmpeg |

- Texto a y≈1300–1560 (tercio inferior), siempre debajo de la cara (detección YuNet cuadro a cuadro).
- Tipografía: Instrument Serif (OFL) regular + cursiva, blanca con sombra suave; línea fina debajo.
- Grade cálido suave + viñeta y degradado inferior para leer el texto.
- Música generada localmente (sin samples ni servicios externos), mezclada a −14 LUFS.
