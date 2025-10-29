"""
Generador de dataset sintético para seguimiento de notas académicas
Genera un CSV con estudiantes y asignaturas (periodos 1-3 con datos)
"""

import random
import numpy as np
import pandas as pd
import argparse
import os
from datetime import datetime


def generar_dataset(
        num_estudiantes=40,
        asignaturas=None,
        num_periodos=3,
        nota_min=0.0,
        nota_max=5.0,
        seed=None,
        output_path="data-generada.csv"
):
    """
    Genera un dataset sintético de notas académicas.

    Args:
        num_estudiantes: Número de estudiantes a generar
        asignaturas: Lista de asignaturas (default: 7 materias)
        num_periodos: Número de periodos con datos (default: 3)
        nota_min: Nota mínima posible (default: 0.0)
        nota_max: Nota máxima posible (default: 5.0)
        seed: Semilla para reproducibilidad (None = aleatorio)
        output_path: Ruta del archivo CSV de salida

    Returns:
        DataFrame con los datos generados y la ruta del archivo
    """

    # Configurar semilla aleatoria
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Asignaturas por defecto
    if asignaturas is None:
        asignaturas = [
            "Programación",
            "Matemáticas",
            "Bases de Datos",
            "Algoritmos",
            "Sistemas",
            "Redes",
            "Ingeniería de Software"
        ]

    # Listas ampliadas de nombres colombianos
    nombres = [
        "Catalina", "Juan", "Sofía", "Andrés", "Valentina", "Diego", "María", "Mateo",
        "Laura", "Felipe", "Isabella", "Luis", "Camila", "Alejandro", "Gabriela", "Carlos",
        "Daniela", "Sebastián", "Natalia", "Miguel", "Paula", "Santiago", "Alejandra", "José",
        "Juliana", "Nicolás", "Valeria", "Samuel", "Ana", "David", "Carolina", "Sebastián",
        "Mariana", "Daniel", "Lucía", "Tomás", "Sara", "Martín", "Emma", "Gabriel",
        "Victoria", "Leonardo", "Manuela", "Emilio", "Valeria", "Maximiliano", "Antonella",
        "Ricardo", "Julieta", "Eduardo", "Renata", "Fernando", "Adriana", "Joaquín"
    ]

    apellidos = [
        "Rodríguez", "Gómez", "García", "Martínez", "López", "Pérez", "Sánchez", "Ramírez",
        "Torres", "Vargas", "Rojas", "Muñoz", "Castro", "Herrera", "Moreno", "Jiménez",
        "Ortiz", "Álvarez", "Romero", "Rincón", "Cárdenas", "Peña", "Mendoza", "Suárez",
        "Zapata", "Vega", "Reyes", "Silva", "Medina", "Gutiérrez", "Ruiz", "Díaz",
        "Parra", "Molina", "Ríos", "Mejía", "Salazar", "Bermúdez", "Pardo", "Valencia"
    ]

    # Generar nombres únicos de estudiantes
    estudiantes = []
    used_names = set()

    for i in range(num_estudiantes):
        intento = 0
        while True:
            nombre_completo = f"{random.choice(nombres)} {random.choice(apellidos)}"
            intento += 1

            # Si después de 20 intentos no encuentra único, agregar número
            if nombre_completo not in used_names:
                used_names.add(nombre_completo)
                break
            elif intento > 20:
                nombre_completo = f"{nombre_completo} {i + 1}"
                used_names.add(nombre_completo)
                break

        estudiantes.append({
            "id_estudiante": i + 1,
            "nombre": nombre_completo
        })

    # Generar datos para cada estudiante
    rows = []

    for est in estudiantes:
        # Rendimiento base del estudiante (distribución normal alrededor de 3.0)
        # Esto simula que cada estudiante tiene una "capacidad" diferente
        base_rendimiento = np.clip(
            np.random.normal(loc=3.0, scale=0.8),
            nota_min,
            nota_max
        )

        # Sesgo individual del estudiante (consistencia)
        student_bias = np.random.normal(loc=0.0, scale=0.25)
        student_bias = np.clip(student_bias, -0.6, 0.6)

        for asignatura in asignaturas:
            # Sesgo por asignatura (fortalezas/debilidades)
            subj_bias = np.random.normal(loc=0.0, scale=0.4)
            subj_bias = np.clip(subj_bias, -0.8, 0.8)

            for periodo in range(1, num_periodos + 1):
                # Tendencia de mejora/empeoramiento a lo largo de los periodos
                periodo_trend = np.random.choice(
                    [-0.15, -0.05, 0.0, 0.05, 0.15],
                    p=[0.15, 0.20, 0.30, 0.20, 0.15]
                )
                ajuste_periodo = periodo_trend * (periodo - 1)

                # Generar 3 notas para el periodo
                media_notas = base_rendimiento + subj_bias + student_bias + ajuste_periodo

                # Las 3 notas tienen variabilidad entre ellas
                notas = np.random.normal(
                    loc=media_notas,
                    scale=0.5,  # Desviación entre las 3 notas
                    size=3
                )
                notas = np.clip(notas, nota_min, nota_max)
                nota1, nota2, nota3 = np.round(notas, 2)

                # Generar asistencia (correlacionada con rendimiento)
                # Estudiantes con mejor rendimiento tienden a mayor asistencia
                asistencia_media = 70 + (base_rendimiento / nota_max) * 25
                asistencia = np.random.normal(loc=asistencia_media, scale=10)
                asistencia = np.clip(asistencia, 50, 100)
                asistencia = round(float(asistencia), 1)

                # Generar participación (también correlacionada con rendimiento)
                participacion_media = 0.4 + (base_rendimiento / nota_max) * 0.5
                participacion = np.random.normal(loc=participacion_media, scale=0.2)
                participacion = np.clip(participacion, 0, 1)
                participacion = round(float(participacion), 2)

                # Agregar fila al dataset
                # NOTA: promedio_periodo NO se incluye - debe ser calculado por el analista
                row = {
                    "id_estudiante": est["id_estudiante"],
                    "nombre": est["nombre"],
                    "asignatura": asignatura,
                    "periodo": periodo,
                    "nota1": nota1,
                    "nota2": nota2,
                    "nota3": nota3,
                    "asistencia_%": asistencia,
                    "participacion": participacion
                }
                rows.append(row)

    # Crear DataFrame
    df = pd.DataFrame(rows)

    # Ordenar por estudiante, asignatura y periodo
    df = df.sort_values(
        by=["id_estudiante", "asignatura", "periodo"]
    ).reset_index(drop=True)

    # Asegurar que el directorio de salida existe
    outdir = os.path.dirname(output_path)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    # Guardar CSV
    df.to_csv(output_path, index=False, float_format="%.2f")

    return df, output_path


def main():
    """Función principal con argumentos de línea de comandos"""

    parser = argparse.ArgumentParser(
        description="Generador de dataset sintético para seguimiento de notas académicas"
    )
    parser.add_argument(
        "--estudiantes",
        type=int,
        default=40,
        help="Número de estudiantes a generar (default: 40)"
    )
    parser.add_argument(
        "--periodos",
        type=int,
        default=3,
        help="Número de periodos académicos (default: 3)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data-generada.csv",
        help="Ruta del archivo CSV de salida (default: data-generada.csv)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semilla para reproducibilidad (default: aleatorio basado en tiempo)"
    )

    args = parser.parse_args()

    # Si no se especifica seed, usar timestamp
    seed_final = args.seed if args.seed is not None else int(datetime.now().timestamp())

    # Generar dataset
    generar_dataset(
        num_estudiantes=args.estudiantes,
        num_periodos=args.periodos,
        seed=seed_final,
        output_path=args.output
    )


if __name__ == "__main__":
    main()