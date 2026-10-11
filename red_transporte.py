"""
red_transporte.py
==================
Módulo base: representa la red de transporte masivo usada en las
actividades anteriores del curso (4 líneas troncales, 16 estaciones,
5 estaciones de transbordo). Se reutiliza aquí como la "fuente de
verdad" sobre la que se simula el dataset de viajes para el
aprendizaje supervisado.

No es el entregable principal de esta actividad (el entregable es el
dataset y el modelo), pero se incluye para que el dataset no salga de
la nada: cada viaje simulado respeta las líneas, estaciones y tiempos
reales definidos aquí, igual que en el sistema experto de la
actividad 3.
"""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple

LINEAS: Dict[str, List[str]] = {
    "Troncal_Caracas": [
        "Portal_Norte", "Calle_100", "Calle_72", "Calle_26",
        "Ricaurte", "Portal_Sur",
    ],
    "Troncal_NQS": [
        "Portal_80", "Minuto_de_Dios", "Salitre",
        "Ricaurte", "Restrepo", "Portal_Usme",
    ],
    "Troncal_Suba": [
        "Portal_Suba", "Suba_Calle_116", "Calle_100",
        "Polo", "Heroes",
    ],
    "Troncal_Autonorte": [
        "Portal_Norte", "Calle_106", "Calle_72", "Heroes",
    ],
}

TIEMPO_ENTRE_ESTACIONES = 3  # minutos, tramo sin congestión
PENALIZACION_TRANSBORDO = 5  # minutos


@dataclass
class Arista:
    destino: str
    linea: str
    peso: float


def construir_adyacencia() -> Dict[str, List[Arista]]:
    adyacencia: Dict[str, List[Arista]] = {}
    estaciones = set()
    for linea, lista in LINEAS.items():
        estaciones.update(lista)
    for e in estaciones:
        adyacencia[e] = []

    for linea, lista in LINEAS.items():
        for i in range(len(lista) - 1):
            a, b = lista[i], lista[i + 1]
            adyacencia[a].append(Arista(b, linea, TIEMPO_ENTRE_ESTACIONES))
            adyacencia[b].append(Arista(a, linea, TIEMPO_ENTRE_ESTACIONES))
    return adyacencia


def estaciones_por_linea() -> Dict[str, set]:
    mapa: Dict[str, set] = {}
    for linea, lista in LINEAS.items():
        for e in lista:
            mapa.setdefault(e, set()).add(linea)
    return mapa


def estaciones_transbordo() -> set:
    mapa = estaciones_por_linea()
    return {e for e, lns in mapa.items() if len(lns) > 1}


def todas_las_estaciones() -> List[str]:
    return sorted(construir_adyacencia().keys())


def ruta_mas_corta(adyacencia, origen: str, destino: str):
    """
    BFS por número de tramos para encontrar una ruta válida entre
    origen y destino (no necesariamente la de menor tiempo con
    transbordos, solo una ruta real y corta usada para simular viajes).
    Devuelve (lista_de_estaciones, lista_de_lineas_usadas) o (None, None)
    si no existe ruta.
    """
    if origen not in adyacencia or destino not in adyacencia:
        return None, None
    if origen == destino:
        return [origen], []

    padre: Dict[str, Tuple[str, str]] = {}
    visitados = {origen}
    cola = deque([origen])

    while cola:
        actual = cola.popleft()
        if actual == destino:
            break
        for arista in adyacencia[actual]:
            if arista.destino not in visitados:
                visitados.add(arista.destino)
                padre[arista.destino] = (actual, arista.linea)
                cola.append(arista.destino)

    if destino not in visitados:
        return None, None

    camino = [destino]
    lineas = []
    nodo = destino
    while nodo != origen:
        anterior, linea = padre[nodo]
        camino.append(anterior)
        lineas.append(linea)
        nodo = anterior
    camino.reverse()
    lineas.reverse()
    return camino, lineas


def resumen_viaje(origen: str, destino: str):
    """
    Calcula, para un par origen-destino, el número de tramos, el
    número de transbordos y el tiempo programado (sin congestión),
    usando la red definida arriba. Es la función que usa
    generar_dataset.py para simular cada fila del dataset.
    """
    adyacencia = construir_adyacencia()
    camino, lineas = ruta_mas_corta(adyacencia, origen, destino)
    if camino is None:
        return None

    numero_tramos = len(camino) - 1
    transbordos = 0
    linea_previa = None
    for linea in lineas:
        if linea_previa is not None and linea != linea_previa:
            transbordos += 1
        linea_previa = linea

    tiempo_programado = numero_tramos * TIEMPO_ENTRE_ESTACIONES + transbordos * PENALIZACION_TRANSBORDO
    linea_principal = lineas[0] if lineas else None

    return {
        "numero_estaciones": len(camino),
        "numero_transbordos": transbordos,
        "tiempo_programado_min": tiempo_programado,
        "linea_principal": linea_principal,
    }
