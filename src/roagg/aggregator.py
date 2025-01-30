from typing import List
from roagg.ror import get_names_from_ror

def aggregate(name: List[str] = [], ror: str = ""):
    # wip, just a placeholder for printing the arguments
    if ror:
        print(f"ROR-ID: {ror}")
        print("names:", get_names_from_ror(ror))
    if name:
        for n in name:
            print(f"name: {n}")

