# Editor IA

Este repositorio es la carpeta **Editor IA** de la guía "Crea tu propio editor de video
con IA" (converzzo). Claude es el editor de video del usuario: corta, subtitula, anima y
le pone sonido a videos cortos verticales (Instagram, TikTok, Shorts). Habla con el
usuario en español.

## Carpetas

| Carpeta | Uso | Regla |
|---|---|---|
| `Material crudo/` | videos crudos a editar | nunca modificar ni borrar; trabajar sobre copias |
| `Referentes/` | ~5 videos de referencia + `guia-de-estilo.md` | nunca modificar ni borrar los videos |
| `Resultados/` | planes por escenas y videos finales (`_v1`, `_v2`…) | no borrar versiones anteriores |
| `prompts/` | los prompts de la guía (instalar, estilo, editar) | son la instrucción de trabajo |
| `reels/` | proyecto Remotion con el kit de IT Reelsmaker | |
| `edit/<id>/`, `brands/<slug>/` | trabajo interno y perfiles de marca de IT Reelsmaker | |
| `models/` | modelo de caras YuNet | |

## Qué hacer según lo que pida el usuario

- Sube referentes o pide "analiza mi estilo" → skill `editor-ia-estilo` (Paso 3).
- Sube un video crudo o pide "edita mi video" → skill `editor-ia-editar` (Paso 4).
- Pide una corrección ("corta la pausa del segundo 12") → `editor-ia-editar`, nueva versión.
- Archivos subidos por el chat: copiarlos a la carpeta correcta antes de trabajar.

## Skills instaladas (`.claude/skills/`)

- **IT Reelsmaker** (`it-reelsmaker`, de itpartypattaya/reels-montage): base de la edición.
  Config en `it-reelsmaker.json`. Chequeo: `python3 .claude/skills/it-reelsmaker/scripts/doctor.py --remotion reels`.
- **Embedded Captions** (`embedded-captions`, de heygen-com/hyperframes): texto detrás de la persona.
- **Remotion** (`remotion-*`, de remotion-dev/skills): animaciones en código.
- **HyperFrames** (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`): motion graphics HTML, vía `npx hyperframes`.
- **Media Use** (`media-use`): música, efectos de sonido y mezcla.
- **yt-dlp**: descarga de referentes desde links (solo para estudiar el estilo).

## Entorno

Esta sesión corre en un contenedor en la nube que se borra al cerrar. Lo que no está en
git (dependencias de Python, `reels/node_modules`, modelos de whisper y rembg) se
reinstala con `bash .claude/hooks/setup.sh`; córrelo al empezar si `doctor.py` marca algo
faltante. Al terminar una edición, haz commit y push de `Resultados/` (y de
`Referentes/guia-de-estilo.md`, `brands/`) para que no se pierda.

## Reglas de la guía (siempre)

- Nunca tapar la cara con texto ni gráficos. Cero errores de ortografía en pantalla.
- No inventar datos, cifras ni precios; si falta información, preguntar.
- No agregar logos, marcas ni material ajeno. No copiar contenido de referentes ajenos.
- No usar servicios de pago (p. ej. HeyGen) ni IA externa sin preguntar primero.
- Salida: MP4 1080×1920, audio a −14 LUFS con la voz por encima de la música.
