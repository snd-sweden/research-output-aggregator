# Research output aggregator

The goal of this project is to create a script to get a summarization for a research organization about the research output.  
First target is to query and process information from DataCite.  

input: ROR-id and list of variants on the organization name.

Properties to get:
```
string doi
int publicationYear
string resourceType
bool haveContributorAffiliation
bool haveCreatorAffiliation
bool isPublisher
bool isLatestVersion
```
