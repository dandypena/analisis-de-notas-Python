import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Constantes y Configuración ---
COLUMNAS_NOTAS = ['nota1', 'nota2', 'nota3']
OUTPUT_IMAGE = 'promedios_curso_hu01.png'
CSV_FILE = 'data-generada.csv'


def calcular_y_graficar_promedios_hu01(csv_path):
    """
    Implementa la HU01 con manejo de errores de ruta y codificación.
    """
    print(f"---  Análisis de Promedios del Curso (HU01) ---")

    df = None

    # --- Lógica de Lectura  ---
    try:
        df = pd.read_csv(csv_path)
        print(f" Archivo '{csv_path}' leído exitosamente con codificación por defecto.")

    except FileNotFoundError:
        full_path = os.path.abspath(csv_path)
        print(f" ERROR: Archivo '{csv_path}' NO ENCONTRADO.")
        print(f"         El script buscó en la ubicación: {full_path}")
        print("         **Asegúrate de que el CSV esté en la misma carpeta que el script.**")
        return

    except Exception as e_default:
        print(
            f"  Advertencia: Falló la lectura con codificación por defecto ({e_default}). Intentando con 'latin-1'...")
        try:
            df = pd.read_csv(csv_path, encoding='latin-1')
            print(f" Archivo '{csv_path}' leído exitosamente con codificación 'latin-1'.")
        except Exception as e_retry:
            print(f" ERROR CRÍTICO: Falló la lectura del archivo CSV incluso con 'latin-1'.")
            print(f"         Revisa el formato del archivo o el separador (debe ser coma ',').")
            print(f"         Error final: {e_retry}")
            return

    # --- Continúa el Análisis Solo si la lectura fue exitosa ---
    if df is not None:
        print(f" {len(df)} filas encontradas y listas para analizar.")

        # 1. Calcular el promedio simple de las 3 notas por fila
        df['promedio_parcial'] = df[COLUMNAS_NOTAS].mean(axis=1)

        # 2. Calcular el Promedio del Curso por Periodo
        promedios_periodos = df.groupby('periodo')['promedio_parcial'].mean()
        periodos_analisis = [1, 2, 3]
        promedios_periodos = promedios_periodos.loc[promedios_periodos.index.isin(periodos_analisis)]

        # 3. Calcular el Promedio Anual Parcial
        if len(promedios_periodos) == len(periodos_analisis):
            promedio_anual = promedios_periodos.mean()
        else:
            print(" Advertencia: Faltan datos para uno o más periodos (1-3). Finalizando.")
            return

        # --- Salida en Consola ---
        print("\n--- Resultados de Promedios del Curso (HU01) ---")

        datos_grafico = {}
        for periodo, promedio in promedios_periodos.items():
            etiqueta = f"Periodo {int(periodo)}"
            datos_grafico[etiqueta] = promedio
            print(f"**Promedio del Curso en {etiqueta}:** {promedio:.2f}")

        etiqueta_anual = "Promedio Anual (P1-3)"
        datos_grafico[etiqueta_anual] = promedio_anual
        print(f"\n**Promedio Anual Parcial del Curso (P1-3):** {promedio_anual:.2f}")

        # --- Generación del Gráfico ---

        nombres = list(datos_grafico.keys())
        valores = list(datos_grafico.values())
        colores = ['skyblue', 'lightgreen', 'salmon', 'gold']

        plt.figure(figsize=(10, 6))
        barras = plt.bar(nombres, valores, color=colores)

        for bar in barras:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval - 0.2, f'{yval:.2f}', ha='center', va='bottom',
                     fontweight='bold', color='black')

        plt.title('Promedio del Curso por Periodo y Promedio Anual Parcial', fontsize=14)
        plt.xlabel('Resultados del Curso', fontsize=12)
        plt.ylabel('Calificación Promedio', fontsize=12)
        plt.ylim(0, 5.5)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.savefig(OUTPUT_IMAGE)
        print(f"\n Gráfico generado y guardado como: **{OUTPUT_IMAGE}**")


#
if __name__ == '__main__':

    calcular_y_graficar_promedios_hu01(CSV_FILE)