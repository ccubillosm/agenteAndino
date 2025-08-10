#!/usr/bin/env python3
"""
Orquestador Principal del Proyecto Agente Cóndor Andino
Ejecuta todo el flujo de trabajo de análisis bursátil de forma secuencial
"""

import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Agregar la raíz del proyecto al path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import config

def ejecutar_etapa_1_descarga():
    """Etapa 1: Descarga de datos de acciones chilenas"""
    print("\n" + "="*60)
    print("ETAPA 1: DESCARGA DE DATOS DE ACCIONES CHILENAS")
    print("="*60)
    
    try:
        from Backend_python.descargar_acciones import main as descargar_acciones
        descargar_acciones()
        
        if os.path.exists(config.ARCHIVO_ACCIONES_MASTER):
            df = pd.read_csv(config.ARCHIVO_ACCIONES_MASTER, sep=';', decimal=',')
            print(f"✓ Datos descargados exitosamente: {len(df)} registros")
            return True
        else:
            print("✗ Error: No se generó el archivo de acciones master")
            return False
    except Exception as e:
        print(f"✗ Error en descarga de acciones: {e}")
        return False

def ejecutar_etapa_2_enriquecimiento():
    """Etapa 2: Enriquecimiento técnico con indicadores"""
    print("\n" + "="*60)
    print("ETAPA 2: ENRIQUECIMIENTO TÉCNICO")
    print("="*60)
    
    try:
        from Backend_python.motor_condor import main as motor_condor
        motor_condor()
        
        if os.path.exists(config.ARCHIVO_TECNICO):
            df = pd.read_csv(config.ARCHIVO_TECNICO, sep=';', decimal=',')
            print(f"✓ Indicadores técnicos calculados: {len(df)} registros")
            return True
        else:
            print("✗ Error: No se generó el archivo técnico")
            return False
    except Exception as e:
        print(f"✗ Error en enriquecimiento técnico: {e}")
        return False

def ejecutar_etapa_3_fundamental():
    """Etapa 3: Verificación de datos fundamentales existentes"""
    print("\n" + "="*60)
    print("ETAPA 3: VERIFICACIÓN DE DATOS FUNDAMENTALES")
    print("="*60)
    
    try:
        # Verificar que existe el archivo fundamental.csv
        if os.path.exists(config.CSV_FUNDAMENTAL):
            df = pd.read_csv(config.CSV_FUNDAMENTAL, sep=';', decimal=',')
            print(f"✓ Datos fundamentales verificados: {len(df)} registros")
            print(f"   Archivo: {config.CSV_FUNDAMENTAL}")
            return True
        else:
            print("✗ Error: No se encontró el archivo fundamental.csv")
            return False
    except Exception as e:
        print(f"✗ Error en verificación de datos fundamentales: {e}")
        return False

def ejecutar_etapa_4_perfilamiento():
    """Etapa 4: Perfilamiento y clustering"""
    print("\n" + "="*60)
    print("ETAPA 4: PERFILAMIENTO Y CLUSTERING")
    print("="*60)
    
    try:
        from Backend_python.generar_perfiles_de_acciones import main as generar_perfiles
        generar_perfiles()
        
        if os.path.exists(config.ARCHIVO_PERFILES):
            df = pd.read_csv(config.ARCHIVO_PERFILES, sep=';', decimal=',')
            print(f"✓ Perfiles generados: {len(df)} acciones")
            return True
        else:
            print("✗ Error: No se generaron los perfiles")
            return False
    except Exception as e:
        print(f"✗ Error en perfilamiento: {e}")
        return False

def ejecutar_etapa_5_fusion():
    """Etapa 5: Fusión estratégica y detección de oportunidades"""
    print("\n" + "="*60)
    print("ETAPA 5: FUSIÓN ESTRATÉGICA")
    print("="*60)
    
    try:
        from Backend_python.analisis_fusion import main as analisis_fusion
        analisis_fusion()
        
        if os.path.exists(config.ARCHIVO_OPORTUNIDADES):
            df = pd.read_csv(config.ARCHIVO_OPORTUNIDADES, sep=';', decimal=',')
            print(f"✓ Oportunidades detectadas: {len(df)} registros")
            return True
        else:
            print("✗ Error: No se generó el archivo de oportunidades")
            return False
    except Exception as e:
        print(f"✗ Error en fusión estratégica: {e}")
        return False

def generar_resumen_ejecutivo():
    """Genera un resumen ejecutivo de todos los resultados"""
    print("\n" + "="*60)
    print("RESUMEN EJECUTIVO")
    print("="*60)
    
    archivos_generados = []
    
    # Verificar archivos generados
    archivos_a_verificar = [
        (config.ARCHIVO_ACCIONES_MASTER, "Datos de acciones"),
        (config.ARCHIVO_TECNICO, "Indicadores técnicos"),
        (config.ARCHIVO_FUNDAMENTAL_DB, "Datos fundamentales"),
        (config.ARCHIVO_PERFILES, "Perfiles de acciones"),
        (config.ARCHIVO_OPORTUNIDADES, "Oportunidades detectadas")
    ]
    
    for archivo, descripcion in archivos_a_verificar:
        if os.path.exists(archivo):
            try:
                df = pd.read_csv(archivo, sep=';', decimal=',')
                print(f"✓ {descripcion}: {archivo} ({len(df)} registros)")
                archivos_generados.append(archivo)
            except Exception as e:
                print(f"✗ {descripcion}: {archivo} (error al leer: {e})")
        else:
            print(f"✗ {descripcion}: {archivo} (no encontrado)")
    
    return archivos_generados

