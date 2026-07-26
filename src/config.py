"""
Pipeline Configuration

Defines stages, paths, and parameters for the ML pipeline.
"""

from pathlib import Path
from typing import Any, Dict


class PipelineConfig:
    """Central configuration for all pipeline stages."""

    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    MODELS_DIR = PROJECT_ROOT / "models"
    LOGS_DIR = PROJECT_ROOT / "logs"

    # Ensure directories exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Kaggle Competition
    KAGGLE_COMPETITION = "titanic"
    TRAIN_FILE = RAW_DATA_DIR / "train.csv"
    TEST_FILE = RAW_DATA_DIR / "test.csv"

    # Processing Configuration
    RANDOM_SEED = 42
    TEST_SIZE = 0.2
    CV_FOLDS = 5

    # Feature Configuration
    NUMERIC_FEATURES = [
        "Age",
        "Fare",
        "Pclass",
        "SibSp",
        "Parch",
    ]
    CATEGORICAL_FEATURES = [
        "Sex",
        "Embarked",
        "Cabin",
    ]
    TARGET = "Survived"

    # Model Configuration
    MODELS_CONFIG: Dict[str, Dict[str, Any]] = {
        "logistic_regression": {
            "params": {"max_iter": 1000, "random_state": RANDOM_SEED},
        },
        "random_forest": {
            "params": {
                "n_estimators": 100,
                "max_depth": 10,
                "random_state": RANDOM_SEED,
            },
        },
        "xgboost": {
            "params": {
                "max_depth": 5,
                "learning_rate": 0.1,
                "random_state": RANDOM_SEED,
            },
        },
    }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Return entire config as dict."""
        return {
            "project_root": str(cls.PROJECT_ROOT),
            "raw_data": str(cls.RAW_DATA_DIR),
            "processed_data": str(cls.PROCESSED_DATA_DIR),
            "models": str(cls.MODELS_DIR),
            "random_seed": cls.RANDOM_SEED,
            "cv_folds": cls.CV_FOLDS,
        }
