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

        # Drop columns with too many missing values
        for col in df.columns:
            missing_ratio = df[col].null_count() / df.height
            if missing_ratio > 0.5:
                logger.debug(f"Dropping {col}: {missing_ratio:.1%} missing")
                df = df.drop(col)

        # Fill numeric missing values with median
        for col in PipelineConfig.NUMERIC_FEATURES:
            if col in df.columns and df[col].null_count() > 0:
                median_val = df[col].median()
                if median_val is not None:
                    df = df.with_columns(pl.col(col).fill_null(median_val))
                    logger.debug(f"Filled {col} with median: {median_val}")

        # Fill categorical missing values with mode
        for col in PipelineConfig.CATEGORICAL_FEATURES:
            if col in df.columns and df[col].null_count() > 0:
                # Get most common value
                mode_df = df[col].value_counts().sort("count", descending=True)
                if len(mode_df) > 0:
                    mode_val = mode_df[0, 0]  # Get first value from first column
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
                        if test_df is not None and col in test_df.columns:
                            test_df = test_df.with_columns(
                                (pl.col(col) == val).cast(pl.Int32).alias(new_col_name)
                            )

        # Drop original categorical columns (only if they exist)
        cols_to_drop = [col for col in PipelineConfig.CATEGORICAL_FEATURES if col in df.columns]
        if cols_to_drop:
            df = df.drop(cols_to_drop)
        if test_df is not None:
            cols_to_drop = [col for col in PipelineConfig.CATEGORICAL_FEATURES if col in test_df.columns]
            if cols_to_drop:
                test_df = test_df.drop(cols_to_drop)

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

        # Drop non-useful columns
        cols_to_drop = ["PassengerId", "Name", "Ticket"]
        train_df = train_df.drop([col for col in cols_to_drop if col in train_df.columns])
        test_df = test_df.drop([col for col in cols_to_drop if col in test_df.columns])

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
