"""
=====================================================================
 MÓDULO · main.py
 Responsable: Evelyn
=====================================================================
Este módulo integra los tres módulos anteriores (red_transporte,
generar_dataset ya ejecutado -> CSV, preprocesamiento, y
modelo_arbol_decision) en un programa usable, igual que se hizo en la
actividad 3 con el sistema experto de rutas.

Ofrece:

  1. Un modo INTERACTIVO: el usuario describe un viaje (origen,
     destino, hora del día, día de la semana) y el sistema predice si
     ese viaje tendría retraso o no, usando el árbol de decisión ya
     entrenado.
  2. Un modo de PRUEBAS (--pruebas): entrena el modelo, muestra sus
     métricas de evaluación, corre varios casos de ejemplo, y genera
     dos gráficas (matriz de confusión e importancia de variables)
     que se usan como evidencia en el PDF de pruebas.

Ejecución:
    python3 main.py            -> modo interactivo (predicción manual)
    python3 main.py --pruebas  -> entrena, evalúa y genera gráficas
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin pantalla, necesario para correr desde terminal
import matplotlib.pyplot as plt

from red_transporte import todas_las_estaciones, resumen_viaje
from preprocesamiento import obtener_datos_listos, COLUMNAS_FEATURES
from modelo_arbol_decision import entrenar_y_evaluar, entrenar_modelo
from preprocesamiento import cargar_dataset, preparar_datos

CARPETA = Path(__file__).parent
DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]


# =====================================================================
# Construir una fila nueva con el mismo formato que el entrenamiento
# =====================================================================
def construir_fila_prediccion(origen: str, destino: str, hora_dia: int, dia_semana: str,
                               columnas_entrenamiento: list) -> pd.DataFrame:
    info = resumen_viaje(origen, destino)
    if info is None:
        return None

    es_fin_de_semana = 1 if dia_semana in ("Sabado", "Domingo") else 0
    es_hora_pico = 1 if (dia_semana not in ("Sabado", "Domingo") and (6 <= hora_dia <= 8 or 17 <= hora_dia <= 19)) else 0

    fila = pd.DataFrame([{
        "hora_dia": hora_dia,
        "dia_semana": dia_semana,
        "es_fin_de_semana": es_fin_de_semana,
        "es_hora_pico": es_hora_pico,
        "linea_principal": info["linea_principal"],
        "numero_estaciones": info["numero_estaciones"],
        "numero_transbordos": info["numero_transbordos"],
        "tiempo_programado_min": info["tiempo_programado_min"],
    }])

    fila_codificada = pd.get_dummies(fila, columns=["dia_semana", "linea_principal"])
    # Alinear con las columnas que vio el modelo en entrenamiento
    # (si falta una columna de línea/día que no aplica a este viaje, se llena con 0)
    fila_alineada = fila_codificada.reindex(columns=columnas_entrenamiento, fill_value=0)
    return fila_alineada, info


# =====================================================================
# Modo interactivo
# =====================================================================
def menu_interactivo():
    print("\nEntrenando el modelo (árbol de decisión) con el dataset actual...")
    X_train, X_test, y_train, y_test, columnas = obtener_datos_listos()
    modelo = entrenar_modelo(X_train, y_train)
    print("Modelo listo.\n")

    print("PREDICTOR DE RETRASOS - SISTEMA DE TRANSPORTE MASIVO")
    print("Escriba 'lista' para ver las estaciones disponibles.")
    print("Escriba 'salir' para terminar.\n")

    while True:
        origen = input("Estación de ORIGEN: ").strip()
        if origen.lower() == "salir":
            break
        if origen.lower() == "lista":
            print(", ".join(todas_las_estaciones()))
            continue

        destino = input("Estación de DESTINO: ").strip()
        if destino.lower() == "salir":
            break

        try:
            hora_dia = int(input("Hora del día (0-23): ").strip())
        except ValueError:
            print("Hora inválida, debe ser un número entre 0 y 23.\n")
            continue

        dia_semana = input(f"Día de la semana {DIAS_SEMANA}: ").strip().capitalize()
        if dia_semana not in DIAS_SEMANA:
            print("Día inválido.\n")
            continue

        resultado = construir_fila_prediccion(origen, destino, hora_dia, dia_semana, columnas)
        if resultado is None:
            print(f"[ERROR] No existe una ruta válida entre '{origen}' y '{destino}'.\n")
            continue

        fila, info = resultado
        prediccion = modelo.predict(fila)[0]
        probabilidad = modelo.predict_proba(fila)[0][1]  # probabilidad de clase "con_retraso"

        print("-" * 60)
        print(f"Ruta: {origen} -> {destino}  (línea principal: {info['linea_principal']})")
        print(f"Transbordos: {info['numero_transbordos']} | Tiempo programado: {info['tiempo_programado_min']} min")
        etiqueta = "CON RETRASO" if prediccion == 1 else "A TIEMPO"
        print(f"Predicción del modelo: {etiqueta}  (probabilidad de retraso: {probabilidad:.1%})")
        print("-" * 60 + "\n")


# =====================================================================
# Modo pruebas: entrena, evalúa, corre casos fijos y genera gráficas
# =====================================================================
CASOS_DE_PRUEBA = [
    ("Portal_Norte", "Portal_Sur", 7, "Lunes", "Hora pico de la mañana, día laboral"),
    ("Portal_Norte", "Portal_Sur", 14, "Martes", "Hora valle, día laboral"),
    ("Portal_Suba", "Portal_Sur", 18, "Viernes", "Hora pico de la tarde, con transbordo"),
    ("Calle_100", "Calle_72", 10, "Sabado", "Fin de semana, ruta corta"),
    ("Portal_80", "Heroes", 8, "Jueves", "Hora pico, ruta con dos transbordos"),
]


def generar_graficas(metricas: dict, importancias: list) -> None:
    # Gráfica 1: matriz de confusión
    matriz = metricas["matriz_confusion"]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(matriz, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["A_tiempo", "Con_retraso"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["A_tiempo", "Con_retraso"])
    ax.set_xlabel("Predicho"); ax.set_ylabel("Real")
    ax.set_title("Matriz de confusión")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matriz[i][j]), ha="center", va="center", fontsize=14)
    fig.tight_layout()
    fig.savefig(CARPETA / "matriz_confusion.png", dpi=120)
    plt.close(fig)

    # Gráfica 2: importancia de variables (top 8)
    top = importancias[:8]
    nombres = [n for n, _ in top][::-1]
    pesos = [p for _, p in top][::-1]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(nombres, pesos, color="#4C72B0")
    ax.set_xlabel("Importancia")
    ax.set_title("Variables más importantes del árbol de decisión")
    fig.tight_layout()
    fig.savefig(CARPETA / "importancia_variables.png", dpi=120)
    plt.close(fig)

    print(f"Gráficas guardadas: matriz_confusion.png, importancia_variables.png")


def ejecutar_pruebas() -> None:
    print("Entrenando y evaluando el modelo...\n")
    modelo, metricas, reglas, importancias, columnas = entrenar_y_evaluar()

    print("=" * 70)
    print("MÉTRICAS DEL MODELO (árbol de decisión, conjunto de prueba)")
    print("=" * 70)
    print(f"Exactitud (accuracy) : {metricas['exactitud']:.2%}")
    print(f"Precisión (precision): {metricas['precision']:.2%}")
    print(f"Sensibilidad (recall): {metricas['recall']:.2%}")
    print(f"F1-score              : {metricas['f1_score']:.2%}")
    print("\nMatriz de confusión (filas=real, columnas=predicho):")
    print(metricas["matriz_confusion"])
    print()

    print("=" * 70)
    print("CASOS DE PRUEBA (predicción sobre viajes nuevos, no vistos en el entrenamiento)")
    print("=" * 70)
    for origen, destino, hora, dia, descripcion in CASOS_DE_PRUEBA:
        print(f"\nCASO: {descripcion}")
        resultado = construir_fila_prediccion(origen, destino, hora, dia, columnas)
        if resultado is None:
            print(f"  [SIN RUTA] No existe conexión entre {origen} y {destino}.")
            continue
        fila, info = resultado
        prediccion = modelo.predict(fila)[0]
        probabilidad = modelo.predict_proba(fila)[0][1]
        etiqueta = "CON RETRASO" if prediccion == 1 else "A TIEMPO"
        print(f"  Ruta: {origen} -> {destino} | {dia} {hora}:00 | "
              f"transbordos={info['numero_transbordos']} | tiempo programado={info['tiempo_programado_min']} min")
        print(f"  Predicción: {etiqueta}  (probabilidad de retraso: {probabilidad:.1%})")

    print("\n" + "=" * 70)
    print("VARIABLES MÁS IMPORTANTES PARA EL MODELO")
    print("=" * 70)
    for nombre, peso in importancias[:5]:
        print(f"  {nombre:35s} {peso:.3f}")

    generar_graficas(metricas, importancias)


def main() -> None:
    if "--pruebas" in sys.argv:
        ejecutar_pruebas()
        return
    menu_interactivo()


if __name__ == "__main__":
    main()
