from dataclasses import dataclass

@dataclass
class ResearchOutputItem:
    doi: str
    clientId: str
    publicationYear: int
    resourceType: str
    title: str
    publisher: str
    createdAt: str = ""
    updatedAt: str = "" 
    isPublisher: bool = False
    haveCreatorAffiliation: bool = False
    haveContributorAffiliation: bool = False
    isLatestVersion: bool = True
    isConceptDoi: bool = False
