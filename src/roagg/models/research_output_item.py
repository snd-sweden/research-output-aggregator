from dataclasses import dataclass

@dataclass
class ResearchOutputItem:
    doi: str
    dataCiteClientId: str = None
    dataCiteClientName: str = None
    publicationYear: int = None
    resourceType: str = None
    title: str = None
    publisher: str = None
    createdAt: str = ""
    updatedAt: str = "" 
    isPublisher: bool = False
    isFunder: bool = None
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
    inOpenAlex: bool = None
    inCrossRef: bool = None
    #openaire specific
    openAireBestAccessRight: str = None
    openAireIndicatorsUsageCountsDownloads: int = None
    openAireIndicatorsUsageCountsViews: int = None
    openAireId: str = None
    #openalex specific
    openAlexId: str = None
    openAlexCitedByCount: int = None
    openAlexReferencedWorksCount: int = None
    #extra fields
    titleWordCount: int = None
    referencedByDoi: str = None
