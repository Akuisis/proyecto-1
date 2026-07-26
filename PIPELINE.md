# 🔄 ML Pipeline Architecture

Documentación técnica de la arquitectura modular del pipeline ML.

## 📐 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML Pipeline Orchestrator                     │
│                       (pipeline.py)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼──────┐  ┌──▼────────┐  ┌─▼──────────┐
        │ Data Stage   │  │Preproc    │  │ Model      │
        │(data_        │  │ Stage     │  │ Stage      │
        │pipeline.py)  │  │(preproc-  │  │(model_     │
        └──────────────┘  │essing_    │  │pipeline.py)│
                          │pipeline)  │  └────────────┘
                          └───────────┘
```

## 🏗️ Componentes Principales

### 1. **PipelineConfig** (`config.py`)
**Responsabilidad:** Gestión centralizada de configuración

```python
# Paths
PROJECT_ROOT, DATA_DIR, MODELS_DIR, LOGS_DIR

# Kaggle
KAGGLE_COMPETITION, TRAIN_FILE, TEST_FILE

# Hyperparameters
RANDOM_SEED, TEST_SIZE, CV_FOLDS

# Feature Config
NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET

# Model Config
MODELS_CONFIG (LogReg, RandomForest, XGBoost)
```

**Beneficios:**
- Single source of truth
- Fácil de mantener
- No repetir configuración

---

### 2. **DataPipeline** (`data_pipeline.py`)
**Responsabilidad:** Descarga, carga y validación de datos

**Métodos:**
```python
download_data()        # Descargar de Kaggle con kagglehub
load_raw_data()        # Cargar train.csv y test.csv con polars
validate_data()        # Validar integridad de datos
save_processed_data()  # Guardar datos procesados
```

**Features:**
- Logging detallado
- Validación automática
- Manejo de errores
- Guardado de datos procesados

---

### 3. **PreprocessingPipeline** (`preprocessing_pipeline.py`)
**Responsabilidad:** Limpieza y transformación de datos

**Métodos:**
```python
handle_missing_values()  # Fill nulls con median/mode
remove_outliers()        # Z-score method
encode_categorical()     # One-hot encoding
scale_features()         # StandardScaler
run_preprocessing()      # Orquestación completa
```

**Features:**
- Manejo de valores nulos (median para numeric, mode para categóricas)
- Detección de outliers
- Encoding categorías
- Normalización features
- Logging de cambios

---

### 4. **ModelPipeline** (`model_pipeline.py`)
**Responsabilidad:** Entrenamiento y evaluación de modelos

**Métodos:**
```python
build_models()        # Crear instancias de modelos
train_model()         # Entrenar un modelo
evaluate_model()      # Calcular métricas
cross_validate()      # Validación cruzada
run_model_pipeline()  # Orquestación completa
```

**Models Soportados:**
- Logistic Regression
- Random Forest
- XGBoost (opcional)

**Métricas:**
- Accuracy
- Precision
- Recall
- F1-Score

---

### 5. **MLPipeline** (`pipeline.py`)
**Responsabilidad:** Orquestación principal de todos los stages

**Métodos:**
```python
run_full_pipeline()  # Ejecutar pipeline completo
_save_results()      # Guardar modelos y métricas
get_predictions()    # Generar predicciones
```

**Stages:**
1. Data Download & Loading
2. Data Validation
3. Preprocessing
4. Model Training & Evaluation
5. Save Results

---

## 🎯 Flujo de Ejecución Completo

```
1. MLPipeline.run_full_pipeline()
   ├─ DataPipeline.download_data()
   ├─ DataPipeline.load_raw_data()
   ├─ DataPipeline.validate_data()
   │
   ├─ PreprocessingPipeline.run_preprocessing()
   │  ├─ handle_missing_values()
   │  ├─ remove_outliers()
   │  ├─ encode_categorical()
   │  └─ scale_features()
   │
   ├─ ModelPipeline.run_model_pipeline()
   │  ├─ build_models()
   │  ├─ train_model()
   │  ├─ evaluate_model()
   │  └─ cross_validate()
   │
   └─ _save_results()
      ├─ save processed data
      ├─ save best model (pickle)
      └─ save metrics (JSON)
```

---

## 📁 Estructura de Salidas

```
proyecto-1/
├── data/
│   ├── raw/
│   │   ├── train.csv          # Descargado de Kaggle
│   │   └── test.csv           # Descargado de Kaggle
│   └── processed/
│       ├── train_processed_v1.csv
│       └── test_processed_v1.csv
│
├── models/
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   └── xgboost.pkl
│
└── logs/
    ├── pipeline.log           # Logs de ejecución
    └── metrics.json           # Métricas de modelos
