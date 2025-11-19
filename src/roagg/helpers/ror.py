import urllib.request
import json
from typing import List

def get_ror_info(ror: str):
    ror_id = ror.split('/')[-1]
    url = f"https://api.ror.org/v2/organizations/{ror_id}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

def get_names_from_ror(ror: str) -> List[str]:
    names = get_ror_info(ror)['names']
    valid_types = {'alias', 'ror_display', 'label'}
    return [n['value'] for n in names if valid_types.intersection(n['types'])]