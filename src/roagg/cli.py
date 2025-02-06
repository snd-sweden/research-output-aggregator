from roagg.aggregator import aggregate
import argparse

def main():
    parser = argparse.ArgumentParser(description="Creates a summary csv file for all research output for a organization")

    parser.add_argument("--ror", type=str, help="ROR-ID of the organization.")
    parser.add_argument("--name", type=str, action='append', help="Name of the organization. This can be used multiple times.")
    parser.add_argument("--name_txt", type=str, help="Name list in text file, one name variant per line.")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    names = args.name if args.name else []

    if args.name_txt:
        with open(args.name_txt) as f:
            names = [line.strip() for line in f]

    aggregate(names, args.ror)

if __name__ == "__main__":
    main()