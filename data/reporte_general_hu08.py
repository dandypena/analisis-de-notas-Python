# python
import pandas as pd

CSV_INPUT = 'data-generada.csv'
CSV_OUTPUT = 'reporte_general.csv'
NOTA_APROBATORIA = 3.0
NOTA_MAXIMA = 5.0
NOTA_TOP = 4.5
PERIODOS_TOTALES = 4
COLUMNAS_NOTAS = ['nota1', 'nota2', 'nota3']


def clasificar_estado(promedio):
    if promedio >= NOTA_TOP:
        return "Top"
    elif promedio < NOTA_APROBATORIA:
        return "En riesgo"
    else:
        return "Aprobado"


def generar_reporte():

    # 1. Leer CSV (intento utf-8 primero, luego latin-1)
    try:
        df = pd.read_csv(CSV_INPUT, encoding='utf-8')
    except FileNotFoundError:
        print(f"ERROR: Archivo `{CSV_INPUT}` no encontrado.")
        return
    except Exception:
        try:
            df = pd.read_csv(CSV_INPUT, encoding='latin-1')
            print(f"Advertencia: lectura con 'latin-1' aplicada para `{CSV_INPUT}`.")
        except Exception as e:
            print(f"ERROR de lectura de CSV: {e}")
            return

    # Validaciones básicas de columnas
    required_cols = ['id_estudiante', 'nombre'] + COLUMNAS_NOTAS
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"ERROR: Faltan columnas requeridas en {CSV_INPUT}: {missing}")
        return

    # Coerción a numérico de notas y manejo de NA
    for c in COLUMNAS_NOTAS:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    # 2. Promedio ACUMULADO por estudiante
    df['promedio_asignatura_periodo'] = df[COLUMNAS_NOTAS].mean(axis=1)

    df_reporte = df.groupby(['id_estudiante', 'nombre'], as_index=False)[
        'promedio_asignatura_periodo'
    ].mean()

    df_reporte.rename(columns={'promedio_asignatura_periodo': 'promedio_actual'}, inplace=True)
    df_reporte['promedio_actual'] = df_reporte['promedio_actual'].round(2)

    # 3. Calcular 'Necesita en Periodo 4' con protección contra división por cero y valores no numéricos
    # Normalizar columna 'periodo' del df de entrada
    periodos_actuales = 0
    if 'periodo' in df.columns:
        df['periodo'] = pd.to_numeric(df['periodo'], errors='coerce')
        if not df['periodo'].dropna().empty:
            try:
                periodos_actuales = int(df['periodo'].dropna().max())
            except Exception:
                periodos_actuales = 0

    if periodos_actuales >= PERIODOS_TOTALES or periodos_actuales <= 0:
        # Si ya completó todos los periodos o no hay información, marcar como 0.0 (no aplica o ya cumplido)
        df_reporte['necesita_en_periodo4'] = 0.0
    else:
        puntaje_acumulado = df_reporte['promedio_actual'] * periodos_actuales
        puntaje_necesario_total = NOTA_APROBATORIA * PERIODOS_TOTALES

        df_reporte['necesita_en_periodo4'] = (
            (puntaje_necesario_total - puntaje_acumulado) / (PERIODOS_TOTALES - periodos_actuales)
        )

        # Limitar el valor (entre 0.0 y NOTA_MAXIMA)
        df_reporte['necesita_en_periodo4'] = df_reporte['necesita_en_periodo4'].apply(
            lambda x: min(max(x, 0.0), NOTA_MAXIMA)
        ).round(2)

    # 4. Agregar Columna 'Estado'
    df_reporte['estado'] = df_reporte['promedio_actual'].apply(clasificar_estado)

    # 5. Guardar CSV
    df_final = df_reporte[['id_estudiante', 'nombre', 'promedio_actual', 'necesita_en_periodo4', 'estado']]

    df_final.to_csv(CSV_OUTPUT, index=False, float_format="%.2f", encoding='utf-8')
    print(f"\nReporte CSV guardado como: {CSV_OUTPUT}")

    # 6. Mostrar Resumen General
    promedio_grupo = df_reporte['promedio_actual'].mean() if not df_reporte.empty else 0.0
    if not df_reporte.empty:
        mejor_estudiante = df_reporte.loc[df_reporte['promedio_actual'].idxmax()]
        estudiantes_en_riesgo = df_reporte[df_reporte['estado'] == 'En riesgo']
        porcentaje_riesgo = (len(estudiantes_en_riesgo) / len(df_reporte)) * 100

        print("\n--- RESUMEN GENERAL DEL CURSO  ---")
        print(f"**Promedio General del Grupo:** {promedio_grupo:.2f}")
        print(f"**Mejor Estudiante:** {mejor_estudiante['nombre']} (Promedio: {mejor_estudiante['promedio_actual']:.2f})")
        print(f"**Porcentaje en Riesgo (< {NOTA_APROBATORIA:.1f}):** {porcentaje_riesgo:.2f}%")
        print("------------------------------------------")
    else:
        print("No hay datos de estudiantes para mostrar resumen.")


if __name__ == '__main__':
    generar_reporte()
