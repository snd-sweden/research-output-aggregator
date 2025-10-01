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
    #match on ROR
    matchPublisherRor: bool = False
    matchCreatorAffiliationRor: bool = False
    matchContributorAffiliationRor: bool = False
    matchFunderRor: bool = False
    #match on free text in name
    matchPublisherName: bool = False
    matchCreatorName: bool = False
    matchContributorName: bool = False
    matchFunderName: bool = False
    #where was the match found
    inDataCite: bool = None
    inOpenAire: bool = None
    inCrossRef: bool = None
    #openaire specific
    openAireBestAccessRight: str = None
    openAireIndicatorsUsageCountsDownloads: int = None
    openAireIndicatorsUsageCountsViews: int = None