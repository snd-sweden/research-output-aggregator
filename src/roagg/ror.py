import urllib.request
import json

def get_ror_info(ror: str):
    ror_id = ror.split('/')[-1]
    # get the json data from the url
    url = f"https://api.ror.org/v2/organizations/{ror_id}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

def get_names_from_ror(ror: str):
    names = get_ror_info(ror)['names']
    result = []
    for n in names:
        if n['lang'] == 'en' and ("alias" in n['types'] or "ror_display" in n['types']):
            result.append(n['value'])
    return result