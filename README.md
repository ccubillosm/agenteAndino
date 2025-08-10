# 🦅 Agente Cóndor Andino - Análisis Bursátil Inteligente

Un sistema completo de análisis bursátil para el mercado chileno que combina análisis técnico, fundamental y machine learning para identificar oportunidades de inversión.

## 🎯 Características Principales

- **Descarga automática** de datos históricos de acciones chilenas
- **Cálculo masivo** de más de 80 indicadores técnicos
- **Análisis fundamental** con ratios financieros clave
- **Clustering inteligente** para clasificar acciones por comportamiento
- **Detección automática** de oportunidades de divergencia
- **Visualizaciones interactivas** y dashboards completos

## 🏗️ Arquitectura del Sistema

El proyecto está organizado en 5 etapas principales:

### Etapa 1: Descarga de Datos
- **Script**: `Backend_python/descargar_acciones.py`
- **Entrada**: `CSV/acciones.csv` (lista de tickers)
- **Salida**: `acciones_master.csv` (datos OHLCV históricos)
- **Fuente**: Yahoo Finance

### Etapa 2: Enriquecimiento Técnico
- **Script**: `Backend_python/motor_condor.py`
- **Entrada**: `acciones_master.csv`
- **Salida**: `database_maestra_tecnica.csv`
- **Proceso**: Cálculo de indicadores técnicos (RSI, MACD, Bollinger Bands, etc.)

### Etapa 3: Verificación de Datos Fundamentales
- **Script**: `Backend_python/orquestador_principal.py` (verificación automática)
- **Entrada**: `CSV/fundamental.csv` (archivo existente)
- **Salida**: Verificación de integridad del archivo
- **Proceso**: Validación de datos fundamentales pre-existentes (no se regeneran)

### Etapa 4: Perfilamiento y Clustering
- **Script**: `Backend_python/generar_perfiles_de_acciones.py`
- **Entrada**: Datos técnicos y fundamentales
- **Salida**: `acciones_con_perfil.csv`
- **Proceso**: Clasificación automática en 3 perfiles de comportamiento

### Etapa 5: Fusión Estratégica
- **Script**: `Backend_python/analisis_fusion.py`
- **Entrada**: Todos los datos anteriores
- **Salida**: `oportunidades_de_divergencia.csv`
- **Proceso**: Detección de oportunidades combinando análisis técnico y fundamental

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Instalar todas las dependencias del proyecto
pip3 install -r requirements.txt

# Si hay problemas de compatibilidad, instalar versiones específicas
pip3 install "numpy<2.0.0"
pip3 install pandas-ta==0.3.14b
```

### 2. Verificar Estructura de Archivos

```
AgenteAndino/
├── config.py                          # Configuración centralizada
├── requirements.txt                   # Dependencias Python
├── CSV/
│   ├── acciones.csv                  # Lista de tickers chilenos
│   └── fundamental.csv               # Datos fundamentales
├── Backend_python/
│   ├── orquestador_principal.py      # Script principal de ejecución
│   ├── visualizador_interactivo.py   # Visualizaciones interactivas
│   ├── descargar_acciones.py         # Descarga de datos
│   ├── motor_condor.py               # Cálculo de indicadores
│   ├── generar_db_fundamental.py     # Análisis fundamental
│   ├── generar_perfiles_de_acciones.py # Clustering
│   └── analisis_fusion.py            # Fusión de análisis
├── output/                            # Directorio de archivos generados
│   ├── .gitignore                    # Configuración Git para archivos de salida
│   ├── *.csv                         # Archivos de datos generados
│   └── *.png                         # Visualizaciones generadas
└── README.md                         # Este archivo
```

## 📊 Uso del Sistema

### 🎯 **Ejecución Automática Completa (Recomendado)**

Para ejecutar todo el flujo de trabajo de una vez desde el directorio raíz:

```bash
# Navegar al directorio del proyecto
cd /Users/acidlabs/Desktop/escritorio/AgenteAndino

# Ejecutar todo el pipeline automáticamente
/usr/local/bin/python3 Backend_python/orquestador_principal.py
```

**Este comando ejecuta automáticamente todas las etapas:**
1. ✅ **Etapa 1**: Descarga de datos históricos (Yahoo Finance)
2. ✅ **Etapa 2**: Enriquecimiento técnico (indicadores)
3. ✅ **Etapa 3**: Análisis fundamental
4. ✅ **Etapa 4**: Perfilamiento y clustering
5. ✅ **Etapa 5**: Identificación de oportunidades

### 🔄 **Ejecución Individual por Etapas (Opcional)**

Si prefieres ejecutar cada etapa por separado para mayor control:

Este script ejecutará automáticamente todas las etapas y generará:
- Archivos CSV con todos los análisis
- Visualización general (`resumen_general_agente_condor.png`)
- Resumen ejecutivo en consola

### Visualización Interactiva

Para explorar los resultados de forma interactiva:

```bash
cd Backend_python
python visualizador_interactivo.py
```

**Opciones disponibles:**
1. 📊 Mostrar resumen general
2. 🎨 Generar dashboard completo
3. 🔍 Analizar ticker específico
4. 📈 Ver top 10 acciones por RSI
5. 💰 Ver top 10 acciones por ROE
6. 🎭 Ver distribución de perfiles
7. 🎯 Ver oportunidades detectadas
8. 💾 Guardar todas las visualizaciones

```bash
# Etapa 1: Descarga de datos históricos
/usr/local/bin/python3 Backend_python/descargar_acciones.py

