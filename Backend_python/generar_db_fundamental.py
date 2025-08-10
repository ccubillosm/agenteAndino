import pandas as pd
import numpy as np
import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)
import config

def crear_base_de_datos_fundamental():
    print("-> Construyendo la base de datos fundamental a partir del análisis de los PDFs...")
    data = [
        {'ticker': 'ENELCHILE', 'year': 2020, 'pe_ratio': 16.1, 'pb_ratio': 1.2, 'roe': 0.078, 'debt_to_equity': 0.85, 'current_ratio': 0.8, 'dividend_yield': 0.045},
        {'ticker': 'ENELCHILE', 'year': 2024, 'pe_ratio': 10.2, 'pb_ratio': 0.9, 'roe': 0.095, 'debt_to_equity': 0.75, 'current_ratio': 0.9, 'dividend_yield': 0.055},
        {'ticker': 'SQM-B', 'year': 2020, 'pe_ratio': 35.5, 'pb_ratio': 3.0, 'roe': 0.088, 'debt_to_equity': 0.55, 'current_ratio': 3.1, 'dividend_yield': 0.018},
        {'ticker': 'SQM-B', 'year': 2024, 'pe_ratio': 6.9, 'pb_ratio': 1.6, 'roe': 0.235, 'debt_to_equity': 0.13, 'current_ratio': 4.5, 'dividend_yield': 0.102},
    ]
    df = pd.DataFrame(data)
    conditions_health = [(df['roe'] > 0.15) & (df['debt_to_equity'] < 1), (df['current_ratio'] < 1)]
    choices_health = ['Alta', 'Riesgo']
    df['salud_financiera'] = np.select(conditions_health, choices_health, default='Estable')
    return df

def main():
    print("--- Generando Base de Datos Fundamental ---")
    df_fundamental = crear_base_de_datos_fundamental()
    output_filename = config.ARCHIVO_FUNDAMENTAL
    print(f"\n-> Guardando resultados en '{output_filename}'...")
    df_fundamental.to_csv(output_filename, index=False, decimal=',', sep=';')
    print(f"\n--- ¡PROCESO COMPLETADO CON ÉXITO! ---")

if __name__ == "__main__":
    main()