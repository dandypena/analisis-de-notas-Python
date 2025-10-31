import pandas as pd
import sys


CSV_INPUT = 'reporte_general.csv'


# -------------------------------

def encontrar_mejor_estudiante():

    # 1. Lectura del CSV
    try:

        df = pd.read_csv(CSV_INPUT, encoding='utf-8')
    except FileNotFoundError:
        print(f"ERROR: Archivo '{CSV_INPUT}' no encontrado.")
        return
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        return

    # 2. Identificar el promedio máximo
    if 'promedio_actual' not in df.columns:
        print("ERROR: La columna 'promedio_actual' no se encontró en el CSV.")
        return

    max_promedio = df['promedio_actual'].max()

    # 3.  Filtra todas las filas que tienen el promedio máximo
    df_mejores = df[df['promedio_actual'] == max_promedio].copy()

    # 4. Preparar la salida
    nombres_mejores = df_mejores['nombre'].tolist()

    # 5. Mostrar en Consola
    print("\n--- MEJOR ESTUDIANTE DEL CURSO ---")
    print(f"**Promedio Máximo del Curso:** {max_promedio:.2f}")

    if len(nombres_mejores) == 1:
        print(f"\n**Mejor Estudiante Único:** {nombres_mejores[0]}")
    else:
        # Muestra la lista de estudiantes si hay empate
        print(f"\n**Mejores Estudiantes (Empate - {len(nombres_mejores)}):**")
        print(", ".join(nombres_mejores))

    print("---------------------------------------------")


if __name__ == '__main__':
    encontrar_mejor_estudiante()