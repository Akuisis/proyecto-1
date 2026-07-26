"""Utility functions for the project"""

import polars as pl
from pathlib import Path


def load_data(filepath: Path) -> pl.DataFrame:
    """Load CSV data using polars"""
    return pl.read_csv(filepath)


def save_data(df: pl.DataFrame, filepath: Path) -> None:
    """Save data to CSV using polars"""
    df.write_csv(filepath)


def get_data_path(filename: str, processed: bool = False) -> Path:
    """Get data file path"""
    folder = "processed" if processed else "raw"
    return Path(__file__).parent.parent / "data" / folder / filename
