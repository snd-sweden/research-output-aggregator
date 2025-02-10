from typing import List
import urllib.request
import logging
import json

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
                "publisher.name",
                "creators.name",
                "contributors.name"
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