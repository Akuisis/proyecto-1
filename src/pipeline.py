"""
Main Pipeline Orchestrator

Coordinates all pipeline stages.
"""

import logging
import sys
from typing import Dict, Any

from .config import PipelineConfig
from .data_pipeline import DataPipeline
from .preprocessing_pipeline import PreprocessingPipeline
from .model_pipeline import ModelPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(PipelineConfig.LOGS_DIR / "pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class MLPipeline:
    """Main ML pipeline orchestrator."""

    def __init__(self):
        """Initialize pipeline."""
        self.config = PipelineConfig.get_config()
        self.train_df = None
        self.test_df = None
        self.model_results = None

    def run_full_pipeline(self, download_data: bool = True) -> Dict[str, Any]:
        """
        Run the complete ML pipeline.

        Args:
            download_data: Whether to download data from Kaggle

        Returns:
            Dict[str, Any]: Pipeline results
        """
        logger.info("\n")
        logger.info("🚀" * 25)
        logger.info("STARTING TITANIC ML PIPELINE")
        logger.info("🚀" * 25)
        logger.info("\n")

        try:
            # Stage 1: Download Data
            if download_data:
                logger.info("Stage 1: Data Download")
                logger.info("-" * 50)
                success = DataPipeline.download_data()
                if not success:
                    logger.error("Failed to download data")
                    return {"status": "failed", "error": "Download failed"}

            # Stage 2: Load & Validate Data
            logger.info("\nStage 2: Data Loading & Validation")
            logger.info("-" * 50)
            self.train_df, self.test_df = DataPipeline.load_raw_data()

            if not DataPipeline.validate_data(self.train_df, self.test_df):
                logger.error("Data validation failed")
                return {"status": "failed", "error": "Validation failed"}

            # Stage 3: Preprocessing
            logger.info("\nStage 3: Data Preprocessing")
            logger.info("-" * 50)
            self.train_df, self.test_df = PreprocessingPipeline.run_preprocessing(
                self.train_df,
                self.test_df,
            )

            # Stage 4: Model Training & Evaluation
            logger.info("\nStage 4: Model Training & Evaluation")
            logger.info("-" * 50)
            self.model_results = ModelPipeline.run_model_pipeline(
                self.train_df,
                self.test_df,
            )

            # Stage 5: Save Results
            logger.info("\nStage 5: Saving Results")
            logger.info("-" * 50)
            self._save_results()

            logger.info("\n")
            logger.info("✅" * 25)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("✅" * 25)
            logger.info("\n")

            return {
                "status": "success",
                "best_model_name": self.model_results["best_model_name"],
                "best_score": self.model_results["best_score"],
                "results": self.model_results,
            }

        except Exception as e:
            logger.error(f"Pipeline failed with error: {e}", exc_info=True)
            return {"status": "failed", "error": str(e)}

    def _save_results(self) -> None:
        """Save pipeline results to disk."""
        try:
            # Save processed data
            DataPipeline.save_processed_data(self.train_df, self.test_df, suffix="_v1")

            # Save best model (pickle)
            import pickle

            model_path = (
                PipelineConfig.MODELS_DIR / f"{self.model_results['best_model_name']}.pkl"
            )
            with open(model_path, "wb") as f:
                pickle.dump(self.model_results["best_model"], f)
            logger.info(f"Model saved: {model_path}")

            # Save metrics (JSON)
            import json

            metrics = {
                model_name: data["metrics"]
                for model_name, data in self.model_results["all_results"].items()
            }
            metrics_path = PipelineConfig.LOGS_DIR / "metrics.json"
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=2)
            logger.info(f"Metrics saved: {metrics_path}")

        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    @staticmethod
    def get_predictions(best_model, test_df):
        """Generate predictions on test set."""
        X_test = test_df.drop(PipelineConfig.TARGET, errors="ignore")
        predictions = best_model.predict(X_test.to_numpy())
        return predictions


if __name__ == "__main__":
    # Run pipeline
    pipeline = MLPipeline()
    results = pipeline.run_full_pipeline(download_data=True)
    print(results)
