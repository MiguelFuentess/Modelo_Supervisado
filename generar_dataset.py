"""
=====================================================================
 MÓDULO · generar_dataset.py
 Responsable: Oscar
=====================================================================
Este módulo cumple el punto 2 de la actividad: "Identifique y
describa fuentes de datos relacionadas con el proyecto del transporte
masivo... En caso de no existir dichas fuentes de datos, desarrolle
un dataset con una muestra de dichos datos."

FUENTES DE DATOS REALES IDENTIFICADAS (ver también
DESCRIPCION_DATOS.md para el detalle completo):

1. Portal de Datos Abiertos de Bogotá — "Consolidado de salidas del
   sistema troncal por franja horaria" (TransMilenio).
   https://datosabiertos.bogota.gov.co/dataset/consolidado-de-salidas-sistema-troncal-por-franja-horaria
2. Datos Abiertos Transmilenio (ArcGIS Hub) — "Trazados troncales de
   TransMilenio" (geometría de las rutas troncales).
   https://datosabiertos-transmilenio.hub.arcgis.com/datasets/trazados-troncales-de-transmilenio
3. Portal de Datos Abiertos de Bogotá — "BibloEstación" (puntos de
   lectura/estaciones del sistema, formato geoespacial GPKG).
   https://datosabiertos.bogota.gov.co/dataset/bibloestacion

Estas fuentes existen y son públicas, pero tienen dos limitaciones
para esta actividad puntual: (a) están armadas sobre la red REAL y
completa de TransMilenio, mientras que nuestro proyecto (desde la
actividad 3) usa una red SIMPLIFICADA de 4 líneas y 16 estaciones
pensada para fines didácticos, por lo que cruzar ambas no sería
consistente; y (b) varias vienen en formatos pesados/geoespaciales
(GPKG, shapefiles) que exceden el alcance de la actividad.

Por eso, siguiendo lo que permite el enunciado, construimos un
DATASET PROPIO simulado: generamos viajes aleatorios sobre la misma
red del proyecto (red_transporte.py), calculamos su tiempo programado
real usando la lógica de rutas ya validada en la actividad 3, y le
sumamos una simulación realista de congestión según la hora del día
(inspirada en el patrón que SÍ reportan las fuentes reales listadas
arriba: más carga en horas pico de la mañana y la tarde).

Salida: dataset_viajes_transmilenio.csv
"""

import csv
import random
from pathlib import Path

from red_transporte import todas_las_estaciones, resumen_viaje

ARCHIVO_SALIDA = Path(__file__).parent / "dataset_viajes_transmilenio.csv"

DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

random.seed(42)  # reproducibilidad: todos obtenemos el mismo dataset al correrlo


def factor_congestion(hora: int, dia: str) -> float:
    """
    Simula cuánto más tarda un viaje real frente al tiempo programado,
    según la hora del día y si es fin de semana. Esto imita el patrón
    de horas pico reportado por las fuentes oficiales de TransMilenio
    (franjas horarias de mayor demanda en la mañana y la tarde).
    """
    if dia in ("Sabado", "Domingo"):
        base = 1.05
    else:
        if 6 <= hora <= 8 or 17 <= hora <= 19:       # horas pico
            base = 1.45
        elif 9 <= hora <= 16:                        # horario valle
            base = 1.10
        else:                                         # madrugada / noche
            base = 1.0
    return base + random.uniform(-0.05, 0.10)


def generar_dataset(n_filas: int = 1200) -> list:
    estaciones = todas_las_estaciones()
    filas = []

    while len(filas) < n_filas:
        origen = random.choice(estaciones)
        destino = random.choice(estaciones)
        if origen == destino:
            continue

        info = resumen_viaje(origen, destino)
        if info is None:
            continue

        hora = random.randint(4, 22)  # el sistema opera de 4am a 10pm aprox.
        dia = random.choice(DIAS_SEMANA)
        es_fin_de_semana = 1 if dia in ("Sabado", "Domingo") else 0
        es_hora_pico = 1 if (dia not in ("Sabado", "Domingo") and (6 <= hora <= 8 or 17 <= hora <= 19)) else 0

        factor = factor_congestion(hora, dia)
        tiempo_real = round(info["tiempo_programado_min"] * factor, 1)

        # Etiqueta a predecir: ¿el viaje llegó con retraso significativo?
        # (más de 20% por encima del tiempo programado)
        con_retraso = 1 if tiempo_real > info["tiempo_programado_min"] * 1.20 else 0

        filas.append({
            "origen": origen,
            "destino": destino,
            "linea_principal": info["linea_principal"],
            "hora_dia": hora,
            "dia_semana": dia,
            "es_fin_de_semana": es_fin_de_semana,
            "es_hora_pico": es_hora_pico,
            "numero_estaciones": info["numero_estaciones"],
            "numero_transbordos": info["numero_transbordos"],
            "tiempo_programado_min": info["tiempo_programado_min"],
            "tiempo_real_min": tiempo_real,
            "con_retraso": con_retraso,
        })

    return filas


def guardar_csv(filas: list, ruta: Path = ARCHIVO_SALIDA) -> None:
    columnas = list(filas[0].keys())
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


if __name__ == "__main__":
    filas = generar_dataset(1200)
    guardar_csv(filas)
    n_retraso = sum(f["con_retraso"] for f in filas)
    print(f"Dataset generado: {len(filas)} viajes -> {ARCHIVO_SALIDA.name}")
    print(f"Viajes con retraso: {n_retraso} ({100 * n_retraso / len(filas):.1f}%)")
    print(f"Viajes a tiempo: {len(filas) - n_retraso} ({100 * (len(filas) - n_retraso) / len(filas):.1f}%)")
