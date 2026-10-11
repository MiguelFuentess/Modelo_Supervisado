# Explicación de mi parte — Evelyn
### Módulo: `main.py` — Integración, predicción interactiva y pruebas

## ¿Qué problema resuelve mi módulo?

Igual que en la actividad 3, mi parte es unir todo lo que hicieron mis
compañeros (la fuente de datos de Oscar, el preprocesamiento de Cristian y
el modelo de Miguel) en un programa que se pueda usar, y comprobar con
pruebas reales que todo funciona de punta a punta.

## Las dos formas de usar el sistema

1. **Modo interactivo** (`python3 main.py`): le pido al usuario una
   estación de origen, una de destino, la hora del día y el día de la
   semana. Con esos datos reconstruyo automáticamente las mismas columnas
   que vio el modelo durante el entrenamiento (incluyendo la codificación
   one-hot, alineada exactamente con las columnas de Cristian), y el árbol
   de decisión de Miguel predice si ese viaje tendrá retraso, junto con la
   probabilidad.

2. **Modo de pruebas** (`python3 main.py --pruebas`): entrena el modelo,
   muestra todas sus métricas de evaluación, corre 5 casos de prueba
   representativos (hora pico, hora valle, fin de semana, con y sin
   transbordos), y genera dos gráficas: la matriz de confusión y la
   importancia de variables. Esa salida y esas gráficas son las que se
   usan para armar el PDF de pruebas que entregamos
   (`Pruebas_Modelo_Supervisado.pdf`).

## El detalle técnico más importante de mi parte

Cuando alguien pide una predicción nueva en el modo interactivo, tengo que
construir una fila con exactamente las mismas columnas que vio el modelo
en entrenamiento — ni una más, ni una menos, en el mismo orden. Por eso uso
`reindex(columns=columnas_entrenamiento, fill_value=0)`: si el viaje nuevo
usa una línea o cae en un día que generó una columna distinta a las que
existían en el entrenamiento, se rellena con 0 en vez de romper el
programa.

## Cómo lo pueden probar ustedes

```bash
python3 main.py --pruebas
```

## Lo que voy a mostrar en el video

1. Ejecutar el modo interactivo en vivo, pidiendo una predicción para un
   viaje en hora pico y otro en hora valle, para que se note la
   diferencia.
2. Ejecutar el modo `--pruebas` y repasar las métricas y los 5 casos.
3. Mostrar brevemente el PDF de pruebas y las gráficas, explicando que
   salen de la misma ejecución que se acaba de ver.
