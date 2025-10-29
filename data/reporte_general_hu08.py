import pandas as pd
import numpy as np
import os
import sys

# --- CONFIGURACIÓN CLAVE ---
CSV_INPUT = 'data-generada.csv'
CSV_OUTPUT = 'reporte_general.csv'
NOTA_APROBATORIA = 3.0
NOTA_MAXIMA = 5.0
NOTA_TOP = 4.5
PERIODOS_TOTALES = 4
COLUMNAS_NOTAS = ['nota1', 'nota2', 'nota3']


# --------------------------

def clasificar_estado(promedio):

    if promedio >= NOTA_TOP:
        return "Top"
    elif promedio < NOTA_APROBATORIA:
        return "En riesgo"
    else:
        return "Aprobado"


def generar_reporte():
    # 1. Leer CSV
    try:
        df = pd.read_csv(CSV_INPUT, encoding='latin-1')
    except FileNotFoundError:
        print(f"ERROR: Archivo '{CSV_INPUT}' no encontrado. Asegúrate de que esté en la misma carpeta.")
        return
    except Exception as e:
        print(f"ERROR de lectura de CSV: {e}")
        return

    # 2. Promedio ACUMULADO por estudiante (Promedio de todas sus asignaturas/periodos)
    df['promedio_asignatura_periodo'] = df[COLUMNAS_NOTAS].mean(axis=1)

    df_reporte = df.groupby(['id_estudiante', 'nombre'], as_index=False)[
        'promedio_asignatura_periodo'
    ].mean()

    df_reporte.rename(columns={'promedio_asignatura_periodo': 'promedio_actual'}, inplace=True)
    df_reporte['promedio_actual'] = df_reporte['promedio_actual'].round(2)

    # 3. Calcular 'Necesita en Periodo 4'
    periodos_actuales = df['periodo'].max()

    puntaje_acumulado = df_reporte['promedio_actual'] * periodos_actuales
    puntaje_necesario_total = NOTA_APROBATORIA * PERIODOS_TOTALES

    df_reporte['necesita_en_periodo4'] = (
                                                 puntaje_necesario_total - puntaje_acumulado
                                         ) / (PERIODOS_TOTALES - periodos_actuales)

    # Limitar el valor (entre 0.0 y 5.0)
    df_reporte['necesita_en_periodo4'] = df_reporte['necesita_en_periodo4'].apply(
        lambda x: min(max(x, 0.0), NOTA_MAXIMA)
    ).round(2)

    # 4. Agregar Columna 'Estado'
    df_reporte['estado'] = df_reporte['promedio_actual'].apply(clasificar_estado)

    # 5. Guardar CSV
    df_final = df_reporte[['id_estudiante', 'nombre', 'promedio_actual', 'necesita_en_periodo4', 'estado']]

    df_final.to_csv(CSV_OUTPUT, index=False, float_format="%.2f", encoding='utf-8')
    print(f"\n Reporte CSV guardado como: {CSV_OUTPUT}")

    # 6. Mostrar Resumen General

    promedio_grupo = df_reporte['promedio_actual'].mean()
    mejor_estudiante = df_reporte.loc[df_reporte['promedio_actual'].idxmax()]
    estudiantes_en_riesgo = df_reporte[df_reporte['estado'] == 'En riesgo']
    porcentaje_riesgo = (len(estudiantes_en_riesgo) / len(df_reporte)) * 100

    print("\n--- RESUMEN GENERAL DEL CURSO (HU08) ---")
    print(f"**Promedio General del Grupo (P1-P3):** {promedio_grupo:.2f}")
    print(f"**Mejor Estudiante:** {mejor_estudiante['nombre']} (Promedio: {mejor_estudiante['promedio_actual']:.2f})")
    print(f"**Porcentaje en Riesgo (< {NOTA_APROBATORIA:.1f}):** {porcentaje_riesgo:.2f}%")
    print("------------------------------------------")


# Ejecutar la función principal
if __name__ == '__main__':
    generar_reporte()