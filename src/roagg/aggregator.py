from typing import List
from roagg.ror import get_names_from_ror
from roagg.datacite import DataCiteAPI
import logging
import json

def aggregate(name: List[str] = [], ror: str = "") -> None:
    if ror:
        ror_name = get_names_from_ror(ror)
        name.extend(ror_name)
    
    # remove duplicates
    name = list(set(name))

    # debug print of the query string
    datacite = DataCiteAPI(name=name, ror=ror)
    url = datacite.api_request_url()
    count = datacite.count()
    logging.info("DataCite url:")
    logging.info(url)
    logging.info(f"Result count: {count}")
