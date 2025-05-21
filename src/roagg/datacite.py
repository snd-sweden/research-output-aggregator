from typing import List
import urllib.request
import logging
import json
from roagg.research_output_item import ResearchOutputItem
from roagg.utils import match_patterns

class DataCiteAPI:
    def __init__(self, page_size: int = 500, name: List[str] = [], ror: str = ""):
        self.page_size = page_size
        self.name = name
        self.ror = ror

    def get_query_string(self) -> str:
        if not self.name and not self.ror:
            return ""
            
        query_parts = []
        
        if self.name:
            name_conditions = ' OR '.join(f'"{n}"' for n in self.name)
            name_fields = [
                "creators.affiliation.name",
                "contributors.affiliation.name", 
                "publisher.name"
                # "creators.name",
                # "contributors.name"
            ]
            
            query_parts.extend([f"{field}:({name_conditions})" for field in name_fields])
        
        if self.ror:
            ror_fields = [
                "publisher.publisherIdentifier",
                "creators.affiliation.affiliationIdentifier", 
                "contributors.affiliation.affiliationIdentifier",
                "creators.nameIdentifiers.nameIdentifier",
                "contributors.nameIdentifiers.nameIdentifier"
            ]
            query_parts.extend([f'{field}:"{self.ror}"' for field in ror_fields])
            # nameIdentifiers are formated without https://ror.org/ prefix from some sources, so we need to check both
            query_parts.extend([f'{field}:"{self.ror.split("https://ror.org/")[1]}"' for field in ror_fields])
        
        return " OR ".join(query_parts)

    def api_request_url(self, page_size: int = None) -> str:
        if page_size is None:
            page_size = self.page_size
        params = urllib.parse.urlencode({
            'page[size]': page_size,
            'affiliation': 'true',
            'publisher': 'true',
            'detail': 'true',
            'query': self.get_query_string()
        })
        return f"https://api.datacite.org/dois?{params}"

    @staticmethod
    def get_api_result(url: str) -> dict:
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed run DataCite query: {e}")
    
    def get_record(self, item: dict) -> ResearchOutputItem:
        attributes = item.get("attributes", {})
        publisher_attr = attributes.get("publisher", {})
        versionCount = 0 if attributes.get("versionCount", {}) is None else int(attributes.get("versionCount", {}))
        versionOfCount = 0 if attributes.get("versionOfCount", {}) is None else int(attributes.get("versionOfCount", {}))

        record = ResearchOutputItem(
            doi=attributes.get("doi"),
            clientId=item["relationships"]["client"]["data"]["id"],
            resourceType=attributes.get("types", None).get("citeproc"),
            publisher=publisher_attr.get("name"),
            publicationYear=attributes.get("publicationYear"),
            title=item["attributes"]["titles"][0]["title"],
        )

        if record.resourceType is None or record.resourceType == "":
            record.resourceType = attributes.get("types", {}).get("bibtex")

        record.isPublisher = (
            publisher_attr.get("publisherIdentifier") == self.ror or 
            match_patterns(publisher_attr.get("name"), self.name)
        )

        for relation in attributes.get("relatedIdentifiers", []):
            if relation.get("relationType") == "IsPreviousVersionOf":
                record.isLatestVersion = False
            if relation.get("relationType") == "HasVersion":
                record.isLatestVersion = False

        record.isConceptDoi = (
            versionCount > 0 and
            versionOfCount == 0   
        )

        record.haveCreatorAffiliation = self.check_agent_list_match(attributes.get("creators", []))
        record.haveContributorAffiliation = self.check_agent_list_match(attributes.get("contributors", []))
        return record

    def check_agent_list_match(self, items: list) -> bool:
        partial_ror = self.ror.split("https://ror.org/")[1] if self.ror else ""
        for agent in items:
            # Check if any nameIdentifier matches the ror
            if any(identifier.get("nameIdentifier") == self.ror for identifier in agent.get("nameIdentifiers", [])):
                return True
            # Check if any nameIdentifier matches the partial ror
            if any(identifier.get("nameIdentifier") == partial_ror for identifier in agent.get("nameIdentifiers", [])):
                return True
            # Check if the agent name matches any pattern
            if match_patterns(agent.get("name"), self.name):
                return True
            # Check each affiliation
            for affiliation in agent.get("affiliation", []):
                if (affiliation.get("affiliationIdentifier") == self.ror or 
                        match_patterns(affiliation.get("name"), self.name)):
                    return True
        return False

    def all(self) -> list:
        result = []
        url = self.api_request_url()
        while True:
            response = self.get_api_result(url)
            result.extend(response["data"])
            logging.info(f"Retrieved {len(result)} of {response['meta']['total']}")
            if response['links'].get('next'):
                url = response['links']['next']
            else:
                break
        return result

    def count(self) -> int:
        if not self.get_query_string():
            return 0
        url = self.api_request_url(page_size=0)
        return self.get_api_result(url)["meta"]["total"]