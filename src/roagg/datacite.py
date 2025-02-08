from typing import List
import urllib.request
import logging
import json

def create_datacite_query_string(name: List[str] = [], ror: str = "") -> str:
    if not name and not ror:
        return ""
        
    query_parts = []
    
    if name:
        name_conditions = ' OR '.join(f'"{n}"' for n in name)
        name_fields = [
            "creators.affiliation.name",
            "contributors.affiliation.name", 
            "publisher.name",
            "creators.name",
            "contributors.name"
        ]
        
        query_parts.extend([f"{field}:({name_conditions})" for field in name_fields])
    
    if ror:
        ror_fields = [
            "publisher.publisherIdentifier",
            "creators.affiliation.affiliationIdentifier", 
            "contributors.affiliation.affiliationIdentifier",
            "creators.nameIdentifiers.nameIdentifier",
            "contributors.nameIdentifiers.nameIdentifier"
        ]

        query_parts.extend([f'{field}:"{ror}"' for field in ror_fields])
    
    return " OR ".join(query_parts)

def api_request_url(query: str, page_size: int = 100) -> str:    
    params = urllib.parse.urlencode({
        'page[size]': page_size,
        'affiliation': 'true',
        'publisher': 'true',
        'query': query
    })
    return f"https://api.datacite.org/dois?{params}"

def get_api_result(url: str) -> dict:
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
      
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"Failed run DataCite query: {e}")
    
def api_all(query: str) -> list:
    result = []
    page_size = 500
    url = api_request_url(query, page_size)
    while True:
        response = get_api_result(url)
        result.extend(response["data"])
        logging.info(f"Retrieved {len(result)} of {response['meta']['total']}")
        if response['links'].get('next'):
            url = response['links']['next']
        else:
            break
    
    return result

def datacite_query_result_count(query: str) -> int:
    if not query:
        return 0
    url = api_request_url(query, 0)
    return get_api_result(url)["meta"]["total"]