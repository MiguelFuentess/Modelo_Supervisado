# Explicación de mi parte — Cristian
### Módulo: `preprocesamiento.py` — Preprocesamiento de los datos

## ¿Qué problema resuelve mi módulo?

El dataset que generó Oscar tiene columnas de texto (por ejemplo
`dia_semana` con valores como "Lunes", "Martes"...) y columnas numéricas
mezcladas. El problema es que los algoritmos de scikit-learn, incluido el
árbol de decisión que entrena Miguel, **solo entienden números**. Mi parte
es dejar los datos listos para que el modelo los pueda recibir.

## Qué hace mi código, paso a paso

1. **Cargo el CSV** con pandas.
2. **Elijo las columnas que sirven para predecir** (features): hora del
   día, día de la semana, si es fin de semana, si es hora pico, línea
   principal, número de estaciones, número de transbordos y tiempo
   programado. Dejo afuera `tiempo_real_min` a propósito, porque esa
   columna solo se conoce *después* de hacer el viaje — usarla sería
   hacer trampa (se llama "fuga de datos" o *data leakage*).
3. **Codificación one-hot:** convierto las columnas de texto (`dia_semana`,
   `linea_principal`) en varias columnas de ceros y unos, una por cada
   valor posible (por ejemplo, `dia_semana_Lunes`, `dia_semana_Martes`,
   etc.). Así cada categoría se vuelve un número que el modelo sí puede
   procesar.
4. **Divido en entrenamiento y prueba:** separo el 80% de los datos para
   que el modelo aprenda con ellos, y dejo el 20% aparte, sin que el
   modelo los vea durante el entrenamiento, para poder evaluar después qué
   tan bien funciona con datos nuevos. Uso `stratify=y` para que la
   proporción de viajes con y sin retraso sea la misma en ambos grupos.

## Por qué es un paso obligatorio

Sin este módulo, Miguel no podría entrenar nada: le estaría pasando texto a
un algoritmo que espera números, y el programa fallaría. Este
"preprocesamiento" o "ingeniería de características" es un paso estándar en
cualquier proyecto real de aprendizaje automático.

## Cómo lo pueden probar ustedes

```bash
python3 preprocesamiento.py
```

Esto muestra cuántas filas quedaron en entrenamiento y en prueba, cuántas
columnas quedaron después de la codificación, y confirma que la proporción
de viajes con retraso es similar en ambos conjuntos.

## Lo que voy a mostrar en el video

1. Explicar por qué un modelo no puede recibir texto directamente.
2. Mostrar en vivo cómo se ve una fila antes y después de la codificación
   one-hot.
3. Ejecutar `python3 preprocesamiento.py` y explicar la salida.
