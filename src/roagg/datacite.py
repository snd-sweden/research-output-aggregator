from typing import List

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
    
    return " OR ".join(query_parts)