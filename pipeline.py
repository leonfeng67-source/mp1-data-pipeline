"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config,
    )

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    required = config["validation"]["required_columns"]
    numeric = config["validation"]["numeric_columns"]

    rows_before = len(df)
    try:
        df = validate_dataframe(df, required, numeric)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows", rows_before, len(df))

    df_original = df.copy()

    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df)
    logger.info("Processing complete: %d -> %d rows", len(df_original), len(df))
    save_data(df, args.output)
    logger.info("Saved cleaned data to %s", args.output)
    print(report)



if __name__ == "__main__":
    main()