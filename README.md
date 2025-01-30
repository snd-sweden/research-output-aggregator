# Research output aggregator

The goal of this project is to create a script to get a summarization for a research organization about the research output.  
First target is to query and process information from DataCite.  

The goal for this script is to create a list over research output where an organization is mentioned as:
* publisher
* creator with affiliation to the organization
* contributor with affiliation to the organization

input: ROR-id and list of variants on the organization name.

Properties to collect for each research output:
```
string doi
int publicationYear
string resourceType
bool isPublisher
bool haveCreatorAffiliation
bool haveContributorAffiliation
bool isLatestVersion
```

## Install dependencies
`pip install .`

## Run during development
`PYTHONPATH=src python src/roagg/cli.py`