```

---

## ⚙️ Configuración de Modelos

```python
# config.py -> MODELS_CONFIG

{
    "logistic_regression": {
        "params": {"max_iter": 1000, "random_state": 42}
    },
    "random_forest": {
        "params": {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        }
    },
    "xgboost": {
        "params": {
            "max_depth": 5,
            "learning_rate": 0.1,
            "random_state": 42
        }
    }
}
```

---

## 🚀 Cómo Usar

### Opción 1: Línea de Comandos (CLI)
```bash
# Ejecutar pipeline completo con descarga
python run_pipeline.py --full

# Ejecutar sin descargar (si ya tienes datos)
python run_pipeline.py --skip-download

# Ver configuración
python run_pipeline.py --config
```

### Opción 2: Python Script
```python
from src.pipeline import MLPipeline

# Crear instancia del pipeline
pipeline = MLPipeline()

# Ejecutar
results = pipeline.run_full_pipeline(download_data=True)

# Acceder resultados
print(f"Best Model: {results['best_model_name']}")
print(f"Best Accuracy: {results['best_score']:.4f}")
```

### Opción 3: Componentes Individuales
```python
from src.data_pipeline import DataPipeline
from src.preprocessing_pipeline import PreprocessingPipeline

# Solo descargar
DataPipeline.download_data()

# Cargar datos
train, test = DataPipeline.load_raw_data()

# Procesar
train_clean, test_clean = PreprocessingPipeline.run_preprocessing(train, test)
```

---

## 📊 Logging

El pipeline genera logs en múltiples niveles:

```
❌ ERROR    - Fallos críticos
⚠️  WARNING - Alertas de datos
ℹ️  INFO    - Eventos principales
🔍 DEBUG   - Detalles de ejecución
```

**Archivos de log:**
- `logs/pipeline.log` - Todos los eventos

---

## ✅ Mejores Prácticas Implementadas

### 1. **Modularidad**
- Cada componente tiene responsabilidad única
- Fácil de testear y mantener

### 2. **Configuración Centralizada**
- Un único `PipelineConfig`
- Cambios fáciles y globales

### 3. **Logging Exhaustivo**
- Todos los eventos registrados
- Debugging facilitado

### 4. **Manejo de Errores**
- Try/except en operaciones críticas
- Mensajes claros de error

### 5. **Validación de Datos**
- Verificación de integridad
- Alertas de problemas

### 6. **Reproducibilidad**
- Seeds fijos (random_state)
- Configuración versionada
- Logs completos

### 7. **Persistencia**
- Modelos guardados (pickle)
- Métricas guardadas (JSON)
- Datos procesados guardados (CSV)

---

## 🔌 Extensibilidad

Para agregar nuevos componentes:

### Agregar un Nuevo Modelo
```python
# En config.py
MODELS_CONFIG["lightgbm"] = {
    "params": {"num_leaves": 31, "random_state": RANDOM_SEED}
}

# En model_pipeline.py
import lightgbm as lgb
models["lightgbm"] = lgb.LGBMClassifier(**params)
```

### Agregar Nueva Métrica
```python
# En model_pipeline.py
from sklearn.metrics import roc_auc_score

metrics["roc_auc"] = roc_auc_score(y_test_np, y_pred_proba)
```

### Agregar Nuevo Stage
```python
# Crear nuevo archivo: src/feature_engineering_pipeline.py
class FeatureEngineeringPipeline:
    @staticmethod
    def run_feature_engineering(train_df, test_df):
        # Crear features nuevas
        return train_df, test_df

# Integrar en MLPipeline.run_full_pipeline()
```

---

## 🎓 Conceptos Clave

**Data Pipeline:**
- Gestión de ciclo de vida de datos
- Validación y limpieza
- Trazabilidad de cambios

**Preprocessing:**
- Preparar datos para ML
- Manejo de valores faltantes
- Feature scaling

**Model Pipeline:**
- Entrenamiento sistemático
- Evaluación consistente
- Comparación de modelos

**Orchestration:**
- Coordinar múltiples stages
- Manejo de dependencias
- Logging centralizado

---

## 📈 Próximas Mejoras

- [ ] Feature Engineering Pipeline
- [ ] Hyperparameter Tuning
- [ ] Model Persistence & Loading
- [ ] Prediction Pipeline
- [ ] API REST para predicciones
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Model Monitoring

---

**Versión:** 0.1.0  
**Última actualización:** Jul 25, 2026
