# Descripción de los datos — Actividad 5 (Aprendizaje supervisado)

## 1. Fuentes de datos reales identificadas

Como pide el punto 2 de la actividad, antes de construir un dataset propio
se identificaron fuentes de datos reales y públicas relacionadas con el
proyecto de transporte masivo (continuación de las actividades 3 y 4):

| Fuente | Descripción | Enlace |
|---|---|---|
| Portal de Datos Abiertos de Bogotá | Consolidado de salidas del sistema troncal de TransMilenio por franja horaria | https://datosabiertos.bogota.gov.co/dataset/consolidado-de-salidas-sistema-troncal-por-franja-horaria |
| Datos Abiertos TransMilenio (ArcGIS Hub) | Trazados troncales de TransMilenio (geometría de las rutas) | https://datosabiertos-transmilenio.hub.arcgis.com/datasets/trazados-troncales-de-transmilenio |
| Portal de Datos Abiertos de Bogotá | BibloEstación — puntos/estaciones del sistema (formato geoespacial GPKG) | https://datosabiertos.bogota.gov.co/dataset/bibloestacion |

**Por qué no se usaron directamente:** estas fuentes están construidas sobre
la red **real y completa** de TransMilenio (más de 140 estaciones), mientras
que nuestro proyecto, desde la actividad 3, trabaja sobre una **red
simplificada** de 4 líneas y 16 estaciones con fines didácticos. Cruzar
ambas haría que el dataset dejara de ser consistente con el sistema experto
ya entregado. Además, varias de estas fuentes vienen en formatos
geoespaciales pesados (GPKG, shapefiles) que exceden el alcance de la
actividad. Por eso, siguiendo lo que el enunciado permite explícitamente
("en caso de no existir dichas fuentes de datos, desarrolle un dataset con
una muestra de dichos datos"), se optó por generar un **dataset propio
simulado**, pero inspirado en el patrón real que sí reportan esas fuentes
(más congestión en horas pico de la mañana y la tarde en días laborales).

## 2. Cómo se generó el dataset propio

El archivo `dataset_viajes_transmilenio.csv` se genera con
`generar_dataset.py`, simulando **1200 viajes** sobre la misma red de
estaciones y líneas definida en `red_transporte.py` (la misma red usada en
la actividad 3). Para cada viaje:

1. Se eligen aleatoriamente una estación de origen y una de destino.
2. Se calcula el **tiempo programado** (sin congestión) usando la misma
   lógica de rutas validada en la actividad 3 (número de tramos, línea
   principal, transbordos).
3. Se simula un **tiempo real** aplicando un factor de congestión que
   depende de la hora del día y si es fin de semana (más alto en horas
   pico de días laborales, más bajo en horario valle y fines de semana),
   más un componente aleatorio para que no sea una fórmula perfecta.
4. Se etiqueta el viaje como `con_retraso = 1` si el tiempo real superó en
   más de un 20% al tiempo programado, o `0` en caso contrario.

El proceso usa una semilla fija (`random.seed(42)`) para que el dataset sea
**reproducible**: cualquiera que corra `generar_dataset.py` obtiene
exactamente el mismo archivo.

## 3. Diccionario de datos (columnas del CSV)

| Columna | Tipo | Descripción |
|---|---|---|
| `origen` | texto | Estación donde inicia el viaje |
| `destino` | texto | Estación donde termina el viaje |
| `linea_principal` | texto (categórica) | Primera línea troncal usada en la ruta |
| `hora_dia` | entero (0-23) | Hora del día en que inicia el viaje |
| `dia_semana` | texto (categórica) | Día de la semana del viaje |
| `es_fin_de_semana` | binario (0/1) | 1 si el viaje fue sábado o domingo |
| `es_hora_pico` | binario (0/1) | 1 si el viaje fue en horario pico de un día laboral (6-8am o 5-7pm) |
| `numero_estaciones` | entero | Cantidad de estaciones recorridas en la ruta |
| `numero_transbordos` | entero | Cantidad de cambios de línea requeridos |
| `tiempo_programado_min` | decimal | Tiempo de viaje sin congestión (minutos) |
| `tiempo_real_min` | decimal | Tiempo de viaje simulado con congestión (minutos) |
| `con_retraso` | binario (0/1) | **Variable objetivo (target)**: 1 si el tiempo real superó el programado en más de 20% |

## 4. Variable objetivo y tipo de problema

El modelo de aprendizaje supervisado busca predecir `con_retraso`
(0 = a tiempo, 1 = con retraso) a partir de las demás columnas (excepto
`tiempo_real_min`, que no se usa como predictor porque solo se conoce
*después* de hacer el viaje). Es un problema de **clasificación binaria**,
resuelto con un **árbol de decisión** (`DecisionTreeClassifier` de
scikit-learn), siguiendo el capítulo 17 de la bibliografía de la unidad
(Palma Méndez, 2008: "Aprendizaje de árboles y reglas de decisión").

## 5. Balance de clases

De los 1200 viajes generados, aproximadamente el 25% quedó etiquetado como
"con retraso" y el 75% como "a tiempo" — un desbalance moderado y realista
(la mayoría de los viajes no tienen retraso significativo). Por eso, al
dividir los datos en entrenamiento y prueba (`preprocesamiento.py`), se usó
`stratify=y` para que esa misma proporción se mantenga en ambos conjuntos.

## 6. Preprocesamiento aplicado

- Se seleccionaron 8 columnas como variables predictoras (features):
  `hora_dia`, `dia_semana`, `es_fin_de_semana`, `es_hora_pico`,
  `linea_principal`, `numero_estaciones`, `numero_transbordos`,
  `tiempo_programado_min`.
- Las dos columnas de texto (`dia_semana`, `linea_principal`) se
  convirtieron a columnas numéricas mediante **codificación one-hot**
  (`pandas.get_dummies`), ya que los árboles de decisión de scikit-learn
  requieren valores numéricos.
- Los datos se dividieron en 80% entrenamiento / 20% prueba, de forma
  aleatoria pero reproducible (`random_state=42`).

## 7. Resultado observado (ver también el PDF de pruebas)

El modelo alcanzó una exactitud (`accuracy`) superior al 99% sobre el
conjunto de prueba, y el análisis de importancia de variables mostró que
`es_hora_pico` es, por un margen amplio, la variable más determinante para
predecir el retraso. Esto es coherente con el diseño del dataset (la
congestión simulada depende principalmente de si el viaje ocurre en horario
pico) y confirma que el árbol de decisión logró capturar correctamente el
patrón real de los datos, sin necesidad de memorizarlos (ver la matriz de
confusión y las reglas de decisión extraídas en `reglas_arbol_decision.txt`).
