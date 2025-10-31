import pandas as pd
import numpy as np
import sys
import os


CSV_INPUT = 'data-generada.csv'
CSV_OUTPUT = 'estudiantes_en_riesgo.csv'
NOTA_APROBATORIA = 3.0
NOTA_MAXIMA = 5.0
PERIODOS_TOTALES = 4
COLUMNAS_NOTAS = ['nota1', 'nota2', 'nota3']




def generar_reporte_riesgo():
    """
    Identifica estudiantes con promedio < 3.0
    """

    # 1. Lectura del CSV
    try:

        df = pd.read_csv(CSV_INPUT, encoding='latin-1')
    except FileNotFoundError:
        print(f"ERROR: Archivo '{CSV_INPUT}' no encontrado.")
        return
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        return

    # 2. Cálculo del Promedio Parcial por Estudiante
    df['promedio_asignatura_periodo'] = df[COLUMNAS_NOTAS].mean(axis=1)

    # Agrupamos para obtener el promedio ACUMULADO por estudiante
    df_promedios = df.groupby(['id_estudiante', 'nombre'], as_index=False)[
        'promedio_asignatura_periodo'
    ].mean()

    df_promedios.rename(columns={'promedio_asignatura_periodo': 'promedio_actual'}, inplace=True)
    df_promedios['promedio_actual'] = df_promedios['promedio_actual'].round(2)

    # 3. Filtrar: Solo Estudiantes en Riesgo
    df_riesgo = df_promedios[df_promedios['promedio_actual'] < NOTA_APROBATORIA].copy()

    if df_riesgo.empty:
        print("\n--- REPORTE DE RIESGO ---")
        print(f" ¡Felicidades! Ningún estudiante tiene un promedio acumulado menor a {NOTA_APROBATORIA:.1f}.")
        return

    periodos_actuales = df['periodo'].max()

    puntaje_acumulado = df_riesgo['promedio_actual'] * periodos_actuales
    puntaje_necesario_total = NOTA_APROBATORIA * PERIODOS_TOTALES

    df_riesgo['nota_necesaria_en_periodo4'] = (
                                                      puntaje_necesario_total - puntaje_acumulado
                                              ) / (PERIODOS_TOTALES - periodos_actuales)

    # 5. Limitar la Nota
    df_riesgo['nota_necesaria_en_periodo4'] = df_riesgo['nota_necesaria_en_periodo4'].apply(
        lambda x: min(max(x, 0.0), NOTA_MAXIMA)
    ).round(2)

    # 6. Preparar para Salida
    df_salida = df_riesgo[['nombre', 'promedio_actual', 'nota_necesaria_en_periodo4']]

    # 7. Mostrar Lista en Consola
    print("\n--- ESTUDIANTES EN RIESGO (HU03) ---")
    print(f"Criterio: Promedio Acumulado Menor a {NOTA_APROBATORIA:.1f}")
    print("\nLista de Estudiantes:")
    print(df_salida.to_markdown(index=False, floatfmt=".2f"))
    print(f"\nTotal de estudiantes en riesgo: {len(df_riesgo)}")

    # 8. Guardar CSV (Criterio de Aceptación)
    df_salida.to_csv(CSV_OUTPUT, index=False, encoding='utf-8')
    print(f"\n Reporte de riesgo guardado como: **{CSV_OUTPUT}**")


# --- Punto de Entrada ---
if __name__ == '__main__':
    generar_reporte_riesgo()