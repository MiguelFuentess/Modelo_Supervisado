# Explicación de mi parte — Oscar
### Módulos: `red_transporte.py` y `generar_dataset.py` — Fuentes de datos y generación del dataset

## ¿Qué problema resuelve mi parte?

La actividad pide dos cosas antes de poder entrenar cualquier modelo:
identificar fuentes de datos reales relacionadas con el proyecto, y si no
sirven directamente, construir un dataset propio. Yo me encargué de ambas.

## Fuentes de datos reales que identifiqué

Busqué datos abiertos de TransMilenio en el portal de datos abiertos de
Bogotá y en su ArcGIS Hub: encontré el consolidado de salidas por franja
horaria, los trazados de las troncales, y las estaciones en formato
geoespacial (BibloEstación). Los dejé documentados con sus enlaces en
`DESCRIPCION_DATOS.md`.

El problema es que esos datos están armados sobre la red **real y completa**
de TransMilenio (más de 140 estaciones), mientras que nuestro proyecto usa
una red simplificada de 16 estaciones desde la actividad 3. Usarlos
directamente habría hecho que el dataset no fuera consistente con el
sistema experto que ya entregamos. Por eso, como el enunciado lo permite,
construí un dataset propio simulado — pero inspirado en el patrón real que
esas fuentes sí reportan: más congestión en horas pico.

## Cómo generé el dataset

En `red_transporte.py` reconstruí la misma red de líneas y estaciones de la
actividad 3 (4 líneas, 16 estaciones), con una función que calcula, para
cualquier par origen-destino, cuántas estaciones recorre, cuántos
transbordos necesita y cuánto tiempo tomaría sin congestión.

En `generar_dataset.py` simulo 1200 viajes aleatorios sobre esa red. Para
cada uno, calculo el tiempo programado, y le aplico un "factor de
congestión" que depende de la hora del día: más alto en horas pico de días
laborales (6-8am y 5-7pm), más bajo en horario valle, y casi nulo los fines
de semana. Con eso obtengo un tiempo real simulado, y etiqueto el viaje
como "con retraso" si ese tiempo real superó el programado en más de 20%.

Uso una semilla fija (`random.seed(42)`) para que el dataset sea
reproducible: cualquiera que corra mi script obtiene exactamente las mismas
1200 filas.

## Cómo lo pueden probar ustedes

```bash
python3 generar_dataset.py
```

Esto imprime cuántos viajes se generaron y qué porcentaje quedó marcado
como "con retraso" (debería dar ~25%).

## Lo que voy a mostrar en el video

1. Mostrar las fuentes de datos reales que encontré y por qué no las usamos
   directamente.
2. Explicar cómo `red_transporte.py` reutiliza la misma red de la
   actividad 3.
3. Ejecutar `python3 generar_dataset.py` en vivo y mostrar unas filas del
   CSV generado.
