# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-10

### Agregado
- **Sistema completo de análisis bursátil** para el mercado chileno
- **Descarga automática** de datos históricos de acciones chilenas usando Yahoo Finance
- **Cálculo masivo** de más de 80 indicadores técnicos (RSI, MACD, Bollinger Bands, etc.)
- **Análisis fundamental** con ratios financieros clave (ROE, P/E, P/B, etc.)
- **Clustering inteligente** para clasificar acciones en 3 perfiles de comportamiento
- **Detección automática** de oportunidades de divergencia técnica-fundamental
- **Visualizaciones interactivas** y dashboards completos
- **Sistema de orquestación** que ejecuta automáticamente todas las etapas
- **Configuración centralizada** para fácil mantenimiento
- **Organización automática** de archivos en directorio `output/`

### Características Técnicas
- **5 etapas principales** de análisis automatizado
- **Formato chileno** respetado (comma decimal, punto y coma separador)
- **Manejo robusto** de errores y excepciones
- **Logging detallado** de todas las operaciones
- **Arquitectura modular** para fácil extensión
- **Compatibilidad** con Python 3.8+

### Archivos Principales
- `orquestador_principal.py` - Script principal de ejecución
- `motor_condor.py` - Motor de cálculo de indicadores técnicos
- `descargar_acciones.py` - Descarga de datos históricos
- `generar_perfiles_de_acciones.py` - Clustering y perfilamiento
- `analisis_fusion.py` - Detección de oportunidades
- `config.py` - Configuración centralizada

### Datos de Entrada
- `CSV/acciones.csv` - Lista de tickers chilenos del IPSA
- `CSV/fundamental.csv` - Datos fundamentales pre-existentes

### Datos de Salida
- `output/acciones_master.csv` - Datos históricos OHLCV
- `output/database_maestra_tecnica.csv` - Indicadores técnicos calculados
- `output/acciones_con_perfil.csv` - Clasificación por perfiles
- `output/oportunidades_de_divergencia.csv` - Oportunidades detectadas
- `output/resumen_general_agente_condor.png` - Dashboard general

### Dependencias Principales
- pandas, numpy - Manipulación de datos
- pandas-ta - Indicadores técnicos
- yfinance - Descarga de datos financieros
- scikit-learn - Clustering y machine learning
- matplotlib, seaborn - Visualizaciones

---

## [Unreleased]

### Planificado
- Interfaz web para visualización de resultados
- API REST para consultas programáticas
- Alertas automáticas por email/SMS
- Análisis de sentimiento de noticias
- Backtesting de estrategias
- Integración con brokers chilenos
