# Research output aggregator 
> [!NOTE]
> This script is under development

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

## Install
`pip install .`

## Install dev
`pip install -e .`

## Development stuff to do
- [x] ROR get name variants from ROR
- [x] CLI add options to get name list from txt
- [ ] DataCite API build query for matching publisher and affiliation
- [ ] Crossref API build query for matching publisher and affiliation

## Run
List arguments:  
`roagg --help`  

### Some example arguments
Chalmers with ror and name list:  
```bash
roagg --ror https://ror.org/040wg7k59 --name-txt tests/name-lists/chalmers.txt
```

GU with ror, name list and extra name not in the text file:  
```bash
roagg --name "Department of Nephrology Gothenburg" --ror https://ror.org/01tm6cn81 --name-txt tests/name-lists/gu.txt
```

KTH with ror and name list:  
```bash
roagg --ror https://ror.org/026vcq606 --name-txt tests/name-lists/kth.txt
```
