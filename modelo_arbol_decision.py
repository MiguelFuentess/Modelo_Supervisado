"""
=====================================================================
 MÓDULO · modelo_arbol_decision.py
 Responsable: Miguel
=====================================================================
Este es el módulo central de la actividad: entrena un modelo de
APRENDIZAJE SUPERVISADO que aprende a predecir si un viaje en el
sistema de transporte masivo va a tener RETRASO (sí/no) a partir de
sus características (hora del día, línea, número de transbordos,
etc.), usando el historial de viajes simulados como ejemplo.

Algoritmo usado: ÁRBOL DE DECISIÓN (DecisionTreeClassifier de
scikit-learn), siguiendo el capítulo 17 del libro de la bibliografía
de la unidad (Palma Méndez, 2008: "Aprendizaje de árboles y reglas de
decisión").

¿Por qué un árbol de decisión y no otro modelo?
- Es un algoritmo SUPERVISADO: aprende de ejemplos ya etiquetados
  (cada fila del dataset ya dice si tuvo retraso o no), que es
  justamente lo que pide la actividad.
- Es un modelo "de caja blanca": el resultado se puede leer como un
  conjunto de REGLAS lógicas tipo "SI hora_dia >= 17 Y es_hora_pico
  == 1 ENTONCES con_retraso", que es exactamente la idea de "árboles
  y reglas de decisión" del capítulo de la bibliografía. Esto permite
  explicar el modelo en el video sin que sea una "caja negra".
- Funciona bien con variables mixtas (numéricas y categóricas ya
  codificadas) sin necesidad de normalizar los datos.

El árbol se entrena limitando su profundidad máxima (max_depth) para
evitar que memorice el dataset de entrenamiento (sobreajuste /
overfitting) y así generalice mejor a datos nuevos.
"""

from pathlib import Path

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from preprocesamiento import obtener_datos_listos

RUTA_REGLAS_TXT = Path(__file__).parent / "reglas_arbol_decision.txt"


def entrenar_modelo(X_train, y_train, profundidad_maxima: int = 4) -> DecisionTreeClassifier:
    modelo = DecisionTreeClassifier(
        max_depth=profundidad_maxima,
        criterion="gini",
        random_state=42,
    )
    modelo.fit(X_train, y_train)
    return modelo


def evaluar_modelo(modelo, X_test, y_test) -> dict:
    predicciones = modelo.predict(X_test)

    metricas = {
        "exactitud": accuracy_score(y_test, predicciones),
        "precision": precision_score(y_test, predicciones, zero_division=0),
        "recall": recall_score(y_test, predicciones, zero_division=0),
        "f1_score": f1_score(y_test, predicciones, zero_division=0),
        "matriz_confusion": confusion_matrix(y_test, predicciones),
        "reporte_completo": classification_report(y_test, predicciones, target_names=["A_tiempo", "Con_retraso"]),
    }
    return metricas


def extraer_reglas(modelo, columnas: list) -> str:
    """
    Convierte el árbol entrenado a reglas lógicas legibles (texto),
    que es la representación del conocimiento que pide explícitamente
    el capítulo 17 de la bibliografía: "reglas de decisión" derivadas
    del árbol.
    """
    return export_text(modelo, feature_names=columnas)


def importancia_variables(modelo, columnas: list) -> list:
    """Qué tanto pesa cada variable en las decisiones del árbol (0 a 1)."""
    pares = list(zip(columnas, modelo.feature_importances_))
    return sorted(pares, key=lambda p: p[1], reverse=True)


def entrenar_y_evaluar():
    X_train, X_test, y_train, y_test, columnas = obtener_datos_listos()
    modelo = entrenar_modelo(X_train, y_train)
    metricas = evaluar_modelo(modelo, X_test, y_test)
    reglas = extraer_reglas(modelo, columnas)
    importancias = importancia_variables(modelo, columnas)
    return modelo, metricas, reglas, importancias, columnas


# --- Prueba rápida del módulo de forma aislada -----------------------
if __name__ == "__main__":
    modelo, metricas, reglas, importancias, columnas = entrenar_y_evaluar()

    print("=" * 70)
    print("MÉTRICAS DEL MODELO (árbol de decisión)")
    print("=" * 70)
    print(f"Exactitud (accuracy) : {metricas['exactitud']:.2%}")
    print(f"Precisión (precision): {metricas['precision']:.2%}")
    print(f"Sensibilidad (recall): {metricas['recall']:.2%}")
    print(f"F1-score              : {metricas['f1_score']:.2%}")
    print("\nMatriz de confusión (filas=real, columnas=predicho):")
    print(metricas["matriz_confusion"])
    print("\nReporte completo:")
    print(metricas["reporte_completo"])

    print("=" * 70)
    print("VARIABLES MÁS IMPORTANTES PARA EL MODELO")
    print("=" * 70)
    for nombre, peso in importancias[:5]:
        print(f"  {nombre:35s} {peso:.3f}")

    print("\n" + "=" * 70)
    print("REGLAS DE DECISIÓN APRENDIDAS (primeras líneas)")
    print("=" * 70)
    print("\n".join(reglas.splitlines()[:20]))

    RUTA_REGLAS_TXT.write_text(reglas, encoding="utf-8")
    print(f"\n(Reglas completas guardadas en {RUTA_REGLAS_TXT.name})")
