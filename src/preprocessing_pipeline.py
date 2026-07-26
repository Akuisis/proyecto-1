"""
Preprocessing Pipeline

Handles data cleaning, feature engineering, and transformation.
"""

import logging
from typing import Tuple

import polars as pl
from sklearn.preprocessing import StandardScaler, LabelEncoder

from .config import PipelineConfig

logger = logging.getLogger(__name__)


class PreprocessingPipeline:
    """Handles data preprocessing and cleaning."""

    @staticmethod
    def handle_missing_values(df: pl.DataFrame) -> pl.DataFrame:
        """
        Handle missing values in dataset.

        Args:
            df: Input dataframe

        Returns:
            pl.DataFrame: Dataframe with missing values handled
        """
        logger.info("Handling missing values...")

        # Log missing values
        missing = df.null_count()
        logger.info(f"Missing values:\n{missing}")

        # Fill numeric missing values with median
        for col in PipelineConfig.NUMERIC_FEATURES:
            if col in df.columns:
                median_val = df[col].median()
                df = df.with_columns(pl.col(col).fill_null(median_val))
                logger.debug(f"Filled {col} with median: {median_val}")

        # Fill categorical missing values with mode
        for col in PipelineConfig.CATEGORICAL_FEATURES:
            if col in df.columns:
                # Get most common value
                mode_val = df[col].mode()[0]
                df = df.with_columns(pl.col(col).fill_null(mode_val))
                logger.debug(f"Filled {col} with mode: {mode_val}")

        logger.info("✅ Missing values handled")
        return df

    @staticmethod
    def remove_outliers(df: pl.DataFrame, column: str, n_std: float = 3) -> pl.DataFrame:
        """
        Remove outliers using z-score method.

        Args:
            df: Input dataframe
            column: Column name
            n_std: Number of standard deviations

        Returns:
            pl.DataFrame: Dataframe without outliers
        """
        mean = df[column].mean()
        std = df[column].std()

        lower_bound = mean - n_std * std
        upper_bound = mean + n_std * std

        n_before = df.height
        df = df.filter((pl.col(column) >= lower_bound) & (pl.col(column) <= upper_bound))
        n_after = df.height

        logger.debug(f"Removed {n_before - n_after} outliers from {column}")
        return df

    @staticmethod
    def encode_categorical(df: pl.DataFrame, test_df: pl.DataFrame = None) -> Tuple:
        """
        Encode categorical variables.

        Args:
            df: Training dataframe
            test_df: Test dataframe (optional)

        Returns:
            Tuple: (encoded_train, encoded_test or None)
        """
        logger.info("Encoding categorical features...")

        # One-hot encoding for categorical features
        for col in PipelineConfig.CATEGORICAL_FEATURES:
            if col in df.columns:
                unique_vals = df[col].unique().to_list()
                for val in unique_vals:
                    if val is not None:
                        new_col_name = f"{col}_{val}"
                        df = df.with_columns(
                            (pl.col(col) == val).cast(pl.Int32).alias(new_col_name)
                        )
                        if test_df is not None:
                            test_df = test_df.with_columns(
                                (pl.col(col) == val).cast(pl.Int32).alias(new_col_name)
                            )

        # Drop original categorical columns
        df = df.drop(PipelineConfig.CATEGORICAL_FEATURES)
        if test_df is not None:
            test_df = test_df.drop(PipelineConfig.CATEGORICAL_FEATURES)

        logger.info("✅ Categorical features encoded")
        return (df, test_df) if test_df is not None else (df, None)

    @staticmethod
    def scale_features(
        df: pl.DataFrame,
        test_df: pl.DataFrame = None,
        fit_scaler=True,
        scaler: StandardScaler = None,
    ) -> Tuple:
        """
        Scale numeric features.

        Args:
            df: Training dataframe
            test_df: Test dataframe (optional)
            fit_scaler: Whether to fit a new scaler
            scaler: Pre-fitted scaler (if fit_scaler=False)

        Returns:
            Tuple: (scaled_train, scaled_test or None, scaler)
        """
        logger.info("Scaling features...")

        if scaler is None:
            scaler = StandardScaler()

        numeric_cols = [col for col in PipelineConfig.NUMERIC_FEATURES if col in df.columns]

        if numeric_cols:
            if fit_scaler:
                scaled_data = scaler.fit_transform(df[numeric_cols].to_numpy())
            else:
                scaled_data = scaler.transform(df[numeric_cols].to_numpy())

            # Convert back to polars
            df = df.with_columns(
                [
                    pl.Series(col, scaled_data[:, i])
                    for i, col in enumerate(numeric_cols)
                ]
            )

            if test_df is not None:
                scaled_test_data = scaler.transform(test_df[numeric_cols].to_numpy())
                test_df = test_df.with_columns(
                    [
                        pl.Series(col, scaled_test_data[:, i])
                        for i, col in enumerate(numeric_cols)
                    ]
                )

        logger.info("✅ Features scaled")
        return (df, test_df, scaler) if test_df is not None else (df, None, scaler)

    @staticmethod
    def run_preprocessing(
        train_df: pl.DataFrame,
        test_df: pl.DataFrame,
    ) -> Tuple[pl.DataFrame, pl.DataFrame]:
        """
        Run complete preprocessing pipeline.

        Args:
            train_df: Training dataset
            test_df: Test dataset

        Returns:
            Tuple[pl.DataFrame, pl.DataFrame]: Preprocessed datasets
        """
        logger.info("=" * 50)
        logger.info("Starting Preprocessing Pipeline")
        logger.info("=" * 50)

        # Handle missing values
        train_df = PreprocessingPipeline.handle_missing_values(train_df)
        test_df = PreprocessingPipeline.handle_missing_values(test_df)

        # Remove outliers (only from train)
        for col in PipelineConfig.NUMERIC_FEATURES:
            if col in train_df.columns:
                train_df = PreprocessingPipeline.remove_outliers(train_df, col)

        # Encode categorical
        train_df, test_df = PreprocessingPipeline.encode_categorical(train_df, test_df)

        # Scale features
        train_df, test_df, _ = PreprocessingPipeline.scale_features(train_df, test_df)

        logger.info("=" * 50)
        logger.info("✅ Preprocessing Pipeline Complete")
        logger.info("=" * 50)

        return train_df, test_df