def crear_visualizacion_general():
    """Crea una visualización general de los resultados"""
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIÓN GENERAL")
    print("="*60)
    
    try:
        # Crear figura con subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Resumen General - Agente Cóndor Andino', fontsize=16, fontweight='bold')
        
        # 1. Distribución de perfiles de acciones
        if os.path.exists(config.ARCHIVO_PERFILES):
            df_perfiles = pd.read_csv(config.ARCHIVO_PERFILES, sep=';', decimal=',')
            if 'personalidad' in df_perfiles.columns:
                perfiles_count = df_perfiles['personalidad'].value_counts()
                axes[0, 0].pie(perfiles_count.values, labels=perfiles_count.index, autopct='%1.1f%%')
                axes[0, 0].set_title('Distribución de Perfiles de Acciones')
        
        # 2. Oportunidades por sector
        if os.path.exists(config.ARCHIVO_OPORTUNIDADES):
            df_oportunidades = pd.read_csv(config.ARCHIVO_OPORTUNIDADES, sep=';', decimal=',')
            if 'ticker' in df_oportunidades.columns:
                # Obtener sector de cada ticker
                df_acciones = pd.read_csv(config.CSV_ACCIONES)
                df_oportunidades = pd.merge(df_oportunidades, df_acciones, left_on='ticker', right_on='NEMOTECNICO', how='left')
                if 'INDUSTRIA' in df_oportunidades.columns:
                    sector_count = df_oportunidades['INDUSTRIA'].value_counts()
                    sector_count.plot(kind='bar', ax=axes[0, 1])
                    axes[0, 1].set_title('Oportunidades por Sector')
                    axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. RSI promedio por ticker (últimos datos)
        if os.path.exists(config.ARCHIVO_TECNICO):
            df_tecnico = pd.read_csv(config.ARCHIVO_TECNICO, sep=';', decimal=',')
            if 'rsi_14' in df_tecnico.columns and 'ticker' in df_tecnico.columns:
                rsi_promedio = df_tecnico.groupby('ticker')['rsi_14'].mean().sort_values(ascending=False)
                rsi_promedio.head(10).plot(kind='bar', ax=axes[1, 0])
                axes[1, 0].set_title('RSI Promedio por Ticker (Top 10)')
                axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Salud financiera de las acciones
        if os.path.exists(config.CSV_FUNDAMENTAL):
            df_fundamental = pd.read_csv(config.CSV_FUNDAMENTAL, sep=';', decimal=',')
            if 'salud_financiera' in df_fundamental.columns:
                salud_count = df_fundamental['salud_financiera'].value_counts()
                salud_count.plot(kind='bar', ax=axes[1, 1], color=['green', 'orange', 'red'])
                axes[1, 1].set_title('Distribución de Salud Financiera')
                axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('output/resumen_general_agente_condor.png', dpi=300, bbox_inches='tight')
        print("✓ Visualización guardada como 'output/resumen_general_agente_condor.png'")
        
    except Exception as e:
        print(f"✗ Error al generar visualización: {e}")

def main():
    """Función principal que ejecuta todo el flujo de trabajo"""
    print("🚀 INICIANDO AGENTE CÓNDOR ANDINO - ANÁLISIS BURSÁTIL COMPLETO")
    print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    inicio_tiempo = time.time()
    
    # Ejecutar todas las etapas
    etapas = [
        ("Descarga de datos", ejecutar_etapa_1_descarga),
        ("Enriquecimiento técnico", ejecutar_etapa_2_enriquecimiento),
        ("Verificación de datos fundamentales", ejecutar_etapa_3_fundamental),
        ("Perfilamiento", ejecutar_etapa_4_perfilamiento),
        ("Fusión estratégica", ejecutar_etapa_5_fusion)
    ]
    
    etapas_exitosas = 0
    for nombre, funcion in etapas:
        try:
            if funcion():
                etapas_exitosas += 1
            time.sleep(1)  # Pausa entre etapas
        except Exception as e:
            print(f"✗ Error crítico en {nombre}: {e}")
    
    # Generar resumen y visualización
    archivos_generados = generar_resumen_ejecutivo()
    crear_visualizacion_general()
    
    tiempo_total = time.time() - inicio_tiempo
    
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"✓ Etapas completadas exitosamente: {etapas_exitosas}/{len(etapas)}")
    print(f"✓ Archivos generados: {len(archivos_generados)}")
    print(f"⏱️  Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    
    if etapas_exitosas == len(etapas):
        print("\n🎉 ¡PROCESO COMPLETADO CON ÉXITO!")
        print("📊 Todos los análisis han sido generados correctamente.")
        print("🔍 Revisa los archivos CSV generados y la visualización PNG.")
    else:
        print(f"\n⚠️  PROCESO COMPLETADO CON ADVERTENCIAS")
        print(f"   {len(etapas) - etapas_exitosas} etapas fallaron.")

if __name__ == "__main__":
    main()
