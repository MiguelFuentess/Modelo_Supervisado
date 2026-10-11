# Guía de entrega — Actividad 5 (equipo de 4: Oscar, Cristian, Miguel, Evelyn)

## 1. Checklist de la rúbrica

- [x] Equipo de máximo 4 estudiantes.
- [x] Fuentes de datos identificadas y descritas (`DESCRIPCION_DATOS.md`,
      sección 1), con dataset propio generado ante la ausencia de una
      fuente directamente usable (`dataset_viajes_transmilenio.csv`).
- [x] Código Python para el modelo de aprendizaje automático
      (`generar_dataset.py`, `preprocesamiento.py`,
      `modelo_arbol_decision.py`, `main.py`).
- [x] Documento con la descripción de los datos (`DESCRIPCION_DATOS.md`).
- [x] Documento PDF con las pruebas realizadas
      (`Pruebas_Modelo_Supervisado.pdf`).
- [ ] Video (máx. 10 min) con participación de los 4 integrantes
      (pendiente: grabarlo, cada uno con su guion en
      `INTEGRANTE_N_explicacion.md`).
- [ ] Repositorio Git/GitLab con el tutor agregado como colaborador.
- [ ] El log de Git debe evidenciar el trabajo de cada integrante (cada
      quien commitea su propio módulo, igual que en la actividad 3).
- [ ] Documento PDF final con el link al repositorio y al video, subido en
      el enlace de entrega del curso.

## 2. Cómo subir esto a Git (mismo flujo que ya usaron en la actividad 3)

Pueden usar el **mismo repositorio** de la actividad 3
(`sistema-rutas-transporte`), agregando estos archivos en una carpeta nueva
(por ejemplo `actividad5-supervisado/`) para mantener todo el proyecto
junto, o crear un repositorio nuevo solo para esta actividad — cualquiera
de las dos formas es válida, lo importante es que el link quede en el PDF
final.

Evelyn sube primero la base (como hizo en la actividad 3):

```bash
cd carpeta_del_proyecto
git init                      # solo si es un repositorio nuevo
git add .
git commit -m "Evelyn: integracion, main.py y estructura inicial de la actividad 5"
git branch -M main
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main
```

Y luego cada integrante, con su propia cuenta, agrega y commitea su parte:

| Integrante | Archivos a commitear |
|---|---|
| Oscar | `red_transporte.py`, `generar_dataset.py`, `dataset_viajes_transmilenio.csv`, `INTEGRANTE_1_explicacion.md` |
| Cristian | `preprocesamiento.py`, `INTEGRANTE_2_explicacion.md` |
| Miguel | `modelo_arbol_decision.py`, `reglas_arbol_decision.txt`, `INTEGRANTE_3_explicacion.md` |
| Evelyn | `main.py`, `generar_pdf_pruebas.py`, `DESCRIPCION_DATOS.md`, `Pruebas_Modelo_Supervisado.pdf`, `INTEGRANTE_4_explicacion.md` |

Ejemplo para Oscar:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>
git config --global user.name "Oscar"
git config --global user.email "su_correo@ejemplo.com"
git add red_transporte.py generar_dataset.py dataset_viajes_transmilenio.csv INTEGRANTE_1_explicacion.md
git commit -m "Oscar: fuentes de datos y generacion del dataset simulado"
git push
```

Verificar al final con:
```bash
git log --oneline --all
```
Deberían ver 4 commits de 4 autores distintos.

## 3. Para el video (máx. 10 minutos)

Reparto sugerido (≈2 min por persona):
1. Evelyn: breve intro del problema y demo del modo interactivo.
2. Oscar: explica las fuentes de datos y cómo se generó el dataset.
3. Cristian: explica el preprocesamiento (codificación y división train/test).
4. Miguel: explica el árbol de decisión, sus métricas y las reglas aprendidas.
5. Evelyn: cierra mostrando `--pruebas`, las gráficas y el PDF de evidencia.

## 4. Entregable final

Un PDF con:
- Link al repositorio (con el tutor agregado como colaborador).
- Link al video.

Ese PDF es lo que se sube en el enlace de entrega de la tarea del curso.
