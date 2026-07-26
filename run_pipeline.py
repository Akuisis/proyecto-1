#!/usr/bin/env python
"""
CLI Entry Point

Command-line interface for the ML pipeline.
"""

import argparse
import sys
from src.pipeline import MLPipeline
from src.config import PipelineConfig


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Titanic ML Pipeline - Complete ML workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py --full                 # Run complete pipeline with download
  python run_pipeline.py --skip-download        # Run pipeline without downloading
  python run_pipeline.py --config               # Show configuration
        """,
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Run complete pipeline including data download",
    )

    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Run pipeline without downloading data",
    )

    parser.add_argument(
        "--config",
        action="store_true",
        help="Show pipeline configuration",
    )

    args = parser.parse_args()

    # Show config
    if args.config:
        print("\n📋 Pipeline Configuration:")
        print("-" * 50)
        for key, value in PipelineConfig.get_config().items():
            print(f"  {key}: {value}")
        print()
        return 0

    # Run pipeline
    if args.full or args.skip_download:
        pipeline = MLPipeline()
        download = args.full
        results = pipeline.run_full_pipeline(download_data=download)

        if results["status"] == "success":
            print(f"\n🎯 Best Model: {results['best_model_name']}")
            print(f"📊 Best Accuracy: {results['best_score']:.4f}")
            return 0
        else:
            print(f"\n❌ Pipeline failed: {results['error']}")
            return 1

    # If no args, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
