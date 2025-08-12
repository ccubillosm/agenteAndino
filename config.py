# Configuración del Proyecto Agente Cóndor Andino
# Archivo de configuración centralizada

import os

# Configuración de archivos CSV
CSV_ACCIONES = 'CSV/acciones.csv'
CSV_FUNDAMENTAL = 'CSV/fundamental.csv'
ARCHIVO_FUNDAMENTAL = 'CSV/fundamental.csv'
ARCHIVO_ACCIONES_MASTER = 'output/acciones_master.csv'
ARCHIVO_TECNICO = 'output/database_maestra_tecnica.csv'
ARCHIVO_FUNDAMENTAL_DB = 'output/database_fundamental.csv'
ARCHIVO_MACRO = 'output/database_macro_expandida.csv'
ARCHIVO_PERFILES = 'output/acciones_con_perfil.csv'
ARCHIVO_OPORTUNIDADES = 'output/oportunidades_de_divergencia.csv'

# Configuración de Yahoo Finance
YF_SANTIAGO_SUFFIX = '.SN'  # Sufijo para acciones chilenas
FECHA_INICIO = "2025-04-01"

# Configuración de análisis
NUMERO_DE_CLUSTERS = 3

# Configuración de base de datos MySQL (opcional)
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'agente_condor_v2'
DB_USER = 'root'
DB_PASSWORD = ''

# Configuración de visualización
FIGURA_TAMANO = (12, 8)
DPI_FIGURA = 300
