import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

# Cargar config desde la raíz del proyecto
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)
import config

ARCHIVO_DATABASE_TECNICA = config.ARCHIVO_TECNICO
ARCHIVO_ACCIONES_ORIGINAL = config.CSV_ACCIONES
ARCHIVO_ACCIONES_SALIDA = config.ARCHIVO_PERFILES
NUMERO_DE_CLUSTERS = config.NUMERO_DE_CLUSTERS

def perfilar_acciones(df_tecnica, df_acciones):
    print("-> Iniciando análisis de clustering para definir perfiles...")
    
    # Calcular características adicionales usando sma_50 en lugar de sma_200
    df_tecnica['atr_normalized'] = df_tecnica['atrr_14'] / df_tecnica['close']
    df_tecnica['dist_sma50'] = (df_tecnica['close'] - df_tecnica['sma_50']) / df_tecnica['sma_50']
    df_tecnica['volumen_normalizado_20'] = df_tecnica['volume'] / df_tecnica['volume'].rolling(20).mean()
    
    # Usar solo las características que están disponibles
    features = ['adx_14', 'rsi_14', 'atr_normalized', 'dist_sma50', 'volumen_normalizado_20']
    
    # Filtrar solo las filas donde todas las características están disponibles
    df_profiles = df_tecnica.groupby('ticker')[features].mean().dropna()
    
    if len(df_profiles) == 0:
        print("!! ERROR: No hay suficientes datos para realizar clustering")
        return None
    
    print(f"   - Perfiles calculados para {len(df_profiles)} tickers")
    
    scaler = StandardScaler()
    scaled_profiles = scaler.fit_transform(df_profiles)
    kmeans = KMeans(n_clusters=NUMERO_DE_CLUSTERS, n_init=10, random_state=42)
    df_profiles['cluster'] = kmeans.fit_predict(scaled_profiles)
    
    df_centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)
    tendency_idx = df_centroids['adx_14'].idxmax()
    range_idx = df_centroids['atr_normalized'].idxmin()
    profile_map = {
        tendency_idx: "Cohete de Tendencia",
        range_idx: "Tortuga de Valor (Rango)"
    }
    # Asignar el perfil restante
    transition_idx = list(set(range(NUMERO_DE_CLUSTERS)) - {tendency_idx, range_idx})[0]
    profile_map[transition_idx] = "Indeciso (En Transición)"
    
    df_asignacion = df_profiles.reset_index()[['ticker', 'cluster']]
    df_asignacion['personalidad'] = df_asignacion['cluster'].map(profile_map)
    
    df_acciones.rename(columns={'NEMOTECNICO': 'ticker'}, inplace=True)
    df_acciones_actualizado = pd.merge(df_acciones, df_asignacion, on='ticker', how='left')
    return df_acciones_actualizado

def main():
    print("--- INICIANDO GENERACIÓN DE PERFILES DE ACCIONES ---")
    
    try:
        df_tecnica = pd.read_csv(ARCHIVO_DATABASE_TECNICA, sep=';', decimal=',')
        df_acciones = pd.read_csv(ARCHIVO_ACCIONES_ORIGINAL)
        
        print(f"   - Datos técnicos cargados: {len(df_tecnica)} registros")
        print(f"   - Acciones cargadas: {len(df_acciones)} tickers")
        
        df_final = perfilar_acciones(df_tecnica, df_acciones)
        
        if df_final is not None:
            df_final.to_csv(ARCHIVO_ACCIONES_SALIDA, index=False, sep=';', encoding='utf-8-sig')
            print(f"\n--- ¡PROCESO COMPLETADO! ---")
            print(f"   - Archivo guardado: {ARCHIVO_ACCIONES_SALIDA}")
            print(f"   - Perfiles generados: {len(df_final)} acciones")
            print("\nDistribución de perfiles:")
            perfiles = df_final['personalidad'].value_counts()
            for perfil, count in perfiles.items():
                print(f"   {perfil}: {count} acciones")
        else:
            print("!! ERROR: No se pudieron generar los perfiles")
            
    except Exception as e:
        print(f"!! ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()