# Podcast péptidos · Dra. Michelle González — 10 reels entregados

Todos: MP4 1080×1920, 30 fps, audio a −14 LUFS (pico ≤ −1 dBFS), sin música, sin títulos, subtítulos "blanco
minimalista" centrados (Montserrat 800, sombra suave, palabra por palabra al ritmo de la voz, palabras clave más
grandes), recorte vertical que sigue la cara de quien habla. Portada (carátula) incluida en cada MP4 y como `_portada`.

| # | Archivo | Duración | Tema |
|---|---|---|---|
| 01 | podcast-peptidos_01_editado_v2.mp4 | 53 s | Por qué a mucha gente no le funcionan los péptidos |
| 02 | podcast-peptidos_02_editado_v1.mp4 | 47 s | BPC-157: "me curé en dos días"… ¿y el riesgo? |
| 03 | podcast-peptidos_03_editado_v1.mp4 | 62 s | Retatrutide: lo venden en Instagram y sigue en estudio |
| 04 | podcast-peptidos_04_editado_v1.mp4 | 57 s | El peligro real de los péptidos no es la molécula |
| 05 | podcast-peptidos_05_editado_v1.mp4 | 50 s | Señal roja: microcursos para recetar péptidos |
| 06 | podcast-peptidos_06_editado_v1.mp4 | 42 s | La médica que pensaba que los péptidos eran irresponsables |
| 07 | podcast-peptidos_07_editado_v1.mp4 | 45 s | "Bajé 5 kilos en dos semanas"… ¿a qué costo? |
| 08 | podcast-peptidos_08_editado_v1.mp4 | 51 s | El problema no es bajar de peso, es sostenerlo |
| 09 | podcast-peptidos_09_editado_v1.mp4 | 57 s | ¿Existe un péptido que alargue la vida? |
| 10 | podcast-peptidos_10_editado_v1.mp4 | 42 s | 3 cosas que una médica jamás haría con péptidos |

`podcast-peptidos_01_editado_v1.mp4` es la primera versión del 01 (con título y subtítulos a la izquierda), guardada
como respaldo.

## Para revisar antes de publicar

- Consentimiento de la Dra. Michelle y de la entrevistadora.
- 03: el nombre del estudio se escribió "TRIUMPH-3" (en el audio suena "Try and Tres"); "esta semana", Lilly y el 20 %
  van tal como ella lo dice (aprobado).
- 06: sin la frase del médico de Medellín (pedido).
- 09: dos frases dudosas de la transcripción: "No sé si lo has notado" (¿"escuchado"?) y "la frase prometedora"
  (¿"la parte"?).

## Cómo se hizo (para correcciones)

Transcripción local (Parakeet), cortes por audio (IT Reelsmaker `speech_mask.py`, ritmo natural), recorte vertical
`tools/reframe_vertical.py`, correcciones de texto `edit/podcast/fixes.json` (`tools/fix_captions.py`), estilo
`reels/src/ReelMinimal.tsx`, armado `tools/serie_build.sh`, render `kit.py render --comp ReelMinimal`, entrega
`tools/serie_deliver.sh` (auditoría de caras, portada, master −14 LUFS).
