---
name: editor-ia-estilo
description: Paso 3 de la guía Editor IA. Estudia los videos de la carpeta "Referentes" y crea la guía de estilo del usuario (paleta, tipografías, subtítulos, ritmo, animaciones, sonido, lo que no hace). Úsala cuando el usuario diga "analiza mi estilo", "define mi estilo", "crea mi guía de estilo", suba videos de referencia o pegue links de referentes para descargar.
---

# Editor IA · Define tu estilo

Sigue al pie de la letra el **prompt completo** de `prompts/02-estilo.md` (secciones
CONTEXTO Y ROL → VERIFICACIÓN FINAL). Es la instrucción de trabajo; no la resumas.

Antes de empezar:

1. Si el usuario pegó links, descárgalos con yt-dlp a `Referentes/`
   (`yt-dlp -o "Referentes/%(uploader)s_%(id)s.%(ext)s" -f "bv*+ba/b" <url>`).
   Solo para estudiar el estilo, nunca para republicar.
2. Si `Referentes/` está vacía, pide los videos o los links y detente.
3. Los datos entre [corchetes] del prompt que el usuario no dio: pregúntalos en una
   sola tanda (máximo 4 preguntas de opción múltiple, con tu recomendación).

Herramientas: transcripción con `faster-whisper` (o
`.claude/skills/it-reelsmaker/scripts/transcribe.py`), hojas de contacto y cortes con
ffmpeg (`-vf "fps=4,scale=270:-1,tile=6x4"`, `select='gt(scene,0.3)'`), colores
medidos con Pillow sobre los frames. Mide, no adivines.

Entrega:

- `Referentes/guia-de-estilo.md`: la guía completa (formato de entrega del prompt).
- Crea o actualiza también el perfil de marca de IT Reelsmaker con esa guía
  (`python3 .claude/skills/it-reelsmaker/scripts/brand.py new|tone|rule`, carpeta
  `brands/<slug>/`, con `guide.md` = la guía) y déjalo como marca por defecto
  (`reelcfg.py defaults --set settings.brand=<slug>`), para que cada edición la use.
- Muestra la guía y pregunta si quiere ajustar algo antes de cerrar.
