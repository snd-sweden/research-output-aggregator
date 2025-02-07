from typing import List
import urllib.request
import json

def create_datacite_query_string(name: List[str] = [], ror: str = ""):
    if not name and not ror:
        return ""
        
    query_parts = []
    
    if name:
        name_conditions = ' OR '.join(f'"{n}"' for n in name)
        fields = [
            "creators.affiliation.name",
            "contributors.affiliation.name", 
            "publisher.name"
        ]
        
        name_queries = [f"{field}:({name_conditions})" for field in fields]
        query_parts.extend(name_queries)
    
    if ror:
        query_parts.append(f'publisher.publisherIdentifier:"{ror}"')
        query_parts.append(f'creators.affiliation.affiliationIdentifier:"{ror}"')
        query_parts.append(f'contributors.affiliation.affiliationIdentifier:"{ror}"')
    
    return " OR ".join(query_parts)

def datacite_query_result_count(query: str) -> int:
    """Get total number of results for a DataCite query."""
    if not query:
        return 0
        
    try:
        params = urllib.parse.urlencode({
            'page[size]': 0,
            'query': query
        })
        url = f"https://api.datacite.org/dois?{params}"
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data["meta"]["total"]
            
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"Failed to get result count from DataCite: {e}")