# Etapa 2: Enriquecimiento técnico (indicadores)
/usr/local/bin/python3 Backend_python/motor_condor.py

# Etapa 3: Análisis fundamental
/usr/local/bin/python3 Backend_python/generar_db_fundamental.py

# Etapa 4: Perfilamiento y clustering
/usr/local/bin/python3 Backend_python/generar_perfiles_de_acciones.py

# Etapa 5: Fusión estratégica
/usr/local/bin/python3 Backend_python/analisis_fusion.py
```

### 📁 **Verificación de Resultados**

Después de la ejecución, puedes verificar los archivos generados:

```bash
# Ver archivos generados
ls -la *.csv
ls -la CSV/*.csv

# Verificar el archivo principal de datos técnicos
head -5 database_maestra_tecnica.csv

# Verificar perfiles generados
head -5 acciones_con_perfil.csv
```

## 🚀 **INSTRUCCIONES COMPLETAS DE EJECUCIÓN**

### **Paso 1: Preparación del Entorno**
```bash
# Navegar al directorio del proyecto
cd /Users/acidlabs/Desktop/escritorio/AgenteAndino

# Instalar dependencias (si no están instaladas)
pip3 install -r requirements.txt
```

### **Paso 2: Ejecución del Pipeline Completo (Recomendado)**
```bash
# Ejecutar todo el pipeline desde el directorio raíz
/usr/local/bin/python3 Backend_python/orquestador_principal.py
```

### **Paso 3: Verificación de Resultados**
```bash
# Ver archivos generados
ls -la *.csv
ls -la CSV/*.csv

# Verificar el archivo principal de datos técnicos
head -5 database_maestra_tecnica.csv

# Verificar perfiles generados
head -5 acciones_con_perfil.csv
```

### **⚠️ Notas Importantes**

1. **Directorio de Ejecución**: Siempre ejecuta desde el directorio raíz del proyecto (`/Users/acidlabs/Desktop/escritorio/AgenteAndino`)

2. **Formato Chileno**: El sistema respeta automáticamente el formato local:
   - **Coma (,) como separador decimal**: `1234,56`
   - **Punto (;) como separador de campos**: `fecha;valor;ticker`

3. **Python Version**: Usa `/usr/local/bin/python3` para asegurar compatibilidad

4. **Dependencias**: Si hay errores, reinstala: `pip3 install -r requirements.txt`

### **🎯 Resultado Esperado**

Al finalizar tendrás:
- **`acciones_master.csv`**: Datos históricos OHLCV (37,746 registros, 27 tickers)
- **`database_maestra_tecnica.csv`**: Datos + indicadores técnicos (41 columnas)
- **`CSV/fundamental.csv`**: Análisis fundamental
- **`acciones_con_perfil.csv`**: Perfiles y clusters de acciones
- **`oportunidades_de_divergencia.csv`**: Oportunidades identificadas

### **🚨 Solución de Problemas Comunes**

```bash
# Si hay error de módulos
pip3 install pandas pandas-ta yfinance scikit-learn matplotlib seaborn

# Si hay problemas de compatibilidad
pip3 install "numpy<2.0.0"
pip3 install pandas-ta==0.3.14b

# Si hay problemas de permisos
chmod +x Backend_python/*.py
```

## 📈 Interpretación de Resultados

### Perfiles de Acciones

El sistema clasifica las acciones en 3 perfiles:

1. **🚀 Cohete de Tendencia**: Acciones con fuerte tendencia y alta volatilidad
2. **🐢 Tortuga de Valor (Rango)**: Acciones estables con bajo riesgo
3. **🤔 Indeciso (En Transición)**: Acciones en cambio de comportamiento

### Indicadores Técnicos Calculados

- **Tendencias**: SMA (5, 20, 50, 200), EMA (9, 12, 26)
- **Momentum**: RSI, MACD, Estocástico, CCI
- **Volatilidad**: Bandas de Bollinger, ATR
- **Volumen**: OBV, AD, Volumen normalizado
- **Tendencia**: ADX, Parabolic SAR, Ichimoku

### Oportunidades Detectadas

El sistema identifica acciones que cumplen:
- **RSI < 30** (sobreventa técnica)
- **Salud financiera = "Alta"** (fundamentos sólidos)
- **Divergencia** entre análisis técnico y fundamental

## 🔧 Configuración Avanzada

### Modificar Configuración

Edita `config.py` para personalizar:

```python
# Cambiar período de análisis
FECHA_INICIO = "2018-01-01"

# Modificar número de clusters
NUMERO_DE_CLUSTERS = 4

# Cambiar sufijo de Yahoo Finance
YF_SANTIAGO_SUFFIX = '.SN'
```

### Agregar Nuevas Acciones

Edita `CSV/acciones.csv` para incluir nuevos tickers:

```csv
NEMOTECNICO,RAZON_SOCIAL,INDUSTRIA
NUEVO,EMPRESA NUEVA S.A.,Nuevo Sector
```

### Personalizar Indicadores Técnicos

Modifica `Backend_python/motor_condor.py` para agregar/quitar indicadores.

### **🇨🇱 Configuración del Formato Chileno**

El sistema está configurado para respetar automáticamente el formato local chileno:

- **Separador decimal**: Coma (,) - `1234,56`
- **Separador de campos**: Punto y coma (;) - `fecha;valor;ticker`
- **Formato de fecha**: DD/MM/YYYY - `02/01/2020`

**No es necesario modificar nada** - el sistema detecta y mantiene automáticamente este formato en todos los archivos CSV generados.

## 📁 Organización del Directorio Output

El sistema organiza automáticamente todos los archivos generados en el directorio `output/` para mantener el proyecto ordenado:

```
output/
├── .gitignore                    # Configuración Git para archivos de salida
├── *.csv                         # Archivos de datos generados
└── *.png                         # Visualizaciones generadas
```

**Ventajas de esta organización:**
- ✅ **Orden**: Todos los archivos generados en un solo lugar
- ✅ **Limpieza**: El directorio raíz se mantiene limpio
- ✅ **Control de versiones**: Archivos de salida no se suben al repositorio
- ✅ **Fácil respaldo**: Un solo directorio para respaldar resultados

## 📊 Archivos de Salida

### Archivos CSV Generados

Todos los archivos CSV se guardan en el directorio `output/`:

- `output/acciones_master.csv`: Datos históricos OHLCV
- `output/database_maestra_tecnica.csv`: Indicadores técnicos calculados
- `CSV/fundamental.csv`: Datos fundamentales pre-existentes (no se regeneran)
- `output/acciones_con_perfil.csv`: Clasificación por perfiles
- `output/oportunidades_de_divergencia.csv`: Oportunidades detectadas

### Visualizaciones Generadas

Todas las visualizaciones se guardan en el directorio `output/`:

- `output/resumen_general_agente_condor.png`: Vista general del sistema
- `output/dashboard_completo_agente_condor.png`: Dashboard completo con 9 gráficos

## 🚨 Solución de Problemas

### Error de Dependencias

```bash
# Actualizar dependencias
pip3 install --upgrade pandas pandas-ta yfinance matplotlib seaborn scikit-learn

# Si hay problemas de compatibilidad
pip3 install "numpy<2.0.0"
pip3 install pandas-ta==0.3.14b
```

### Error de Configuración

Verifica que `config.py` esté en la raíz del proyecto y que las rutas sean correctas.

### Error de Descarga de Datos

- Verifica conexión a internet
- Algunos tickers pueden no estar disponibles en Yahoo Finance
- Revisa el formato de fechas en `config.py`

### Error de Memoria

Para datasets grandes, considera procesar por lotes o reducir el período de análisis.

## 📚 Recursos Adicionales

### Bibliotecas Utilizadas

- **pandas**: Manipulación de datos
- **pandas-ta**: Indicadores técnicos
- **yfinance**: Descarga de datos financieros
- **scikit-learn**: Clustering y machine learning
- **matplotlib/seaborn**: Visualizaciones

### Conceptos Financieros

- **RSI**: Índice de Fuerza Relativa (sobrecompra/sobreventa)
- **MACD**: Convergencia/Divergencia de Medias Móviles
- **ROE**: Retorno sobre el Patrimonio
- **P/E Ratio**: Ratio Precio/Beneficio

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:

- Revisa la documentación en este README
- Verifica los logs de error en consola
- Consulta las instrucciones detalladas en `instrucciones.txt`

---

## 🎯 **RESUMEN RÁPIDO DE EJECUCIÓN**

```bash
# 1. Navegar al proyecto
cd /Users/acidlabs/Desktop/escritorio/AgenteAndino

# 2. Ejecutar todo el pipeline
/usr/local/bin/python3 Backend_python/orquestador_principal.py

# 3. Verificar resultados
ls -la output/*.csv
head -5 output/database_maestra_tecnica.csv
```

**🚀 ¡Disfruta analizando el mercado chileno con el Agente Cóndor Andino! 🚀**
