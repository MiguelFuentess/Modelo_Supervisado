# Explicación de mi parte — Miguel
### Módulo: `modelo_arbol_decision.py` — Entrenamiento y evaluación del modelo

## ¿Qué problema resuelve mi módulo?

Este es el corazón de la actividad: entrenar el modelo de **aprendizaje
supervisado** que aprende, a partir de los 1200 viajes ya etiquetados que
preparó Cristian, a predecir si un viaje nuevo tendrá retraso o no.

## Por qué usé un árbol de decisión

El capítulo 17 de la bibliografía de la unidad se llama justamente
"Aprendizaje de árboles y reglas de decisión", así que usé
`DecisionTreeClassifier` de scikit-learn por varias razones:

- Es un algoritmo **supervisado**: aprende de ejemplos ya etiquetados (cada
  fila del dataset ya dice si tuvo retraso o no), que es exactamente lo que
  pide la actividad — a diferencia de un modelo no supervisado, que
  tendría que encontrar patrones sin que nadie le diga la respuesta
  correcta (eso es lo que haremos en la actividad 6).
- Es un modelo **interpretable** ("de caja blanca"): el resultado se puede
  leer como un conjunto de reglas lógicas tipo "SI es_hora_pico = 1
  ENTONCES con_retraso", que es exactamente la idea de "reglas de
  decisión" del capítulo de la bibliografía. Eso nos permite explicar el
  modelo en el video sin que sea una caja negra.
- Funciona bien con variables numéricas y categóricas ya codificadas, sin
  necesitar normalizar los datos.

Limité la profundidad del árbol (`max_depth=4`) para evitar que memorice
el dataset de entrenamiento (sobreajuste) y así generalice mejor a datos
que nunca vio.

## Qué métricas calculo y por qué

No basta con decir "el modelo acertó X% de las veces" — por eso calculo:
- **Exactitud (accuracy):** porcentaje total de aciertos.
- **Precisión:** de los viajes que el modelo dijo que tendrían retraso,
  cuántos realmente lo tuvieron.
- **Sensibilidad (recall):** de los viajes que sí tuvieron retraso, cuántos
  el modelo logró detectar.
- **F1-score:** un balance entre precisión y sensibilidad.
- **Matriz de confusión:** una tabla que compara predicción contra realidad.

También extraigo las **reglas de decisión** en texto legible
(`reglas_arbol_decision.txt`) y la **importancia de cada variable**, que
en nuestro caso mostró que `es_hora_pico` es, por mucho, el factor más
determinante — justo lo que uno esperaría intuitivamente de un sistema de
transporte.

## Cómo lo pueden probar ustedes

```bash
python3 modelo_arbol_decision.py
```

Esto entrena el modelo, imprime todas las métricas, la matriz de confusión,
las variables más importantes y las primeras reglas del árbol.

## Lo que voy a mostrar en el video

1. Explicar por qué elegimos un árbol de decisión y no otro modelo.
2. Mostrar las métricas y la matriz de confusión en vivo.
3. Leer un par de reglas de decisión del archivo generado, explicando cómo
   se leen ("si tal condición, entonces tal predicción").
