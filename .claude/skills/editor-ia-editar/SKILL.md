---
name: editor-ia-editar
description: Paso 4 de la guía Editor IA. Edita un video crudo de "Material crudo" con la guía de estilo de "Referentes" y exporta un MP4 1080×1920 a "Resultados", usando IT Reelsmaker, Embedded Captions, Remotion, HyperFrames y Media Use. Úsala cuando el usuario diga "edita mi video", "edita el más reciente", suba un video crudo, o pida correcciones sobre un video ya editado ("corta la pausa del segundo 12", "baja la música").
---

# Editor IA · Graba y edita

Sigue al pie de la letra el **prompt maestro** de `prompts/03-editar.md` (secciones
CONTEXTO Y ROL → VERIFICACIÓN FINAL). Es la instrucción de trabajo; no la resumas.

Preparación:

1. Si el usuario subió el video por el chat, cópialo a `Material crudo/` (nunca lo
   edites ahí: trabaja sobre una copia en `edit/<id>/`).
2. Lee `Referentes/guia-de-estilo.md`. Si no existe, analiza lo que haya en
   `Referentes/` y propone 2 o 3 direcciones visuales (como dice el prompt).
3. Datos de [MI VIDEO] que falten: pregúntalos junto con tus dudas, máximo 4
   preguntas de opción múltiple con tu recomendación marcada.

Transcripción: si el modelo de faster-whisper no se puede descargar (Hugging Face bloqueado en
la nube), usa el respaldo local: `python3 .claude/skills/it-reelsmaker/scripts/transcribe.py audio edit/<id> <fuente>`
y luego `python3 tools/transcribe_parakeet.py <wav> edit/<id>/transcripts/<stem>.json`, y valida con
`transcribe.py check`.

Mapa de skills (orden del FLUJO):

| Paso | Skill | Para qué |
|---|---|---|
| Corte, vertical, subtítulos base, −14 LUFS | `it-reelsmaker` | la base; scripts en `.claude/skills/it-reelsmaker/scripts/`, proyecto Remotion en `reels/` |
| Texto/gráficos detrás de la persona, recortes | `embedded-captions` (+ `matte.py` de it-reelsmaker con rembg) | solo si un efecto lo necesita |
| Animaciones en código con motion blur | `remotion-best-practices`, `remotion-captions`, `remotion-render` | tarjetas, contadores, tier lists, transiciones |
| Motion graphics HTML | `hyperframes`, `hyperframes-cli`, `hyperframes-registry` | pantallas, producto, títulos |
| Sonido y mezcla | `media-use` | whoosh/pop/impacto/riser, música, voz por encima |

Entregables en `Resultados/`: `<nombre>_plan_v1.md` (tabla por escenas; **espera la
aprobación** antes de producir) y `<nombre>_editado_v1.mp4` (v2, v3… en cada
corrección, sin borrar la anterior). Verifica con `ffprobe` (duración, 1080×1920) y
`ffmpeg -af ebur128` (≈ −14 LUFS) antes de entregar.

Correcciones: aplica el cambio pedido y exporta la siguiente versión. Si es una
preferencia general ("siempre…", "nunca…"), guárdala también en
`Referentes/guia-de-estilo.md` y en `brands/<slug>/rules.md`.
