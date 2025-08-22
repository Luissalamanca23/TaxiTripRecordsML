# NYC Yellow Taxi Trip Records - Datos Raw

## Información General

Este directorio contiene los datos originales de viajes en taxi amarillo de Nueva York desde 2009 hasta 2023, proporcionados por la Comisión de Taxis y Limusinas de NYC (TLC).

### Fuente de Datos

**Dataset Original**: [NYC Yellow Taxi Trip Records](https://www.kaggle.com/datasets/psvishnu/nyc-yellow-taxi-trip-records)  
**Proveedor**: NYC Taxi & Limousine Commission (TLC)  
**Licencia**: Open Data  
**Formato**: Archivos Parquet mensuales

## Instrucciones de Descarga

### Método 1: Descarga Manual desde Kaggle

1. **Acceder al dataset**: Visita [https://www.kaggle.com/datasets/psvishnu/nyc-yellow-taxi-trip-records](https://www.kaggle.com/datasets/psvishnu/nyc-yellow-taxi-trip-records)

2. **Crear cuenta Kaggle** (si no tienes una):
   - Regístrate en [kaggle.com](https://www.kaggle.com)
   - Verifica tu cuenta por email

3. **Descargar el dataset**:
   - Haz clic en "Download" (botón azul)
   - Se descargará `archive.zip` (~3.5 GB comprimido)

4. **Extraer los archivos**:
   ```bash
   # Mover el archivo descargado a esta carpeta
   mv ~/Downloads/archive.zip ./data/01_raw/
   
   # Descomprimir
   cd ./data/01_raw/
   unzip archive.zip
   
   # Esto creará la carpeta 'archive' con todos los archivos Parquet
   ```

### Método 2: Usando Kaggle API (Recomendado)

1. **Instalar Kaggle API**:
   ```bash
   pip install kaggle
   ```

2. **Configurar credenciales**:
   - Ve a tu perfil de Kaggle → Account → API → Create New Token
   - Descarga `kaggle.json` y colócalo en `~/.kaggle/`
   - En Windows: `C:\Users\<username>\.kaggle\kaggle.json`

3. **Descargar automáticamente**:
   ```bash
   cd ./data/01_raw/
   kaggle datasets download -d psvishnu/nyc-yellow-taxi-trip-records
   unzip nyc-yellow-taxi-trip-records.zip
   ```

## Estructura de Datos

### Estructura de Archivos

```
01_raw/
├── README.md                           # Este archivo
├── archive.zip                         # Archivo comprimido original
└── archive/                           # Directorio con datos extraídos
    ├── yellow_tripdata_2009-01.parquet
    ├── yellow_tripdata_2009-02.parquet
    ├── ...
    ├── yellow_tripdata_2023-02.parquet
    └── yellow_tripdata_2023-03.parquet
```

### Información de Archivos

- **Total de archivos**: 171 archivos Parquet
- **Período**: Enero 2009 - Marzo 2023
- **Nombrado**: `yellow_tripdata_YYYY-MM.parquet`
- **Tamaño total**: 27.8 GB descomprimidos
- **Registros totales**: 1,708,142,581 (~1.7 mil millones)

## Análisis Técnico del Dataset

### Evolución Temporal de Esquemas

El dataset presenta **3 períodos evolutivos** con esquemas diferentes:

#### Período 1: 2009 (Esquema Original)
- **Archivos**: 12 archivos (yellow_tripdata_2009-XX.parquet)
- **Columnas**: 18 variables
- **Volumen**: 170,896,055 registros
- **Tamaño**: 5.5 GB

**Variables específicas del período**:
```
- vendor_name (string)
- Trip_Pickup_DateTime (string)
- Trip_Dropoff_DateTime (string)
- Passenger_Count (int64)
- Trip_Distance (double)
- Start_Lon, Start_Lat (double)      # Coordenadas originales
- End_Lon, End_Lat (double)          # Coordenadas destino
- Rate_Code (double)
- Payment_Type (string)
- Fare_Amt, Tip_Amt, Tolls_Amt, Total_Amt (double)
- surcharge, mta_tax (double)
- store_and_forward (double)
```

#### Período 2: 2010 (Esquema Transición)
- **Archivos**: 12 archivos (yellow_tripdata_2010-XX.parquet)
- **Columnas**: 18 variables
- **Volumen**: 169,001,162 registros
- **Tamaño**: 5.4 GB

**Variables específicas del período**:
```
- vendor_id (string)                 # Cambio de nombre
- pickup_datetime, dropoff_datetime (string)
- passenger_count (int64)
- trip_distance (double)
- pickup_longitude, pickup_latitude (double)    # Nombres estandarizados
- dropoff_longitude, dropoff_latitude (double)
- rate_code (string)
- payment_type (string)
- fare_amount, tip_amount, tolls_amount, total_amount (double)
- surcharge, mta_tax (double)
- store_and_fwd_flag (string)
```

#### Período 3: 2011-2023 (Esquema TLC Estándar)
- **Archivos**: 147 archivos (yellow_tripdata_2011-01 hasta 2023-03)
- **Columnas**: 19 variables
- **Volumen**: 1,368,245,364 registros
- **Tamaño**: 17.6 GB

**Variables del esquema estándar**:
```
- VendorID (int64)
- tpep_pickup_datetime, tpep_dropoff_datetime (timestamp[us])
- passenger_count (int64 → double desde 2019)
- trip_distance (double)
- RatecodeID (int64 → double desde 2019)
- store_and_fwd_flag (string)
- PULocationID, DOLocationID (int64)            # Sistema de zonas TLC
- payment_type (int64)
- fare_amount, extra, mta_tax (double)
- tip_amount, tolls_amount (double)
- improvement_surcharge (double)
- total_amount (double)
- congestion_surcharge (double)                 # Introducido 2014
- airport_fee (double)                          # Introducido 2018
```

### Estadísticas por Año

| Año | Archivos | Registros | Tamaño (GB) | Promedio/Mes | Notas |
|-----|----------|-----------|-------------|--------------|-------|
| 2009 | 12 | 170.9M | 5.5 | 14.2M | Pico histórico |
| 2010 | 12 | 169.0M | 5.4 | 14.1M | Volumen alto |
| 2011 | 12 | 176.9M | 2.1 | 14.7M | Cambio compresión |
| 2012 | 12 | 171.4M | 2.1 | 14.3M | Estable |
| 2013 | 12 | 171.8M | 2.0 | 14.3M | Estable |
| 2014 | 12 | 165.4M | 2.0 | 13.8M | Introducción congestion_surcharge |
| 2015 | 12 | 146.0M | 1.9 | 12.2M | Declive inicio |
| 2016 | 12 | 131.1M | 1.7 | 10.9M | Declive continuo |
| 2017 | 12 | 113.5M | 1.5 | 9.5M | Declive acentuado |
| 2018 | 12 | 102.9M | 1.4 | 8.6M | Introducción airport_fee |
| 2019 | 12 | 84.6M | 1.2 | 7.0M | Cambio tipos datos |
| 2020 | 12 | 24.6M | 0.4 | 2.1M | **Impacto COVID-19** |
| 2021 | 12 | 30.9M | 0.5 | 2.6M | Mínimo histórico |
| 2022 | 12 | 39.7M | 0.6 | 3.3M | Recuperación lenta |
| 2023 | 3 | 9.4M | 0.1 | 3.1M | Solo Q1 disponible |

### Calidad de Datos

#### Completitud por Período

**2009 - Problemas identificados**:
- `Rate_Code`: 100% valores nulos
- `mta_tax`: 100% valores nulos  
- `store_and_forward`: 100% valores nulos

**2015 - Calidad mejorada**:
- `congestion_surcharge`: 100% nulos (no aplicaba aún)
- `airport_fee`: 100% nulos (no aplicaba aún)
- Resto de campos: >98% completitud

**2023 - Estado actual**:
- Completitud general: >97%
- Campos con valores faltantes: <3%
- Calidad alta en variables core

#### Variables Críticas Identificadas

**Variable única presente en todos los años**:
- `mta_tax` (única variable común 2009-2023)

**Variables con cambios evolutivos**:
- `congestion_surcharge`: Nula hasta 2013, presente desde 2014
- `airport_fee`: Nula hasta 2017, presente desde 2018
- Tipos de datos: Cambios en 2019 (`int64` → `double`)

## Consideraciones Técnicas

### Formatos y Codificación

- **Formato**: Apache Parquet (columnar, optimizado)
- **Compresión**: SNAPPY (rápida lectura)
- **Codificación**: UTF-8
- **Precisión temporal**: Microsegundos (2011+)

### Rendimiento de Lectura

```python
# Lectura eficiente por lotes
import pandas as pd
import pyarrow.parquet as pq

# Leer archivo individual
df = pd.read_parquet('archive/yellow_tripdata_2023-01.parquet')

# Leer múltiples archivos con filtros
table = pq.read_table(
    'archive/',
    filters=[('year', '>=', 2020)]
)
```

### Limitaciones Identificadas

1. **Inconsistencia de esquemas**: Requiere normalización
2. **Valores faltantes**: Especialmente en años tempranos
3. **Cambios de tipos**: Requiere casting cuidadoso
4. **Volumen**: 27.8 GB requieren procesamiento por lotes

## Estrategias de Procesamiento

### Consolidación Recomendada

**Opción 1: Por Períodos**
- Grupo Legacy: 2009-2010 (mapeo manual)
- Grupo Principal: 2011-2023 (esquema homogéneo)

**Opción 2: Por Variables Core**
- Solo `mta_tax` común a todos los años
- Pérdida significativa de información

**Recomendación**: Usar Opción 1 con mapeo de variables legacy

### Pipeline Sugerido

1. **Extracción**: Lectura por lotes de archivos Parquet
2. **Normalización**: Mapeo a esquema target común
3. **Validación**: Verificación de calidad por año
4. **Consolidación**: Particionamiento por año/mes
5. **Optimización**: Re-compresión y indexación

## Metadatos del Dataset

### Información de Licencia
- **Licencia**: Open Data License
- **Uso**: Permitido para investigación y análisis
- **Atribución**: NYC Taxi & Limousine Commission

### Contacto y Soporte
- **Dataset Kaggle**: [psvishnu](https://www.kaggle.com/psvishnu)
- **Fuente Original**: [NYC TLC](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Documentación oficial**: [TLC Data Dictionary](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

## Notas Importantes

1. **Descarga requerida**: Los archivos no están incluidos en el repositorio por su tamaño
2. **Espacio en disco**: Asegurar al menos 30 GB libres
3. **Tiempo de descarga**: Dependiendo de la conexión, puede tomar 1-2 horas
4. **Verificación**: Comprobar integridad de archivos después de la descarga

---

*Este README proporciona información detallada sobre los datos raw. Para análisis técnicos completos, consulte el notebook `../notebooks/data_understanding.ipynb`*