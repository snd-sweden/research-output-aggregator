from typing import List
import urllib.request
import logging
import json
from roagg.research_output_item import ResearchOutputItem
from roagg.utils import match_patterns

class OpenAireAPI:
    openaire_base_url = "https://api.openaire.eu/graph/v1/"

    def __init__(self, page_size: int = 100, ror: str = "", results: List[ResearchOutputItem] = []):
        self.page_size = page_size
        self.ror = ror
        self.results = results
    
    def get_openaire_id_from_ror(self) -> str:
        url = f"{self.openaire_base_url}organizations?pid={self.ror}"
        with urllib.request.urlopen(url) as response:
            json_response = json.loads(response.read())
            
            if 'results' in json_response and len(json_response['results']) > 0:
                return json_response['results'][0]['id']
            else:
                return ""

    def get_records(self) -> List[dict]:
        if not self.ror:
            return []
        openaire_results = []
        openaire_id = self.get_openaire_id_from_ror()
        
        if not openaire_id:
            logging.info(f"No OpenAire ID found for ROR {self.ror}")
            return []

        params = {
            'pageSize': self.page_size,
            'cursor': '*',
            'type': 'dataset', # limit to only datasets for now
            'relOrganizationId': openaire_id
        }
        retrieve_count = 0
        while True:
            query_string = urllib.parse.urlencode(params)
            url = f"{self.openaire_base_url}researchProducts?{query_string}"
            with urllib.request.urlopen(url) as response:
                json_response = json.loads(response.read())
                if 'results' in json_response:
                    openaire_results.extend(json_response['results'])

                retrieve_count = len(openaire_results)
                logging.info(f"Retrieved OpenAire {retrieve_count} of {json_response['header']['numFound']}")

                if 'nextCursor' in json_response['header'] and json_response['header']['nextCursor']:
                    params['cursor'] = json_response['header']['nextCursor']
                else:
                    break

        # Create a dictionary for O(1) lookups
        doi_to_item = {item.doi.lower(): item for item in self.results if item.doi}
        
        for r in openaire_results:
            openAireBestAccessRight = None
            if 'bestAccessRight' in r and r['bestAccessRight'] and 'label' in r['bestAccessRight']:
                openAireBestAccessRight = r['bestAccessRight']['label']
            
            openAireIndicatorsUsageCountsDownloads = None
            if 'indicators' in r and r['indicators'] and 'usageCounts' in r['indicators']:
                if 'downloads' in r['indicators']['usageCounts']:
                    openAireIndicatorsUsageCountsDownloads = r['indicators']['usageCounts']['downloads']

            openAireIndicatorsUsageCountsViews = None
            if 'indicators' in r and r['indicators'] and 'usageCounts' in r['indicators']:
                if 'views' in r['indicators']['usageCounts']:
                    openAireIndicatorsUsageCountsViews = r['indicators']['usageCounts']['views']
            
            dois = self.get_doi_list_from_resource(r)
            for doi in dois:
                item = doi_to_item.get(doi.lower())
                if item:
                    item.openAireBestAccessRight = openAireBestAccessRight
                    item.openAireIndicatorsUsageCountsDownloads = openAireIndicatorsUsageCountsDownloads
                    item.openAireIndicatorsUsageCountsViews = openAireIndicatorsUsageCountsViews
                    item.inOpenAire = True
        
        return openaire_results

    def get_doi_list_from_resource(self, resource: dict) -> List[str]:
        doi_list = []
        
        for instance in resource['instances']:
            logging.debug(f"Instance: {instance}")

            if 'pids' in instance and len(instance['pids']) > 0:
                for pid in instance['pids']:
                    if pid['scheme'].lower() == 'doi':
                        doi_list.append(pid['value'])

            if 'alternateIdentifiers' in instance and len(instance['alternateIdentifiers']) > 0:
                for alternateIdentifier in instance['alternateIdentifiers']:
                    if alternateIdentifier['scheme'].lower() == 'doi':
                        doi_list.append(alternateIdentifier['value'])

            if len(doi_list) == 0:
                for url in instance['urls']:
                    url = url.replace("http://dx.doi.org/", "")
                    url = url.replace("https://dx.doi.org/", "")
                    url = url.replace("https://doi.pangaea.de/", "")
                    url = url.replace("https://zenodo.org/doi/", "")
                    url = url.replace("https://zenodo.org/records/", "10.5281/zenodo.")

                    if match_patterns(url, [r'10\.\d{4,9}/[-._;()/:A-Z0-9]+$']):
                        doi_list.append(url)

        # if doi_list is empty print json for instances
        if len(doi_list) == 0:
            logging.warning(f"No DOI found in resource: {json.dumps(resource['instances'], indent=2)}")

        return list(set(doi_list))



