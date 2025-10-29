import csv
import logging
from typing import List

from roagg.datacite import DataCiteAPI
from roagg.openaire import OpenAireAPI
from roagg.research_output_item import ResearchOutputItem
from roagg.ror import get_names_from_ror
from roagg.utils import wildcard_match


def aggregate(name: List[str] = [], ror: str = "", output: str = "output.csv") -> None:
    # Store original name filters for client-side processing.
    # DataCiteAPI may not interpret wildcards, and we don't want to use ROR-derived names
    # as wildcard patterns. Use a set for automatic de-duplication.
    original_name_filters = set(name)

    # Combine original names with ROR-derived names for the DataCiteAPI query.
    api_query_names = set(name)
    if ror:
        ror_names = get_names_from_ror(ror)
        api_query_names.update(ror_names)

    datacite = DataCiteAPI(name=list(api_query_names), ror=ror)
    url = datacite.api_request_url()
    logging.info("DataCite url:")
    logging.info(url)

    records = datacite.all()

    # Process all records received from DataCite into ResearchOutputItem objects first.
    # This allows for consistent client-side filtering afterwards.
    all_parsed_items = []
    logging.info(f"Attempting to parse {len(records)} records retrieved from DataCite...")
    for record in records:
        item = datacite.get_record(record)
        if item:  # get_record might return None if parsing fails
            all_parsed_items.append(item)

    logging.info(f"Successfully parsed {len(all_parsed_items)} research output items from DataCite results.")

    # Apply client-side filtering using wildcard_match if original_name_filters were provided.
    if original_name_filters:
        logging.info(f"Applying client-side name filters: {original_name_filters}")
        # An item is kept if its title or publisher matches ANY of the provided patterns.
        research_output_items = [
            item for item in all_parsed_items
            if any(
                wildcard_match(pattern, item.title or "") or wildcard_match(pattern, item.publisher or "")
                for pattern in original_name_filters
            )
        ]
        logging.info(f"Filtered down to {len(research_output_items)} items after applying name filters.")
    else:
        # If no client-side name filters, all parsed items are kept.
        research_output_items = all_parsed_items

    openaire = OpenAireAPI(ror=ror, results=research_output_items)
    openaire_id = openaire.get_openaire_id_from_ror()
    logging.info(f"OpenAire ID from ROR {ror} : {openaire_id}")
    openaire.get_records()

    logging.info(f"Writing: {output}")

    write_csv(research_output_items, output)
    logging.info(f"Writing output to csv: {output} - Done")


def write_csv(records: List[ResearchOutputItem], output: str,) -> None:
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
                "titleWordCount",
                "referencedByDOI",
            ]

    with open(output, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        writer.writerows([
            [
                r.doi,
                r.clientId if r.clientId is not None else "",
                r.publicationYear,
                r.resourceType,
                r.title,
                r.publisher,
                1 if r.isPublisher else 0 if r.isPublisher is not None else "",
                1 if r.haveCreatorAffiliation else 0 if r.haveCreatorAffiliation is not None else "",
                1 if r.haveContributorAffiliation else 0 if r.haveContributorAffiliation is not None else "",
                1 if r.isLatestVersion else 0 if r.isLatestVersion is not None else "",
                1 if r.isConceptDoi else 0 if r.isConceptDoi is not None else "",
                r.createdAt,
                r.updatedAt,
                1 if r.inDataCite else 0 if r.inDataCite is not None else "",
                1 if r.inOpenAire else 0 if r.inOpenAire is not None else "",
                r.openAireBestAccessRight if r.openAireBestAccessRight is not None else "",
                r.openAireIndicatorsUsageCountsDownloads if r.openAireIndicatorsUsageCountsDownloads is not None else "",
                r.openAireIndicatorsUsageCountsViews if r.openAireIndicatorsUsageCountsViews is not None else "",
                r.titleWordCount if r.titleWordCount is not None else "",
                r.referencedByDoi if r.referencedByDoi is not None else "",
            ]
            for r in records
        ])