#!/usr/bin/env python3
"""
Visualizador Interactivo del Agente Cóndor Andino
Permite explorar los resultados del análisis de forma sencilla e interactiva
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Agregar la raíz del proyecto al path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import config

# Configurar estilo de matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VisualizadorCondor:
    def __init__(self):
        self.df_acciones = None
        self.df_tecnico = None
        self.df_fundamental = None
        self.df_perfiles = None
        self.df_oportunidades = None
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga todos los archivos de datos generados"""
        print("📊 Cargando datos del Agente Cóndor...")
        
        # Cargar datos de acciones
        if os.path.exists(config.CSV_ACCIONES):
            self.df_acciones = pd.read_csv(config.CSV_ACCIONES)
            print(f"✓ Acciones cargadas: {len(self.df_acciones)}")
        
        # Cargar datos técnicos
        if os.path.exists(config.ARCHIVO_TECNICO):
            self.df_tecnico = pd.read_csv(config.ARCHIVO_TECNICO, sep=';', decimal=',')
            print(f"✓ Datos técnicos cargados: {len(self.df_tecnico)}")
        
        # Cargar datos fundamentales
        if os.path.exists(config.ARCHIVO_FUNDAMENTAL_DB):
            self.df_fundamental = pd.read_csv(config.ARCHIVO_FUNDAMENTAL_DB, sep=';', decimal=',')
            print(f"✓ Datos fundamentales cargados: {len(self.df_fundamental)}")
        
        # Cargar perfiles
        if os.path.exists(config.ARCHIVO_PERFILES):
            self.df_perfiles = pd.read_csv(config.ARCHIVO_PERFILES, sep=';', decimal=',')
            print(f"✓ Perfiles cargados: {len(self.df_perfiles)}")
        
        # Cargar oportunidades
        if os.path.exists(config.ARCHIVO_OPORTUNIDADES):
            self.df_oportunidades = pd.read_csv(config.ARCHIVO_OPORTUNIDADES, sep=';', decimal=',')
            print(f"✓ Oportunidades cargadas: {len(self.df_oportunidades)}")
    
    def mostrar_resumen_general(self):
        """Muestra un resumen general de todos los datos"""
        print("\n" + "="*60)
        print("📈 RESUMEN GENERAL DEL AGENTE CÓNDOR")
        print("="*60)
        
        if self.df_acciones is not None:
            print(f"\n🏢 ACCIONES ANALIZADAS: {len(self.df_acciones)}")
            print(f"   Sectores: {self.df_acciones['INDUSTRIA'].nunique()}")
            print(f"   Sectores principales: {', '.join(self.df_acciones['INDUSTRIA'].value_counts().head(3).index)}")
        
        if self.df_tecnico is not None:
            print(f"\n📊 DATOS TÉCNICOS: {len(self.df_tecnico)} registros")
            print(f"   Tickers únicos: {self.df_tecnico['ticker'].nunique()}")
            print(f"   Período: {self.df_tecnico['date'].min()} a {self.df_tecnico['date'].max()}")
        
        if self.df_fundamental is not None:
            print(f"\n💰 ANÁLISIS FUNDAMENTAL: {len(self.df_fundamental)} registros")
            print(f"   Años cubiertos: {sorted(self.df_fundamental['year'].unique())}")
            print(f"   Salud financiera: {self.df_fundamental['salud_financiera'].value_counts().to_dict()}")
        
        if self.df_perfiles is not None:
            print(f"\n🎭 PERFILES DE ACCIONES: {len(self.df_perfiles)}")
            perfiles = self.df_perfiles['personalidad'].value_counts()
            for perfil, count in perfiles.items():
                print(f"   {perfil}: {count} acciones")
        
        if self.df_oportunidades is not None:
            print(f"\n🎯 OPORTUNIDADES DETECTADAS: {len(self.df_oportunidades)}")
            if 'ticker' in self.df_oportunidades.columns:
                tickers_unicos = self.df_oportunidades['ticker'].nunique()
                print(f"   Tickers únicos: {tickers_unicos}")
    
    def crear_dashboard_completo(self):
        """Crea un dashboard completo con todas las visualizaciones"""
        print("\n🎨 Generando dashboard completo...")
        
        # Crear figura grande con múltiples subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Distribución de perfiles (arriba izquierda)
        ax1 = plt.subplot(3, 3, 1)
        if self.df_perfiles is not None and 'personalidad' in self.df_perfiles.columns:
            perfiles_count = self.df_perfiles['personalidad'].value_counts()
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            ax1.pie(perfiles_count.values, labels=perfiles_count.index, autopct='%1.1f%%', colors=colors)
            ax1.set_title('Distribución de Perfiles de Acciones', fontweight='bold')
        
        # 2. Oportunidades por sector (arriba centro)
        ax2 = plt.subplot(3, 3, 2)
        if self.df_oportunidades is not None and self.df_acciones is not None:
            try:
                df_merged = pd.merge(self.df_oportunidades, self.df_acciones, 
                                   left_on='ticker', right_on='NEMOTECNICO', how='left')
                if 'INDUSTRIA' in df_merged.columns:
                    sector_count = df_merged['INDUSTRIA'].value_counts()
                    sector_count.plot(kind='bar', ax=ax2, color='#FFA07A')
                    ax2.set_title('Oportunidades por Sector', fontweight='bold')
                    ax2.tick_params(axis='x', rotation=45)
            except:
                ax2.text(0.5, 0.5, 'Sin datos de oportunidades', ha='center', va='center', transform=ax2.transAxes)
        
        # 3. RSI promedio por ticker (arriba derecha)
        ax3 = plt.subplot(3, 3, 3)
        if self.df_tecnico is not None and 'rsi' in self.df_tecnico.columns:
            rsi_promedio = self.df_tecnico.groupby('ticker')['rsi'].mean().sort_values(ascending=False)
            rsi_promedio.head(8).plot(kind='barh', ax=ax3, color='#98D8C8')
            ax3.set_title('RSI Promedio por Ticker (Top 8)', fontweight='bold')
        
        # 4. Salud financiera (centro izquierda)
        ax4 = plt.subplot(3, 3, 4)
        if self.df_fundamental is not None and 'salud_financiera' in self.df_fundamental.columns:
            salud_count = self.df_fundamental['salud_financiera'].value_counts()
            colors = ['#90EE90', '#FFD700', '#FF6B6B']
            salud_count.plot(kind='bar', ax=ax4, color=colors)
            ax4.set_title('Distribución de Salud Financiera', fontweight='bold')
            ax4.tick_params(axis='x', rotation=45)
        
        # 5. Evolución del ROE (centro)
        ax5 = plt.subplot(3, 3, 5)
        if self.df_fundamental is not None and 'roe' in self.df_fundamental.columns:
            roe_evolucion = self.df_fundamental.groupby('year')['roe'].mean()
            roe_evolucion.plot(kind='line', ax=ax5, marker='o', color='#FF6B6B', linewidth=2)
            ax5.set_title('Evolución del ROE Promedio', fontweight='bold')
            ax5.set_ylabel('ROE Promedio')
            ax5.grid(True, alpha=0.3)
        
        # 6. Volatilidad por ticker (centro derecha)
        ax6 = plt.subplot(3, 3, 6)
        if self.df_tecnico is not None and 'close' in self.df_tecnico.columns:
            volatilidad = self.df_tecnico.groupby('ticker')['close'].agg(lambda x: x.pct_change().std() * np.sqrt(252))
            volatilidad.sort_values(ascending=False).head(8).plot(kind='barh', ax=ax6, color='#FFB6C1')
            ax6.set_title('Volatilidad Anualizada (Top 8)', fontweight='bold')
        
        # 7. Distribución de sectores (abajo izquierda)
        ax7 = plt.subplot(3, 3, 7)
        if self.df_acciones is not None:
            sector_dist = self.df_acciones['INDUSTRIA'].value_counts()
            sector_dist.plot(kind='bar', ax=ax7, color='#DDA0DD')
            ax7.set_title('Distribución de Sectores', fontweight='bold')
            ax7.tick_params(axis='x', rotation=45)
        
        # 8. Correlación entre indicadores (abajo centro)
        ax8 = plt.subplot(3, 3, 8)
        if self.df_tecnico is not None:
            try:
                indicadores = ['rsi', 'close', 'volume']
                columnas_validas = [col for col in indicadores if col in self.df_tecnico.columns]
                if len(columnas_validas) >= 2:
                    df_corr = self.df_tecnico[columnas_validas].corr()
                    sns.heatmap(df_corr, annot=True, cmap='coolwarm', ax=ax8, fmt='.2f')
                    ax8.set_title('Correlación entre Indicadores', fontweight='bold')
            except:
                ax8.text(0.5, 0.5, 'Sin datos de correlación', ha='center', va='center', transform=ax8.transAxes)
        
        # 9. Resumen de oportunidades (abajo derecha)
        ax9 = plt.subplot(3, 3, 9)
        if self.df_oportunidades is not None:
            try:
                if 'rsi' in self.df_oportunidades.columns:
                    ax9.hist(self.df_oportunidades['rsi'], bins=10, color='#87CEEB', alpha=0.7)
                    ax9.set_title('Distribución de RSI en Oportunidades', fontweight='bold')
                    ax9.set_xlabel('RSI')
                    ax9.set_ylabel('Frecuencia')
                else:
                    ax9.text(0.5, 0.5, 'Sin datos de RSI', ha='center', va='center', transform=ax9.transAxes)
            except:
                ax9.text(0.5, 0.5, 'Sin datos de oportunidades', ha='center', va='center', transform=ax9.transAxes)
        
        plt.tight_layout()
        plt.savefig('dashboard_completo_agente_condor.png', dpi=300, bbox_inches='tight')
        print("✓ Dashboard guardado como 'dashboard_completo_agente_condor.png'")
        
        return fig
    
    def analizar_ticker_especifico(self, ticker):
        """Analiza un ticker específico en detalle"""
        print(f"\n🔍 ANÁLISIS DETALLADO DEL TICKER: {ticker}")
        print("="*50)
        
        # Información básica
        if self.df_acciones is not None:
            info_accion = self.df_acciones[self.df_acciones['NEMOTECNICO'] == ticker]
            if not info_accion.empty:
                print(f"Razón Social: {info_accion.iloc[0]['RAZON_SOCIAL']}")
                print(f"Sector: {info_accion.iloc[0]['INDUSTRIA']}")
        
        # Datos técnicos
        if self.df_tecnico is not None:
            df_ticker = self.df_tecnico[self.df_tecnico['ticker'] == ticker]
            if not df_ticker.empty:
                print(f"\n📊 DATOS TÉCNICOS:")
                print(f"   Registros: {len(df_ticker)}")
                print(f"   Período: {df_ticker['date'].min()} a {df_ticker['date'].max()}")
                
                # Últimos valores
                ultimo = df_ticker.iloc[-1]
                print(f"   Precio actual: ${ultimo.get('close', 'N/A'):,.2f}")
                print(f"   RSI: {ultimo.get('rsi', 'N/A'):.2f}")
                print(f"   Volumen: {ultimo.get('volume', 'N/A'):,}")
        
        # Datos fundamentales
        if self.df_fundamental is not None:
            df_fund = self.df_fundamental[self.df_fundamental['ticker'] == ticker]
            if not df_fund.empty:
                print(f"\n💰 DATOS FUNDAMENTALES:")
                ultimo_fund = df_fund.iloc[-1]
                print(f"   Año: {ultimo_fund['year']}")
                print(f"   P/E Ratio: {ultimo_fund.get('pe_ratio', 'N/A'):.2f}")
                print(f"   ROE: {ultimo_fund.get('roe', 'N/A'):.3f}")
                print(f"   Salud Financiera: {ultimo_fund.get('salud_financiera', 'N/A')}")
        
        # Perfil
        if self.df_perfiles is not None:
            perfil = self.df_perfiles[self.df_perfiles['ticker'] == ticker]
            if not perfil.empty:
                print(f"\n🎭 PERFIL:")
                print(f"   Personalidad: {perfil.iloc[0].get('personalidad', 'N/A')}")
        
        # Oportunidades
        if self.df_oportunidades is not None:
            oportunidades = self.df_oportunidades[self.df_oportunidades['ticker'] == ticker]
            if not oportunidades.empty:
                print(f"\n🎯 OPORTUNIDADES:")
                print(f"   Oportunidades detectadas: {len(oportunidades)}")
                for _, op in oportunidades.iterrows():
                    print(f"   - Fecha: {op.get('date', 'N/A')}, RSI: {op.get('rsi', 'N/A'):.2f}")
    
    def mostrar_menu_interactivo(self):
        """Muestra un menú interactivo para explorar los datos"""
        while True:
            print("\n" + "="*60)
            print("🎯 MENÚ INTERACTIVO - AGENTE CÓNDOR ANDINO")
            print("="*60)
            print("1. 📊 Mostrar resumen general")
            print("2. 🎨 Generar dashboard completo")
            print("3. 🔍 Analizar ticker específico")
            print("4. 📈 Ver top 10 acciones por RSI")
            print("5. 💰 Ver top 10 acciones por ROE")
            print("6. 🎭 Ver distribución de perfiles")
            print("7. 🎯 Ver oportunidades detectadas")
            print("8. 💾 Guardar todas las visualizaciones")
            print("0. 🚪 Salir")
            
            opcion = input("\nSelecciona una opción (0-8): ").strip()
            
            if opcion == "1":
                self.mostrar_resumen_general()
            
            elif opcion == "2":
                self.crear_dashboard_completo()
            
            elif opcion == "3":
                if self.df_acciones is not None:
                    tickers_disponibles = self.df_acciones['NEMOTECNICO'].tolist()
                    print(f"\nTickers disponibles: {', '.join(tickers_disponibles[:10])}...")
                    ticker = input("Ingresa el ticker a analizar: ").strip().upper()
                    if ticker in tickers_disponibles:
                        self.analizar_ticker_especifico(ticker)
                    else:
                        print("❌ Ticker no encontrado")
                else:
                    print("❌ No hay datos de acciones disponibles")
            
            elif opcion == "4":
                if self.df_tecnico is not None and 'rsi' in self.df_tecnico.columns:
                    rsi_promedio = self.df_tecnico.groupby('ticker')['rsi'].mean().sort_values(ascending=False)
                    print("\n📈 TOP 10 ACCIONES POR RSI PROMEDIO:")
                    print(rsi_promedio.head(10).to_string())
                else:
                    print("❌ No hay datos técnicos disponibles")
            
            elif opcion == "5":
                if self.df_fundamental is not None and 'roe' in self.df_fundamental.columns:
                    roe_ultimo = self.df_fundamental.groupby('ticker')['roe'].last().sort_values(ascending=False)
                    print("\n💰 TOP 10 ACCIONES POR ROE (ÚLTIMO AÑO):")
                    print(roe_ultimo.head(10).to_string())
                else:
                    print("❌ No hay datos fundamentales disponibles")
            
            elif opcion == "6":
                if self.df_perfiles is not None and 'personalidad' in self.df_perfiles.columns:
                    perfiles = self.df_perfiles['personalidad'].value_counts()
                    print("\n🎭 DISTRIBUCIÓN DE PERFILES:")
                    for perfil, count in perfiles.items():
                        print(f"   {perfil}: {count} acciones")
                else:
                    print("❌ No hay datos de perfiles disponibles")
            
            elif opcion == "7":
                if self.df_oportunidades is not None:
                    print(f"\n🎯 OPORTUNIDADES DETECTADAS: {len(self.df_oportunidades)}")
                    if not self.df_oportunidades.empty:
                        cols = ['date', 'ticker', 'rsi', 'close']
                        cols_disponibles = [col for col in cols if col in self.df_oportunidades.columns]
                        print(self.df_oportunidades[cols_disponibles].head(10).to_string())
                else:
                    print("❌ No hay oportunidades detectadas")
            
            elif opcion == "8":
                print("\n💾 Guardando todas las visualizaciones...")
                self.crear_dashboard_completo()
                print("✓ Visualizaciones guardadas")
            
            elif opcion == "0":
                print("\n👋 ¡Hasta luego! Gracias por usar el Agente Cóndor Andino")
                break
            
            else:
                print("❌ Opción no válida. Intenta de nuevo.")

def main():
    """Función principal del visualizador"""
    print("🎨 VISUALIZADOR INTERACTIVO - AGENTE CÓNDOR ANDINO")
    print("="*60)
    
    try:
        visualizador = VisualizadorCondor()
        visualizador.mostrar_menu_interactivo()
    except Exception as e:
        print(f"❌ Error en el visualizador: {e}")
        print("💡 Asegúrate de haber ejecutado primero el orquestador principal")

if __name__ == "__main__":
    main()
