#!/usr/bin/env python3
from typing import List, Optional
import argparse
import logging
import sys
from pathlib import Path

from roagg.aggregator import aggregate

def validate_ror_id(ror_id: str) -> str:
    """Validate ROR ID format (should start with https://ror.org/)."""
    if not ror_id.startswith('https://ror.org/'):
        raise argparse.ArgumentTypeError("ROR ID must start with 'https://ror.org/'")
    return ror_id

def read_names_from_file(filepath: Path) -> List[str]:
    """Read organization names from a file, one per line."""
    try:
        return [line.strip() for line in filepath.read_text().splitlines() if line.strip()]
    except IOError as e:
        logging.error(f"Failed to read names file: {e}")
        sys.exit(1)

def main() -> None:
    """Create a summary CSV file for all research output for an organization."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description="Aggregate research outputs for an organization into a CSV file",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--name",
        type=str,
        action='append',
        help="Name variant of the organization (can be used multiple times)"
    )
    parser.add_argument(
        "--name-txt",
        type=Path,
        help="Path to text file containing organization name variants (one per line)"
    )

    parser.add_argument(
        "--ror",
        type=validate_ror_id,
        help="ROR ID of the organization (must start with https://ror.org/)"
    )

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    names: List[str] = []
    if args.name:
        names = args.name
    
    if args.name_txt:
        names.extend(read_names_from_file(args.name_txt))

    try:
        aggregate(names, args.ror)
    except Exception as e:
        logging.error(f"Aggregation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()