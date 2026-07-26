# 🚢 Titanic ML - Predicción de Supervivencia

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Polars](https://img.shields.io/badge/polars-1.43-orange.svg)](https://www.pola-rs.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-green.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)](#fases-del-proyecto)

Proyecto de **Machine Learning** para predecir la supervivencia de pasajeros del Titanic. Implementado con herramientas modernas y mejores prácticas de ingeniería de datos.

## 📋 Tabla de Contenidos

- [Objetivo](#-objetivo)
- [Dataset](#-dataset)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Fases del Proyecto](#-fases-del-proyecto)
- [Cómo Usar](#-cómo-usar)
- [Mejores Prácticas](#-mejores-prácticas)
- [Recursos](#-recursos)

---

## 🎯 Objetivo

Construir un modelo de **Machine Learning** que prediga si un pasajero del Titanic sobrevivió o no, basándose en características demográficas y del viaje.

**Métrica:** Precisión (Accuracy) del modelo en el conjunto de prueba.

---

## 📊 Dataset

| Aspecto | Detalles |
|---------|----------|
| **Fuente** | [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic) |
| **Entrenamiento** | 891 registros con etiqueta de supervivencia |
| **Prueba** | 418 registros (predicciones requeridas) |
| **Features** | Edad, Género, Clase, Tarifa, Familiares, Puerta |
| **Target** | Survived (0 = No, 1 = Sí) |

---

## 🛠️ Stack Tecnológico

| Herramienta | Propósito | Versión |
|-------------|----------|---------|
| **uv** | Gestor de paquetes (rápido & moderno) | Latest |
| **Python** | Lenguaje principal | 3.11+ |
| **Polars** | DataFrames ultra-rápido | 1.43.0 |
| **scikit-learn** | Modelos ML & preprocessing | 1.9.0 |
| **XGBoost** | Gradient boosting avanzado | 3.2.0 |
| **LightGBM** | Gradient boosting ligero | 4.0+ |
| **Jupyter** | Notebooks interactivos | 4.0+ |
| **Matplotlib/Seaborn** | Visualización | Latest |
| **Black** | Formateo de código | 23.0+ |
| **Ruff** | Linting rápido | 0.1+ |
| **Pytest** | Testing unitario | 7.4+ |

---

## ⚙️ Instalación

### Requisitos Previos
- Python 3.11 o superior
- Git
- Terminal (bash, zsh, PowerShell)

### Paso 1️⃣ - Clonar Repositorio
```bash
git clone https://github.com/Akuisis/proyecto-1.git
cd proyecto-1
```

### Paso 2️⃣ - Instalar uv
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Paso 3️⃣ - Crear Entorno Virtual
```bash
uv venv .venv
```

### Paso 4️⃣ - Activar Entorno
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Paso 5️⃣ - Instalar Dependencias
```bash
# Con herramientas de desarrollo
uv pip install -e ".[dev]"
```

### Verificar ✅
```bash
python -c "import polars, sklearn, xgboost; print('✅ Listo!')"
```

---

## 📁 Estructura del Proyecto

```
proyecto-1/
├── 📂 data/
│   ├── raw/              # Datos crudos de Kaggle (git-ignored)
│   └── processed/        # Datos procesados (git-ignored)
├── 📂 src/
│   ├── __init__.py
│   └── utils.py          # Funciones de utilidad
├── 📂 notebooks/         # Jupyter notebooks
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modeling.ipynb
├── 📂 tests/
│   ├── __init__.py
│   └── test_utils.py
├── 📄 pyproject.toml     # Configuración del proyecto
├── 📝 README.md          # Este archivo
├── .gitignore
└── .venv/                # Entorno virtual (git-ignored)
```

---

## 🚀 Fases del Proyecto

### ✅ Fase 1: Setup del Proyecto (COMPLETADO)
- [x] Estructura de directorios
- [x] Configuración de `pyproject.toml`
- [x] Instalación de dependencias
- [x] Utilidades básicas
- [x] Control de versiones

### 📥 Fase 2: Descarga de Datos (PRÓXIMO)
- [ ] Descargar `train.csv` y `test.csv`
- [ ] Validación de integridad
- [ ] Exploración inicial

### 📊 Fase 3: Análisis Exploratorio (EDA)
- [ ] Estadísticas descriptivas
- [ ] Distribuciones
- [ ] Valores faltantes
- [ ] Correlaciones
- [ ] Visualizaciones

### 🧹 Fase 4: Limpieza y Preprocessing
- [ ] Manejo de nulos
- [ ] Outliers
- [ ] Encoding categóricas
- [ ] Normalización/Escalado

### ⚙️ Fase 5: Feature Engineering
- [ ] Crear nuevas features
- [ ] Selección de features
- [ ] Validación

### 🤖 Fase 6: Entrenamiento de Modelos
- [ ] Logistic Regression
- [ ] Decision Tree
- [ ] Random Forest
- [ ] XGBoost
- [ ] LightGBM

### 🎯 Fase 7: Evaluación y Tuning
- [ ] Validación cruzada
- [ ] Hyperparameter tuning
- [ ] Análisis de importancia
- [ ] Selección de mejor modelo

### 📤 Fase 8: Predicciones y Submission
- [ ] Predicciones en test
- [ ] Archivo de envío
- [ ] Envío a Kaggle

---

## 💻 Cómo Usar

### Activar Entorno
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Ejecutar Jupyter Lab
```bash
jupyter lab
```

### Ejecutar Tests
```bash
pytest tests/ -v
pytest tests/ --cov=src
```

### Formatear Código
```bash
black src/
```

### Verificar Calidad
```bash
ruff check src/
```

### Ejemplo: Cargar Datos
```python
from src.utils import load_data
import polars as pl

train = load_data("data/raw/train.csv")
print(train.head())
print(train.shape)
```

---

## 📝 Mejores Prácticas Implementadas

✅ **Gestión de Dependencias**
- `pyproject.toml` centralizado
- Separación dev vs producción
- uv para instalación rápida

✅ **Calidad de Código**
- Black para formateo
- Ruff para linting
- Docstrings en funciones
- Type hints

✅ **Organización**
- Separación código/datos/notebooks
- `.gitignore` configurado
- Funciones reutilizables
- Tests organizados

✅ **Reproducibilidad**
- Seeds configuradas
- Versionado de datos
- Notebooks documentados
- Entorno reproducible

✅ **Documentación**
- README completo
- Docstrings
- Comentarios claros
- Roadmap explícito

---

## 📚 Recursos

### Documentación Oficial
- 🔗 [Titanic Kaggle](https://www.kaggle.com/c/titanic)
- 🔗 [Polars](https://www.pola-rs.com/docs/)
- 🔗 [Scikit-learn](https://scikit-learn.org/)
- 🔗 [XGBoost](https://xgboost.readthedocs.io/)
- 🔗 [uv](https://docs.astral.sh/uv/)

### Tutoriales
- 📖 [Kaggle Learn - Intro ML](https://www.kaggle.com/learn/intro-to-machine-learning)
- 📖 [Kaggle Learn - Intermediate ML](https://www.kaggle.com/learn/intermediate-machine-learning)
- 📖 [Data Cleaning](https://www.kaggle.com/learn/data-cleaning)

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea rama (`git checkout -b feature/mi-feature`)
3. Commit (`git commit -am 'Add feature'`)
4. Push (`git push origin feature/mi-feature`)
5. Pull Request

---

## 👤 Autor

**Angel** - [@Akuisis](https://github.com/Akuisis)

---

**Última actualización:** Jul 25, 2026  
**Versión:** 0.1.0

---

## 👥 Contribuidores

<table>
  <tr>
    <td align="center"><a href="https://github.com/angelcruzlasso"><img src="https://avatars.githubusercontent.com/u/angelcruzlasso?v=4" width="100px;" alt="Angel Cruz"/><br /><sub><b>angelcruzlasso</b></sub></a><br /><a href="#code-angelcruzlasso" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/features/copilot"><img src="https://avatars.githubusercontent.com/u/223556219?v=4" width="100px;" alt="Copilot"/><br /><sub><b>Copilot</b></sub></a><br /><a href="#code-copilot" title="Code">💻</a> <a href="#architecture" title="Architecture">🏗️</a></td>
    <td align="center"><a href="https://github.com/Akuisis"><img src="https://avatars.githubusercontent.com/u/Akuisis?v=4" width="100px;" alt="Akuisis"/><br /><sub><b>Akuisis</b></sub></a><br /><a href="#ideas" title="Ideas">🤔</a> <a href="#project" title="Project Management">📆</a></td>
  </tr>
</table>

### 🎖️ Roles

- **angelcruzlasso** - Data Engineer, Project Lead
- **Copilot** - Architecture Design, Code Implementation
- **Akuisis** - Project Coordination, Kaggle Competition

---

## 📝 Changelog

### v0.1.0 (2026-07-25)
- ✅ Initial project setup with uv
- ✅ Professional ML pipeline architecture
- ✅ Data, preprocessing, and model pipelines
- ✅ CLI interface for easy execution
- ✅ Comprehensive documentation
- 📝 README with contributor credits
