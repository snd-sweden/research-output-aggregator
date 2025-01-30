from roagg.aggregator import aggregate
import argparse

def main():
    parser = argparse.ArgumentParser(description="Creates a summary csv file for all research output for a organization")

    parser.add_argument("--ror", type=str, help="ROR-ID of the organization.")
    parser.add_argument("--name", type=str, action='append', help="Name of the organization. This can be used multiple times.")

    args = parser.parse_args()

    names = args.name if args.name else []

    aggregate(names, args.ror)

if __name__ == "__main__":
    main()