from dataclasses import dataclass

@dataclass
class ResearchOutputItem:
    doi: str
    clientId: str
    publicationYear: int
    resourceType: str
    publisher: str
    isPublisher: bool = False
    haveCreatorAffiliation: bool = False
    haveContributorAffiliation: bool = False
    isLatestVersion: bool = True
