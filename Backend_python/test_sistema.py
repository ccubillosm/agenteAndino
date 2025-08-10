#!/usr/bin/env python3
"""
Script de Prueba del Sistema Agente Cóndor Andino
Verifica que todos los componentes estén funcionando correctamente
"""

import os
import sys
import importlib
import pandas as pd

# Agregar la raíz del proyecto al path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

def test_imports():
    """Prueba que todas las dependencias se puedan importar"""
    print("🔍 Probando importaciones...")
    
    dependencias = [
        'pandas',
        'numpy', 
        'pandas_ta',
        'yfinance',
        'matplotlib',
        'seaborn',
        'sklearn'
    ]
    
    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"  ✓ {dep}")
        except ImportError as e:
            print(f"  ✗ {dep}: {e}")
            return False
    
    return True

def test_archivos_entrada():
    """Prueba que los archivos de entrada existan"""
    print("\n📁 Probando archivos de entrada...")
    
    archivos_entrada = [
        'CSV/acciones.csv',
        'CSV/fundamental.csv'
    ]
    
    for archivo in archivos_entrada:
        if os.path.exists(archivo):
            print(f"  ✓ {archivo}")
            # Verificar que se pueda leer
            try:
                df = pd.read_csv(archivo)
                print(f"    - Registros: {len(df)}")
                print(f"    - Columnas: {list(df.columns)}")
            except Exception as e:
                print(f"    ✗ Error al leer: {e}")
                return False
        else:
            print(f"  ✗ {archivo} (no encontrado)")
            return False
    
    return True

def test_config():
    """Prueba que la configuración se pueda cargar"""
    print("\n⚙️ Probando configuración...")
    
    try:
        import config
        print(f"  ✓ config.py cargado")
        print(f"  - Fecha inicio: {config.FECHA_INICIO}")
        print(f"  - Sufijo YF: {config.YF_SANTIAGO_SUFFIX}")
        print(f"  - Clusters: {config.NUMERO_DE_CLUSTERS}")
        return True
    except Exception as e:
        print(f"  ✗ Error al cargar config.py: {e}")
        return False

def test_scripts():
    """Prueba que todos los scripts se puedan importar"""
    print("\n📜 Probando scripts...")
    
    scripts = [
        'descargar_acciones',
        'motor_condor', 
        'generar_db_fundamental',
        'generar_perfiles_de_acciones',
        'analisis_fusion'
    ]
    
    for script in scripts:
        try:
            modulo = importlib.import_module(script)
            print(f"  ✓ {script}.py")
        except Exception as e:
            print(f"  ✗ {script}.py: {e}")
            return False
    
    return True

def test_funcionalidades_basicas():
    """Prueba funcionalidades básicas de pandas y numpy"""
    print("\n🧪 Probando funcionalidades básicas...")
    
    try:
        # Test pandas
        df_test = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })
        print(f"  ✓ DataFrame creado: {df_test.shape}")
        
        # Test numpy
        import numpy as np
        array_test = np.array([1, 2, 3, 4, 5])
        print(f"  ✓ Array numpy creado: {array_test.shape}")
        
        # Test pandas-ta básico
        import pandas_ta as ta
        df_test['SMA'] = ta.sma(df_test['A'], length=3)
        print(f"  ✓ Indicador técnico calculado: {df_test['SMA'].notna().sum()}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error en funcionalidades básicas: {e}")
        return False

def test_yfinance():
    """Prueba que yfinance funcione correctamente"""
    print("\n📡 Probando yfinance...")
    
    try:
        import yfinance as yf
        
        # Test con un ticker simple
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        print(f"  ✓ yfinance funcionando")
        print(f"    - Ticker de prueba: AAPL")
        print(f"    - Nombre: {info.get('longName', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error en yfinance: {e}")
        return False

def test_visualizacion():
    """Prueba que matplotlib y seaborn funcionen"""
    print("\n🎨 Probando visualización...")
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Crear un gráfico simple
        fig, ax = plt.subplots(figsize=(6, 4))
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        ax.plot(x, y, 'o-')
        ax.set_title('Test de Visualización')
        
        # Guardar y cerrar
        plt.savefig('test_visualizacion.png', dpi=100)
        plt.close()
        
        # Limpiar archivo de prueba
        if os.path.exists('test_visualizacion.png'):
            os.remove('test_visualizacion.png')
        
        print(f"  ✓ matplotlib y seaborn funcionando")
        return True
    except Exception as e:
        print(f"  ✗ Error en visualización: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA AGENTE CÓNDOR ANDINO")
    print("="*60)
    
    pruebas = [
        ("Importaciones", test_imports),
        ("Archivos de entrada", test_archivos_entrada),
        ("Configuración", test_config),
        ("Scripts", test_scripts),
        ("Funcionalidades básicas", test_funcionalidades_basicas),
        ("Yahoo Finance", test_yfinance),
        ("Visualización", test_visualizacion)
    ]
    
    resultados = []
    
    for nombre, funcion in pruebas:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"  ✗ Error crítico en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    exitosas = 0
    for nombre, resultado in resultados:
        status = "✓ PASÓ" if resultado else "✗ FALLÓ"
        print(f"{status} - {nombre}")
        if resultado:
            exitosas += 1
    
    print(f"\n🎯 Resultado: {exitosas}/{len(resultados)} pruebas exitosas")
    
    if exitosas == len(resultados):
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está listo para usar")
        print("\n💡 Para ejecutar el sistema completo:")
        print("   cd Backend_python")
        print("   python orquestador_principal.py")
    else:
        print(f"\n⚠️  {len(resultados) - exitosas} pruebas fallaron")
        print("🔧 Revisa los errores arriba y corrige los problemas")
        print("\n💡 Comandos útiles:")
        print("   pip install -r requirements.txt")
        print("   pip install --upgrade pandas pandas-ta yfinance matplotlib seaborn scikit-learn")
    
    return exitosas == len(resultados)

if __name__ == "__main__":
    main()
