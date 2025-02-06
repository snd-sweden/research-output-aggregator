from typing import List
from roagg.ror import get_names_from_ror
from roagg.datacite import create_datacite_query_string, datacite_query_result_count

def aggregate(name: List[str] = [], ror: str = ""):
    # if ror is provided, get the name from the ror api
    if ror:
        ror_name = get_names_from_ror(ror)
        name.extend(ror_name)
    
    # remove duplicates
    name = list(set(name))

    # debug print of the query string
    query = create_datacite_query_string(name, ror)
    query_result_count = datacite_query_result_count(query)
    print("DataCite query:")
    print(query)
    print(f"Result count: {query_result_count}")
