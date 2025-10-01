import sys
from typing import List
from roagg.ror import get_names_from_ror
from roagg.datacite import DataCiteAPI
from roagg.openaire import OpenAireAPI
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

    openaire = OpenAireAPI(ror=ror, results=research_output_items)
    openaire_id = openaire.get_openaire_id_from_ror()
    logging.info(f"OpenAire ID from ROR {ror} : {openaire_id}")
    records = openaire.get_records()

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
                "updatedAt",
                "inDataCite",
                "inOpenAire",
                "openAireBestAccessRight",
                "openAireIndicatorsDownloads",
                "openAireIndicatorsViews",
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
                r.updatedAt,
                1 if r.inDataCite else 0 if r.inDataCite is not None else "",
                1 if r.inOpenAire else 0 if r.inOpenAire is not None else "",
                r.openAireBestAccessRight if r.openAireBestAccessRight is not None else "",
                r.openAireIndicatorsUsageCountsDownloads if r.openAireIndicatorsUsageCountsDownloads is not None else "",
                r.openAireIndicatorsUsageCountsViews if r.openAireIndicatorsUsageCountsViews is not None else "",
            ]
            for r in records
        ])
