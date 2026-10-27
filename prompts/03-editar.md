# Prompt · Editar (Paso 4)

Atajo: di **"edita mi video"** (skill `editor-ia-editar`). Abajo, los textos
originales de la guía por si quieres pegarlos completos.

## Versión corta

```
Edita mi video de la carpeta Material crudo:
1. Corta silencios y repeticiones.
2. Agrega subtítulos y animaciones con mi guía de estilo.
3. Suma música y efectos de sonido.
4. Muéstrame el plan y exporta a Resultados en 1080×1920.
```

## Prompt maestro (llena lo que está entre [corchetes])

```
[CONTEXTO Y ROL]
Eres editor de video y motion designer senior, especializado en videos cortos verticales para Instagram, TikTok y Shorts. Trabajas dentro de mi carpeta "Editor IA" con las skills que te indico abajo, que corren localmente y no requieren pagar herramientas externas.

[MIS CARPETAS]
Todo el trabajo pasa por la carpeta "Editor IA". Entra a cada subcarpeta según lo que estés haciendo:
- "Material crudo": entra aquí para buscar el video que vas a editar. Es tu material de partida: no lo modifiques ni lo borres, trabaja siempre sobre una copia.
- "Referentes": entra aquí antes de editar para leer mi guía de estilo y revisar los videos de referencia. Todo lo visual (colores, tipografías, subtítulos, ritmo, animaciones y sonido) sale de aquí.
- "Resultados": entra aquí solo para guardar lo que entregas: el plan por escenas y el video final, con un nombre claro (por ejemplo: nombre-del-video_editado_v1.mp4). Si haces una corrección, guarda una versión nueva (v2, v3) sin borrar la anterior.
Si alguna carpeta está vacía o no encuentras lo que necesitas, avísame antes de seguir.

[SKILLS QUE VAS A USAR]
- IT Reelsmaker: la base de la edición. Transcribe el video, corta silencios y tomas repetidas, arma el formato vertical 1080×1920, genera subtítulos sincronizados por palabra, aplica mi perfil de marca y deja el audio en −14 LUFS.
- Embedded Captions: recorta a la persona del fondo. Sirve para subtítulos o gráficos que pasan por detrás de mí, y para efectos como fondo verde, recorte tipo papel, dolly zoom y texto detrás de la cabeza.
- Remotion: animaciones y efectos en código: subtítulos kinéticos, tarjetas, contadores, tier lists y transiciones, siempre con motion blur.
- HyperFrames: motion graphics hechos como HTML, para animar interfaces, pantallas, producto o títulos.
- Media Use: el sonido. Efectos sutiles (whoosh, pop, impacto, riser) sincronizados con cada animación, música de fondo y mezcla final con la voz siempre por encima.

[MI VIDEO]
- Archivo en "Material crudo": [nombre del archivo, o "el más reciente"]
- De qué trata y para quién es: [tema + público]
- Objetivo: [educar / vender / entretener / posicionar mi marca]
- Duración máxima: [X segundos]
- Cierre o llamado a la acción: [p. ej. "sígueme", "comenta X", "link en bio"] (opcional)

[MI ESTILO]
Por defecto, usa la guía de estilo que está en "Referentes". Si quiero cambiar algo solo para este video, lo escribo aquí:
- Ajustes de este video: [p. ej. "más animaciones", "sin música", "subtítulos más grandes"] (opcional)
- Efectos que quiero: [tier list, recorte tipo papel, dolly zoom, panel de vidrio, fondo verde, texto detrás de mí, zooms, transiciones; o "elige tú según el contenido"]
- Lo que NO quiero: [p. ej. emojis, transiciones exageradas, música con letra]
Si no hay guía de estilo en "Referentes", analiza los videos que haya ahí y propónme 2 o 3 direcciones visuales para que yo elija.

[FLUJO]
1. Entra a "Referentes" y lee mi guía de estilo.
2. Entra a "Material crudo", busca el video y analízalo: transcribe con tiempos por palabra, revisa los frames y detecta silencios, tomas repetidas o errores, el encuadre y dónde está mi cara.
3. Pregúntame lo que necesites antes de producir: máximo 4 preguntas de opción múltiple, con tu recomendación marcada.
4. Guarda en "Resultados" un plan por escenas para aprobar: tiempo, qué se dice, qué se ve, qué efecto lleva y con qué skill se hace. Espera mi aprobación.
5. Edita en este orden: IT Reelsmaker (corte, formato y subtítulos base) → Embedded Captions (recorte, si algún efecto lo necesita) → Remotion y HyperFrames (efectos y animaciones con motion blur) → Media Use (sonido y mezcla).
6. Antes del render final, revisa tomas fijas en los momentos clave y corrige lo que se vea mal.
7. Exporta el video final a "Resultados".

[REGLAS]
- Nunca modifiques ni borres los archivos de "Material crudo" ni de "Referentes".
- Nunca tapes mi cara con texto ni gráficos.
- Cero errores de ortografía en pantalla. Respeta los nombres propios y las marcas tal como los escribo.
- No inventes datos, cifras ni precios. Si falta información, pregúntame.
- No agregues logos, marcas ni material ajeno a mi video.
- No uses servicios de pago ni generes contenido con IA externa sin preguntarme primero.

[CRITERIOS DE CALIDAD]
- El gancho funciona en los primeros 2 segundos, incluso sin sonido.
- Los subtítulos se leen bien en el celular y van al tiempo exacto de la voz.
- Cada efecto tiene una razón: refuerza lo que se dice, no distrae.
- Las animaciones llevan motion blur y efecto de sonido; nada aparece de golpe sin intención.
- El audio queda limpio, con la voz por encima de la música y el volumen en −14 LUFS.

[ENTREGA]
1. El plan por escenas (tabla), guardado en "Resultados", antes de editar.
2. El video final en MP4 de 1080×1920, guardado en "Resultados".
3. Un resumen corto: qué efecto va en cada segundo, con qué skill se hizo y qué puedo ajustar fácilmente.

[VERIFICACIÓN FINAL]
Antes de entregar, revisa el video exportado en "Resultados": duración, resolución, sincronía de subtítulos, volumen, que nada tape la cara y que no haya elementos ajenos.
```

## Correcciones (página 13)

Háblale a Claude como a un editor de verdad. Ejemplos:

- "Haz el gancho más grande."
- "Corta la pausa del segundo 12."
- "Pon los subtítulos más arriba, me tapan la mano."
- "Baja la música, se come mi voz."
- "Agrega una animación cuando digo el número."

Entre más específico seas (qué, dónde y en qué segundo), mejor y más rápido queda la corrección.
