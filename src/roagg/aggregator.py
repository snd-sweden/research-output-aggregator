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
    logging.info(f"Writing output to csv: {output} - Done")

def write_csv(records: List[str], output: str,) -> None:
    header = [
                "doi", 
                "clientId",
                "publicationYear", 
                "resourceType",
                "title", 
                "publisher", 
                "isPublisher", 
                "haveCreatorAffiliation", 
                "haveContributorAffiliation", 
                "isLatestVersion",
                "isConceptDoi",
                "createdAt",
                "updatedAt"
            ]

    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        writer.writerows([
            [
                r.doi,
                r.clientId,
                r.publicationYear,
                r.resourceType,
                r.title,
                r.publisher,
                1 if r.isPublisher else 0,
                1 if r.haveCreatorAffiliation else 0,
                1 if r.haveContributorAffiliation else 0,
                1 if r.isLatestVersion else 0,
                1 if r.isConceptDoi else 0,
                r.createdAt,
                r.updatedAt
            ]
            for r in records
        ])
