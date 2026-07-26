"""
Data Pipeline

Handles data download, validation, and loading.
"""

import logging
from typing import Tuple

import kagglehub
import polars as pl

from .config import PipelineConfig

logger = logging.getLogger(__name__)


class DataPipeline:
    """Manages data acquisition and validation."""

    @staticmethod
    def download_data() -> bool:
        """
        Download Titanic dataset from Kaggle using kagglehub.

        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            import shutil

            logger.info(f"Downloading {PipelineConfig.KAGGLE_COMPETITION} competition data...")

            path = kagglehub.competition_download(
                PipelineConfig.KAGGLE_COMPETITION,
            )
            logger.info(f"✅ Download complete at: {path}")

            # Copy files to project data/raw directory
            import os

            for file in os.listdir(path):
                src = os.path.join(path, file)
                dst = PipelineConfig.RAW_DATA_DIR / file
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    logger.info(f"Copied {file} to {PipelineConfig.RAW_DATA_DIR}")

            return True

        except Exception as e:
            logger.error(
                "❌ Kaggle download failed. Verify KAGGLE_USERNAME/KAGGLE_KEY and "
                "that the account accepted competition rules: "
                "https://kaggle.com/competitions/titanic/rules",
            )
            logger.error(f"Original error: {e}")
            return False

    @staticmethod
    def load_raw_data() -> Tuple[pl.DataFrame, pl.DataFrame]:
        """
        Load train and test datasets.

        Returns:
            Tuple[pl.DataFrame, pl.DataFrame]: (train_df, test_df)

        Raises:
            FileNotFoundError: If CSV files not found
        """
        if not PipelineConfig.TRAIN_FILE.exists():
            raise FileNotFoundError(f"Train file not found: {PipelineConfig.TRAIN_FILE}")

        if not PipelineConfig.TEST_FILE.exists():
            raise FileNotFoundError(f"Test file not found: {PipelineConfig.TEST_FILE}")

        logger.info("Loading raw data...")
        train_df = pl.read_csv(PipelineConfig.TRAIN_FILE)
        test_df = pl.read_csv(PipelineConfig.TEST_FILE)

        logger.info(f"Train shape: {train_df.shape}")
        logger.info(f"Test shape: {test_df.shape}")

        return train_df, test_df

    @staticmethod
    def validate_data(train_df: pl.DataFrame, test_df: pl.DataFrame) -> bool:
        """
        Validate data integrity.

        Args:
            train_df: Training dataset
            test_df: Test dataset

        Returns:
            bool: True if validation passes
        """
        logger.info("Validating data...")

        # Check train has target column
        if PipelineConfig.TARGET not in train_df.columns:
            logger.error(f"Target column '{PipelineConfig.TARGET}' not found in train data")
            return False

        # Check no duplicates
        if train_df.is_duplicated().sum() > 0:
            logger.warning(f"Found {train_df.is_duplicated().sum()} duplicate rows in train")

        # Check shapes
        if train_df.height == 0 or test_df.height == 0:
            logger.error("Data is empty")
            return False

        logger.info("✅ Data validation passed")
        return True

    @staticmethod
    def save_processed_data(
        train_df: pl.DataFrame,
        test_df: pl.DataFrame,
        suffix: str = "",
    ) -> None:
        """
        Save processed datasets to disk.

        Args:
            train_df: Training dataset
            test_df: Test dataset
            suffix: Optional suffix for filename
        """
        train_path = PipelineConfig.PROCESSED_DATA_DIR / f"train_processed{suffix}.csv"
        test_path = PipelineConfig.PROCESSED_DATA_DIR / f"test_processed{suffix}.csv"

        train_df.write_csv(train_path)
        test_df.write_csv(test_path)

        logger.info(f"Saved processed data to {PipelineConfig.PROCESSED_DATA_DIR}")
