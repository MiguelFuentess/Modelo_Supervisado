"""
=====================================================================
 MÓDULO · preprocesamiento.py
 Responsable: Cristian
=====================================================================
Este módulo toma el dataset crudo (dataset_viajes_transmilenio.csv,
generado por Oscar) y lo deja listo para entrenar un modelo de
aprendizaje automático. En machine learning esto se llama
"preprocesamiento" o "ingeniería de características" (feature
engineering), y es un paso obligatorio porque los algoritmos de
scikit-learn solo entienden números, no texto.

Pasos que realiza:

1. Cargar el CSV con pandas.
2. Seleccionar las columnas que sirven como variables predictoras
   (features, X) y la columna objetivo (target, y = con_retraso).
3. Convertir las columnas de texto (linea_principal, dia_semana) a
   columnas numéricas usando codificación one-hot (get_dummies), ya
   que un árbol de decisión de scikit-learn no puede recibir strings
   directamente.
4. Dividir el dataset en conjunto de entrenamiento (80%) y de prueba
   (20%), de forma aleatoria pero reproducible (random_state fijo),
   para poder evaluar después qué tan bien generaliza el modelo a
   datos que nunca vio.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

RUTA_DATASET = Path(__file__).parent / "dataset_viajes_transmilenio.csv"

# Columnas que se usan para predecir (features)
COLUMNAS_FEATURES = [
    "hora_dia",
    "dia_semana",
    "es_fin_de_semana",
    "es_hora_pico",
    "linea_principal",
    "numero_estaciones",
    "numero_transbordos",
    "tiempo_programado_min",
]

COLUMNA_OBJETIVO = "con_retraso"


def cargar_dataset(ruta: Path = RUTA_DATASET) -> pd.DataFrame:
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta.name}. Primero corre: python3 generar_dataset.py"
        )
    return pd.read_csv(ruta)


def preparar_datos(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, list]:
    """
    Devuelve (X, y, nombres_columnas_codificadas) listos para entrenar.
    """
    datos = df[COLUMNAS_FEATURES + [COLUMNA_OBJETIVO]].copy()

    # Codificación one-hot de las variables categóricas (texto -> columnas 0/1)
    datos_codificados = pd.get_dummies(
        datos, columns=["dia_semana", "linea_principal"], drop_first=False
    )

    y = datos_codificados[COLUMNA_OBJETIVO]
    X = datos_codificados.drop(columns=[COLUMNA_OBJETIVO])

    return X, y, list(X.columns)


def dividir_entrenamiento_prueba(X, y, test_size: float = 0.2, random_state: int = 42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def obtener_datos_listos():
    """Función de conveniencia usada por modelo_arbol_decision.py y main.py."""
    df = cargar_dataset()
    X, y, columnas = preparar_datos(df)
    X_train, X_test, y_train, y_test = dividir_entrenamiento_prueba(X, y)
    return X_train, X_test, y_train, y_test, columnas


# --- Prueba rápida del módulo de forma aislada -----------------------
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, columnas = obtener_datos_listos()
    print(f"Filas totales: {len(X_train) + len(X_test)}")
    print(f"Entrenamiento: {len(X_train)} filas | Prueba: {len(X_test)} filas")
    print(f"Columnas usadas como features ({len(columnas)}): {columnas}")
    print(f"Proporción de 'con_retraso' en entrenamiento: {y_train.mean():.2%}")
    print(f"Proporción de 'con_retraso' en prueba: {y_test.mean():.2%}")
