import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import os

ARCHIVO_DATABASE = 'database_maestra_tecnica.csv'
ARCHIVO_ELBOW_PLOT = 'elbow_plot_clusters.png'
ARCHIVO_CLUSTER_PLOT = 'resultado_clustering.png'

def analizar_clusters(df):
    print("-> Iniciando análisis de clustering...")
    df['atr_normalized'] = df['atr'] / df['close']
    features = ['adx', 'rsi', 'atr_normalized', 'dist_sma200', 'volumen_normalizado_20']
    df_profiles = df.groupby('ticker')[features].mean().dropna()
    scaler = StandardScaler()
    scaled_profiles = scaler.fit_transform(df_profiles)
    
    inertia = []
    k_range = range(1, min(10, len(df_profiles)))
    for k in k_range:
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42).fit(scaled_profiles)
        inertia.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertia, 'bo-')
    plt.title('Método del Codo')
    plt.savefig(ARCHIVO_ELBOW_PLOT)
    
    try:
        optimal_k = int(input("\n>> Viendo 'elbow_plot_clusters.png', ¿cuántos clusters usar? (ej: 3): "))
    except:
        optimal_k = 3
    
    kmeans = KMeans(n_clusters=optimal_k, n_init=10, random_state=42)
    df_profiles['cluster'] = kmeans.fit_predict(scaled_profiles)
    
    print("\n--- RESULTADOS DEL CLUSTERING ---")
    for i in range(optimal_k):
        print(f"\nCLUSTER {i}: {df_profiles[df_profiles['cluster'] == i].index.tolist()}")
    
    pairplot = sns.pairplot(df_profiles.reset_index(), hue='cluster', vars=features)
    plt.savefig(ARCHIVO_CLUSTER_PLOT)

def main():
    if not os.path.exists(ARCHIVO_DATABASE):
        print(f"!! ERROR: El archivo '{ARCHIVO_DATABASE}' no se encontró.")
        return
    df = pd.read_csv(ARCHIVO_DATABASE, sep=';', decimal=',')
    analizar_clusters(df)

if __name__ == "__main__":
    main()