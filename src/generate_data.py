"""
Genera datos sinteticos de scoring crediticio.
Simula solicitudes de crédito de una fintech colombiana.

el target (default) se genera con una lógica de negocio realista:
- Mayor mora historica -> mayor probabilidad de default
- Mayor utilización del cupo -> mayor probabilidad de default
- Menor ingresos -> mayor probabilidad de default
- Antigüedad laboral -> menor probabilidad de default
"""

import numpy as np
import pandas as pd


# Generar semilla para reproducibilidad
np.random.seed(42) 

N_SAMPLES = 1000  # Número de solicitudes de crédito a simular

def generate_credit_data(n=N_SAMPLES):
    """Genera un dataset sintético de solicitudes de crédito."""

    #================================
    # 1. Variables demograficas
    #================================
    edad = np.random.normal(30, 12, n).clip(18, 75).astype(int)

    # ciudades principales de Colombia (con pesos realistas)
    ciudades = np.random.choice(
        ["Bogota", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga"],
        p=[0.30, 0.18, 0.15, 0.10, 0.07, 0.20],
        size=n
    )

    # Estrato socioeconómico (1 a 6)
    estrato = np.random.choice([1, 2, 3, 4, 5, 6], size=n,
                               p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.10])

    #================================
    # 2. Variables financieras
    #================================
    # Ingresos mensuales en COP (Una distribucion log-normal)
    ingreso_mensual = np.random.lognormal(mean=13.8, sigma=0.6, size=n)
    ingreso_mensual = np.clip(ingreso_mensual, 1_000_000, 30_000_000).round(-3)


    # Antigüedad laboral en meses
    antiguedad_laboral = np.random.exponential(scale=48, size=n).clip(0, 360).astype(int)


    #============================================
    # 3. Variables de comportamiento crediticio
    #============================================
    # Numero de créditos activos
    num_creditos_activos = np.random.poisson(lam=1.8, size=n).clip(0, 8)

    #utilizacion del cupo de tarjeta de credito (entre 0 y 1)
    utilizacion_cupo = np.random.beta(a=2, b=5, size=n).round(3)

    # Mora maxima historica en los ultimo 12 meses (dias)
    mora_maxima_12m = np.random.choice(
        [0, 30, 60, 90, 120, 150, 180], 
        size=n, 
        p=[0.6, 0.15, 0.10, 0.07, 0.04, 0.03, 0.01]
    )

    # Numero de consultas a centrales de riesgo en los ultimos 6 meses
    num_consultas_6m = np.random.poisson(lam=2.5, size=n).clip(0,15)

    # Relacion deuda/ingreso (DTI)
    dti = (num_creditos_activos * np.random.uniform(0.05, 0.15, n)).round(3)
    dti = np.clip(dti, 0, 0.9)


    #==================================================
    # 4. Generacion del target con logica del negocio
    #==================================================
    # Calculamos un "Score latente" que combina factores de riesgo
    # a mayor score latente -> mayor probabilidad de default

    score_latente = ( 
        -0.00000005 * ingreso_mensual         # Más ingresos -> menor riesgo
        -0.00015 * antiguedad_laboral         # Más antigüedad -> menor riesgo
        +0.35 * dti                           # Mayor DTI -> mayor riesgo
        +1.20 * utilizacion_cupo              # Mayor utilización del cupo -> mayor riesgo
        +0.015 * mora_maxima_12m              # Mayor mora histórica -> mayor riesgo
        +0.12 * num_consultas_6m              # Mayor número de consultas -> mayor riesgo
        +0.08 * num_creditos_activos          # Mayor número de créditos activos -> mayor riesgo
        - 0.02 * edad                         # Mayor edad -> menor riesgo
        + np.random.normal(0, 0.8, n)         # Ruido aleatorio
    )

    # Convertimos el score latente en probabilidad con funcion sigmoide
    prob_default = 1 / (1 + np.exp(-(score_latente - 1.5)))

    # Generamos el target binario (1: default, 0: no default)
    default = (np.random.uniform(0, 1, n) < prob_default).astype(int)

    #==================================
    # Ensamblar el dataframe final
    #==================================

    df = pd.DataFrame({
        'id_solicitud': [f'SC-{i:06d}' for i in range(n)],
        'edad': edad,
        'ciudad': ciudades,
        'estrato': estrato,
        'ingreso_mensual': ingreso_mensual,
        'antiguedad_laboral_meses': antiguedad_laboral,
        'num_creditos_activos': num_creditos_activos,
        'utilizacion_cupo': utilizacion_cupo,
        'mora_maxima_12m': mora_maxima_12m,
        'num_consultas_6m': num_consultas_6m,
        'dti': dti,
        'default': default
    })

    return df

if __name__ == '__main__':
    df = generate_credit_data()

    # Guardar en Data/raw
    df.to_csv("D:\\05 - Modelo Scoring Crediticion\\Codigo\\scoring_crediticio\\data\\raw\\scoring_crediticio.csv", index=False)

    # Resumen
    print("=" * 60)
    print("✅ Dataset generado exitosamente")
    print("=" * 60)
    print(f"Registros: {len(df):,}")
    print(f"Columnas: {len(df.columns):,}")
    print(f"\nTasa de default: {df['default'].mean():.2%}")
    print(f" - Buenos Pagadores: {(df['default'] == 0).sum():,}")
    print(f" - Malos Pagadores: {(df['default'] == 1).sum():,}")
    print("\nPrimeras filas:")
    print(df.head())
    print("\nEstadisticas Descriptivas:")
    print(df.describe().round(2))
    