import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

ARCHIVO_DATABASE = 'database_maestra_tecnica.csv'
ARCHIVO_HEATMAP_SALIDA = 'heatmap_correlacion.png'

def analizar_correlaciones(df):
    print("-> Seleccionando indicadores clave para el análisis...")
    indicadores = ['close', 'rsi', 'stoch_k', 'cci', 'adx', 'volumen_normalizado_20']
    columnas_validas = [col for col in indicadores if col in df.columns]
    df_corr = df[columnas_validas].corr()
    print("\n--- MATRIZ DE CORRELACIÓN NUMÉRICA ---")
    print(df_corr.round(2))
    print(f"\n-> Generando mapa de calor y guardándolo como '{ARCHIVO_HEATMAP_SALIDA}'...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Mapa de Calor de Correlación')
    plt.savefig(ARCHIVO_HEATMAP_SALIDA)
    print("-> ¡Mapa de calor guardado!")

def main():
    if not os.path.exists(ARCHIVO_DATABASE):
        print(f"!! ERROR: El archivo '{ARCHIVO_DATABASE}' no se encontró.")
        return
    df = pd.read_csv(ARCHIVO_DATABASE, sep=';', decimal=',')
    analizar_correlaciones(df)

if __name__ == "__main__":
    main()