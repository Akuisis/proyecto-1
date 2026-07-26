"""
Model Pipeline

Handles model training, evaluation, and prediction.
"""

import logging
from typing import Dict, Tuple, Any

import polars as pl
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from .config import PipelineConfig

logger = logging.getLogger(__name__)


class ModelPipeline:
    """Handles model training and evaluation."""

    @staticmethod
    def build_models() -> Dict[str, Any]:
        """
        Build all model instances.

        Returns:
            Dict[str, Any]: Dictionary of model name -> model instance
        """
        logger.info("Building models...")

        models = {}

        # Logistic Regression
        models["logistic_regression"] = LogisticRegression(
            **PipelineConfig.MODELS_CONFIG["logistic_regression"]["params"]
        )

        # Random Forest
        models["random_forest"] = RandomForestClassifier(
            **PipelineConfig.MODELS_CONFIG["random_forest"]["params"]
        )

        # XGBoost (if available)
        if XGBOOST_AVAILABLE:
            models["xgboost"] = xgb.XGBClassifier(
                **PipelineConfig.MODELS_CONFIG["xgboost"]["params"]
            )

        logger.info(f"✅ Built {len(models)} models")
        return models

    @staticmethod
    def train_model(model: Any, X_train: pl.DataFrame, y_train: pl.Series) -> Any:
        """
        Train a single model.

        Args:
            model: Model instance
            X_train: Training features
            y_train: Training target

        Returns:
            Any: Trained model
        """
        X_train_np = X_train.to_numpy()
        y_train_np = y_train.to_numpy().flatten()

        model.fit(X_train_np, y_train_np)
        return model

    @staticmethod
    def evaluate_model(
        model: Any,
        X_test: pl.DataFrame,
        y_test: pl.Series,
        model_name: str = "Model",
    ) -> Dict[str, float]:
        """
        Evaluate model performance.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            model_name: Name of model

        Returns:
            Dict[str, float]: Metrics dictionary
        """
        X_test_np = X_test.to_numpy()
        y_test_np = y_test.to_numpy().flatten()

        y_pred = model.predict(X_test_np)

        metrics = {
            "accuracy": accuracy_score(y_test_np, y_pred),
            "precision": precision_score(y_test_np, y_pred, zero_division=0),
            "recall": recall_score(y_test_np, y_pred, zero_division=0),
            "f1": f1_score(y_test_np, y_pred, zero_division=0),
        }

        logger.info(f"\n{model_name} Results:")
        logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall:    {metrics['recall']:.4f}")
        logger.info(f"  F1 Score:  {metrics['f1']:.4f}")

        return metrics

    @staticmethod
    def cross_validate(
        model: Any,
        X: pl.DataFrame,
        y: pl.Series,
        cv: int = 5,
    ) -> Dict[str, float]:
        """
        Perform cross-validation.

        Args:
            model: Model instance
            X: Features
            y: Target
            cv: Number of folds

        Returns:
            Dict[str, float]: Cross-validation scores
        """
        X_np = X.to_numpy()
        y_np = y.to_numpy().flatten()

        scores = cross_val_score(model, X_np, y_np, cv=cv, scoring="accuracy")

        return {
            "mean": scores.mean(),
            "std": scores.std(),
            "scores": scores.tolist(),
        }

    @staticmethod
    def run_model_pipeline(
        train_df: pl.DataFrame,
        test_df: pl.DataFrame,
    ) -> Dict[str, Any]:
        """
        Run complete model training and evaluation pipeline.

        Args:
            train_df: Preprocessed training data
            test_df: Preprocessed test data

        Returns:
            Dict[str, Any]: Results dictionary with trained models and metrics
        """
        logger.info("=" * 50)
        logger.info("Starting Model Pipeline")
        logger.info("=" * 50)

        # Separate features and target
        X_train = train_df.drop(PipelineConfig.TARGET)
        y_train = train_df[PipelineConfig.TARGET]

        # Split into train/validation
        X_tr, X_val, y_tr, y_val = train_test_split(
            X_train,
            y_train,
            test_size=PipelineConfig.TEST_SIZE,
            random_state=PipelineConfig.RANDOM_SEED,
        )

        # Build models
        models = ModelPipeline.build_models()

        # Train and evaluate each model
        results = {}
        best_model = None
        best_score = -1
        best_model_name = None

        for model_name, model in models.items():
            logger.info(f"\nTraining {model_name}...")

            # Train
            trained_model = ModelPipeline.train_model(model, X_tr, y_tr)

            # Evaluate
            metrics = ModelPipeline.evaluate_model(trained_model, X_val, y_val, model_name)

            # Cross-validate
            cv_scores = ModelPipeline.cross_validate(
                trained_model,
                X_tr,
                y_tr,
                cv=PipelineConfig.CV_FOLDS,
            )
            logger.info(f"  CV Mean: {cv_scores['mean']:.4f} (+/- {cv_scores['std']:.4f})")

            results[model_name] = {
                "model": trained_model,
                "metrics": metrics,
                "cv_scores": cv_scores,
            }

            # Track best model
            if metrics["accuracy"] > best_score:
                best_score = metrics["accuracy"]
                best_model = trained_model
                best_model_name = model_name

        logger.info(f"\n✅ Best Model: {best_model_name} (Accuracy: {best_score:.4f})")

        logger.info("=" * 50)
        logger.info("✅ Model Pipeline Complete")
        logger.info("=" * 50)

        return {
            "best_model": best_model,
            "best_model_name": best_model_name,
            "best_score": best_score,
            "all_results": results,
        }
