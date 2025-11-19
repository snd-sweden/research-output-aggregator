from typing import List
import urllib.request
import logging
import json
from roagg.models.research_output_item import ResearchOutputItem
from roagg.helpers.utils import string_word_count, remove_resolver_prefix_from_doi

class OpenAlexAPI:
    openalex_base_url = "https://api.openalex.org/"

    def __init__(self, page_size: int = 200, ror: str = "", results: List[ResearchOutputItem] = []):
        self.page_size = page_size
        self.ror = ror
        self.results = results

    def get_openalex_id_from_ror(self) -> str:
        url = f"{self.openalex_base_url}institutions/ror:{self.ror}"
        with urllib.request.urlopen(url) as response:
            json_response = json.loads(response.read())
            
            if 'id' in json_response:
                return json_response['id']
            else:
                return ""
            
    def get_records(self) -> List[ResearchOutputItem]:
        if not self.ror:
            return []
        openalex_results = []
        openalex_id = self.get_openalex_id_from_ror()
        
        if not openalex_id:
            logging.info(f"No OpenAlex ID found for ROR {self.ror}")
            return []

        params = {
            'per-page': self.page_size,
            'cursor': '*',
            'filter': f'institutions.id:{openalex_id},type:dataset' # limit to only datasets for now
        }
        retrieve_count = 0

        while True:
            query_string = urllib.parse.urlencode(params)
            url = f"{self.openalex_base_url}works?{query_string}"
            with urllib.request.urlopen(url) as response:
                json_response = json.loads(response.read())
                if 'results' in json_response:
                    openalex_results.extend(json_response['results'])
                retrieve_count = len(openalex_results)
                logging.info(f"Retrieved OpenAlex {retrieve_count} of {json_response['meta']['count']}")

                if 'next_cursor' in json_response['meta'] and json_response['meta']['next_cursor']:
                    params['cursor'] = json_response['meta']['next_cursor']
                else:
                    break

        # Create a dictionary for O(1) lookups
        doi_to_item = {item.doi.lower(): item for item in self.results if item.doi}
        
        for r in openalex_results:
            openAlexCitedByCount = None
            if 'cited_by_count' in r:
                openAlexCitedByCount = r['cited_by_count']

            openAlexReferencedWorksCount = None
            if 'referenced_works_count' in r:
                openAlexReferencedWorksCount = r['referenced_works_count']

            haveCreatorAffiliation = False
 
            for authorship in r.get('institutions', []):
                for affiliation in authorship.get('institutions', []):
                    if affiliation.get('ror') == self.ror:
                        haveCreatorAffiliation = True
                        break

            doi = remove_resolver_prefix_from_doi(r.get('doi', None))

            item = doi_to_item.get(doi.lower())
            if item:
                recordMatch = True
                item.openAlexCitedByCount = openAlexCitedByCount
                item.openAlexReferencedWorksCount = openAlexReferencedWorksCount
                item.inOpenAlex = True
                item.openAlexId = r.get('id', None)
                item.haveCreatorAffiliation = haveCreatorAffiliation
            if not recordMatch and len(dois) > 0:
                publication_date = r.get('publication_date', None)
                publication_year = r.get('publication_year', None)
                if publication_date:
                    publication_year = publication_date[:4] if len(publication_date) >= 4 else None
                item = ResearchOutputItem(
                    doi=doi,
                    isPublisher=None,
                    resourceType=r.get('type', None),
                    title=r.get('title', None),
                    publisher=None,
                    publicationYear=publication_year,
                    createdAt=r.get('created_date', None),
                    updatedAt=r.get('updated_date', None),
                    haveContributorAffiliation=None,
                    haveCreatorAffiliation=haveCreatorAffiliation,
                    isLatestVersion=None,   
                    isConceptDoi=None,
                    inOpenAlex=True,
                    openAlexCitedByCount=openAlexCitedByCount,
                    openAlexReferencedWorksCount=openAlexReferencedWorksCount,
                    openAlexId=r.get('id', None),
                    titleWordCount=string_word_count(r.get('title', None))
                )
                self.results.append(item)
                doi_to_item[item.doi.lower()] = item  # Add to lookup dictionary

        return openalex_results