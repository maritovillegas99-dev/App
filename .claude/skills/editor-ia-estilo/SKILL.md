---
name: editor-ia-estilo
description: Paso 3 de la guía Editor IA. Estudia los videos de la carpeta "Referentes" y crea la guía de estilo del usuario (paleta, tipografías, subtítulos, ritmo, animaciones, sonido, lo que no hace). Úsala cuando el usuario diga "analiza mi estilo", "define mi estilo", "crea mi guía de estilo", suba videos de referencia o pegue links de referentes para descargar. También cuando no tenga estilo ni referentes y pida que le propongas uno ("no tengo estilo", "propónme un estilo").
---

# Editor IA · Define tu estilo

Sigue al pie de la letra el **prompt completo** de `prompts/02-estilo.md` (secciones
CONTEXTO Y ROL → VERIFICACIÓN FINAL). Es la instrucción de trabajo; no la resumas.

Antes de empezar:

1. Si el usuario pegó links, descárgalos con yt-dlp a `Referentes/`
   (`yt-dlp -o "Referentes/%(uploader)s_%(id)s.%(ext)s" -f "bv*+ba/b" <url>`).
   Solo para estudiar el estilo, nunca para republicar.
2. Si `Referentes/` está vacía: ofrece subir videos o links, o que tú le propongas un
   estilo desde cero. Para proponerlo, sigue "Sin referentes" abajo.
3. Los datos entre [corchetes] del prompt que el usuario no dio: pregúntalos en una
   sola tanda (máximo 4 preguntas de opción múltiple, con tu recomendación).

Herramientas: transcripción con `faster-whisper` (o
`.claude/skills/it-reelsmaker/scripts/transcribe.py`; sin Hugging Face, `tools/transcribe_parakeet.py`), hojas de contacto y cortes con
ffmpeg (`-vf "fps=4,scale=270:-1,tile=6x4"`, `select='gt(scene,0.3)'`), colores
medidos con Pillow sobre los frames. Mide, no adivines.

Sin referentes (el usuario no tiene estilo y quiere una propuesta):

1. Pregunta en una sola tanda (máximo 4 preguntas de opción múltiple, con tu
   recomendación): tema y público; nombre o @ de la cuenta y colores que ya use (si los
   tiene); energía (calmada y premium / cercana / enérgica y directa); qué le gusta o no
   le gusta ver en reels.
2. Propón 3 direcciones visuales distintas, basadas en los estilos del kit de IT
   Reelsmaker ("Marker", "Brand", "Minimal", "Editorial", "Bold") y en los tonos de marca
   de `.claude/skills/it-reelsmaker/references/brands.md`. Cada una con: esencia en una
   frase, paleta con hex, tipografías gratuitas de Google Fonts, modo de subtítulos,
   ritmo, animaciones y sonido. Muestra una vista previa de cada una (un frame con
   `kit.py still` o una imagen hecha con Pillow), no solo texto.
3. Cuando elija una, escribe `Referentes/guia-de-estilo.md` con el mismo formato de
   entrega del prompt, marcando que es una propuesta inicial sin referentes medidos.
   Ajústala con sus primeros videos editados y sus correcciones.

Entrega:

- `Referentes/guia-de-estilo.md`: la guía completa (formato de entrega del prompt).
- Crea o actualiza también el perfil de marca de IT Reelsmaker con esa guía
  (`python3 .claude/skills/it-reelsmaker/scripts/brand.py new|tone|rule`, carpeta
  `brands/<slug>/`, con `guide.md` = la guía) y déjalo como marca por defecto
  (`reelcfg.py defaults --set settings.brand=<slug>`), para que cada edición la use.
- Muestra la guía y pregunta si quiere ajustar algo antes de cerrar.
