# Actividad 5 — Aprendizaje Supervisado: Predicción de Retrasos en Transporte Masivo

Continuación del proyecto de las actividades anteriores (sistema experto de
rutas, actividad 3). Aquí se construye un **modelo de aprendizaje
supervisado** (árbol de decisión) que predice si un viaje en el sistema de
transporte masivo tendrá **retraso** o no, a partir de sus características
(hora del día, día de la semana, línea, transbordos, etc.).

Basado en:
> Palma Méndez, J. T. (2008). *Inteligencia artificial: métodos, técnicas y
> aplicaciones*. Madrid: McGraw-Hill España. Capítulo 17 (Aprendizaje de
> árboles y reglas de decisión).

## Equipo de trabajo

| Integrante | Responsabilidad | Archivo(s) |
|---|---|---|
| Oscar | Fuentes de datos y generación del dataset | `red_transporte.py`, `generar_dataset.py` |
| Cristian | Preprocesamiento de los datos | `preprocesamiento.py` |
| Miguel | Entrenamiento y evaluación del modelo (árbol de decisión) | `modelo_arbol_decision.py` |
| Evelyn | Integración, predicción interactiva y pruebas | `main.py`, `generar_pdf_pruebas.py` |

Cada integrante tiene su guion de explicación en
`INTEGRANTE_N_explicacion.md`, para usar en el video y como evidencia de
autoría en su commit de Git.

## Estructura del repositorio

```
.
├── red_transporte.py                 # Red de estaciones/líneas (base del proyecto)
├── generar_dataset.py                # Genera el dataset simulado de viajes
├── dataset_viajes_transmilenio.csv   # Entregable: fuente de datos (1200 viajes)
├── preprocesamiento.py               # Limpieza, codificación y división train/test
├── modelo_arbol_decision.py          # Entrenamiento y evaluación del árbol de decisión
├── reglas_arbol_decision.txt         # Reglas lógicas extraídas del árbol entrenado
├── main.py                           # CLI interactiva + modo de pruebas
├── generar_pdf_pruebas.py            # Script de apoyo: genera el PDF de pruebas
├── matriz_confusion.png              # Gráfica generada por las pruebas
├── importancia_variables.png         # Gráfica generada por las pruebas
├── Pruebas_Modelo_Supervisado.pdf    # Entregable: documento de pruebas
├── DESCRIPCION_DATOS.md              # Entregable: descripción de los datos
├── INTEGRANTE_1_explicacion.md … INTEGRANTE_4_explicacion.md
└── README.md
```

## Requisitos

```bash
pip install pandas scikit-learn matplotlib reportlab
```

## Cómo ejecutarlo (en orden)

```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>

# 1. Generar el dataset (ya viene generado, pero se puede regenerar):
python3 generar_dataset.py

# 2. (Opcional) Ver el preprocesamiento por separado:
python3 preprocesamiento.py

# 3. (Opcional) Ver el modelo entrenado por separado:
python3 modelo_arbol_decision.py

# 4. Modo interactivo (predicción manual de un viaje):
python3 main.py

# 5. Modo de pruebas (entrena, evalúa, corre 5 casos y genera gráficas):
python3 main.py --pruebas

# 6. Regenerar el PDF de pruebas (requiere reportlab):
python3 generar_pdf_pruebas.py
```

En Windows, si `python3` no funciona, usar `python`.

## Diseño del sistema (resumen)

1. **Fuente de datos:** se identificaron fuentes reales de datos abiertos de
   TransMilenio (ver `DESCRIPCION_DATOS.md`), y al no ser compatibles con la
   red simplificada del proyecto, se construyó un dataset propio simulado
   (1200 viajes) reutilizando la lógica de rutas de la actividad 3.
2. **Preprocesamiento:** codificación one-hot de variables categóricas y
   división 80/20 en entrenamiento y prueba, estratificada por la variable
   objetivo.
3. **Modelo:** árbol de decisión (`DecisionTreeClassifier`), elegido por ser
   un modelo interpretable que produce reglas lógicas legibles, en línea con
   el capítulo 17 de la bibliografía.
4. **Evaluación:** exactitud, precisión, sensibilidad, F1-score y matriz de
   confusión sobre datos de prueba nunca vistos por el modelo, más 5 casos
   de prueba manuales y un documento PDF con toda la evidencia.
