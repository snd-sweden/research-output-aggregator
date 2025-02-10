from typing import List
from roagg.ror import get_names_from_ror
from roagg.datacite import DataCiteAPI
import logging
from roagg.research_output_item import ResearchOutputItem
import json
import csv

def aggregate(name: List[str] = [], ror: str = "", output: str = "output.csv") -> None:
    if ror:
        ror_name = get_names_from_ror(ror)
        name.extend(ror_name)
    
    # remove duplicates
    name = list(set(name))

    datacite = DataCiteAPI(name=name, ror=ror)
    url = datacite.api_request_url()
    # debug print of the query string
    logging.info("DataCite url:")
    logging.info(url)

    records = datacite.all()
    research_output_items = []
    logging.info(f"Checking {len(records)} records...")
    for record in records:
        research_output_items.append(datacite.get_record(record))
    
    logging.info(f"Writing: {output}")
    write_csv(research_output_items, output)
    logging.info(f"Writing: {output} - Done")


def write_csv(records: List[str], output: str) -> None:
    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = [
                    "doi", 
                    "publicationYear", 
                    "resourceType", 
                    "publisher", 
                    "isPublisher", 
                    "haveCreatorAffiliation", 
                    "haveContributorAffiliation", 
                    "isLatestVersion"
                ]

        writer.writerow(field)
        for v in records:
            
            writer.writerow([
                    v.doi, 
                    v.publicationYear, 
                    v.resourceType, 
                    v.publisher, 
                    v.isPublisher, 
                    v.haveCreatorAffiliation, 
                    v.haveContributorAffiliation, 
                    v.isLatestVersion
                ])
