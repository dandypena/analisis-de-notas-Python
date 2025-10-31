import pandas as pd
import os
import sys

CSV_INPUT = 'reporte_general.csv'
CSV_OUTPUT = 'estudiantes_en_riesgo.csv'
NOTA_APROBATORIA = 3.0


def generar_reporte_riesgo():

    # 1. Lectura del CSV
    try:
        df = pd.read_csv(CSV_INPUT, encoding='utf-8')
    except FileNotFoundError:
        print(f"ERROR: Archivo '{CSV_INPUT}' no encontrado.")
        print("Asegúrate de haber generado el reporte general (HU08) primero.")
        return
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        return

    # 2. Filtrar: Solo Estudiantes en Riesgo (< 3.0)
    df_riesgo = df[df['promedio_actual'] < NOTA_APROBATORIA].copy()

    if df_riesgo.empty:
        print("\n--- REPORTE DE RIESGO ---")
        print(f"¡Felicidades! Ningún estudiante tiene un promedio acumulado menor a {NOTA_APROBATORIA:.1f}.")
        return

    # 3. Preparar para Salida
    df_salida = df_riesgo[['nombre', 'promedio_actual', 'necesita_en_periodo4']]

    # 4. Mostrar Lista en Consola (Criterio de Aceptación)
    print("\n--- ESTUDIANTES EN RIESGO ---")
    print(f" Promedio Acumulado Menor a {NOTA_APROBATORIA:.1f} (Basado en {CSV_INPUT})")
    print("\nLista de Estudiantes:")

    print(df_salida.to_string(index=False, float_format="%.2f"))

    print(f"\nTotal de estudiantes en riesgo: {len(df_riesgo)}")

    # 5. Guardar CSV
    df_salida.to_csv(CSV_OUTPUT, index=False, encoding='utf-8')
    print(f"\n Reporte de riesgo guardado como: **{CSV_OUTPUT}**")


# --- Punto de Entrada ---
if __name__ == '__main__':
    generar_reporte_riesgo()