# Auto generated from nmdc_sfas_brcs.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-05-19T20:51:07
# Schema: nmdc-sfas-brcs
#
# id: https://w3id.org/nmdc/sfas-brcs
# description: A LinkML schema for representing DOE BER (Biological and Environmental Research)
#   funded Scientific Focus Areas (SFAs) and Bioenergy Research Centers (BRCs),
#   including their metadata, datasets, publications, and organizational structure.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URI, URIorCURIE, XSDDate

metamodel_version = "1.7.0"
version = None

# Namespaces
BERVO = CurieNamespace('BERVO', 'https://w3id.org/bervo/BERVO_')
EFO = CurieNamespace('EFO', 'http://www.ebi.ac.uk/efo/EFO_')
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
MIXS = CurieNamespace('MIXS', 'https://w3id.org/mixs/')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
STATO = CurieNamespace('STATO', 'http://purl.obolibrary.org/obo/STATO_')
COMMUNITYMECH = CurieNamespace('communitymech', 'https://w3id.org/communitymech/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
DOI = CurieNamespace('doi', 'https://doi.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NMDC_SFAS_BRCS = CurieNamespace('nmdc_sfas_brcs', 'https://w3id.org/nmdc/sfas-brcs/')
OBO = CurieNamespace('obo', 'http://purl.obolibrary.org/obo/')
ORCID = CurieNamespace('orcid', 'https://orcid.org/')
PMID = CurieNamespace('pmid', 'https://www.ncbi.nlm.nih.gov/pubmed/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
ROR = CurieNamespace('ror', 'https://ror.org/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
DEFAULT_ = NMDC_SFAS_BRCS


# Types

# Class references
class NamedThingId(URIorCURIE):
    pass


class ResearchProgramId(NamedThingId):
    pass


class BioenergyResearchCenterId(ResearchProgramId):
    pass


class ScientificFocusAreaId(ResearchProgramId):
    pass


class OtherProgramId(ResearchProgramId):
    pass


class ArtificialIntelligenceProjectId(OtherProgramId):
    pass


class UserFacilityId(NamedThingId):
    pass


class OntologyTermId(URIorCURIE):
    pass


class BERVOTermId(OntologyTermId):
    pass


class MIXSTermId(OntologyTermId):
    pass


class ReferenceId(URIorCURIE):
    pass


class FieldSiteId(NamedThingId):
    pass


class AnalysisId(NamedThingId):
    pass


class KBaseNarrativeId(AnalysisId):
    pass


@dataclass(repr=False)
class ResearchProgramCollection(YAMLRoot):
    """
    A container for DOE BER funded research programs including Bioenergy Research Centers (BRCs), Scientific Focus
    Areas (SFAs), and User Facilities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ResearchProgramCollection"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ResearchProgramCollection"
    class_name: ClassVar[str] = "ResearchProgramCollection"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ResearchProgramCollection

    bioenergy_research_centers: Optional[Union[dict[Union[str, BioenergyResearchCenterId], Union[dict, "BioenergyResearchCenter"]], list[Union[dict, "BioenergyResearchCenter"]]]] = empty_dict()
    genomic_science_sfas: Optional[Union[dict[Union[str, ScientificFocusAreaId], Union[dict, "ScientificFocusArea"]], list[Union[dict, "ScientificFocusArea"]]]] = empty_dict()
    environmental_system_science_sfas: Optional[Union[dict[Union[str, ScientificFocusAreaId], Union[dict, "ScientificFocusArea"]], list[Union[dict, "ScientificFocusArea"]]]] = empty_dict()
    user_facilities: Optional[Union[dict[Union[str, UserFacilityId], Union[dict, "UserFacility"]], list[Union[dict, "UserFacility"]]]] = empty_dict()
    other_programs: Optional[Union[dict[Union[str, OtherProgramId], Union[dict, "OtherProgram"]], list[Union[dict, "OtherProgram"]]]] = empty_dict()
    ai_projects: Optional[Union[dict[Union[str, ArtificialIntelligenceProjectId], Union[dict, "ArtificialIntelligenceProject"]], list[Union[dict, "ArtificialIntelligenceProject"]]]] = empty_dict()
    sites: Optional[Union[dict[Union[str, FieldSiteId], Union[dict, "FieldSite"]], list[Union[dict, "FieldSite"]]]] = empty_dict()
    metadata: Optional[Union[dict, "CollectionMetadata"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="bioenergy_research_centers", slot_type=BioenergyResearchCenter, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="genomic_science_sfas", slot_type=ScientificFocusArea, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="environmental_system_science_sfas", slot_type=ScientificFocusArea, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="user_facilities", slot_type=UserFacility, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="other_programs", slot_type=OtherProgram, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="ai_projects", slot_type=ArtificialIntelligenceProject, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="sites", slot_type=FieldSite, key_name="id", keyed=True)

        if self.metadata is not None and not isinstance(self.metadata, CollectionMetadata):
            self.metadata = CollectionMetadata(**as_dict(self.metadata))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CollectionMetadata(YAMLRoot):
    """
    Metadata about the research program collection
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["CollectionMetadata"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:CollectionMetadata"
    class_name: ClassVar[str] = "CollectionMetadata"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.CollectionMetadata

    compiled_date: Optional[str] = None
    sources: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.compiled_date is not None and not isinstance(self.compiled_date, str):
            self.compiled_date = str(self.compiled_date)

        if not isinstance(self.sources, list):
            self.sources = [self.sources] if self.sources is not None else []
        self.sources = [v if isinstance(v, str) else str(v) for v in self.sources]

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Thing"]
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.NamedThing

    id: Union[str, NamedThingId] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResearchProgram(NamedThing):
    """
    A DOE BER funded research program. This is the common parent class for Bioenergy Research Centers (BRCs) and
    Scientific Focus Areas (SFAs). Both program types share common attributes including funding, institutions,
    personnel, research focus, and outputs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ResearchProgram"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ResearchProgram"
    class_name: ClassVar[str] = "ResearchProgram"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ResearchProgram

    id: Union[str, ResearchProgramId] = None
    name: str = None
    acronym: Optional[str] = None
    program_type: Optional[Union[str, "ProgramType"]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    lead_institution: Optional[str] = None
    partner_institutions: Optional[Union[str, list[str]]] = empty_list()
    principal_investigators: Optional[Union[Union[dict, "Person"], list[Union[dict, "Person"]]]] = empty_list()
    funding: Optional[Union[dict, "FundingInfo"]] = None
    location: Optional[Union[dict, "Location"]] = None
    websites: Optional[Union[dict, "WebResources"]] = None
    scientific_questions: Optional[Union[str, list[str]]] = empty_list()
    keywords: Optional[Union[Union[str, "Keyword"], list[Union[str, "Keyword"]]]] = empty_list()
    data_types: Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]] = empty_list()
    data_collection_modalities: Optional[Union[Union[str, "DataCollectionModality"], list[Union[str, "DataCollectionModality"]]]] = empty_list()
    interaction_types: Optional[Union[Union[str, "InteractionType"], list[Union[str, "InteractionType"]]]] = empty_list()
    interaction_modes: Optional[Union[Union[str, "InteractionMode"], list[Union[str, "InteractionMode"]]]] = empty_list()
    nmdc_umbrella_study: Optional[Union[str, URIorCURIE]] = None
    studies: Optional[Union[Union[dict, "NMDCStudyReference"], list[Union[dict, "NMDCStudyReference"]]]] = empty_list()
    analyses: Optional[Union[dict[Union[str, KBaseNarrativeId], Union[dict, "KBaseNarrative"]], list[Union[dict, "KBaseNarrative"]]]] = empty_dict()
    kbase_genome_collection: Optional[Union[str, "KBaseCollection"]] = None
    datasets: Optional[Union[Union[dict, "Dataset"], list[Union[dict, "Dataset"]]]] = empty_list()
    field_site_ids: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    key_publications: Optional[Union[dict[Union[str, ReferenceId], Union[dict, "Reference"]], list[Union[dict, "Reference"]]]] = empty_dict()
    established: Optional[int] = None
    collaborators: Optional[str] = None
    isolate_collections: Optional[Union[Union[dict, "IsolateCollection"], list[Union[dict, "IsolateCollection"]]]] = empty_list()
    research_resources: Optional[Union[Union[dict, "ResearchResource"], list[Union[dict, "ResearchResource"]]]] = empty_list()
    phenotype_assays: Optional[Union[Union[str, "PhenotypeAssayType"], list[Union[str, "PhenotypeAssayType"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResearchProgramId):
            self.id = ResearchProgramId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.acronym is not None and not isinstance(self.acronym, str):
            self.acronym = str(self.acronym)

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = ProgramType(self.program_type)

        if self.start_date is not None and not isinstance(self.start_date, str):
            self.start_date = str(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, str):
            self.end_date = str(self.end_date)

        if self.lead_institution is not None and not isinstance(self.lead_institution, str):
            self.lead_institution = str(self.lead_institution)

        if not isinstance(self.partner_institutions, list):
            self.partner_institutions = [self.partner_institutions] if self.partner_institutions is not None else []
        self.partner_institutions = [v if isinstance(v, str) else str(v) for v in self.partner_institutions]

        if not isinstance(self.principal_investigators, list):
            self.principal_investigators = [self.principal_investigators] if self.principal_investigators is not None else []
        self.principal_investigators = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.principal_investigators]

        if self.funding is not None and not isinstance(self.funding, FundingInfo):
            self.funding = FundingInfo(**as_dict(self.funding))

        if self.location is not None and not isinstance(self.location, Location):
            self.location = Location(**as_dict(self.location))

        if self.websites is not None and not isinstance(self.websites, WebResources):
            self.websites = WebResources(**as_dict(self.websites))

        if not isinstance(self.scientific_questions, list):
            self.scientific_questions = [self.scientific_questions] if self.scientific_questions is not None else []
        self.scientific_questions = [v if isinstance(v, str) else str(v) for v in self.scientific_questions]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, Keyword) else Keyword(v) for v in self.keywords]

        if not isinstance(self.data_types, list):
            self.data_types = [self.data_types] if self.data_types is not None else []
        self.data_types = [v if isinstance(v, DataType) else DataType(v) for v in self.data_types]

        if not isinstance(self.data_collection_modalities, list):
            self.data_collection_modalities = [self.data_collection_modalities] if self.data_collection_modalities is not None else []
        self.data_collection_modalities = [v if isinstance(v, DataCollectionModality) else DataCollectionModality(v) for v in self.data_collection_modalities]

        if not isinstance(self.interaction_types, list):
            self.interaction_types = [self.interaction_types] if self.interaction_types is not None else []
        self.interaction_types = [v if isinstance(v, InteractionType) else InteractionType(v) for v in self.interaction_types]

        if not isinstance(self.interaction_modes, list):
            self.interaction_modes = [self.interaction_modes] if self.interaction_modes is not None else []
        self.interaction_modes = [v if isinstance(v, InteractionMode) else InteractionMode(v) for v in self.interaction_modes]

        if self.nmdc_umbrella_study is not None and not isinstance(self.nmdc_umbrella_study, URIorCURIE):
            self.nmdc_umbrella_study = URIorCURIE(self.nmdc_umbrella_study)

        if not isinstance(self.studies, list):
            self.studies = [self.studies] if self.studies is not None else []
        self.studies = [v if isinstance(v, NMDCStudyReference) else NMDCStudyReference(**as_dict(v)) for v in self.studies]

        self._normalize_inlined_as_list(slot_name="analyses", slot_type=KBaseNarrative, key_name="id", keyed=True)

        if self.kbase_genome_collection is not None and not isinstance(self.kbase_genome_collection, KBaseCollection):
            self.kbase_genome_collection = KBaseCollection(self.kbase_genome_collection)

        if not isinstance(self.datasets, list):
            self.datasets = [self.datasets] if self.datasets is not None else []
        self.datasets = [v if isinstance(v, Dataset) else Dataset(**as_dict(v)) for v in self.datasets]

        if not isinstance(self.field_site_ids, list):
            self.field_site_ids = [self.field_site_ids] if self.field_site_ids is not None else []
        self.field_site_ids = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.field_site_ids]

        self._normalize_inlined_as_list(slot_name="key_publications", slot_type=Reference, key_name="id", keyed=True)

        if self.established is not None and not isinstance(self.established, int):
            self.established = int(self.established)

        if self.collaborators is not None and not isinstance(self.collaborators, str):
            self.collaborators = str(self.collaborators)

        if not isinstance(self.isolate_collections, list):
            self.isolate_collections = [self.isolate_collections] if self.isolate_collections is not None else []
        self.isolate_collections = [v if isinstance(v, IsolateCollection) else IsolateCollection(**as_dict(v)) for v in self.isolate_collections]

        if not isinstance(self.research_resources, list):
            self.research_resources = [self.research_resources] if self.research_resources is not None else []
        self.research_resources = [v if isinstance(v, ResearchResource) else ResearchResource(**as_dict(v)) for v in self.research_resources]

        if not isinstance(self.phenotype_assays, list):
            self.phenotype_assays = [self.phenotype_assays] if self.phenotype_assays is not None else []
        self.phenotype_assays = [v if isinstance(v, PhenotypeAssayType) else PhenotypeAssayType(v) for v in self.phenotype_assays]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioenergyResearchCenter(ResearchProgram):
    """
    A DOE Bioenergy Research Center (BRC). BRCs are large-scale, multi-institutional research centers focused on
    developing sustainable biofuels and bioproducts from plant biomass. The BRC program is part of the Genomic Science
    portfolio within DOE's Office of Science Office of Biological and Environmental Research.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OBI["0000835"]
    class_class_curie: ClassVar[str] = "OBI:0000835"
    class_name: ClassVar[str] = "BioenergyResearchCenter"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.BioenergyResearchCenter

    id: Union[str, BioenergyResearchCenterId] = None
    name: str = None
    outputs: Optional[Union[dict, "ProgramOutputs"]] = None
    predecessor: Optional[str] = None
    program_type: Optional[Union[str, "ProgramType"]] = 'BIOENERGY_RESEARCH_CENTER'

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioenergyResearchCenterId):
            self.id = BioenergyResearchCenterId(self.id)

        if self.outputs is not None and not isinstance(self.outputs, ProgramOutputs):
            self.outputs = ProgramOutputs(**as_dict(self.outputs))

        if self.predecessor is not None and not isinstance(self.predecessor, str):
            self.predecessor = str(self.predecessor)

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = getattr(ProgramType, self.program_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScientificFocusArea(ResearchProgram):
    """
    A DOE Scientific Focus Area (SFA). SFAs are integrated research programs at DOE national laboratories focused on
    specific scientific areas within BER's portfolio. SFAs conduct coordinated, team-oriented research taking
    advantage of national laboratory strengths.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ScientificFocusArea"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ScientificFocusArea"
    class_name: ClassVar[str] = "ScientificFocusArea"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ScientificFocusArea

    id: Union[str, ScientificFocusAreaId] = None
    name: str = None
    sfa_type: Optional[Union[str, "SFAType"]] = None
    technologies_developed: Optional[Union[Union[dict, "Technology"], list[Union[dict, "Technology"]]]] = empty_list()
    co_investigators: Optional[Union[Union[dict, "Person"], list[Union[dict, "Person"]]]] = empty_list()
    program_type: Optional[Union[str, "ProgramType"]] = 'SCIENTIFIC_FOCUS_AREA'

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScientificFocusAreaId):
            self.id = ScientificFocusAreaId(self.id)

        if self.sfa_type is not None and not isinstance(self.sfa_type, SFAType):
            self.sfa_type = SFAType(self.sfa_type)

        if not isinstance(self.technologies_developed, list):
            self.technologies_developed = [self.technologies_developed] if self.technologies_developed is not None else []
        self.technologies_developed = [v if isinstance(v, Technology) else Technology(**as_dict(v)) for v in self.technologies_developed]

        if not isinstance(self.co_investigators, list):
            self.co_investigators = [self.co_investigators] if self.co_investigators is not None else []
        self.co_investigators = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.co_investigators]

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = getattr(ProgramType, self.program_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OtherProgram(ResearchProgram):
    """
    Other DOE research programs and initiatives that don't fit the traditional SFA/BRC/Facility categories. Examples
    include BRaVE (Biopreparedness Research Virtual Environment) projects, cross-cutting initiatives, and time-limited
    collaborative projects spanning multiple DOE offices.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["OtherProgram"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:OtherProgram"
    class_name: ClassVar[str] = "OtherProgram"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.OtherProgram

    id: Union[str, OtherProgramId] = None
    name: str = None
    initiative_name: Optional[str] = None
    funding_period: Optional[str] = None
    participating_offices: Optional[Union[str, list[str]]] = empty_list()
    program_type: Optional[Union[str, "ProgramType"]] = 'OTHER_INITIATIVE'

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OtherProgramId):
            self.id = OtherProgramId(self.id)

        if self.initiative_name is not None and not isinstance(self.initiative_name, str):
            self.initiative_name = str(self.initiative_name)

        if self.funding_period is not None and not isinstance(self.funding_period, str):
            self.funding_period = str(self.funding_period)

        if not isinstance(self.participating_offices, list):
            self.participating_offices = [self.participating_offices] if self.participating_offices is not None else []
        self.participating_offices = [v if isinstance(v, str) else str(v) for v in self.participating_offices]

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = getattr(ProgramType, self.program_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ArtificialIntelligenceProject(OtherProgram):
    """
    A DOE artificial intelligence project or pilot initiative using AI/ML, agentic systems, data lakehouses,
    autonomous laboratories, or related computational methods to advance BER-relevant biological and environmental
    science.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ArtificialIntelligenceProject"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ArtificialIntelligenceProject"
    class_name: ClassVar[str] = "ArtificialIntelligenceProject"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ArtificialIntelligenceProject

    id: Union[str, ArtificialIntelligenceProjectId] = None
    name: str = None
    program_type: Optional[Union[str, "ProgramType"]] = 'AI_PILOT_PROJECT'

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ArtificialIntelligenceProjectId):
            self.id = ArtificialIntelligenceProjectId(self.id)

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = getattr(ProgramType, self.program_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UserFacility(NamedThing):
    """
    A DOE BER User Facility providing resources and capabilities to the broader scientific community. Examples include
    JGI, EMSL, and KBase.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["UserFacility"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:UserFacility"
    class_name: ClassVar[str] = "UserFacility"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.UserFacility

    id: Union[str, UserFacilityId] = None
    acronym: Optional[str] = None
    program_type: Optional[Union[str, "ProgramType"]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    lead_institution: Optional[str] = None
    lead_institutions: Optional[Union[str, list[str]]] = empty_list()
    funding: Optional[Union[dict, "FundingInfo"]] = None
    websites: Optional[Union[dict, "WebResources"]] = None
    services: Optional[Union[str, list[str]]] = empty_list()
    capabilities: Optional[Union[Union[dict, "Capability"], list[Union[dict, "Capability"]]]] = empty_list()
    flagship_genomes: Optional[Union[Union[dict, "FlagshipGenome"], list[Union[dict, "FlagshipGenome"]]]] = empty_list()
    reference_data: Optional[Union[dict, "ReferenceData"]] = None
    supported_data_types: Optional[Union[str, list[str]]] = empty_list()
    research_resources: Optional[Union[Union[dict, "ResearchResource"], list[Union[dict, "ResearchResource"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UserFacilityId):
            self.id = UserFacilityId(self.id)

        if self.acronym is not None and not isinstance(self.acronym, str):
            self.acronym = str(self.acronym)

        if self.program_type is not None and not isinstance(self.program_type, ProgramType):
            self.program_type = ProgramType(self.program_type)

        if self.start_date is not None and not isinstance(self.start_date, str):
            self.start_date = str(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, str):
            self.end_date = str(self.end_date)

        if self.lead_institution is not None and not isinstance(self.lead_institution, str):
            self.lead_institution = str(self.lead_institution)

        if not isinstance(self.lead_institutions, list):
            self.lead_institutions = [self.lead_institutions] if self.lead_institutions is not None else []
        self.lead_institutions = [v if isinstance(v, str) else str(v) for v in self.lead_institutions]

        if self.funding is not None and not isinstance(self.funding, FundingInfo):
            self.funding = FundingInfo(**as_dict(self.funding))

        if self.websites is not None and not isinstance(self.websites, WebResources):
            self.websites = WebResources(**as_dict(self.websites))

        if not isinstance(self.services, list):
            self.services = [self.services] if self.services is not None else []
        self.services = [v if isinstance(v, str) else str(v) for v in self.services]

        if not isinstance(self.capabilities, list):
            self.capabilities = [self.capabilities] if self.capabilities is not None else []
        self.capabilities = [v if isinstance(v, Capability) else Capability(**as_dict(v)) for v in self.capabilities]

        if not isinstance(self.flagship_genomes, list):
            self.flagship_genomes = [self.flagship_genomes] if self.flagship_genomes is not None else []
        self.flagship_genomes = [v if isinstance(v, FlagshipGenome) else FlagshipGenome(**as_dict(v)) for v in self.flagship_genomes]

        if self.reference_data is not None and not isinstance(self.reference_data, ReferenceData):
            self.reference_data = ReferenceData(**as_dict(self.reference_data))

        if not isinstance(self.supported_data_types, list):
            self.supported_data_types = [self.supported_data_types] if self.supported_data_types is not None else []
        self.supported_data_types = [v if isinstance(v, str) else str(v) for v in self.supported_data_types]

        if not isinstance(self.research_resources, list):
            self.research_resources = [self.research_resources] if self.research_resources is not None else []
        self.research_resources = [v if isinstance(v, ResearchResource) else ResearchResource(**as_dict(v)) for v in self.research_resources]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Institution(YAMLRoot):
    """
    A research institution such as a national laboratory, university, or research institute.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Organization"]
    class_class_curie: ClassVar[str] = "schema:Organization"
    class_name: ClassVar[str] = "Institution"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Institution

    name: Optional[str] = None
    description: Optional[str] = None
    ror_id: Optional[Union[str, URIorCURIE]] = None
    institution_type: Optional[Union[str, "InstitutionType"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.ror_id is not None and not isinstance(self.ror_id, URIorCURIE):
            self.ror_id = URIorCURIE(self.ror_id)

        if self.institution_type is not None and not isinstance(self.institution_type, InstitutionType):
            self.institution_type = InstitutionType(self.institution_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(YAMLRoot):
    """
    A person involved in a research program, such as a principal investigator, co-investigator, or other key personnel.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Person"]
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Person

    name: Optional[str] = None
    role: Optional[str] = None
    affiliation: Optional[str] = None
    email: Optional[str] = None
    orcid: Optional[Union[str, URIorCURIE]] = None
    expertise: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.role is not None and not isinstance(self.role, str):
            self.role = str(self.role)

        if self.affiliation is not None and not isinstance(self.affiliation, str):
            self.affiliation = str(self.affiliation)

        if self.email is not None and not isinstance(self.email, str):
            self.email = str(self.email)

        if self.orcid is not None and not isinstance(self.orcid, URIorCURIE):
            self.orcid = URIorCURIE(self.orcid)

        if self.expertise is not None and not isinstance(self.expertise, str):
            self.expertise = str(self.expertise)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FundingInfo(YAMLRoot):
    """
    Information about funding for a research program including agency, program, and award details.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["FundingInfo"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:FundingInfo"
    class_name: ClassVar[str] = "FundingInfo"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.FundingInfo

    agency: Optional[str] = None
    program: Optional[str] = None
    division: Optional[str] = None
    subprogram: Optional[str] = None
    area: Optional[str] = None
    contract: Optional[str] = None
    grant: Optional[str] = None
    total_funding: Optional[str] = None
    amount: Optional[str] = None
    award_2017: Optional[str] = None
    current_period: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.agency is not None and not isinstance(self.agency, str):
            self.agency = str(self.agency)

        if self.program is not None and not isinstance(self.program, str):
            self.program = str(self.program)

        if self.division is not None and not isinstance(self.division, str):
            self.division = str(self.division)

        if self.subprogram is not None and not isinstance(self.subprogram, str):
            self.subprogram = str(self.subprogram)

        if self.area is not None and not isinstance(self.area, str):
            self.area = str(self.area)

        if self.contract is not None and not isinstance(self.contract, str):
            self.contract = str(self.contract)

        if self.grant is not None and not isinstance(self.grant, str):
            self.grant = str(self.grant)

        if self.total_funding is not None and not isinstance(self.total_funding, str):
            self.total_funding = str(self.total_funding)

        if self.amount is not None and not isinstance(self.amount, str):
            self.amount = str(self.amount)

        if self.award_2017 is not None and not isinstance(self.award_2017, str):
            self.award_2017 = str(self.award_2017)

        if self.current_period is not None and not isinstance(self.current_period, str):
            self.current_period = str(self.current_period)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Location(YAMLRoot):
    """
    Geographic location information for a research program
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Location"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Location

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "USA"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.address is not None and not isinstance(self.address, str):
            self.address = str(self.address)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        if self.state is not None and not isinstance(self.state, str):
            self.state = str(self.state)

        if self.country is not None and not isinstance(self.country, str):
            self.country = str(self.country)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WebResources(YAMLRoot):
    """
    Collection of web resources associated with a research program
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["WebResources"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:WebResources"
    class_name: ClassVar[str] = "WebResources"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.WebResources

    main: Optional[Union[str, URI]] = None
    doe_page: Optional[Union[str, URI]] = None
    award_list: Optional[Union[str, URI]] = None
    ornl_page: Optional[Union[str, URI]] = None
    llnl_page: Optional[Union[str, URI]] = None
    data_portal: Optional[Union[str, URI]] = None
    data_hub: Optional[Union[str, URI]] = None
    data_page: Optional[Union[str, URI]] = None
    atlas: Optional[Union[str, URI]] = None
    github: Optional[Union[str, URI]] = None
    kbase: Optional[Union[str, URI]] = None
    ess_dive: Optional[Union[str, URI]] = None
    ideas_watersheds: Optional[Union[str, URI]] = None
    czen: Optional[Union[str, URI]] = None
    publications: Optional[Union[str, URI]] = None
    highlights: Optional[Union[str, URI]] = None
    documentation: Optional[Union[str, URI]] = None
    bacterial_strains: Optional[Union[str, URI]] = None
    bfi_portal: Optional[Union[str, URI]] = None
    ssrl_page: Optional[Union[str, URI]] = None
    anl_page: Optional[Union[str, URI]] = None
    team: Optional[Union[str, URI]] = None
    phytozome: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.main is not None and not isinstance(self.main, URI):
            self.main = URI(self.main)

        if self.doe_page is not None and not isinstance(self.doe_page, URI):
            self.doe_page = URI(self.doe_page)

        if self.award_list is not None and not isinstance(self.award_list, URI):
            self.award_list = URI(self.award_list)

        if self.ornl_page is not None and not isinstance(self.ornl_page, URI):
            self.ornl_page = URI(self.ornl_page)

        if self.llnl_page is not None and not isinstance(self.llnl_page, URI):
            self.llnl_page = URI(self.llnl_page)

        if self.data_portal is not None and not isinstance(self.data_portal, URI):
            self.data_portal = URI(self.data_portal)

        if self.data_hub is not None and not isinstance(self.data_hub, URI):
            self.data_hub = URI(self.data_hub)

        if self.data_page is not None and not isinstance(self.data_page, URI):
            self.data_page = URI(self.data_page)

        if self.atlas is not None and not isinstance(self.atlas, URI):
            self.atlas = URI(self.atlas)

        if self.github is not None and not isinstance(self.github, URI):
            self.github = URI(self.github)

        if self.kbase is not None and not isinstance(self.kbase, URI):
            self.kbase = URI(self.kbase)

        if self.ess_dive is not None and not isinstance(self.ess_dive, URI):
            self.ess_dive = URI(self.ess_dive)

        if self.ideas_watersheds is not None and not isinstance(self.ideas_watersheds, URI):
            self.ideas_watersheds = URI(self.ideas_watersheds)

        if self.czen is not None and not isinstance(self.czen, URI):
            self.czen = URI(self.czen)

        if self.publications is not None and not isinstance(self.publications, URI):
            self.publications = URI(self.publications)

        if self.highlights is not None and not isinstance(self.highlights, URI):
            self.highlights = URI(self.highlights)

        if self.documentation is not None and not isinstance(self.documentation, URI):
            self.documentation = URI(self.documentation)

        if self.bacterial_strains is not None and not isinstance(self.bacterial_strains, URI):
            self.bacterial_strains = URI(self.bacterial_strains)

        if self.bfi_portal is not None and not isinstance(self.bfi_portal, URI):
            self.bfi_portal = URI(self.bfi_portal)

        if self.ssrl_page is not None and not isinstance(self.ssrl_page, URI):
            self.ssrl_page = URI(self.ssrl_page)

        if self.anl_page is not None and not isinstance(self.anl_page, URI):
            self.anl_page = URI(self.anl_page)

        if self.team is not None and not isinstance(self.team, URI):
            self.team = URI(self.team)

        if self.phytozome is not None and not isinstance(self.phytozome, URI):
            self.phytozome = URI(self.phytozome)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Dataset(YAMLRoot):
    """
    A dataset produced by or associated with a research program.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Dataset"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Dataset

    name: Optional[str] = None
    description: Optional[str] = None
    doi: Optional[Union[str, URIorCURIE]] = None
    url: Optional[Union[str, URI]] = None
    repository: Optional[str] = None
    data_type: Optional[str] = None
    size: Optional[str] = None
    version: Optional[str] = None
    years: Optional[str] = None
    reference: Optional[str] = None
    count: Optional[str] = None
    osti_id: Optional[str] = None
    doi_examples: Optional[Union[str, list[str]]] = empty_list()
    nmdc_study_id: Optional[Union[str, URIorCURIE]] = None
    jgi_project_id: Optional[str] = None
    ameriflux_site_id: Optional[str] = None
    lter_dataset_id: Optional[str] = None
    pride_id: Optional[str] = None
    massive_id: Optional[str] = None
    primary_reference: Optional[Union[str, URIorCURIE]] = None
    additional_references: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    interaction_types: Optional[Union[Union[str, "InteractionType"], list[Union[str, "InteractionType"]]]] = empty_list()
    interaction_modes: Optional[Union[Union[str, "InteractionMode"], list[Union[str, "InteractionMode"]]]] = empty_list()
    variables: Optional[Union[Union[dict, "Variable"], list[Union[dict, "Variable"]]]] = empty_list()
    primary_reference_info: Optional[Union[dict, "PrimaryReferenceInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.doi is not None and not isinstance(self.doi, URIorCURIE):
            self.doi = URIorCURIE(self.doi)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.repository is not None and not isinstance(self.repository, str):
            self.repository = str(self.repository)

        if self.data_type is not None and not isinstance(self.data_type, str):
            self.data_type = str(self.data_type)

        if self.size is not None and not isinstance(self.size, str):
            self.size = str(self.size)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.years is not None and not isinstance(self.years, str):
            self.years = str(self.years)

        if self.reference is not None and not isinstance(self.reference, str):
            self.reference = str(self.reference)

        if self.count is not None and not isinstance(self.count, str):
            self.count = str(self.count)

        if self.osti_id is not None and not isinstance(self.osti_id, str):
            self.osti_id = str(self.osti_id)

        if not isinstance(self.doi_examples, list):
            self.doi_examples = [self.doi_examples] if self.doi_examples is not None else []
        self.doi_examples = [v if isinstance(v, str) else str(v) for v in self.doi_examples]

        if self.nmdc_study_id is not None and not isinstance(self.nmdc_study_id, URIorCURIE):
            self.nmdc_study_id = URIorCURIE(self.nmdc_study_id)

        if self.jgi_project_id is not None and not isinstance(self.jgi_project_id, str):
            self.jgi_project_id = str(self.jgi_project_id)

        if self.ameriflux_site_id is not None and not isinstance(self.ameriflux_site_id, str):
            self.ameriflux_site_id = str(self.ameriflux_site_id)

        if self.lter_dataset_id is not None and not isinstance(self.lter_dataset_id, str):
            self.lter_dataset_id = str(self.lter_dataset_id)

        if self.pride_id is not None and not isinstance(self.pride_id, str):
            self.pride_id = str(self.pride_id)

        if self.massive_id is not None and not isinstance(self.massive_id, str):
            self.massive_id = str(self.massive_id)

        if self.primary_reference is not None and not isinstance(self.primary_reference, URIorCURIE):
            self.primary_reference = URIorCURIE(self.primary_reference)

        if not isinstance(self.additional_references, list):
            self.additional_references = [self.additional_references] if self.additional_references is not None else []
        self.additional_references = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.additional_references]

        if not isinstance(self.interaction_types, list):
            self.interaction_types = [self.interaction_types] if self.interaction_types is not None else []
        self.interaction_types = [v if isinstance(v, InteractionType) else InteractionType(v) for v in self.interaction_types]

        if not isinstance(self.interaction_modes, list):
            self.interaction_modes = [self.interaction_modes] if self.interaction_modes is not None else []
        self.interaction_modes = [v if isinstance(v, InteractionMode) else InteractionMode(v) for v in self.interaction_modes]

        if not isinstance(self.variables, list):
            self.variables = [self.variables] if self.variables is not None else []
        self.variables = [v if isinstance(v, Variable) else Variable(**as_dict(v)) for v in self.variables]

        if self.primary_reference_info is not None and not isinstance(self.primary_reference_info, PrimaryReferenceInfo):
            self.primary_reference_info = PrimaryReferenceInfo(**as_dict(self.primary_reference_info))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Variable(YAMLRoot):
    """
    A variable, factor, measurement, or metadata field observed, manipulated, derived, or otherwise used in a study or
    dataset. Variables act as a lightweight data dictionary and can be tagged with analytical roles, time-series
    behavior, units, methods, and ontology mappings such as BERVO. Ontology references are modeled as id/label objects
    so linkml-term-validator can check both the identifier and the canonical label.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["PropertyValue"]
    class_class_curie: ClassVar[str] = "schema:PropertyValue"
    class_name: ClassVar[str] = "Variable"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Variable

    name: str = None
    description: Optional[str] = None
    roles: Optional[Union[Union[str, "VariableRole"], list[Union[str, "VariableRole"]]]] = empty_list()
    value_type: Optional[Union[str, "VariableValueType"]] = None
    units: Optional[str] = None
    unit_term: Optional[Union[dict, "OntologyTerm"]] = None
    bervo_term: Optional[Union[dict, "BERVOTerm"]] = None
    mixs_terms: Optional[Union[dict[Union[str, MIXSTermId], Union[dict, "MIXSTerm"]], list[Union[dict, "MIXSTerm"]]]] = empty_dict()
    ontology_mappings: Optional[Union[dict[Union[str, OntologyTermId], Union[dict, "OntologyTerm"]], list[Union[dict, "OntologyTerm"]]]] = empty_dict()
    measured_entity: Optional[str] = None
    material_or_matrix: Optional[str] = None
    method: Optional[str] = None
    time_series: Optional[Union[bool, Bool]] = None
    temporal_resolution: Optional[str] = None
    spatial_resolution: Optional[str] = None
    levels: Optional[Union[str, list[str]]] = empty_list()
    source_field_names: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.roles, list):
            self.roles = [self.roles] if self.roles is not None else []
        self.roles = [v if isinstance(v, VariableRole) else VariableRole(v) for v in self.roles]

        if self.value_type is not None and not isinstance(self.value_type, VariableValueType):
            self.value_type = VariableValueType(self.value_type)

        if self.units is not None and not isinstance(self.units, str):
            self.units = str(self.units)

        if self.unit_term is not None and not isinstance(self.unit_term, OntologyTerm):
            self.unit_term = OntologyTerm(**as_dict(self.unit_term))

        if self.bervo_term is not None and not isinstance(self.bervo_term, BERVOTerm):
            self.bervo_term = BERVOTerm(**as_dict(self.bervo_term))

        self._normalize_inlined_as_list(slot_name="mixs_terms", slot_type=MIXSTerm, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="ontology_mappings", slot_type=OntologyTerm, key_name="id", keyed=True)

        if self.measured_entity is not None and not isinstance(self.measured_entity, str):
            self.measured_entity = str(self.measured_entity)

        if self.material_or_matrix is not None and not isinstance(self.material_or_matrix, str):
            self.material_or_matrix = str(self.material_or_matrix)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        if self.time_series is not None and not isinstance(self.time_series, Bool):
            self.time_series = Bool(self.time_series)

        if self.temporal_resolution is not None and not isinstance(self.temporal_resolution, str):
            self.temporal_resolution = str(self.temporal_resolution)

        if self.spatial_resolution is not None and not isinstance(self.spatial_resolution, str):
            self.spatial_resolution = str(self.spatial_resolution)

        if not isinstance(self.levels, list):
            self.levels = [self.levels] if self.levels is not None else []
        self.levels = [v if isinstance(v, str) else str(v) for v in self.levels]

        if not isinstance(self.source_field_names, list):
            self.source_field_names = [self.source_field_names] if self.source_field_names is not None else []
        self.source_field_names = [v if isinstance(v, str) else str(v) for v in self.source_field_names]

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OntologyTerm(YAMLRoot):
    """
    A reference to an ontology term, represented as an identifier plus the term label expected from the source
    ontology. The label field is marked as rdfs:label for linkml-term-validator label checks.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["OntologyTerm"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:OntologyTerm"
    class_name: ClassVar[str] = "OntologyTerm"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.OntologyTerm

    id: Union[str, OntologyTermId] = None
    label: str = None
    mapping_relation: Optional[Union[str, "OntologyMappingRelation"]] = None
    mapping_note: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyTermId):
            self.id = OntologyTermId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.mapping_relation is not None and not isinstance(self.mapping_relation, OntologyMappingRelation):
            self.mapping_relation = OntologyMappingRelation(self.mapping_relation)

        if self.mapping_note is not None and not isinstance(self.mapping_note, str):
            self.mapping_note = str(self.mapping_note)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BERVOTerm(OntologyTerm):
    """
    A BERVO ontology term represented with an identifier and label
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["BERVOTerm"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:BERVOTerm"
    class_name: ClassVar[str] = "BERVOTerm"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.BERVOTerm

    id: Union[str, BERVOTermId] = None
    label: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BERVOTermId):
            self.id = BERVOTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MIXSTerm(OntologyTerm):
    """
    A MIxS metadata term represented with an identifier and label
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["MIXSTerm"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:MIXSTerm"
    class_name: ClassVar[str] = "MIXSTerm"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.MIXSTerm

    id: Union[str, MIXSTermId] = None
    label: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MIXSTermId):
            self.id = MIXSTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reference(YAMLRoot):
    """
    A publication reference with key findings. Minimal metadata is stored here; full bibliographic data can be
    fetched/cached via linkml-reference-validator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Reference"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Reference"
    class_name: ClassVar[str] = "Reference"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Reference

    id: Union[str, ReferenceId] = None
    title: Optional[str] = None
    findings: Optional[Union[Union[dict, "Finding"], list[Union[dict, "Finding"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceId):
            self.id = ReferenceId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if not isinstance(self.findings, list):
            self.findings = [self.findings] if self.findings is not None else []
        self.findings = [v if isinstance(v, Finding) else Finding(**as_dict(v)) for v in self.findings]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Finding(YAMLRoot):
    """
    A key finding or claim extracted from a publication
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Finding"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Finding"
    class_name: ClassVar[str] = "Finding"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Finding

    statement: str = None
    supporting_text: Optional[str] = None
    reference: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.statement):
            self.MissingRequiredField("statement")
        if not isinstance(self.statement, str):
            self.statement = str(self.statement)

        if self.supporting_text is not None and not isinstance(self.supporting_text, str):
            self.supporting_text = str(self.supporting_text)

        if self.reference is not None and not isinstance(self.reference, URIorCURIE):
            self.reference = URIorCURIE(self.reference)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PrimaryReferenceInfo(YAMLRoot):
    """
    Container for a primary reference with its metadata. Provides a structured way to associate a publication
    reference with an entity (e.g., IsolateCollection, Dataset) while allowing future annotations about the
    relationship.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["PrimaryReferenceInfo"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:PrimaryReferenceInfo"
    class_name: ClassVar[str] = "PrimaryReferenceInfo"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.PrimaryReferenceInfo

    reference: Union[dict, Reference] = None
    relationship_note: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.reference):
            self.MissingRequiredField("reference")
        if not isinstance(self.reference, Reference):
            self.reference = Reference(**as_dict(self.reference))

        if self.relationship_note is not None and not isinstance(self.relationship_note, str):
            self.relationship_note = str(self.relationship_note)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProgramOutputs(YAMLRoot):
    """
    Summary of research outputs from a program
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ProgramOutputs"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ProgramOutputs"
    class_name: ClassVar[str] = "ProgramOutputs"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ProgramOutputs

    publication_count: Optional[str] = None
    patent_applications: Optional[int] = None
    invention_disclosures: Optional[int] = None
    licenses_options: Optional[int] = None
    patents: Optional[int] = None
    startups: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.publication_count is not None and not isinstance(self.publication_count, str):
            self.publication_count = str(self.publication_count)

        if self.patent_applications is not None and not isinstance(self.patent_applications, int):
            self.patent_applications = int(self.patent_applications)

        if self.invention_disclosures is not None and not isinstance(self.invention_disclosures, int):
            self.invention_disclosures = int(self.invention_disclosures)

        if self.licenses_options is not None and not isinstance(self.licenses_options, int):
            self.licenses_options = int(self.licenses_options)

        if self.patents is not None and not isinstance(self.patents, int):
            self.patents = int(self.patents)

        if self.startups is not None and not isinstance(self.startups, int):
            self.startups = int(self.startups)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResearchResource(YAMLRoot):
    """
    A large-grain research resource maintained or produced by a research program: an isolate collection, mutant
    library, phage bank, reference genome set, plasmid collection, synthetic community, knowledgebase, or similar
    reagent or data resource. Catalog-level metadata only; detailed records are expected to live in external systems
    referenced via identifiers. IsolateCollection is a subtype; other resource kinds are distinguished by the
    resource_type discriminator rather than by proliferating subclasses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ResearchResource"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ResearchResource"
    class_name: ClassVar[str] = "ResearchResource"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ResearchResource

    name: Optional[str] = None
    description: Optional[str] = None
    primary_reference: Optional[Union[str, URIorCURIE]] = None
    resource_type: Optional[Union[str, "ResourceType"]] = None
    identifiers: Optional[Union[Union[dict, "ResourceIdentifier"], list[Union[dict, "ResourceIdentifier"]]]] = empty_list()
    provider: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    count: Optional[str] = None
    members: Optional[Union[str, list[str]]] = empty_list()
    member_count: Optional[int] = None
    primary_reference_info: Optional[Union[dict, PrimaryReferenceInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.primary_reference is not None and not isinstance(self.primary_reference, URIorCURIE):
            self.primary_reference = URIorCURIE(self.primary_reference)

        if self.resource_type is not None and not isinstance(self.resource_type, ResourceType):
            self.resource_type = ResourceType(self.resource_type)

        if not isinstance(self.identifiers, list):
            self.identifiers = [self.identifiers] if self.identifiers is not None else []
        self.identifiers = [v if isinstance(v, ResourceIdentifier) else ResourceIdentifier(**as_dict(v)) for v in self.identifiers]

        if self.provider is not None and not isinstance(self.provider, str):
            self.provider = str(self.provider)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.count is not None and not isinstance(self.count, str):
            self.count = str(self.count)

        if not isinstance(self.members, list):
            self.members = [self.members] if self.members is not None else []
        self.members = [v if isinstance(v, str) else str(v) for v in self.members]

        if self.member_count is not None and not isinstance(self.member_count, int):
            self.member_count = int(self.member_count)

        if self.primary_reference_info is not None and not isinstance(self.primary_reference_info, PrimaryReferenceInfo):
            self.primary_reference_info = PrimaryReferenceInfo(**as_dict(self.primary_reference_info))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResourceIdentifier(YAMLRoot):
    """
    A typed external identifier for a research resource: a {registry, accession} tuple with an optional resolvable URL
    and citation. Used to point at a resource's record in any external catalog or registry — examples include Addgene,
    BEI, ATCC, DSMZ, KBase narrative IDs, NCBI:Assembly accessions, a Fitness Browser organism ID, an RRID, or a lab
    catalog identifier.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ResourceIdentifier"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ResourceIdentifier"
    class_name: ClassVar[str] = "ResourceIdentifier"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ResourceIdentifier

    registry: str = None
    accession: str = None
    url: Optional[Union[str, URI]] = None
    citation: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.registry):
            self.MissingRequiredField("registry")
        if not isinstance(self.registry, str):
            self.registry = str(self.registry)

        if self._is_empty(self.accession):
            self.MissingRequiredField("accession")
        if not isinstance(self.accession, str):
            self.accession = str(self.accession)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.citation is not None and not isinstance(self.citation, URIorCURIE):
            self.citation = URIorCURIE(self.citation)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IsolateCollection(ResearchResource):
    """
    A collection of cultured microbial isolates maintained by a research program. Provides catalog-level metadata
    about the collection; detailed isolate records are maintained in external systems (KBase, JGI, culture
    collections). Subtype of ResearchResource; other resource kinds (mutant libraries, phage banks, knowledgebases)
    are modeled as ResearchResource directly using the resource_type discriminator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["IsolateCollection"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:IsolateCollection"
    class_name: ClassVar[str] = "IsolateCollection"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.IsolateCollection

    name: Optional[str] = None
    description: Optional[str] = None
    organism_types: Optional[Union[Union[str, "OrganismType"], list[Union[str, "OrganismType"]]]] = empty_list()
    isolate_count: Optional[int] = None
    genome_count: Optional[int] = None
    source_environments: Optional[Union[str, list[str]]] = empty_list()
    isolation_methods: Optional[Union[str, list[str]]] = empty_list()
    host_organisms: Optional[Union[str, list[str]]] = empty_list()
    culture_collection_url: Optional[Union[str, URI]] = None
    genome_catalog_url: Optional[Union[str, URI]] = None
    kbase_narrative_id: Optional[str] = None
    primary_reference: Optional[Union[str, URIorCURIE]] = None
    primary_reference_info: Optional[Union[dict, PrimaryReferenceInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.organism_types, list):
            self.organism_types = [self.organism_types] if self.organism_types is not None else []
        self.organism_types = [v if isinstance(v, OrganismType) else OrganismType(v) for v in self.organism_types]

        if self.isolate_count is not None and not isinstance(self.isolate_count, int):
            self.isolate_count = int(self.isolate_count)

        if self.genome_count is not None and not isinstance(self.genome_count, int):
            self.genome_count = int(self.genome_count)

        if not isinstance(self.source_environments, list):
            self.source_environments = [self.source_environments] if self.source_environments is not None else []
        self.source_environments = [v if isinstance(v, str) else str(v) for v in self.source_environments]

        if not isinstance(self.isolation_methods, list):
            self.isolation_methods = [self.isolation_methods] if self.isolation_methods is not None else []
        self.isolation_methods = [v if isinstance(v, str) else str(v) for v in self.isolation_methods]

        if not isinstance(self.host_organisms, list):
            self.host_organisms = [self.host_organisms] if self.host_organisms is not None else []
        self.host_organisms = [v if isinstance(v, str) else str(v) for v in self.host_organisms]

        if self.culture_collection_url is not None and not isinstance(self.culture_collection_url, URI):
            self.culture_collection_url = URI(self.culture_collection_url)

        if self.genome_catalog_url is not None and not isinstance(self.genome_catalog_url, URI):
            self.genome_catalog_url = URI(self.genome_catalog_url)

        if self.kbase_narrative_id is not None and not isinstance(self.kbase_narrative_id, str):
            self.kbase_narrative_id = str(self.kbase_narrative_id)

        if self.primary_reference is not None and not isinstance(self.primary_reference, URIorCURIE):
            self.primary_reference = URIorCURIE(self.primary_reference)

        if self.primary_reference_info is not None and not isinstance(self.primary_reference_info, PrimaryReferenceInfo):
            self.primary_reference_info = PrimaryReferenceInfo(**as_dict(self.primary_reference_info))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FieldSite(NamedThing):
    """
    A field research site associated with a research program
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Place"]
    class_class_curie: ClassVar[str] = "schema:Place"
    class_name: ClassVar[str] = "FieldSite"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.FieldSite

    id: Union[str, FieldSiteId] = None
    name: str = None
    location: Optional[str] = None
    site_type: Optional[str] = None
    pi: Optional[str] = None
    institution: Optional[str] = None
    relevance: Optional[Union[str, list[str]]] = empty_list()
    contaminants: Optional[Union[str, list[str]]] = empty_list()
    contamination_source: Optional[str] = None
    elevation_m: Optional[int] = None
    mean_annual_temp_c: Optional[float] = None
    mean_annual_precip_cm: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FieldSiteId):
            self.id = FieldSiteId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        if self.site_type is not None and not isinstance(self.site_type, str):
            self.site_type = str(self.site_type)

        if self.pi is not None and not isinstance(self.pi, str):
            self.pi = str(self.pi)

        if self.institution is not None and not isinstance(self.institution, str):
            self.institution = str(self.institution)

        if not isinstance(self.relevance, list):
            self.relevance = [self.relevance] if self.relevance is not None else []
        self.relevance = [v if isinstance(v, str) else str(v) for v in self.relevance]

        if not isinstance(self.contaminants, list):
            self.contaminants = [self.contaminants] if self.contaminants is not None else []
        self.contaminants = [v if isinstance(v, str) else str(v) for v in self.contaminants]

        if self.contamination_source is not None and not isinstance(self.contamination_source, str):
            self.contamination_source = str(self.contamination_source)

        if self.elevation_m is not None and not isinstance(self.elevation_m, int):
            self.elevation_m = int(self.elevation_m)

        if self.mean_annual_temp_c is not None and not isinstance(self.mean_annual_temp_c, float):
            self.mean_annual_temp_c = float(self.mean_annual_temp_c)

        if self.mean_annual_precip_cm is not None and not isinstance(self.mean_annual_precip_cm, float):
            self.mean_annual_precip_cm = float(self.mean_annual_precip_cm)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Technology(YAMLRoot):
    """
    A technology or tool developed by a research program
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Technology"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Technology"
    class_name: ClassVar[str] = "Technology"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Technology

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WebReference(YAMLRoot):
    """
    A reference to a web resource such as a project page, news article, or documentation. Used for citing non-DOI
    sources that document research activities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["WebReference"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:WebReference"
    class_name: ClassVar[str] = "WebReference"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.WebReference

    url: Union[str, URI] = None
    title: str = None
    summary: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.url):
            self.MissingRequiredField("url")
        if not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyDesign(YAMLRoot):
    """
    Study-level design metadata that applies across variables and datasets. This captures the design pattern,
    experimental or observational units, replication, blocking, randomization, and related notes separately from the
    data dictionary entries for individual variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["StudyDesign"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:StudyDesign"
    class_name: ClassVar[str] = "StudyDesign"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.StudyDesign

    description: Optional[str] = None
    design_types: Optional[Union[dict[Union[str, OntologyTermId], Union[dict, OntologyTerm]], list[Union[dict, OntologyTerm]]]] = empty_dict()
    factor_panels: Optional[Union[str, list[str]]] = empty_list()
    experimental_units: Optional[Union[str, list[str]]] = empty_list()
    observational_units: Optional[Union[str, list[str]]] = empty_list()
    sampling_strategy: Optional[str] = None
    replication: Optional[str] = None
    randomization: Optional[str] = None
    blocking: Optional[str] = None
    controls: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="design_types", slot_type=OntologyTerm, key_name="id", keyed=True)

        if not isinstance(self.factor_panels, list):
            self.factor_panels = [self.factor_panels] if self.factor_panels is not None else []
        self.factor_panels = [v if isinstance(v, str) else str(v) for v in self.factor_panels]

        if not isinstance(self.experimental_units, list):
            self.experimental_units = [self.experimental_units] if self.experimental_units is not None else []
        self.experimental_units = [v if isinstance(v, str) else str(v) for v in self.experimental_units]

        if not isinstance(self.observational_units, list):
            self.observational_units = [self.observational_units] if self.observational_units is not None else []
        self.observational_units = [v if isinstance(v, str) else str(v) for v in self.observational_units]

        if self.sampling_strategy is not None and not isinstance(self.sampling_strategy, str):
            self.sampling_strategy = str(self.sampling_strategy)

        if self.replication is not None and not isinstance(self.replication, str):
            self.replication = str(self.replication)

        if self.randomization is not None and not isinstance(self.randomization, str):
            self.randomization = str(self.randomization)

        if self.blocking is not None and not isinstance(self.blocking, str):
            self.blocking = str(self.blocking)

        if self.controls is not None and not isinstance(self.controls, str):
            self.controls = str(self.controls)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NMDCStudyReference(YAMLRoot):
    """
    A reference to an NMDC study associated with a research program. Links BRC/SFA research to specific studies in the
    National Microbiome Data Collaborative. Can also represent studies that are candidates for NMDC ingest
    (nmdc_ingest_target=true).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["NMDCStudyReference"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:NMDCStudyReference"
    class_name: ClassVar[str] = "NMDCStudyReference"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.NMDCStudyReference

    nmdc_study_id: Optional[Union[str, URIorCURIE]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    primary_reference: Optional[Union[str, URIorCURIE]] = None
    keywords: Optional[Union[Union[str, "Keyword"], list[Union[str, "Keyword"]]]] = empty_list()
    field_site_ids: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    study_design: Optional[Union[dict, StudyDesign]] = None
    variables: Optional[Union[Union[dict, Variable], list[Union[dict, Variable]]]] = empty_list()
    pi: Optional[str] = None
    bioproject_ids: Optional[Union[str, list[str]]] = empty_list()
    gold_study_id: Optional[str] = None
    jgi_proposal_id: Optional[str] = None
    brc_dataset_ids: Optional[Union[str, list[str]]] = empty_list()
    nmdc_ingest_target: Optional[Union[bool, Bool]] = None
    nmdc_ingest_priority: Optional[Union[str, "NMDCIngestPriority"]] = None
    data_modalities: Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]] = empty_list()
    sample_count: Optional[int] = None
    organism: Optional[str] = None
    preprocessed_data_available: Optional[Union[Union[str, "PreprocessedDataType"], list[Union[str, "PreprocessedDataType"]]]] = empty_list()
    preprocessed_data_counts: Optional[str] = None
    ncbi_data_quality_notes: Optional[str] = None
    primary_reference_info: Optional[Union[dict, PrimaryReferenceInfo]] = None
    source_reference: Optional[Union[dict, WebReference]] = None
    synthetic_communities: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.nmdc_study_id is not None and not isinstance(self.nmdc_study_id, URIorCURIE):
            self.nmdc_study_id = URIorCURIE(self.nmdc_study_id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.primary_reference is not None and not isinstance(self.primary_reference, URIorCURIE):
            self.primary_reference = URIorCURIE(self.primary_reference)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, Keyword) else Keyword(v) for v in self.keywords]

        if not isinstance(self.field_site_ids, list):
            self.field_site_ids = [self.field_site_ids] if self.field_site_ids is not None else []
        self.field_site_ids = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.field_site_ids]

        if self.study_design is not None and not isinstance(self.study_design, StudyDesign):
            self.study_design = StudyDesign(**as_dict(self.study_design))

        if not isinstance(self.variables, list):
            self.variables = [self.variables] if self.variables is not None else []
        self.variables = [v if isinstance(v, Variable) else Variable(**as_dict(v)) for v in self.variables]

        if self.pi is not None and not isinstance(self.pi, str):
            self.pi = str(self.pi)

        if not isinstance(self.bioproject_ids, list):
            self.bioproject_ids = [self.bioproject_ids] if self.bioproject_ids is not None else []
        self.bioproject_ids = [v if isinstance(v, str) else str(v) for v in self.bioproject_ids]

        if self.gold_study_id is not None and not isinstance(self.gold_study_id, str):
            self.gold_study_id = str(self.gold_study_id)

        if self.jgi_proposal_id is not None and not isinstance(self.jgi_proposal_id, str):
            self.jgi_proposal_id = str(self.jgi_proposal_id)

        if not isinstance(self.brc_dataset_ids, list):
            self.brc_dataset_ids = [self.brc_dataset_ids] if self.brc_dataset_ids is not None else []
        self.brc_dataset_ids = [v if isinstance(v, str) else str(v) for v in self.brc_dataset_ids]

        if self.nmdc_ingest_target is not None and not isinstance(self.nmdc_ingest_target, Bool):
            self.nmdc_ingest_target = Bool(self.nmdc_ingest_target)

        if self.nmdc_ingest_priority is not None and not isinstance(self.nmdc_ingest_priority, NMDCIngestPriority):
            self.nmdc_ingest_priority = NMDCIngestPriority(self.nmdc_ingest_priority)

        if not isinstance(self.data_modalities, list):
            self.data_modalities = [self.data_modalities] if self.data_modalities is not None else []
        self.data_modalities = [v if isinstance(v, DataType) else DataType(v) for v in self.data_modalities]

        if self.sample_count is not None and not isinstance(self.sample_count, int):
            self.sample_count = int(self.sample_count)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if not isinstance(self.preprocessed_data_available, list):
            self.preprocessed_data_available = [self.preprocessed_data_available] if self.preprocessed_data_available is not None else []
        self.preprocessed_data_available = [v if isinstance(v, PreprocessedDataType) else PreprocessedDataType(v) for v in self.preprocessed_data_available]

        if self.preprocessed_data_counts is not None and not isinstance(self.preprocessed_data_counts, str):
            self.preprocessed_data_counts = str(self.preprocessed_data_counts)

        if self.ncbi_data_quality_notes is not None and not isinstance(self.ncbi_data_quality_notes, str):
            self.ncbi_data_quality_notes = str(self.ncbi_data_quality_notes)

        if self.primary_reference_info is not None and not isinstance(self.primary_reference_info, PrimaryReferenceInfo):
            self.primary_reference_info = PrimaryReferenceInfo(**as_dict(self.primary_reference_info))

        if self.source_reference is not None and not isinstance(self.source_reference, WebReference):
            self.source_reference = WebReference(**as_dict(self.source_reference))

        if not isinstance(self.synthetic_communities, list):
            self.synthetic_communities = [self.synthetic_communities] if self.synthetic_communities is not None else []
        self.synthetic_communities = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.synthetic_communities]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Analysis(NamedThing):
    """
    A computational analysis performed on research data. This is an abstract base class for different types of
    analyses including KBase narratives, pipeline runs, and other computational workflows.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Analysis"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Analysis"
    class_name: ClassVar[str] = "Analysis"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Analysis

    id: Union[str, AnalysisId] = None
    primary_reference: Optional[Union[str, URIorCURIE]] = None
    additional_references: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    analysis_type: Optional[Union[str, "AnalysisType"]] = None
    input_data_description: Optional[str] = None
    output_data_types: Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]] = empty_list()
    primary_reference_info: Optional[Union[dict, PrimaryReferenceInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.primary_reference is not None and not isinstance(self.primary_reference, URIorCURIE):
            self.primary_reference = URIorCURIE(self.primary_reference)

        if not isinstance(self.additional_references, list):
            self.additional_references = [self.additional_references] if self.additional_references is not None else []
        self.additional_references = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.additional_references]

        if self.analysis_type is not None and not isinstance(self.analysis_type, AnalysisType):
            self.analysis_type = AnalysisType(self.analysis_type)

        if self.input_data_description is not None and not isinstance(self.input_data_description, str):
            self.input_data_description = str(self.input_data_description)

        if not isinstance(self.output_data_types, list):
            self.output_data_types = [self.output_data_types] if self.output_data_types is not None else []
        self.output_data_types = [v if isinstance(v, DataType) else DataType(v) for v in self.output_data_types]

        if self.primary_reference_info is not None and not isinstance(self.primary_reference_info, PrimaryReferenceInfo):
            self.primary_reference_info = PrimaryReferenceInfo(**as_dict(self.primary_reference_info))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KBaseNarrative(Analysis):
    """
    A KBase Narrative - a reproducible, shareable analysis workflow in the DOE Systems Biology Knowledgebase.
    Narratives combine data, analysis steps, and documentation in an executable Jupyter-like notebook format. Can be
    made public, shared, and assigned DOIs for citation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["KBaseNarrative"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:KBaseNarrative"
    class_name: ClassVar[str] = "KBaseNarrative"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.KBaseNarrative

    id: Union[str, KBaseNarrativeId] = None
    kbase_narrative_id: Optional[str] = None
    kbase_narrative_url: Optional[Union[str, URI]] = None
    kbase_workspace_id: Optional[str] = None
    osti_doi: Optional[str] = None
    is_static: Optional[Union[bool, Bool]] = None
    genome_count: Optional[int] = None
    sample_count: Optional[int] = None
    related_narratives: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, KBaseNarrativeId):
            self.id = KBaseNarrativeId(self.id)

        if self.kbase_narrative_id is not None and not isinstance(self.kbase_narrative_id, str):
            self.kbase_narrative_id = str(self.kbase_narrative_id)

        if self.kbase_narrative_url is not None and not isinstance(self.kbase_narrative_url, URI):
            self.kbase_narrative_url = URI(self.kbase_narrative_url)

        if self.kbase_workspace_id is not None and not isinstance(self.kbase_workspace_id, str):
            self.kbase_workspace_id = str(self.kbase_workspace_id)

        if self.osti_doi is not None and not isinstance(self.osti_doi, str):
            self.osti_doi = str(self.osti_doi)

        if self.is_static is not None and not isinstance(self.is_static, Bool):
            self.is_static = Bool(self.is_static)

        if self.genome_count is not None and not isinstance(self.genome_count, int):
            self.genome_count = int(self.genome_count)

        if self.sample_count is not None and not isinstance(self.sample_count, int):
            self.sample_count = int(self.sample_count)

        if not isinstance(self.related_narratives, list):
            self.related_narratives = [self.related_narratives] if self.related_narratives is not None else []
        self.related_narratives = [v if isinstance(v, str) else str(v) for v in self.related_narratives]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FlagshipGenome(YAMLRoot):
    """
    A flagship genome sequenced and maintained by a facility
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["FlagshipGenome"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:FlagshipGenome"
    class_name: ClassVar[str] = "FlagshipGenome"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.FlagshipGenome

    name: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    year: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.common_name is not None and not isinstance(self.common_name, str):
            self.common_name = str(self.common_name)

        if self.year is not None and not isinstance(self.year, int):
            self.year = int(self.year)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceData(YAMLRoot):
    """
    Reference data maintained by a facility
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["ReferenceData"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:ReferenceData"
    class_name: ClassVar[str] = "ReferenceData"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.ReferenceData

    microbial_genomes: Optional[str] = None
    plant_genomes: Optional[str] = None
    biolog_media: Optional[str] = None
    reactions_compounds: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.microbial_genomes is not None and not isinstance(self.microbial_genomes, str):
            self.microbial_genomes = str(self.microbial_genomes)

        if self.plant_genomes is not None and not isinstance(self.plant_genomes, str):
            self.plant_genomes = str(self.plant_genomes)

        if self.biolog_media is not None and not isinstance(self.biolog_media, str):
            self.biolog_media = str(self.biolog_media)

        if self.reactions_compounds is not None and not isinstance(self.reactions_compounds, str):
            self.reactions_compounds = str(self.reactions_compounds)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Capability(YAMLRoot):
    """
    A scientific capability or resource provided by a user facility, including instrumentation, platforms, and
    analytical services.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Capability"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Capability"
    class_name: ClassVar[str] = "Capability"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Capability

    name: Optional[str] = None
    description: Optional[str] = None
    capability_type: Optional[Union[str, "CapabilityType"]] = None
    instruments: Optional[Union[Union[dict, "Instrument"], list[Union[dict, "Instrument"]]]] = empty_list()
    access_mode: Optional[str] = None
    throughput: Optional[str] = None
    year_established: Optional[int] = None
    url: Optional[Union[str, URI]] = None
    applications: Optional[Union[str, list[str]]] = empty_list()
    data_products: Optional[Union[str, list[str]]] = empty_list()
    status: Optional[Union[str, "CapabilityStatus"]] = None
    commissioned_date: Optional[Union[str, XSDDate]] = None
    leader: Optional[str] = None
    future_expansion: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.capability_type is not None and not isinstance(self.capability_type, CapabilityType):
            self.capability_type = CapabilityType(self.capability_type)

        if not isinstance(self.instruments, list):
            self.instruments = [self.instruments] if self.instruments is not None else []
        self.instruments = [v if isinstance(v, Instrument) else Instrument(**as_dict(v)) for v in self.instruments]

        if self.access_mode is not None and not isinstance(self.access_mode, str):
            self.access_mode = str(self.access_mode)

        if self.throughput is not None and not isinstance(self.throughput, str):
            self.throughput = str(self.throughput)

        if self.year_established is not None and not isinstance(self.year_established, int):
            self.year_established = int(self.year_established)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if not isinstance(self.applications, list):
            self.applications = [self.applications] if self.applications is not None else []
        self.applications = [v if isinstance(v, str) else str(v) for v in self.applications]

        if not isinstance(self.data_products, list):
            self.data_products = [self.data_products] if self.data_products is not None else []
        self.data_products = [v if isinstance(v, str) else str(v) for v in self.data_products]

        if self.status is not None and not isinstance(self.status, CapabilityStatus):
            self.status = CapabilityStatus(self.status)

        if self.commissioned_date is not None and not isinstance(self.commissioned_date, XSDDate):
            self.commissioned_date = XSDDate(self.commissioned_date)

        if self.leader is not None and not isinstance(self.leader, str):
            self.leader = str(self.leader)

        if self.future_expansion is not None and not isinstance(self.future_expansion, str):
            self.future_expansion = str(self.future_expansion)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Instrument(YAMLRoot):
    """
    A scientific instrument or piece of equipment that supports a capability.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS["Instrument"]
    class_class_curie: ClassVar[str] = "nmdc_sfas_brcs:Instrument"
    class_name: ClassVar[str] = "Instrument"
    class_model_uri: ClassVar[URIRef] = NMDC_SFAS_BRCS.Instrument

    name: Optional[str] = None
    description: Optional[str] = None
    instrument_type: Optional[Union[str, "InstrumentType"]] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    count: Optional[int] = None
    specifications: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.instrument_type is not None and not isinstance(self.instrument_type, InstrumentType):
            self.instrument_type = InstrumentType(self.instrument_type)

        if self.manufacturer is not None and not isinstance(self.manufacturer, str):
            self.manufacturer = str(self.manufacturer)

        if self.model is not None and not isinstance(self.model, str):
            self.model = str(self.model)

        if self.count is not None and not isinstance(self.count, int):
            self.count = int(self.count)

        if self.specifications is not None and not isinstance(self.specifications, str):
            self.specifications = str(self.specifications)

        super().__post_init__(**kwargs)


# Enumerations
class ProgramType(EnumDefinitionImpl):
    """
    Types of DOE BER research programs
    """
    BIOENERGY_RESEARCH_CENTER = PermissibleValue(
        text="BIOENERGY_RESEARCH_CENTER",
        description="""A Bioenergy Research Center (BRC) - large-scale, multi-institutional center focused on biofuels and bioproducts from plant biomass""")
    SCIENTIFIC_FOCUS_AREA = PermissibleValue(
        text="SCIENTIFIC_FOCUS_AREA",
        description="A Scientific Focus Area (SFA) - integrated research program at DOE national laboratories")
    USER_FACILITY = PermissibleValue(
        text="USER_FACILITY",
        description="A DOE BER User Facility providing resources to the scientific community")
    DATA_REPOSITORY = PermissibleValue(
        text="DATA_REPOSITORY",
        description="A data repository or archive")
    DATA_COLLABORATIVE = PermissibleValue(
        text="DATA_COLLABORATIVE",
        description="A collaborative data initiative")
    BIOPREPAREDNESS_INITIATIVE = PermissibleValue(
        text="BIOPREPAREDNESS_INITIATIVE",
        description="""A biopreparedness research initiative such as BRaVE (Biopreparedness Research Virtual Environment) - typically cross-cutting, time-limited projects spanning multiple DOE offices""")
    AI_PILOT_PROJECT = PermissibleValue(
        text="AI_PILOT_PROJECT",
        description="""Artificial intelligence pilot project or AI-enabled science initiative, typically cross-cutting and often involving BER and ASCR.""")
    FIELD_CAMPAIGN = PermissibleValue(
        text="FIELD_CAMPAIGN",
        description="""Time-limited coordinated field campaign, often associated with an SFA or other BER program, producing campaign-specific observations and datasets.""")
    OTHER_INITIATIVE = PermissibleValue(
        text="OTHER_INITIATIVE",
        description="Other research initiatives that don't fit traditional categories")

    _defn = EnumDefinition(
        name="ProgramType",
        description="Types of DOE BER research programs",
    )

class SFAType(EnumDefinitionImpl):
    """
    Types of Scientific Focus Areas by program area
    """
    GENOMIC_SCIENCE_SFA = PermissibleValue(
        text="GENOMIC_SCIENCE_SFA",
        description="SFA within the Genomic Science Program focusing on plant and microbial systems biology")
    ENVIRONMENTAL_SYSTEM_SCIENCE_SFA = PermissibleValue(
        text="ENVIRONMENTAL_SYSTEM_SCIENCE_SFA",
        description="""SFA within the Environmental System Science program focusing on watershed and ecosystem processes""")
    ENVIRONMENTAL_MICROBIOME_SCIENCE = PermissibleValue(
        text="ENVIRONMENTAL_MICROBIOME_SCIENCE",
        description="SFA focused on environmental microbiome research")
    SECURE_BIOSYSTEMS_DESIGN = PermissibleValue(
        text="SECURE_BIOSYSTEMS_DESIGN",
        description="SFA focused on secure biosystems design and biocontainment")

    _defn = EnumDefinition(
        name="SFAType",
        description="Types of Scientific Focus Areas by program area",
    )

class InstitutionType(EnumDefinitionImpl):
    """
    Types of research institutions
    """
    NATIONAL_LABORATORY = PermissibleValue(
        text="NATIONAL_LABORATORY",
        description="A DOE National Laboratory")
    UNIVERSITY = PermissibleValue(
        text="UNIVERSITY",
        description="A university or academic institution")
    RESEARCH_INSTITUTE = PermissibleValue(
        text="RESEARCH_INSTITUTE",
        description="A research institute")
    FEDERAL_AGENCY = PermissibleValue(
        text="FEDERAL_AGENCY",
        description="A federal government agency")
    PRIVATE_SECTOR = PermissibleValue(
        text="PRIVATE_SECTOR",
        description="A private sector organization")

    _defn = EnumDefinition(
        name="InstitutionType",
        description="Types of research institutions",
    )

class PreprocessedDataType(EnumDefinitionImpl):
    """
    Types of preprocessed or derived data products available in public repositories. Used to identify studies with
    analysis-ready data for NMDC consideration.
    """
    MAGS = PermissibleValue(
        text="MAGS",
        description="""Metagenome-assembled genomes - draft genomes reconstructed from metagenomic data through binning and assembly""")
    GENOME_ASSEMBLIES = PermissibleValue(
        text="GENOME_ASSEMBLIES",
        description="Assembled genome sequences (contigs, scaffolds, or complete)")
    GENE_ANNOTATIONS = PermissibleValue(
        text="GENE_ANNOTATIONS",
        description="Predicted gene calls and functional annotations")
    FUNCTIONAL_ANNOTATIONS = PermissibleValue(
        text="FUNCTIONAL_ANNOTATIONS",
        description="Functional annotations (COG, KEGG, Pfam, etc.)")
    TAXONOMIC_CLASSIFICATIONS = PermissibleValue(
        text="TAXONOMIC_CLASSIFICATIONS",
        description="Taxonomic assignments for sequences or bins")
    READ_QC = PermissibleValue(
        text="READ_QC",
        description="Quality-controlled sequencing reads")
    ASSEMBLY_QC = PermissibleValue(
        text="ASSEMBLY_QC",
        description="Assembly quality metrics (CheckM, QUAST, etc.)")
    METABOLIC_MODELS = PermissibleValue(
        text="METABOLIC_MODELS",
        description="Genome-scale metabolic reconstructions")
    PHYLOGENETIC_TREES = PermissibleValue(
        text="PHYLOGENETIC_TREES",
        description="Phylogenetic trees or placements")

    _defn = EnumDefinition(
        name="PreprocessedDataType",
        description="""Types of preprocessed or derived data products available in public repositories. Used to identify studies with analysis-ready data for NMDC consideration.""",
    )

class DataType(EnumDefinitionImpl):
    """
    Types of scientific data
    """
    GENOMICS = PermissibleValue(
        text="GENOMICS",
        title="DNA sequencing assay",
        description="Genomic sequence data",
        meaning=OBI["0000626"])
    METAGENOMICS = PermissibleValue(
        text="METAGENOMICS",
        title="whole metagenome sequencing assay",
        description="Metagenomic sequence data",
        meaning=OBI["0002623"])
    TRANSCRIPTOMICS = PermissibleValue(
        text="TRANSCRIPTOMICS",
        title="transcription profiling assay",
        description="Transcriptomic expression data",
        meaning=OBI["0000424"])
    METATRANSCRIPTOMICS = PermissibleValue(
        text="METATRANSCRIPTOMICS",
        description="Metatranscriptomic data")
    AMPLICON_16S = PermissibleValue(
        text="AMPLICON_16S",
        title="16s ribosomal gene sequencing assay",
        description="16S rRNA gene amplicon sequencing for bacterial/archaeal profiling",
        meaning=OBI["0002763"])
    AMPLICON_ITS = PermissibleValue(
        text="AMPLICON_ITS",
        title="ITS rRNA gene sequencing assay",
        description="ITS amplicon sequencing for fungal profiling")
    AMPLICON_18S = PermissibleValue(
        text="AMPLICON_18S",
        description="18S rRNA gene amplicon sequencing for eukaryotic profiling")
    PROTEOMICS = PermissibleValue(
        text="PROTEOMICS",
        title="protein expression profiling assay",
        description="Proteomic data",
        meaning=OBI["0000615"])
    METABOLOMICS = PermissibleValue(
        text="METABOLOMICS",
        title="metabolite profiling assay",
        description="Metabolomic data",
        meaning=OBI["0000366"])
    EXOMETABOLOMICS = PermissibleValue(
        text="EXOMETABOLOMICS",
        description="Exometabolomic data (extracellular metabolites)")
    GEOSPATIAL = PermissibleValue(
        text="GEOSPATIAL",
        description="Geospatial or GIS data")
    PHENOTYPIC_DATA = PermissibleValue(
        text="PHENOTYPIC_DATA",
        description="Phenotypic measurement data")
    IMAGING_DATA = PermissibleValue(
        text="IMAGING_DATA",
        description="Various imaging data")
    ENVIRONMENTAL_SENSOR_DATA = PermissibleValue(
        text="ENVIRONMENTAL_SENSOR_DATA",
        description="Environmental sensor time series data")
    HYDROLOGICAL_DATA = PermissibleValue(
        text="HYDROLOGICAL_DATA",
        description="Hydrological measurements")
    BIOGEOCHEMICAL_DATA = PermissibleValue(
        text="BIOGEOCHEMICAL_DATA",
        description="Biogeochemical measurements")
    STABLE_ISOTOPE_DATA = PermissibleValue(
        text="STABLE_ISOTOPE_DATA",
        description="Stable isotope measurements")
    SYNTHETIC_BIOLOGY_CONSTRUCTS = PermissibleValue(
        text="SYNTHETIC_BIOLOGY_CONSTRUCTS",
        description="Synthetic biology parts and constructs")
    FIELD_TRIAL_DATA = PermissibleValue(
        text="FIELD_TRIAL_DATA",
        description="Data from field trials")
    CROP_YIELD_DATA = PermissibleValue(
        text="CROP_YIELD_DATA",
        description="Crop yield measurements")
    SOIL_MICROBIOME_DATA = PermissibleValue(
        text="SOIL_MICROBIOME_DATA",
        description="Soil microbiome characterization data")
    ENZYME_ACTIVITY_DATA = PermissibleValue(
        text="ENZYME_ACTIVITY_DATA",
        description="Enzyme activity measurements")
    ENZYME_KINETICS = PermissibleValue(
        text="ENZYME_KINETICS",
        description="Enzyme kinetics data")
    STRUCTURAL_BIOLOGY = PermissibleValue(
        text="STRUCTURAL_BIOLOGY",
        description="Structural biology data")
    GWAS_DATA = PermissibleValue(
        text="GWAS_DATA",
        description="Genome-wide association study data")
    ISOLATE_COLLECTIONS = PermissibleValue(
        text="ISOLATE_COLLECTIONS",
        description="Microbial isolate collection data")
    WATER_CHEMISTRY = PermissibleValue(
        text="WATER_CHEMISTRY",
        description="Water chemistry measurements")
    GROUNDWATER_CHEMISTRY = PermissibleValue(
        text="GROUNDWATER_CHEMISTRY",
        description="Groundwater chemistry data")
    MERCURY_SPECIATION = PermissibleValue(
        text="MERCURY_SPECIATION",
        description="Mercury speciation data")
    RADIOCARBON_DATA = PermissibleValue(
        text="RADIOCARBON_DATA",
        description="Radiocarbon dating data")
    REMOTE_SENSING = PermissibleValue(
        text="REMOTE_SENSING",
        description="Remote sensing imagery")
    SATELLITE_IMAGERY = PermissibleValue(
        text="SATELLITE_IMAGERY",
        description="Satellite imagery data")
    ECONOMIC_MODELING_DATA = PermissibleValue(
        text="ECONOMIC_MODELING_DATA",
        description="Techno-economic modeling outputs")
    LIFE_CYCLE_ASSESSMENT_DATA = PermissibleValue(
        text="LIFE_CYCLE_ASSESSMENT_DATA",
        description="Life cycle assessment data")
    FITNESS_DATA = PermissibleValue(
        text="FITNESS_DATA",
        description="Organism fitness data")
    CONTAINMENT_EFFICACY_DATA = PermissibleValue(
        text="CONTAINMENT_EFFICACY_DATA",
        description="Biocontainment efficacy measurements")
    FISH_IMAGING = PermissibleValue(
        text="FISH_IMAGING",
        description="Fluorescence in situ hybridization imaging data")
    SIDEROPHORE_DATA = PermissibleValue(
        text="SIDEROPHORE_DATA",
        description="Siderophore profile and iron-chelating compound data")
    ENDOHYPHAL_MICROBIOME_DATA = PermissibleValue(
        text="ENDOHYPHAL_MICROBIOME_DATA",
        description="Data on microorganisms living within fungal hyphae")
    BACTERIAL_FUNGAL_INTERACTION_DATA = PermissibleValue(
        text="BACTERIAL_FUNGAL_INTERACTION_DATA",
        description="Curated bacterial-fungal interaction records from literature or experiments")
    FUNGAL_HIGHWAY_DATA = PermissibleValue(
        text="FUNGAL_HIGHWAY_DATA",
        description="Data from fungal highway column experiments on bacterial dispersal via mycelia")

    _defn = EnumDefinition(
        name="DataType",
        description="Types of scientific data",
    )

class DataCollectionModality(EnumDefinitionImpl):
    """
    Methods and modalities for data collection
    """
    FIELD_EXPERIMENTS = PermissibleValue(
        text="FIELD_EXPERIMENTS",
        description="Field-based experimental studies")
    FIELD_TRIALS = PermissibleValue(
        text="FIELD_TRIALS",
        description="Agricultural or ecological field trials")
    GREENHOUSE_STUDIES = PermissibleValue(
        text="GREENHOUSE_STUDIES",
        description="Greenhouse-based studies")
    LABORATORY_EXPERIMENTS = PermissibleValue(
        text="LABORATORY_EXPERIMENTS",
        description="Laboratory-based experiments")
    LABORATORY_FERMENTATION = PermissibleValue(
        text="LABORATORY_FERMENTATION",
        description="Laboratory-scale fermentation studies")
    HIGH_THROUGHPUT_SCREENING = PermissibleValue(
        text="HIGH_THROUGHPUT_SCREENING",
        description="High-throughput screening methods")
    HIGH_THROUGHPUT_SEQUENCING = PermissibleValue(
        text="HIGH_THROUGHPUT_SEQUENCING",
        description="High-throughput DNA/RNA sequencing")
    HIGH_THROUGHPUT_PHENOTYPING = PermissibleValue(
        text="HIGH_THROUGHPUT_PHENOTYPING",
        description="High-throughput phenotyping methods")
    GENOME_SEQUENCING = PermissibleValue(
        text="GENOME_SEQUENCING",
        description="Whole genome sequencing")
    METAGENOMICS = PermissibleValue(
        text="METAGENOMICS",
        description="Metagenomic sequencing and analysis")
    TARGETED_METAGENOMICS = PermissibleValue(
        text="TARGETED_METAGENOMICS",
        description="Targeted metagenomic approaches")
    MULTI_OMICS = PermissibleValue(
        text="MULTI_OMICS",
        description="Integrated multi-omics approaches")
    REMOTE_SENSING = PermissibleValue(
        text="REMOTE_SENSING",
        description="Remote sensing and satellite imagery")
    MASS_SPECTROMETRY = PermissibleValue(
        text="MASS_SPECTROMETRY",
        description="Mass spectrometry analysis")
    NMR_SPECTROSCOPY = PermissibleValue(
        text="NMR_SPECTROSCOPY",
        description="Nuclear magnetic resonance spectroscopy")
    IMAGING = PermissibleValue(
        text="IMAGING",
        description="Various imaging techniques")
    BIOIMAGING = PermissibleValue(
        text="BIOIMAGING",
        description="Biological imaging techniques")
    CHEMICAL_IMAGING = PermissibleValue(
        text="CHEMICAL_IMAGING",
        description="Chemical imaging methods")
    LIVE_CELL_IMAGING = PermissibleValue(
        text="LIVE_CELL_IMAGING",
        description="Live cell imaging")
    NANOSIMS = PermissibleValue(
        text="NANOSIMS",
        description="NanoSIMS imaging")
    SYNCHROTRON_METHODS = PermissibleValue(
        text="SYNCHROTRON_METHODS",
        description="Synchrotron-based analytical methods")
    COMPUTATIONAL_MODELING = PermissibleValue(
        text="COMPUTATIONAL_MODELING",
        description="Computational and mathematical modeling")
    ECOSYSTEM_MODELING = PermissibleValue(
        text="ECOSYSTEM_MODELING",
        description="Ecosystem-scale modeling")
    STABLE_ISOTOPE_PROBING = PermissibleValue(
        text="STABLE_ISOTOPE_PROBING",
        description="Quantitative stable isotope probing (qSIP)")
    RADIOISOTOPE_APPROACHES = PermissibleValue(
        text="RADIOISOTOPE_APPROACHES",
        description="Radioisotope tracer methods")
    GENOME_WIDE_ASSOCIATION = PermissibleValue(
        text="GENOME_WIDE_ASSOCIATION",
        description="Genome-wide association studies")
    COMMON_GARDEN_EXPERIMENTS = PermissibleValue(
        text="COMMON_GARDEN_EXPERIMENTS",
        description="Common garden experimental designs")
    FERMENTATION_STUDIES = PermissibleValue(
        text="FERMENTATION_STUDIES",
        description="Fermentation process studies")
    METABOLIC_FLUX_ANALYSIS = PermissibleValue(
        text="METABOLIC_FLUX_ANALYSIS",
        description="Metabolic flux analysis")
    TECHNO_ECONOMIC_ANALYSIS = PermissibleValue(
        text="TECHNO_ECONOMIC_ANALYSIS",
        description="Techno-economic analysis")
    ROBOTIC_AUTOMATION = PermissibleValue(
        text="ROBOTIC_AUTOMATION",
        description="Robotic/automated laboratory systems")
    GENOME_SCALE_ENGINEERING = PermissibleValue(
        text="GENOME_SCALE_ENGINEERING",
        description="Genome-scale engineering approaches")
    CRISPR_GENE_EDITING = PermissibleValue(
        text="CRISPR_GENE_EDITING",
        description="CRISPR-based gene editing")
    BACTERIAL_ISOLATION = PermissibleValue(
        text="BACTERIAL_ISOLATION",
        description="Bacterial isolation and culturing")
    FIELD_SENSORS = PermissibleValue(
        text="FIELD_SENSORS",
        description="Field-deployed environmental sensors")
    STREAM_SAMPLING = PermissibleValue(
        text="STREAM_SAMPLING",
        description="Stream and water body sampling")
    GROUNDWATER_MONITORING = PermissibleValue(
        text="GROUNDWATER_MONITORING",
        description="Groundwater monitoring")
    LONG_TERM_ECOLOGICAL_RESEARCH = PermissibleValue(
        text="LONG_TERM_ECOLOGICAL_RESEARCH",
        description="Long-term ecological research sites")
    FABRICATED_ECOSYSTEMS = PermissibleValue(
        text="FABRICATED_ECOSYSTEMS",
        description="Fabricated/controlled ecosystem platforms (e.g., EcoFAB)")
    FUNGAL_HIGHWAY_COLUMNS = PermissibleValue(
        text="FUNGAL_HIGHWAY_COLUMNS",
        description="Fungal highway column devices for studying bacterial dispersal via mycelia")
    FISH_MICROSCOPY = PermissibleValue(
        text="FISH_MICROSCOPY",
        description="Fluorescence in situ hybridization microscopy")
    COCULTURE_EXPERIMENTS = PermissibleValue(
        text="COCULTURE_EXPERIMENTS",
        description="Bacterial-fungal co-culture experiments")
    SEQUENCE_ENRICHMENT = PermissibleValue(
        text="SEQUENCE_ENRICHMENT",
        description="Sequence-based enrichment techniques for detecting endosymbionts")

    _defn = EnumDefinition(
        name="DataCollectionModality",
        description="Methods and modalities for data collection",
    )

class VariableRole(EnumDefinitionImpl):
    """
    Roles that a variable can play in a study design, dataset, or analysis. Where possible, roles are aligned to OBI,
    STATO, or EFO terms. Use the narrower study-design roles when the variable's role is known from the experimental
    design; use MEASURED_VARIABLE for observed data fields when no dependent/independent interpretation is intended.
    """
    STUDY_DESIGN_INDEPENDENT_VARIABLE = PermissibleValue(
        text="STUDY_DESIGN_INDEPENDENT_VARIABLE",
        title="study design independent variable",
        description="""Study design variable that is varied, selected, or otherwise used to explain or predict changes in another variable.""",
        meaning=OBI["0000750"])
    STUDY_DESIGN_DEPENDENT_VARIABLE = PermissibleValue(
        text="STUDY_DESIGN_DEPENDENT_VARIABLE",
        title="study design dependent variable",
        description="Study design variable whose value is expected to vary as a result of other variables.",
        meaning=OBI["0000751"])
    STUDY_DESIGN_CONTROLLED_VARIABLE = PermissibleValue(
        text="STUDY_DESIGN_CONTROLLED_VARIABLE",
        title="study design controlled variable",
        description="Study design variable held constant or constrained by the study design.",
        meaning=OBI["0000785"])
    EXPERIMENTAL_FACTOR = PermissibleValue(
        text="EXPERIMENTAL_FACTOR",
        title="experimental factor",
        description="Variable representing an experimental factor or condition.",
        meaning=EFO["0000001"])
    BLOCKING_VARIABLE = PermissibleValue(
        text="BLOCKING_VARIABLE",
        title="blocking variable",
        description="Variable used to form blocks or strata in a study design or analysis.",
        meaning=STATO["0000248"])
    MEASURED_VARIABLE = PermissibleValue(
        text="MEASURED_VARIABLE",
        description="Directly observed or measured variable.")
    COVARIATE = PermissibleValue(
        text="COVARIATE",
        description="Additional contextual or adjustment variable included in an analysis.")
    DERIVED = PermissibleValue(
        text="DERIVED",
        description="Variable computed, transformed, or inferred from other variables")
    DATE_TIME_VARIABLE = PermissibleValue(
        text="DATE_TIME_VARIABLE",
        title="date Time variable",
        description="Variable whose values represent dates or times.",
        meaning=STATO["0000729"])
    TIME_TO_EVENT_VARIABLE = PermissibleValue(
        text="TIME_TO_EVENT_VARIABLE",
        title="time-to-event variable",
        description="Variable whose values represent elapsed time until an event.",
        meaning=STATO["0000731"])
    SPATIAL_INDEX = PermissibleValue(
        text="SPATIAL_INDEX",
        description="Location, plot, coordinate, depth, transect, or other spatial index")
    GROUPING = PermissibleValue(
        text="GROUPING",
        description="Replicate group, block, batch, genotype group, or other grouping variable")
    IDENTIFIER = PermissibleValue(
        text="IDENTIFIER",
        description="Sample, subject, feature, file, or other identifier field")
    QUALITY_CONTROL = PermissibleValue(
        text="QUALITY_CONTROL",
        description="Quality flag, censoring flag, uncertainty estimate, or QC metric")

    _defn = EnumDefinition(
        name="VariableRole",
        description="""Roles that a variable can play in a study design, dataset, or analysis. Where possible, roles are aligned to OBI, STATO, or EFO terms. Use the narrower study-design roles when the variable's role is known from the experimental design; use MEASURED_VARIABLE for observed data fields when no dependent/independent interpretation is intended.""",
    )

class VariableValueType(EnumDefinitionImpl):
    """
    Basic value shape for variables
    """
    NUMERIC = PermissibleValue(
        text="NUMERIC",
        description="Numeric value that may include decimals")
    INTEGER = PermissibleValue(
        text="INTEGER",
        description="Integer count or whole-number value")
    CATEGORICAL = PermissibleValue(
        text="CATEGORICAL",
        description="Value drawn from a finite set of categories or levels")
    BOOLEAN = PermissibleValue(
        text="BOOLEAN",
        description="True/false value")
    DATETIME = PermissibleValue(
        text="DATETIME",
        description="Date, time, or timestamp value")
    TEXT = PermissibleValue(
        text="TEXT",
        description="Free-text string value")
    IDENTIFIER = PermissibleValue(
        text="IDENTIFIER",
        description="Identifier or accession value")
    ONTOLOGY_TERM = PermissibleValue(
        text="ONTOLOGY_TERM",
        description="Ontology CURIE, URI, or controlled vocabulary term")
    ARRAY = PermissibleValue(
        text="ARRAY",
        description="Ordered list, vector, spectrum, profile, or other repeated values")
    OBJECT = PermissibleValue(
        text="OBJECT",
        description="Structured object or nested record")

    _defn = EnumDefinition(
        name="VariableValueType",
        description="Basic value shape for variables",
    )

class OntologyMappingRelation(EnumDefinitionImpl):
    """
    SSSOM/SKOS mapping predicate used to qualify how a local variable, field, or data-dictionary entry maps to an
    ontology term.
    """
    EXACT_MATCH = PermissibleValue(
        text="EXACT_MATCH",
        title="exact match",
        description="The local variable and ontology term can be used interchangeably in this context.")
    CLOSE_MATCH = PermissibleValue(
        text="CLOSE_MATCH",
        title="close match",
        description="""The local variable and ontology term are sufficiently similar for many uses but should not be treated as exact equivalents.""")
    BROAD_MATCH = PermissibleValue(
        text="BROAD_MATCH",
        title="broad match",
        description="The ontology term is broader than the local variable.")
    NARROW_MATCH = PermissibleValue(
        text="NARROW_MATCH",
        title="narrow match",
        description="The ontology term is narrower than the local variable.")
    RELATED_MATCH = PermissibleValue(
        text="RELATED_MATCH",
        title="related match",
        description="The local variable and ontology term are associated but not equivalent or hierarchical.")

    _defn = EnumDefinition(
        name="OntologyMappingRelation",
        description="""SSSOM/SKOS mapping predicate used to qualify how a local variable, field, or data-dictionary entry maps to an ontology term.""",
    )

class StudyDesignTerm(EnumDefinitionImpl):
    """
    OBI study design terms
    """
    _defn = EnumDefinition(
        name="StudyDesignTerm",
        description="OBI study design terms",
    )

class MIXSVariableTerm(EnumDefinitionImpl):
    """
    MIxS terms commonly useful when mapping catalogued study or dataset variables to sample, host, environment, and
    sequencing metadata fields.
    """
    EXPERIMENTAL_FACTOR = PermissibleValue(
        text="EXPERIMENTAL_FACTOR",
        title="experimental factor",
        meaning=MIXS["0000008"])
    COLLECTION_DATE = PermissibleValue(
        text="COLLECTION_DATE",
        title="collection date",
        meaning=MIXS["0000011"])
    ENV_BROAD_SCALE = PermissibleValue(
        text="ENV_BROAD_SCALE",
        title="broad-scale environmental context",
        meaning=MIXS["0000012"])
    ENV_LOCAL_SCALE = PermissibleValue(
        text="ENV_LOCAL_SCALE",
        title="local environmental context",
        meaning=MIXS["0000013"])
    ENV_MEDIUM = PermissibleValue(
        text="ENV_MEDIUM",
        title="environmental medium",
        meaning=MIXS["0000014"])
    DEPTH = PermissibleValue(
        text="DEPTH",
        title="depth",
        meaning=MIXS["0000018"])
    WATER_CONTENT = PermissibleValue(
        text="WATER_CONTENT",
        title="water content",
        meaning=MIXS["0000185"])
    HOST_COMMON_NAME = PermissibleValue(
        text="HOST_COMMON_NAME",
        title="host common name",
        meaning=MIXS["0000248"])
    HOST_TAXID = PermissibleValue(
        text="HOST_TAXID",
        title="host taxid",
        meaning=MIXS["0000250"])
    HOST_GENOTYPE = PermissibleValue(
        text="HOST_GENOTYPE",
        title="host genotype",
        meaning=MIXS["0000365"])
    FERTILIZER_REGIMEN = PermissibleValue(
        text="FERTILIZER_REGIMEN",
        title="fertilizer regimen",
        meaning=MIXS["0000556"])
    WATERING_REGIMEN = PermissibleValue(
        text="WATERING_REGIMEN",
        title="watering regimen",
        meaning=MIXS["0000591"])
    CHEMICAL_ADMINISTRATION = PermissibleValue(
        text="CHEMICAL_ADMINISTRATION",
        title="chemical administration",
        meaning=MIXS["0000751"])
    PERTURBATION = PermissibleValue(
        text="PERTURBATION",
        title="perturbation",
        meaning=MIXS["0000754"])
    SEASON = PermissibleValue(
        text="SEASON",
        title="season",
        meaning=MIXS["0000829"])
    PLANT_GROWTH_MEDIUM = PermissibleValue(
        text="PLANT_GROWTH_MEDIUM",
        title="plant growth medium",
        meaning=MIXS["0001057"])
    SAMPLE_NAME = PermissibleValue(
        text="SAMPLE_NAME",
        title="sample name",
        meaning=MIXS["0001107"])
    SOIL_TEMPERATURE = PermissibleValue(
        text="SOIL_TEMPERATURE",
        title="soil temperature",
        meaning=MIXS["0001163"])

    _defn = EnumDefinition(
        name="MIXSVariableTerm",
        description="""MIxS terms commonly useful when mapping catalogued study or dataset variables to sample, host, environment, and sequencing metadata fields.""",
    )

class Keyword(EnumDefinitionImpl):
    """
    Keywords describing research focus areas with hierarchical organization
    """
    BIOENERGY = PermissibleValue(
        text="BIOENERGY",
        description="Bioenergy research focus area")
    FEEDSTOCK_CROP = PermissibleValue(
        text="FEEDSTOCK_CROP",
        description="Bioenergy feedstock crops")
    CARBON_AND_NUTRIENT_CYCLING = PermissibleValue(
        text="CARBON_AND_NUTRIENT_CYCLING",
        description="Carbon and nutrient cycling processes")
    SOIL_MICROBIOME = PermissibleValue(
        text="SOIL_MICROBIOME",
        description="Soil microbiome research")
    PLANT_MICROBE_INTERACTIONS = PermissibleValue(
        text="PLANT_MICROBE_INTERACTIONS",
        description="Plant-microbe interactions")
    WATERSHED_SCIENCE = PermissibleValue(
        text="WATERSHED_SCIENCE",
        description="Watershed and hydrology science")
    BIOGEOCHEMISTRY = PermissibleValue(
        text="BIOGEOCHEMISTRY",
        description="Biogeochemical processes")
    CONTAMINANT_SCIENCE = PermissibleValue(
        text="CONTAMINANT_SCIENCE",
        description="Contaminant fate and transport")
    SYNTHETIC_BIOLOGY = PermissibleValue(
        text="SYNTHETIC_BIOLOGY",
        description="Synthetic biology and engineering")
    OMICS_METHODS = PermissibleValue(
        text="OMICS_METHODS",
        description="Omics methods and approaches")
    WETLAND_SCIENCE = PermissibleValue(
        text="WETLAND_SCIENCE",
        description="Wetland ecosystem science")
    TECHNOLOGY_PLATFORM = PermissibleValue(
        text="TECHNOLOGY_PLATFORM",
        description="Technology platforms and tools")
    BIOFUELS = PermissibleValue(
        text="BIOFUELS",
        description="Biofuel production")
    BIOPRODUCTS = PermissibleValue(
        text="BIOPRODUCTS",
        description="Bio-based products")
    SUSTAINABLE_AVIATION_FUEL = PermissibleValue(
        text="SUSTAINABLE_AVIATION_FUEL",
        description="Sustainable aviation fuel production")
    LIGNOCELLULOSE = PermissibleValue(
        text="LIGNOCELLULOSE",
        description="Lignocellulosic biomass")
    CELLULOSIC_BIOMASS = PermissibleValue(
        text="CELLULOSIC_BIOMASS",
        description="Cellulosic biomass conversion")
    LIGNIN = PermissibleValue(
        text="LIGNIN",
        description="Lignin structure and valorization")
    LIGNIN_VALORIZATION = PermissibleValue(
        text="LIGNIN_VALORIZATION",
        description="Lignin valorization for products")
    BIOMASS_RECALCITRANCE = PermissibleValue(
        text="BIOMASS_RECALCITRANCE",
        description="Biomass recalcitrance and deconstruction")
    MICROBIAL_CONVERSION = PermissibleValue(
        text="MICROBIAL_CONVERSION",
        description="Microbial conversion of biomass")
    SUSTAINABILITY = PermissibleValue(
        text="SUSTAINABILITY",
        description="Sustainability aspects of bioenergy")
    MARGINAL_LANDS = PermissibleValue(
        text="MARGINAL_LANDS",
        description="Marginal lands for bioenergy production")
    LIFE_CYCLE_ASSESSMENT = PermissibleValue(
        text="LIFE_CYCLE_ASSESSMENT",
        description="Life cycle assessment for sustainability")
    IONIC_LIQUIDS = PermissibleValue(
        text="IONIC_LIQUIDS",
        description="Ionic liquids for biomass pretreatment")
    LIPID_ACCUMULATION = PermissibleValue(
        text="LIPID_ACCUMULATION",
        description="Lipid accumulation in plants")
    OIL_CROPS = PermissibleValue(
        text="OIL_CROPS",
        description="Oil crops for biofuel production")
    TERPENES = PermissibleValue(
        text="TERPENES",
        description="Terpene-based biofuels")
    FATTY_ACIDS = PermissibleValue(
        text="FATTY_ACIDS",
        description="Fatty acid-based biofuels")
    SWITCHGRASS = PermissibleValue(
        text="SWITCHGRASS",
        description="Panicum virgatum (switchgrass)")
    POPLAR = PermissibleValue(
        text="POPLAR",
        description="Populus species (poplar/cottonwood)")
    POPULUS = PermissibleValue(
        text="POPULUS",
        description="Populus genus")
    MISCANTHUS = PermissibleValue(
        text="MISCANTHUS",
        description="Miscanthus grass")
    SORGHUM = PermissibleValue(
        text="SORGHUM",
        description="Sorghum species")
    ENERGY_SORGHUM = PermissibleValue(
        text="ENERGY_SORGHUM",
        description="Energy sorghum varieties")
    SUGARCANE = PermissibleValue(
        text="SUGARCANE",
        description="Sugarcane")
    BRACHYPODIUM = PermissibleValue(
        text="BRACHYPODIUM",
        description="Brachypodium distachyon model grass")
    TALL_WHEATGRASS = PermissibleValue(
        text="TALL_WHEATGRASS",
        description="Tall wheatgrass")
    PERENNIAL_CROPS = PermissibleValue(
        text="PERENNIAL_CROPS",
        description="Perennial bioenergy crops")
    PLANT_CELL_WALLS = PermissibleValue(
        text="PLANT_CELL_WALLS",
        description="Plant cell wall composition and deconstruction")
    CARBON_CYCLING = PermissibleValue(
        text="CARBON_CYCLING",
        description="Carbon cycling processes")
    SOIL_CARBON = PermissibleValue(
        text="SOIL_CARBON",
        description="Soil carbon dynamics")
    CARBON_PERSISTENCE = PermissibleValue(
        text="CARBON_PERSISTENCE",
        description="Soil carbon persistence mechanisms")
    CARBON_FLUX = PermissibleValue(
        text="CARBON_FLUX",
        description="Carbon flux measurements")
    CARBON_USE_EFFICIENCY = PermissibleValue(
        text="CARBON_USE_EFFICIENCY",
        description="Carbon use efficiency in microbes")
    NUTRIENT_CYCLING = PermissibleValue(
        text="NUTRIENT_CYCLING",
        description="Nutrient cycling processes")
    DENITRIFICATION = PermissibleValue(
        text="DENITRIFICATION",
        description="Microbial denitrification")
    NITRATE = PermissibleValue(
        text="NITRATE",
        description="Nitrate cycling")
    DECOMPOSITION = PermissibleValue(
        text="DECOMPOSITION",
        description="Decomposition processes")
    SOIL_ORGANIC_MATTER = PermissibleValue(
        text="SOIL_ORGANIC_MATTER",
        description="Soil organic matter dynamics")
    RHIZOSPHERE = PermissibleValue(
        text="RHIZOSPHERE",
        description="Rhizosphere microbial communities")
    MICROBIAL_ECOSYSTEMS = PermissibleValue(
        text="MICROBIAL_ECOSYSTEMS",
        description="Microbial ecosystem dynamics")
    MICROBIAL_INTERACTIONS = PermissibleValue(
        text="MICROBIAL_INTERACTIONS",
        description="Microbial community interactions")
    VIROME = PermissibleValue(
        text="VIROME",
        description="Soil viral communities")
    PHAGE = PermissibleValue(
        text="PHAGE",
        description="Bacteriophages in soil")
    BACTERIAL_FUNGAL_INTERACTIONS = PermissibleValue(
        text="BACTERIAL_FUNGAL_INTERACTIONS",
        description="Bacterial-fungal interactions in soil")
    ENDOHYPHAL_BACTERIA = PermissibleValue(
        text="ENDOHYPHAL_BACTERIA",
        description="Bacteria living within fungal hyphae")
    FUNGAL_HIGHWAYS = PermissibleValue(
        text="FUNGAL_HIGHWAYS",
        description="Bacterial dispersal via fungal mycelial networks")
    SIDEROPHORES = PermissibleValue(
        text="SIDEROPHORES",
        description="Iron-chelating compounds mediating microbial interactions")
    SUBSURFACE_MICROBIOLOGY = PermissibleValue(
        text="SUBSURFACE_MICROBIOLOGY",
        description="Subsurface microbial communities")
    METAPHENOME = PermissibleValue(
        text="METAPHENOME",
        description="Metaphenome and community phenotypes")
    PLANT_PRODUCTIVITY = PermissibleValue(
        text="PLANT_PRODUCTIVITY",
        description="Plant productivity impacts")
    MOISTURE_EFFECTS = PermissibleValue(
        text="MOISTURE_EFFECTS",
        description="Moisture effects on microbiomes")
    MOISTURE_REGIMES = PermissibleValue(
        text="MOISTURE_REGIMES",
        description="Moisture regime effects")
    ENDOPHYTES = PermissibleValue(
        text="ENDOPHYTES",
        description="Endophytic microorganisms")
    MYCORRHIZAE = PermissibleValue(
        text="MYCORRHIZAE",
        description="Mycorrhizal associations")
    BIOENERGY_CROPS = PermissibleValue(
        text="BIOENERGY_CROPS",
        description="Plant-microbe interactions in bioenergy crops")
    PLANT_GROWTH_PROMOTING_BACTERIA = PermissibleValue(
        text="PLANT_GROWTH_PROMOTING_BACTERIA",
        description="Plant growth promoting bacteria")
    CO_EVOLUTION = PermissibleValue(
        text="CO_EVOLUTION",
        description="Co-evolution of plants and microbes")
    WATERSHED_HYDROLOGY = PermissibleValue(
        text="WATERSHED_HYDROLOGY",
        description="Watershed hydrological processes")
    WATERSHED_DYNAMICS = PermissibleValue(
        text="WATERSHED_DYNAMICS",
        description="Watershed dynamics and evolution")
    MOUNTAIN_HYDROLOGY = PermissibleValue(
        text="MOUNTAIN_HYDROLOGY",
        description="Mountain watershed hydrology")
    HYDROLOGIC_CONNECTIVITY = PermissibleValue(
        text="HYDROLOGIC_CONNECTIVITY",
        description="Hydrological connectivity")
    SNOWMELT = PermissibleValue(
        text="SNOWMELT",
        description="Snowmelt hydrology")
    DROUGHT = PermissibleValue(
        text="DROUGHT",
        description="Drought impacts")
    STREAM_NETWORKS = PermissibleValue(
        text="STREAM_NETWORKS",
        description="Stream network structure and function")
    RIVER_CORRIDORS = PermissibleValue(
        text="RIVER_CORRIDORS",
        description="River corridor processes")
    GROUNDWATER_QUALITY = PermissibleValue(
        text="GROUNDWATER_QUALITY",
        description="Groundwater quality")
    UPPER_COLORADO_RIVER_BASIN = PermissibleValue(
        text="UPPER_COLORADO_RIVER_BASIN",
        description="Upper Colorado River Basin study site")
    TENNESSEE_RIVER_BASIN = PermissibleValue(
        text="TENNESSEE_RIVER_BASIN",
        description="Tennessee River Basin study site")
    YAKIMA_RIVER_BASIN = PermissibleValue(
        text="YAKIMA_RIVER_BASIN",
        description="Yakima River Basin study site")
    LAND_COVER = PermissibleValue(
        text="LAND_COVER",
        description="Land cover effects on watersheds")
    WILDFIRE = PermissibleValue(
        text="WILDFIRE",
        description="Wildfire impacts on watersheds")
    STREAM_DRYING = PermissibleValue(
        text="STREAM_DRYING",
        description="Stream drying processes")
    HYDRO_BIOGEOCHEMISTRY = PermissibleValue(
        text="HYDRO_BIOGEOCHEMISTRY",
        description="Hydro-biogeochemical processes")
    SEDIMENT_WATER_INTERFACE = PermissibleValue(
        text="SEDIMENT_WATER_INTERFACE",
        description="Sediment-water interface processes")
    SUBSURFACE_INTERFACES = PermissibleValue(
        text="SUBSURFACE_INTERFACES",
        description="Subsurface interface processes")
    REDOX_CYCLING = PermissibleValue(
        text="REDOX_CYCLING",
        description="Redox cycling processes")
    METAL_REDUCTION = PermissibleValue(
        text="METAL_REDUCTION",
        description="Microbial metal reduction")
    INTERFACES = PermissibleValue(
        text="INTERFACES",
        description="Interface-mediated processes")
    MERCURY = PermissibleValue(
        text="MERCURY",
        description="Mercury contamination and cycling")
    METHYLMERCURY = PermissibleValue(
        text="METHYLMERCURY",
        description="Mercury methylation")
    MERCURY_METHYLATION = PermissibleValue(
        text="MERCURY_METHYLATION",
        description="Mercury methylation processes")
    HGCA = PermissibleValue(
        text="HGCA",
        description="hgcA gene for mercury methylation")
    HGCB = PermissibleValue(
        text="HGCB",
        description="hgcB gene for mercury methylation")
    URANIUM = PermissibleValue(
        text="URANIUM",
        description="Uranium contamination")
    ACTINIDES = PermissibleValue(
        text="ACTINIDES",
        description="Actinide behavior")
    CONTAMINANT_TRANSPORT = PermissibleValue(
        text="CONTAMINANT_TRANSPORT",
        description="Contaminant transport processes")
    COLLOID_TRANSPORT = PermissibleValue(
        text="COLLOID_TRANSPORT",
        description="Colloid-facilitated transport")
    METABOLIC_ENGINEERING = PermissibleValue(
        text="METABOLIC_ENGINEERING",
        description="Metabolic engineering approaches")
    GENOME_ENGINEERING = PermissibleValue(
        text="GENOME_ENGINEERING",
        description="Genome engineering technologies")
    CRISPR = PermissibleValue(
        text="CRISPR",
        description="CRISPR-based gene editing")
    GENOMIC_SELECTION = PermissibleValue(
        text="GENOMIC_SELECTION",
        description="Genomic selection methods")
    MICROBIAL_CHASSIS = PermissibleValue(
        text="MICROBIAL_CHASSIS",
        description="Microbial chassis organisms")
    SHEWANELLA = PermissibleValue(
        text="SHEWANELLA",
        description="Shewanella as chassis organism")
    BIOCONTAINMENT = PermissibleValue(
        text="BIOCONTAINMENT",
        description="Biocontainment strategies")
    BIOSECURITY = PermissibleValue(
        text="BIOSECURITY",
        description="Biosecurity considerations")
    BIODEFENSE = PermissibleValue(
        text="BIODEFENSE",
        description="Biodefense applications")
    BIOSYSTEMS_DESIGN = PermissibleValue(
        text="BIOSYSTEMS_DESIGN",
        description="Biosystems design approaches")
    ECOSYSTEM_ENGINEERING = PermissibleValue(
        text="ECOSYSTEM_ENGINEERING",
        description="Ecosystem engineering")
    MICROBIAL_INVASION = PermissibleValue(
        text="MICROBIAL_INVASION",
        description="Microbial invasion dynamics")
    FUNGAL_PATHOGENS = PermissibleValue(
        text="FUNGAL_PATHOGENS",
        description="Fungal pathogens")
    SYSTEMS_BIOLOGY = PermissibleValue(
        text="SYSTEMS_BIOLOGY",
        description="Systems biology approaches")
    MACHINE_LEARNING = PermissibleValue(
        text="MACHINE_LEARNING",
        description="Machine learning for biological design")
    DNA_BARCODING = PermissibleValue(
        text="DNA_BARCODING",
        description="DNA barcoding for tracking")
    COMBIGEM = PermissibleValue(
        text="COMBIGEM",
        description="CombiGEM combinatorial engineering")
    METAGENOMICS = PermissibleValue(
        text="METAGENOMICS",
        description="Metagenomic approaches")
    STABLE_ISOTOPES = PermissibleValue(
        text="STABLE_ISOTOPES",
        description="Stable isotope approaches")
    QSIP = PermissibleValue(
        text="QSIP",
        description="Quantitative stable isotope probing")
    NANOSIMS = PermissibleValue(
        text="NANOSIMS",
        description="NanoSIMS imaging")
    MODEX = PermissibleValue(
        text="MODEX",
        description="Model-experiment integration")
    WHONDRS = PermissibleValue(
        text="WHONDRS",
        description="WHONDRS consortium")
    WETLAND_BIOGEOCHEMISTRY = PermissibleValue(
        text="WETLAND_BIOGEOCHEMISTRY",
        description="Wetland biogeochemistry")
    WETLAND_RESILIENCE = PermissibleValue(
        text="WETLAND_RESILIENCE",
        description="Wetland resilience")
    RIPARIAN_WETLAND = PermissibleValue(
        text="RIPARIAN_WETLAND",
        description="Riparian wetland ecosystems")
    FLOODPLAIN = PermissibleValue(
        text="FLOODPLAIN",
        description="Floodplain ecosystems")
    CAPILLARY_FRINGE = PermissibleValue(
        text="CAPILLARY_FRINGE",
        description="Capillary fringe processes")
    SAVANNAH_RIVER_SITE = PermissibleValue(
        text="SAVANNAH_RIVER_SITE",
        description="Savannah River Site study location")
    ENVIRONMENTAL_CHANGE = PermissibleValue(
        text="ENVIRONMENTAL_CHANGE",
        description="Environmental change impacts")
    ENVIRONMENTAL_SYSTEMS = PermissibleValue(
        text="ENVIRONMENTAL_SYSTEMS",
        description="Environmental systems")
    FABRICATED_ECOSYSTEMS = PermissibleValue(
        text="FABRICATED_ECOSYSTEMS",
        description="Fabricated ecosystem platforms")
    ECOFAB = PermissibleValue(
        text="ECOFAB",
        description="EcoFAB platform")
    LONG_TERM_ECOLOGICAL_RESEARCH = PermissibleValue(
        text="LONG_TERM_ECOLOGICAL_RESEARCH",
        description="Long-term ecological research sites (e.g., LTER network)")

    _defn = EnumDefinition(
        name="Keyword",
        description="Keywords describing research focus areas with hierarchical organization",
    )

class CapabilityType(EnumDefinitionImpl):
    """
    Types of scientific capabilities provided by user facilities
    """
    SEQUENCING = PermissibleValue(
        text="SEQUENCING",
        description="DNA/RNA sequencing capabilities")
    SYNTHESIS = PermissibleValue(
        text="SYNTHESIS",
        description="DNA/protein synthesis capabilities")
    MASS_SPECTROMETRY = PermissibleValue(
        text="MASS_SPECTROMETRY",
        description="Mass spectrometry capabilities")
    NMR = PermissibleValue(
        text="NMR",
        description="Nuclear magnetic resonance capabilities")
    IMAGING = PermissibleValue(
        text="IMAGING",
        description="Imaging and microscopy capabilities")
    PHENOTYPING = PermissibleValue(
        text="PHENOTYPING",
        description="Phenotyping and functional characterization")
    COMPUTATIONAL = PermissibleValue(
        text="COMPUTATIONAL",
        description="Computational and data analysis capabilities")
    SAMPLE_PREPARATION = PermissibleValue(
        text="SAMPLE_PREPARATION",
        description="Sample preparation and processing")
    SHORT_READ_SEQUENCING = PermissibleValue(
        text="SHORT_READ_SEQUENCING",
        description="Short-read sequencing (Illumina, etc.)")
    LONG_READ_SEQUENCING = PermissibleValue(
        text="LONG_READ_SEQUENCING",
        description="Long-read sequencing (PacBio, Oxford Nanopore)")
    SINGLE_CELL_SEQUENCING = PermissibleValue(
        text="SINGLE_CELL_SEQUENCING",
        description="Single-cell genomics and transcriptomics")
    METAGENOME_SEQUENCING = PermissibleValue(
        text="METAGENOME_SEQUENCING",
        description="Metagenomic sequencing")
    RNASEQ = PermissibleValue(
        text="RNASEQ",
        description="RNA sequencing and transcriptomics")
    DNA_SYNTHESIS = PermissibleValue(
        text="DNA_SYNTHESIS",
        description="DNA synthesis and assembly")
    GENE_SYNTHESIS = PermissibleValue(
        text="GENE_SYNTHESIS",
        description="Gene synthesis")
    PATHWAY_SYNTHESIS = PermissibleValue(
        text="PATHWAY_SYNTHESIS",
        description="Pathway and construct synthesis")
    PROTEIN_EXPRESSION = PermissibleValue(
        text="PROTEIN_EXPRESSION",
        description="Protein expression systems")
    METABOLOMICS_MS = PermissibleValue(
        text="METABOLOMICS_MS",
        description="Mass spectrometry for metabolomics")
    PROTEOMICS_MS = PermissibleValue(
        text="PROTEOMICS_MS",
        description="Mass spectrometry for proteomics")
    LIPIDOMICS_MS = PermissibleValue(
        text="LIPIDOMICS_MS",
        description="Mass spectrometry for lipidomics")
    NATIVE_MS = PermissibleValue(
        text="NATIVE_MS",
        description="Native mass spectrometry for intact complexes")
    MS_IMAGING = PermissibleValue(
        text="MS_IMAGING",
        description="Mass spectrometry imaging")
    GC_MS = PermissibleValue(
        text="GC_MS",
        description="Gas chromatography-mass spectrometry")
    LC_MS = PermissibleValue(
        text="LC_MS",
        description="Liquid chromatography-mass spectrometry")
    FTICR_MS = PermissibleValue(
        text="FTICR_MS",
        description="Fourier-transform ion cyclotron resonance MS")
    LIQUID_STATE_NMR = PermissibleValue(
        text="LIQUID_STATE_NMR",
        description="Liquid-state NMR spectroscopy")
    SOLID_STATE_NMR = PermissibleValue(
        text="SOLID_STATE_NMR",
        description="Solid-state NMR spectroscopy")
    METABOLOMICS_NMR = PermissibleValue(
        text="METABOLOMICS_NMR",
        description="NMR for metabolomics")
    CRYO_EM = PermissibleValue(
        text="CRYO_EM",
        description="Cryogenic electron microscopy")
    CRYO_ET = PermissibleValue(
        text="CRYO_ET",
        description="Cryogenic electron tomography")
    CRYO_FIB_SEM = PermissibleValue(
        text="CRYO_FIB_SEM",
        description="Cryogenic focused ion beam-SEM")
    LIGHT_MICROSCOPY = PermissibleValue(
        text="LIGHT_MICROSCOPY",
        description="Light and fluorescence microscopy")
    SUPER_RESOLUTION_MICROSCOPY = PermissibleValue(
        text="SUPER_RESOLUTION_MICROSCOPY",
        description="Super-resolution microscopy")
    CHEMICAL_IMAGING = PermissibleValue(
        text="CHEMICAL_IMAGING",
        description="Chemical imaging methods")
    NANOSIMS_IMAGING = PermissibleValue(
        text="NANOSIMS_IMAGING",
        description="NanoSIMS imaging")
    SYNCHROTRON_IMAGING = PermissibleValue(
        text="SYNCHROTRON_IMAGING",
        description="Synchrotron-based imaging")
    MICROBIAL_PHENOTYPING = PermissibleValue(
        text="MICROBIAL_PHENOTYPING",
        description="Microbial phenotyping platforms")
    ANAEROBIC_PHENOTYPING = PermissibleValue(
        text="ANAEROBIC_PHENOTYPING",
        description="Anaerobic microbial phenotyping (AMP2)")
    HIGH_THROUGHPUT_PHENOTYPING = PermissibleValue(
        text="HIGH_THROUGHPUT_PHENOTYPING",
        description="High-throughput phenotyping")
    GROWTH_PHENOTYPING = PermissibleValue(
        text="GROWTH_PHENOTYPING",
        description="Growth and fitness phenotyping")
    FLOW_CYTOMETRY = PermissibleValue(
        text="FLOW_CYTOMETRY",
        description="Flow cytometry analysis")
    GENOME_ANNOTATION = PermissibleValue(
        text="GENOME_ANNOTATION",
        description="Genome annotation services")
    METABOLIC_MODELING = PermissibleValue(
        text="METABOLIC_MODELING",
        description="Metabolic modeling and simulation")
    METAGENOME_ANALYSIS = PermissibleValue(
        text="METAGENOME_ANALYSIS",
        description="Metagenome analysis pipelines")
    AI_ML_ANALYSIS = PermissibleValue(
        text="AI_ML_ANALYSIS",
        description="AI/ML-based analysis")
    HIGH_PERFORMANCE_COMPUTING = PermissibleValue(
        text="HIGH_PERFORMANCE_COMPUTING",
        description="High-performance computing resources")

    _defn = EnumDefinition(
        name="CapabilityType",
        description="Types of scientific capabilities provided by user facilities",
    )

class CapabilityStatus(EnumDefinitionImpl):
    """
    Operational status of a capability
    """
    OPERATIONAL = PermissibleValue(
        text="OPERATIONAL",
        description="Fully operational and available to users")
    COMING_ONLINE = PermissibleValue(
        text="COMING_ONLINE",
        description="Being commissioned, coming online soon")
    PILOT = PermissibleValue(
        text="PILOT",
        description="In pilot phase with limited access")
    UNDER_DEVELOPMENT = PermissibleValue(
        text="UNDER_DEVELOPMENT",
        description="Under development, not yet available")
    DECOMMISSIONED = PermissibleValue(
        text="DECOMMISSIONED",
        description="No longer available")

    _defn = EnumDefinition(
        name="CapabilityStatus",
        description="Operational status of a capability",
    )

class InstrumentType(EnumDefinitionImpl):
    """
    Types of scientific instruments
    """
    ILLUMINA_SEQUENCER = PermissibleValue(
        text="ILLUMINA_SEQUENCER",
        description="Illumina short-read sequencer")
    PACBIO_SEQUENCER = PermissibleValue(
        text="PACBIO_SEQUENCER",
        description="PacBio long-read sequencer")
    OXFORD_NANOPORE = PermissibleValue(
        text="OXFORD_NANOPORE",
        description="Oxford Nanopore sequencer")
    ORBITRAP = PermissibleValue(
        text="ORBITRAP",
        description="Orbitrap mass spectrometer")
    TRIPLE_QUADRUPOLE = PermissibleValue(
        text="TRIPLE_QUADRUPOLE",
        description="Triple quadrupole mass spectrometer")
    FTICR = PermissibleValue(
        text="FTICR",
        description="Fourier-transform ion cyclotron resonance MS")
    TOF = PermissibleValue(
        text="TOF",
        description="Time-of-flight mass spectrometer")
    NMR_SPECTROMETER = PermissibleValue(
        text="NMR_SPECTROMETER",
        description="NMR spectrometer")
    CRYO_TEM = PermissibleValue(
        text="CRYO_TEM",
        description="Cryogenic transmission electron microscope")
    CRYO_SEM = PermissibleValue(
        text="CRYO_SEM",
        description="Cryogenic scanning electron microscope")
    FIB_SEM = PermissibleValue(
        text="FIB_SEM",
        description="Focused ion beam-SEM")
    FLOW_CYTOMETER = PermissibleValue(
        text="FLOW_CYTOMETER",
        description="Flow cytometer")
    LIQUID_HANDLER = PermissibleValue(
        text="LIQUID_HANDLER",
        description="Automated liquid handler")
    PLATE_READER = PermissibleValue(
        text="PLATE_READER",
        description="Microplate reader")
    HPLC = PermissibleValue(
        text="HPLC",
        description="High-performance liquid chromatography")
    GC = PermissibleValue(
        text="GC",
        description="Gas chromatograph")
    ANAEROBIC_CHAMBER = PermissibleValue(
        text="ANAEROBIC_CHAMBER",
        description="Anaerobic chamber or glove box")
    INCUBATOR = PermissibleValue(
        text="INCUBATOR",
        description="Microbial cultivation incubator")
    ELECTROPORATOR = PermissibleValue(
        text="ELECTROPORATOR",
        description="Electroporation device for cell transformation")

    _defn = EnumDefinition(
        name="InstrumentType",
        description="Types of scientific instruments",
    )

class AnalysisType(EnumDefinitionImpl):
    """
    Types of computational analyses
    """
    KBASE_NARRATIVE = PermissibleValue(
        text="KBASE_NARRATIVE",
        description="""KBase reproducible analysis workflow - a Jupyter-like notebook combining data, analysis steps, and documentation""")
    NMDC_WORKFLOW = PermissibleValue(
        text="NMDC_WORKFLOW",
        description="NMDC standardized bioinformatics workflow (e.g., metagenome annotation, MAG assembly)")
    CUSTOM_PIPELINE = PermissibleValue(
        text="CUSTOM_PIPELINE",
        description="Custom analysis pipeline not in KBase or NMDC")

    _defn = EnumDefinition(
        name="AnalysisType",
        description="Types of computational analyses",
    )

class KBaseCollection(EnumDefinitionImpl):
    """
    Available KBase genome collections (as of 2024). Collections are curated datasets searchable by sequence
    similarity, taxonomy (GTDB), and functional traits (microTrait).
    """
    GTDB = PermissibleValue(
        text="GTDB",
        description="""Genome Taxonomy Database reference collection - standardized microbial taxonomy based on genome phylogeny""")
    ENIGMA = PermissibleValue(
        text="ENIGMA",
        description="ENIGMA SFA subsurface microbiome genomes from Oak Ridge Reservation contaminated site studies")
    PMI = PermissibleValue(
        text="PMI",
        description="""Plant Microbe Interfaces SFA rhizosphere genomes - plant-host associated microbial genomes showing Populus rhizosphere diversity""")
    GROW = PermissibleValue(
        text="GROW",
        description="""Genome Resolved Open Watersheds (GROWdb) river microbiome MAGs from WHONDRS worldwide river sampling""")

    _defn = EnumDefinition(
        name="KBaseCollection",
        description="""Available KBase genome collections (as of 2024). Collections are curated datasets searchable by sequence similarity, taxonomy (GTDB), and functional traits (microTrait).""",
    )

class NMDCIngestPriority(EnumDefinitionImpl):
    """
    Priority level for considering a study/dataset for NMDC ingest. Used to help prioritize which external datasets
    should be targeted for ingestion into the National Microbiome Data Collaborative.
    """
    HIGH = PermissibleValue(
        text="HIGH",
        description="""High priority - dataset has rich microbiome data (metagenomes, amplicon sequences) with good metadata, ready for NMDC processing. Should be prioritized for ingest.""")
    MEDIUM = PermissibleValue(
        text="MEDIUM",
        description="""Medium priority - dataset has relevant microbiome data but may need metadata enrichment or format conversion before ingest.""")
    LOW = PermissibleValue(
        text="LOW",
        description="""Low priority - dataset has some microbiome relevance but is either small, has limited metadata, or is a marginal candidate.""")

    _defn = EnumDefinition(
        name="NMDCIngestPriority",
        description="""Priority level for considering a study/dataset for NMDC ingest. Used to help prioritize which external datasets should be targeted for ingestion into the National Microbiome Data Collaborative.""",
    )

class ResourceType(EnumDefinitionImpl):
    """
    Coarse type of a research resource, used as a discriminator on the ResearchResource class. Lets the catalog
    represent isolate collections, mutant libraries, phage banks, knowledgebases, and similar large-grain reagent or
    data resources without proliferating subclasses.
    """
    ISOLATE_COLLECTION = PermissibleValue(
        text="ISOLATE_COLLECTION",
        description="A collection of cultured microbial isolates.")
    MUTANT_LIBRARY = PermissibleValue(
        text="MUTANT_LIBRARY",
        description="""A pooled mutant library, e.g. a randomly-barcoded transposon (RB-TnSeq) insertion library or a CRISPRi library.""")
    PHAGE_BANK = PermissibleValue(
        text="PHAGE_BANK",
        description="A collection of bacteriophage isolates maintained as a reagent bank.")
    REFERENCE_GENOME_SET = PermissibleValue(
        text="REFERENCE_GENOME_SET",
        description="A curated set of reference genomes maintained by a program.")
    PLASMID_COLLECTION = PermissibleValue(
        text="PLASMID_COLLECTION",
        description="A collection of plasmids or other genetic constructs.")
    SYNTHETIC_COMMUNITY = PermissibleValue(
        text="SYNTHETIC_COMMUNITY",
        description="A defined synthetic microbial community maintained as a reagent.")
    ORGANISM_PANEL = PermissibleValue(
        text="ORGANISM_PANEL",
        description="""A defined set of organisms used as an experimental factor across one or more studies (e.g., the LBNL Fitness Browser organism set).""")
    CONDITION_PANEL = PermissibleValue(
        text="CONDITION_PANEL",
        description="""A defined set of growth conditions, media, stressors, or selective agents used as an experimental factor across one or more studies.""")
    KNOWLEDGEBASE = PermissibleValue(
        text="KNOWLEDGEBASE",
        description="""A versioned data resource or knowledgebase produced and maintained by the program (e.g., the LBNL Fitness Browser, the Phage Foundry Knowledge-Base).""")
    SOFTWARE = PermissibleValue(
        text="SOFTWARE",
        description="A software tool or pipeline produced as a research resource.")
    OTHER = PermissibleValue(
        text="OTHER",
        description="A research resource not covered by the above categories.")

    _defn = EnumDefinition(
        name="ResourceType",
        description="""Coarse type of a research resource, used as a discriminator on the ResearchResource class. Lets the catalog represent isolate collections, mutant libraries, phage banks, knowledgebases, and similar large-grain reagent or data resources without proliferating subclasses.""",
    )

class OrganismType(EnumDefinitionImpl):
    """
    Types of organisms in a microbial isolate collection. Used to characterize the taxonomic breadth of culture
    collections maintained by research programs.
    """
    BACTERIA = PermissibleValue(
        text="BACTERIA",
        description="Bacterial isolates",
        meaning=NCBITAXON["2"])
    ARCHAEA = PermissibleValue(
        text="ARCHAEA",
        description="Archaeal isolates",
        meaning=NCBITAXON["2157"])
    FUNGI = PermissibleValue(
        text="FUNGI",
        description="Fungal isolates including yeasts and filamentous fungi",
        meaning=NCBITAXON["4751"])
    PHAGE = PermissibleValue(
        text="PHAGE",
        description="Bacteriophages and archaeal viruses")
    OTHER_VIRUS = PermissibleValue(
        text="OTHER_VIRUS",
        description="Other viruses (not phage)")
    PROTIST = PermissibleValue(
        text="PROTIST",
        description="Protist/microeukaryote isolates")
    MICROALGAE = PermissibleValue(
        text="MICROALGAE",
        description="Microalgae isolates")

    _defn = EnumDefinition(
        name="OrganismType",
        description="""Types of organisms in a microbial isolate collection. Used to characterize the taxonomic breadth of culture collections maintained by research programs.""",
    )

class PhenotypeAssayType(EnumDefinitionImpl):
    """
    Types of phenotype assays performed by research programs. Used to catalog what phenotyping capabilities and data
    types each SFA/BRC generates.
    """
    GROWTH_CURVES = PermissibleValue(
        text="GROWTH_CURVES",
        description="Growth rate measurements in liquid culture")
    BIOLOG_PHENOTYPING = PermissibleValue(
        text="BIOLOG_PHENOTYPING",
        description="Biolog plate carbon/nitrogen source utilization profiling")
    ANAEROBIC_GROWTH = PermissibleValue(
        text="ANAEROBIC_GROWTH",
        description="Growth characterization under anaerobic conditions")
    STRESS_TOLERANCE = PermissibleValue(
        text="STRESS_TOLERANCE",
        description="Growth under stress conditions (pH, temperature, osmotic, metal)")
    ANTIBIOTIC_RESISTANCE = PermissibleValue(
        text="ANTIBIOTIC_RESISTANCE",
        description="Antibiotic susceptibility/resistance profiling")
    RBTSEQ_FITNESS = PermissibleValue(
        text="RBTSEQ_FITNESS",
        description="""Random barcode transposon sequencing (RB-TnSeq) for genome-wide fitness profiling across conditions""")
    TRANSPOSON_MUTAGENESIS = PermissibleValue(
        text="TRANSPOSON_MUTAGENESIS",
        description="Transposon insertion sequencing for gene essentiality/fitness")
    CRISPR_SCREENS = PermissibleValue(
        text="CRISPR_SCREENS",
        description="CRISPR-based genetic screens (CRISPRi, knockout libraries)")
    TNSEQ = PermissibleValue(
        text="TNSEQ",
        description="Transposon sequencing for fitness profiling")
    COCULTURE_INTERACTIONS = PermissibleValue(
        text="COCULTURE_INTERACTIONS",
        description="Pairwise or multi-species co-culture interaction assays")
    BACTERIAL_FUNGAL_INTERACTION_ASSAY = PermissibleValue(
        text="BACTERIAL_FUNGAL_INTERACTION_ASSAY",
        description="Bacterial-fungal co-culture or proximity interaction assays")
    FUNGAL_HIGHWAY_ASSAY = PermissibleValue(
        text="FUNGAL_HIGHWAY_ASSAY",
        description="Fungal highway column assays for bacterial dispersal via mycelia")
    ENDOHYPHAL_SCREENING = PermissibleValue(
        text="ENDOHYPHAL_SCREENING",
        description="Screening for endohyphal bacteria within fungal isolates")
    INTERNALIZATION_ASSAY = PermissibleValue(
        text="INTERNALIZATION_ASSAY",
        description="In vitro bacterial internalization into fungal cells")
    SIDEROPHORE_ASSAY = PermissibleValue(
        text="SIDEROPHORE_ASSAY",
        description="Siderophore production and iron chelation assays")
    PLANT_COLONIZATION = PermissibleValue(
        text="PLANT_COLONIZATION",
        description="Plant root or leaf colonization assays")
    PHAGE_HOST_RANGE = PermissibleValue(
        text="PHAGE_HOST_RANGE",
        description="Phage-host infection range and specificity testing")
    SYNTHETIC_COMMUNITY = PermissibleValue(
        text="SYNTHETIC_COMMUNITY",
        description="Defined synthetic community assembly and dynamics")
    COMPETITION_ASSAYS = PermissibleValue(
        text="COMPETITION_ASSAYS",
        description="Competitive fitness assays between strains")
    EXOMETABOLOMICS = PermissibleValue(
        text="EXOMETABOLOMICS",
        description="Extracellular metabolite profiling (spent media analysis)")
    ENZYME_ACTIVITY_ASSAY = PermissibleValue(
        text="ENZYME_ACTIVITY_ASSAY",
        description="Enzyme activity measurements")
    SUBSTRATE_UTILIZATION = PermissibleValue(
        text="SUBSTRATE_UTILIZATION",
        description="Carbon/nitrogen substrate utilization profiling")
    METABOLIC_FLUX = PermissibleValue(
        text="METABOLIC_FLUX",
        description="Metabolic flux analysis (13C labeling)")
    RESPIRATION = PermissibleValue(
        text="RESPIRATION",
        description="Respiration rate measurements (O2 consumption, CO2 production)")
    LIVE_CELL_IMAGING = PermissibleValue(
        text="LIVE_CELL_IMAGING",
        description="Time-lapse microscopy of live cells")
    FLOW_CYTOMETRY_PHENOTYPING = PermissibleValue(
        text="FLOW_CYTOMETRY_PHENOTYPING",
        description="Single-cell phenotyping via flow cytometry")
    NANOSIMS_ACTIVITY = PermissibleValue(
        text="NANOSIMS_ACTIVITY",
        description="NanoSIMS stable isotope incorporation for activity measurement")
    CELL_MORPHOLOGY = PermissibleValue(
        text="CELL_MORPHOLOGY",
        description="Cell morphology and size measurements")
    BIOFILM_ASSAYS = PermissibleValue(
        text="BIOFILM_ASSAYS",
        description="Biofilm formation and structure assays")
    SOIL_INCUBATION = PermissibleValue(
        text="SOIL_INCUBATION",
        description="Soil microcosm incubation experiments")
    QSIP_ACTIVITY = PermissibleValue(
        text="QSIP_ACTIVITY",
        description="Quantitative stable isotope probing for in-situ activity")
    ECOFAB_PHENOTYPING = PermissibleValue(
        text="ECOFAB_PHENOTYPING",
        description="EcoFAB fabricated ecosystem phenotyping")

    _defn = EnumDefinition(
        name="PhenotypeAssayType",
        description="""Types of phenotype assays performed by research programs. Used to catalog what phenotyping capabilities and data types each SFA/BRC generates.""",
    )

class InteractionType(EnumDefinitionImpl):
    """
    Types of bacterial-fungal interactions based on ecological outcome
    """
    MUTUALISM = PermissibleValue(
        text="MUTUALISM",
        description="""Win-win interaction where bacteria and fungi achieve functional complementarity through resource sharing (e.g., mycorrhizal symbiosis, lichen symbiosis)""")
    ANTAGONISM = PermissibleValue(
        text="ANTAGONISM",
        description="""Reciprocal inhibition including pathogen infection, antibiotic production, and biological control mechanisms""")
    COMPETITION = PermissibleValue(
        text="COMPETITION",
        description="""Resource and spatial rivalry maintaining community stability through niche differentiation (e.g., iron, biotin, adhesion sites)""")
    COMMENSALISM = PermissibleValue(
        text="COMMENSALISM",
        description="Interaction where one partner benefits while the other is unaffected")
    PARASITISM = PermissibleValue(
        text="PARASITISM",
        description="Interaction where one partner benefits at the expense of the other")
    ENDOSYMBIOSIS = PermissibleValue(
        text="ENDOSYMBIOSIS",
        description="""Obligate or facultative intracellular association where bacteria live within fungal cells (endohyphal bacteria)""")

    _defn = EnumDefinition(
        name="InteractionType",
        description="Types of bacterial-fungal interactions based on ecological outcome",
    )

class InteractionMode(EnumDefinitionImpl):
    """
    Physical or chemical mode of bacterial-fungal interaction
    """
    PHYSICAL_ATTACHMENT = PermissibleValue(
        text="PHYSICAL_ATTACHMENT",
        description="External attachment of bacteria to fungal surfaces (hyphae, spores)")
    ENDOHYPHAL = PermissibleValue(
        text="ENDOHYPHAL",
        description="Bacteria residing within fungal hyphae")
    BIOFILM_FORMATION = PermissibleValue(
        text="BIOFILM_FORMATION",
        description="Biofilm formation on fungal structures")
    FUNGAL_HIGHWAY = PermissibleValue(
        text="FUNGAL_HIGHWAY",
        description="Bacterial dispersal using fungal mycelia as transport networks")
    QUORUM_SENSING = PermissibleValue(
        text="QUORUM_SENSING",
        description="Chemical signaling via quorum sensing molecules")
    VOLATILE_METABOLITES = PermissibleValue(
        text="VOLATILE_METABOLITES",
        description="Interaction mediated by volatile organic compounds")
    SIDEROPHORE_MEDIATED = PermissibleValue(
        text="SIDEROPHORE_MEDIATED",
        description="Iron competition via siderophore production")
    ANTIBIOTIC_PRODUCTION = PermissibleValue(
        text="ANTIBIOTIC_PRODUCTION",
        description="Interaction mediated by antibiotic secretion")
    NUTRIENT_EXCHANGE = PermissibleValue(
        text="NUTRIENT_EXCHANGE",
        description="Metabolite exchange including carbon, nitrogen, vitamins")
    CHEMOTAXIS = PermissibleValue(
        text="CHEMOTAXIS",
        description="Directed movement in response to chemical gradients")

    _defn = EnumDefinition(
        name="InteractionMode",
        description="Physical or chemical mode of bacterial-fungal interaction",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.id, domain=None, range=URIRef)

slots.acronym = Slot(uri=SCHEMA.alternateName, name="acronym", curie=SCHEMA.curie('alternateName'),
                   model_uri=NMDC_SFAS_BRCS.acronym, domain=None, range=Optional[str])

slots.ror_id = Slot(uri=NMDC_SFAS_BRCS.ror_id, name="ror_id", curie=NMDC_SFAS_BRCS.curie('ror_id'),
                   model_uri=NMDC_SFAS_BRCS.ror_id, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^ror:\d{9}$'))

slots.orcid = Slot(uri=NMDC_SFAS_BRCS.orcid, name="orcid", curie=NMDC_SFAS_BRCS.curie('orcid'),
                   model_uri=NMDC_SFAS_BRCS.orcid, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^orcid:\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$'))

slots.doi = Slot(uri=NMDC_SFAS_BRCS.doi, name="doi", curie=NMDC_SFAS_BRCS.curie('doi'),
                   model_uri=NMDC_SFAS_BRCS.doi, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.pmid = Slot(uri=NMDC_SFAS_BRCS.pmid, name="pmid", curie=NMDC_SFAS_BRCS.curie('pmid'),
                   model_uri=NMDC_SFAS_BRCS.pmid, domain=None, range=Optional[str])

slots.osti_id = Slot(uri=NMDC_SFAS_BRCS.osti_id, name="osti_id", curie=NMDC_SFAS_BRCS.curie('osti_id'),
                   model_uri=NMDC_SFAS_BRCS.osti_id, domain=None, range=Optional[str])

slots.nmdc_study_id = Slot(uri=NMDC_SFAS_BRCS.nmdc_study_id, name="nmdc_study_id", curie=NMDC_SFAS_BRCS.curie('nmdc_study_id'),
                   model_uri=NMDC_SFAS_BRCS.nmdc_study_id, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^nmdc:sty-[a-z0-9-]+$'))

slots.nmdc_umbrella_study = Slot(uri=NMDC_SFAS_BRCS.nmdc_umbrella_study, name="nmdc_umbrella_study", curie=NMDC_SFAS_BRCS.curie('nmdc_umbrella_study'),
                   model_uri=NMDC_SFAS_BRCS.nmdc_umbrella_study, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^nmdc:sty-[a-z0-9-]+$'))

slots.studies = Slot(uri=NMDC_SFAS_BRCS.studies, name="studies", curie=NMDC_SFAS_BRCS.curie('studies'),
                   model_uri=NMDC_SFAS_BRCS.studies, domain=None, range=Optional[Union[Union[dict, NMDCStudyReference], list[Union[dict, NMDCStudyReference]]]])

slots.analyses = Slot(uri=NMDC_SFAS_BRCS.analyses, name="analyses", curie=NMDC_SFAS_BRCS.curie('analyses'),
                   model_uri=NMDC_SFAS_BRCS.analyses, domain=None, range=Optional[Union[dict[Union[str, KBaseNarrativeId], Union[dict, KBaseNarrative]], list[Union[dict, KBaseNarrative]]]])

slots.kbase_genome_collection = Slot(uri=NMDC_SFAS_BRCS.kbase_genome_collection, name="kbase_genome_collection", curie=NMDC_SFAS_BRCS.curie('kbase_genome_collection'),
                   model_uri=NMDC_SFAS_BRCS.kbase_genome_collection, domain=None, range=Optional[Union[str, "KBaseCollection"]])

slots.jgi_project_id = Slot(uri=NMDC_SFAS_BRCS.jgi_project_id, name="jgi_project_id", curie=NMDC_SFAS_BRCS.curie('jgi_project_id'),
                   model_uri=NMDC_SFAS_BRCS.jgi_project_id, domain=None, range=Optional[str])

slots.ameriflux_site_id = Slot(uri=NMDC_SFAS_BRCS.ameriflux_site_id, name="ameriflux_site_id", curie=NMDC_SFAS_BRCS.curie('ameriflux_site_id'),
                   model_uri=NMDC_SFAS_BRCS.ameriflux_site_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[A-Z]{2}-[A-Za-z0-9]+$'))

slots.lter_dataset_id = Slot(uri=NMDC_SFAS_BRCS.lter_dataset_id, name="lter_dataset_id", curie=NMDC_SFAS_BRCS.curie('lter_dataset_id'),
                   model_uri=NMDC_SFAS_BRCS.lter_dataset_id, domain=None, range=Optional[str])

slots.pride_id = Slot(uri=NMDC_SFAS_BRCS.pride_id, name="pride_id", curie=NMDC_SFAS_BRCS.curie('pride_id'),
                   model_uri=NMDC_SFAS_BRCS.pride_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^PXD\d+$'))

slots.massive_id = Slot(uri=NMDC_SFAS_BRCS.massive_id, name="massive_id", curie=NMDC_SFAS_BRCS.curie('massive_id'),
                   model_uri=NMDC_SFAS_BRCS.massive_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^MSV\d+$'))

slots.primary_reference = Slot(uri=NMDC_SFAS_BRCS.primary_reference, name="primary_reference", curie=NMDC_SFAS_BRCS.curie('primary_reference'),
                   model_uri=NMDC_SFAS_BRCS.primary_reference, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.additional_references = Slot(uri=NMDC_SFAS_BRCS.additional_references, name="additional_references", curie=NMDC_SFAS_BRCS.curie('additional_references'),
                   model_uri=NMDC_SFAS_BRCS.additional_references, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=NMDC_SFAS_BRCS.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=NMDC_SFAS_BRCS.description, domain=None, range=Optional[str])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=NMDC_SFAS_BRCS.title, domain=None, range=Optional[str])

slots.program_type = Slot(uri=NMDC_SFAS_BRCS.program_type, name="program_type", curie=NMDC_SFAS_BRCS.curie('program_type'),
                   model_uri=NMDC_SFAS_BRCS.program_type, domain=None, range=Optional[Union[str, "ProgramType"]])

slots.sfa_type = Slot(uri=NMDC_SFAS_BRCS.sfa_type, name="sfa_type", curie=NMDC_SFAS_BRCS.curie('sfa_type'),
                   model_uri=NMDC_SFAS_BRCS.sfa_type, domain=None, range=Optional[Union[str, "SFAType"]])

slots.initiative_name = Slot(uri=NMDC_SFAS_BRCS.initiative_name, name="initiative_name", curie=NMDC_SFAS_BRCS.curie('initiative_name'),
                   model_uri=NMDC_SFAS_BRCS.initiative_name, domain=None, range=Optional[str])

slots.funding_period = Slot(uri=NMDC_SFAS_BRCS.funding_period, name="funding_period", curie=NMDC_SFAS_BRCS.curie('funding_period'),
                   model_uri=NMDC_SFAS_BRCS.funding_period, domain=None, range=Optional[str])

slots.participating_offices = Slot(uri=NMDC_SFAS_BRCS.participating_offices, name="participating_offices", curie=NMDC_SFAS_BRCS.curie('participating_offices'),
                   model_uri=NMDC_SFAS_BRCS.participating_offices, domain=None, range=Optional[Union[str, list[str]]])

slots.institution_type = Slot(uri=NMDC_SFAS_BRCS.institution_type, name="institution_type", curie=NMDC_SFAS_BRCS.curie('institution_type'),
                   model_uri=NMDC_SFAS_BRCS.institution_type, domain=None, range=Optional[Union[str, "InstitutionType"]])

slots.lead_institution = Slot(uri=NMDC_SFAS_BRCS.lead_institution, name="lead_institution", curie=NMDC_SFAS_BRCS.curie('lead_institution'),
                   model_uri=NMDC_SFAS_BRCS.lead_institution, domain=None, range=Optional[str])

slots.lead_institutions = Slot(uri=NMDC_SFAS_BRCS.lead_institutions, name="lead_institutions", curie=NMDC_SFAS_BRCS.curie('lead_institutions'),
                   model_uri=NMDC_SFAS_BRCS.lead_institutions, domain=None, range=Optional[Union[str, list[str]]])

slots.partner_institutions = Slot(uri=NMDC_SFAS_BRCS.partner_institutions, name="partner_institutions", curie=NMDC_SFAS_BRCS.curie('partner_institutions'),
                   model_uri=NMDC_SFAS_BRCS.partner_institutions, domain=None, range=Optional[Union[str, list[str]]])

slots.principal_investigators = Slot(uri=NMDC_SFAS_BRCS.principal_investigators, name="principal_investigators", curie=NMDC_SFAS_BRCS.curie('principal_investigators'),
                   model_uri=NMDC_SFAS_BRCS.principal_investigators, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.co_investigators = Slot(uri=NMDC_SFAS_BRCS.co_investigators, name="co_investigators", curie=NMDC_SFAS_BRCS.curie('co_investigators'),
                   model_uri=NMDC_SFAS_BRCS.co_investigators, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.collaborators = Slot(uri=NMDC_SFAS_BRCS.collaborators, name="collaborators", curie=NMDC_SFAS_BRCS.curie('collaborators'),
                   model_uri=NMDC_SFAS_BRCS.collaborators, domain=None, range=Optional[str])

slots.isolate_collections = Slot(uri=NMDC_SFAS_BRCS.isolate_collections, name="isolate_collections", curie=NMDC_SFAS_BRCS.curie('isolate_collections'),
                   model_uri=NMDC_SFAS_BRCS.isolate_collections, domain=None, range=Optional[Union[Union[dict, IsolateCollection], list[Union[dict, IsolateCollection]]]])

slots.research_resources = Slot(uri=NMDC_SFAS_BRCS.research_resources, name="research_resources", curie=NMDC_SFAS_BRCS.curie('research_resources'),
                   model_uri=NMDC_SFAS_BRCS.research_resources, domain=None, range=Optional[Union[Union[dict, ResearchResource], list[Union[dict, ResearchResource]]]])

slots.phenotype_assays = Slot(uri=NMDC_SFAS_BRCS.phenotype_assays, name="phenotype_assays", curie=NMDC_SFAS_BRCS.curie('phenotype_assays'),
                   model_uri=NMDC_SFAS_BRCS.phenotype_assays, domain=None, range=Optional[Union[Union[str, "PhenotypeAssayType"], list[Union[str, "PhenotypeAssayType"]]]])

slots.role = Slot(uri=NMDC_SFAS_BRCS.role, name="role", curie=NMDC_SFAS_BRCS.curie('role'),
                   model_uri=NMDC_SFAS_BRCS.role, domain=None, range=Optional[str])

slots.affiliation = Slot(uri=NMDC_SFAS_BRCS.affiliation, name="affiliation", curie=NMDC_SFAS_BRCS.curie('affiliation'),
                   model_uri=NMDC_SFAS_BRCS.affiliation, domain=None, range=Optional[str])

slots.email = Slot(uri=SCHEMA.email, name="email", curie=SCHEMA.curie('email'),
                   model_uri=NMDC_SFAS_BRCS.email, domain=None, range=Optional[str])

slots.expertise = Slot(uri=NMDC_SFAS_BRCS.expertise, name="expertise", curie=NMDC_SFAS_BRCS.curie('expertise'),
                   model_uri=NMDC_SFAS_BRCS.expertise, domain=None, range=Optional[str])

slots.location = Slot(uri=NMDC_SFAS_BRCS.location, name="location", curie=NMDC_SFAS_BRCS.curie('location'),
                   model_uri=NMDC_SFAS_BRCS.location, domain=None, range=Optional[Union[dict, Location]])

slots.websites = Slot(uri=NMDC_SFAS_BRCS.websites, name="websites", curie=NMDC_SFAS_BRCS.curie('websites'),
                   model_uri=NMDC_SFAS_BRCS.websites, domain=None, range=Optional[Union[dict, WebResources]])

slots.url = Slot(uri=SCHEMA.url, name="url", curie=SCHEMA.curie('url'),
                   model_uri=NMDC_SFAS_BRCS.url, domain=None, range=Optional[Union[str, URI]])

slots.repository = Slot(uri=NMDC_SFAS_BRCS.repository, name="repository", curie=NMDC_SFAS_BRCS.curie('repository'),
                   model_uri=NMDC_SFAS_BRCS.repository, domain=None, range=Optional[str])

slots.funding = Slot(uri=NMDC_SFAS_BRCS.funding, name="funding", curie=NMDC_SFAS_BRCS.curie('funding'),
                   model_uri=NMDC_SFAS_BRCS.funding, domain=None, range=Optional[Union[dict, FundingInfo]])

slots.scientific_questions = Slot(uri=NMDC_SFAS_BRCS.scientific_questions, name="scientific_questions", curie=NMDC_SFAS_BRCS.curie('scientific_questions'),
                   model_uri=NMDC_SFAS_BRCS.scientific_questions, domain=None, range=Optional[Union[str, list[str]]])

slots.keywords = Slot(uri=SCHEMA.keywords, name="keywords", curie=SCHEMA.curie('keywords'),
                   model_uri=NMDC_SFAS_BRCS.keywords, domain=None, range=Optional[Union[Union[str, "Keyword"], list[Union[str, "Keyword"]]]])

slots.data_types = Slot(uri=NMDC_SFAS_BRCS.data_types, name="data_types", curie=NMDC_SFAS_BRCS.curie('data_types'),
                   model_uri=NMDC_SFAS_BRCS.data_types, domain=None, range=Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]])

slots.data_collection_modalities = Slot(uri=NMDC_SFAS_BRCS.data_collection_modalities, name="data_collection_modalities", curie=NMDC_SFAS_BRCS.curie('data_collection_modalities'),
                   model_uri=NMDC_SFAS_BRCS.data_collection_modalities, domain=None, range=Optional[Union[Union[str, "DataCollectionModality"], list[Union[str, "DataCollectionModality"]]]])

slots.interaction_types = Slot(uri=NMDC_SFAS_BRCS.interaction_types, name="interaction_types", curie=NMDC_SFAS_BRCS.curie('interaction_types'),
                   model_uri=NMDC_SFAS_BRCS.interaction_types, domain=None, range=Optional[Union[Union[str, "InteractionType"], list[Union[str, "InteractionType"]]]])

slots.interaction_modes = Slot(uri=NMDC_SFAS_BRCS.interaction_modes, name="interaction_modes", curie=NMDC_SFAS_BRCS.curie('interaction_modes'),
                   model_uri=NMDC_SFAS_BRCS.interaction_modes, domain=None, range=Optional[Union[Union[str, "InteractionMode"], list[Union[str, "InteractionMode"]]]])

slots.services = Slot(uri=NMDC_SFAS_BRCS.services, name="services", curie=NMDC_SFAS_BRCS.curie('services'),
                   model_uri=NMDC_SFAS_BRCS.services, domain=None, range=Optional[Union[str, list[str]]])

slots.capabilities = Slot(uri=NMDC_SFAS_BRCS.capabilities, name="capabilities", curie=NMDC_SFAS_BRCS.curie('capabilities'),
                   model_uri=NMDC_SFAS_BRCS.capabilities, domain=None, range=Optional[Union[Union[dict, Capability], list[Union[dict, Capability]]]])

slots.supported_data_types = Slot(uri=NMDC_SFAS_BRCS.supported_data_types, name="supported_data_types", curie=NMDC_SFAS_BRCS.curie('supported_data_types'),
                   model_uri=NMDC_SFAS_BRCS.supported_data_types, domain=None, range=Optional[Union[str, list[str]]])

slots.datasets = Slot(uri=NMDC_SFAS_BRCS.datasets, name="datasets", curie=NMDC_SFAS_BRCS.curie('datasets'),
                   model_uri=NMDC_SFAS_BRCS.datasets, domain=None, range=Optional[Union[Union[dict, Dataset], list[Union[dict, Dataset]]]])

slots.field_site_ids = Slot(uri=NMDC_SFAS_BRCS.field_site_ids, name="field_site_ids", curie=NMDC_SFAS_BRCS.curie('field_site_ids'),
                   model_uri=NMDC_SFAS_BRCS.field_site_ids, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.study_design = Slot(uri=NMDC_SFAS_BRCS.study_design, name="study_design", curie=NMDC_SFAS_BRCS.curie('study_design'),
                   model_uri=NMDC_SFAS_BRCS.study_design, domain=None, range=Optional[Union[dict, StudyDesign]])

slots.variables = Slot(uri=NMDC_SFAS_BRCS.variables, name="variables", curie=NMDC_SFAS_BRCS.curie('variables'),
                   model_uri=NMDC_SFAS_BRCS.variables, domain=None, range=Optional[Union[Union[dict, Variable], list[Union[dict, Variable]]]])

slots.key_publications = Slot(uri=NMDC_SFAS_BRCS.key_publications, name="key_publications", curie=NMDC_SFAS_BRCS.curie('key_publications'),
                   model_uri=NMDC_SFAS_BRCS.key_publications, domain=None, range=Optional[Union[dict[Union[str, ReferenceId], Union[dict, Reference]], list[Union[dict, Reference]]]])

slots.outputs = Slot(uri=NMDC_SFAS_BRCS.outputs, name="outputs", curie=NMDC_SFAS_BRCS.curie('outputs'),
                   model_uri=NMDC_SFAS_BRCS.outputs, domain=None, range=Optional[Union[dict, ProgramOutputs]])

slots.technologies_developed = Slot(uri=NMDC_SFAS_BRCS.technologies_developed, name="technologies_developed", curie=NMDC_SFAS_BRCS.curie('technologies_developed'),
                   model_uri=NMDC_SFAS_BRCS.technologies_developed, domain=None, range=Optional[Union[Union[dict, Technology], list[Union[dict, Technology]]]])

slots.flagship_genomes = Slot(uri=NMDC_SFAS_BRCS.flagship_genomes, name="flagship_genomes", curie=NMDC_SFAS_BRCS.curie('flagship_genomes'),
                   model_uri=NMDC_SFAS_BRCS.flagship_genomes, domain=None, range=Optional[Union[Union[dict, FlagshipGenome], list[Union[dict, FlagshipGenome]]]])

slots.reference_data = Slot(uri=NMDC_SFAS_BRCS.reference_data, name="reference_data", curie=NMDC_SFAS_BRCS.curie('reference_data'),
                   model_uri=NMDC_SFAS_BRCS.reference_data, domain=None, range=Optional[Union[dict, ReferenceData]])

slots.findings = Slot(uri=NMDC_SFAS_BRCS.findings, name="findings", curie=NMDC_SFAS_BRCS.curie('findings'),
                   model_uri=NMDC_SFAS_BRCS.findings, domain=None, range=Optional[Union[Union[dict, Finding], list[Union[dict, Finding]]]])

slots.statement = Slot(uri=NMDC_SFAS_BRCS.statement, name="statement", curie=NMDC_SFAS_BRCS.curie('statement'),
                   model_uri=NMDC_SFAS_BRCS.statement, domain=None, range=str)

slots.supporting_text = Slot(uri=NMDC_SFAS_BRCS.supporting_text, name="supporting_text", curie=NMDC_SFAS_BRCS.curie('supporting_text'),
                   model_uri=NMDC_SFAS_BRCS.supporting_text, domain=None, range=Optional[str])

slots.year = Slot(uri=NMDC_SFAS_BRCS.year, name="year", curie=NMDC_SFAS_BRCS.curie('year'),
                   model_uri=NMDC_SFAS_BRCS.year, domain=None, range=Optional[int])

slots.data_type = Slot(uri=NMDC_SFAS_BRCS.data_type, name="data_type", curie=NMDC_SFAS_BRCS.curie('data_type'),
                   model_uri=NMDC_SFAS_BRCS.data_type, domain=None, range=Optional[str])

slots.size = Slot(uri=NMDC_SFAS_BRCS.size, name="size", curie=NMDC_SFAS_BRCS.curie('size'),
                   model_uri=NMDC_SFAS_BRCS.size, domain=None, range=Optional[str])

slots.version = Slot(uri=NMDC_SFAS_BRCS.version, name="version", curie=NMDC_SFAS_BRCS.curie('version'),
                   model_uri=NMDC_SFAS_BRCS.version, domain=None, range=Optional[str])

slots.years = Slot(uri=NMDC_SFAS_BRCS.years, name="years", curie=NMDC_SFAS_BRCS.curie('years'),
                   model_uri=NMDC_SFAS_BRCS.years, domain=None, range=Optional[str])

slots.reference = Slot(uri=NMDC_SFAS_BRCS.reference, name="reference", curie=NMDC_SFAS_BRCS.curie('reference'),
                   model_uri=NMDC_SFAS_BRCS.reference, domain=None, range=Optional[str])

slots.count = Slot(uri=NMDC_SFAS_BRCS.count, name="count", curie=NMDC_SFAS_BRCS.curie('count'),
                   model_uri=NMDC_SFAS_BRCS.count, domain=None, range=Optional[str])

slots.doi_examples = Slot(uri=NMDC_SFAS_BRCS.doi_examples, name="doi_examples", curie=NMDC_SFAS_BRCS.curie('doi_examples'),
                   model_uri=NMDC_SFAS_BRCS.doi_examples, domain=None, range=Optional[Union[str, list[str]]])

slots.established = Slot(uri=NMDC_SFAS_BRCS.established, name="established", curie=NMDC_SFAS_BRCS.curie('established'),
                   model_uri=NMDC_SFAS_BRCS.established, domain=None, range=Optional[int])

slots.start_date = Slot(uri=NMDC_SFAS_BRCS.start_date, name="start_date", curie=NMDC_SFAS_BRCS.curie('start_date'),
                   model_uri=NMDC_SFAS_BRCS.start_date, domain=None, range=Optional[str])

slots.end_date = Slot(uri=NMDC_SFAS_BRCS.end_date, name="end_date", curie=NMDC_SFAS_BRCS.curie('end_date'),
                   model_uri=NMDC_SFAS_BRCS.end_date, domain=None, range=Optional[str])

slots.predecessor = Slot(uri=NMDC_SFAS_BRCS.predecessor, name="predecessor", curie=NMDC_SFAS_BRCS.curie('predecessor'),
                   model_uri=NMDC_SFAS_BRCS.predecessor, domain=None, range=Optional[str])

slots.researchProgramCollection__bioenergy_research_centers = Slot(uri=NMDC_SFAS_BRCS.bioenergy_research_centers, name="researchProgramCollection__bioenergy_research_centers", curie=NMDC_SFAS_BRCS.curie('bioenergy_research_centers'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__bioenergy_research_centers, domain=None, range=Optional[Union[dict[Union[str, BioenergyResearchCenterId], Union[dict, BioenergyResearchCenter]], list[Union[dict, BioenergyResearchCenter]]]])

slots.researchProgramCollection__genomic_science_sfas = Slot(uri=NMDC_SFAS_BRCS.genomic_science_sfas, name="researchProgramCollection__genomic_science_sfas", curie=NMDC_SFAS_BRCS.curie('genomic_science_sfas'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__genomic_science_sfas, domain=None, range=Optional[Union[dict[Union[str, ScientificFocusAreaId], Union[dict, ScientificFocusArea]], list[Union[dict, ScientificFocusArea]]]])

slots.researchProgramCollection__environmental_system_science_sfas = Slot(uri=NMDC_SFAS_BRCS.environmental_system_science_sfas, name="researchProgramCollection__environmental_system_science_sfas", curie=NMDC_SFAS_BRCS.curie('environmental_system_science_sfas'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__environmental_system_science_sfas, domain=None, range=Optional[Union[dict[Union[str, ScientificFocusAreaId], Union[dict, ScientificFocusArea]], list[Union[dict, ScientificFocusArea]]]])

slots.researchProgramCollection__user_facilities = Slot(uri=NMDC_SFAS_BRCS.user_facilities, name="researchProgramCollection__user_facilities", curie=NMDC_SFAS_BRCS.curie('user_facilities'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__user_facilities, domain=None, range=Optional[Union[dict[Union[str, UserFacilityId], Union[dict, UserFacility]], list[Union[dict, UserFacility]]]])

slots.researchProgramCollection__other_programs = Slot(uri=NMDC_SFAS_BRCS.other_programs, name="researchProgramCollection__other_programs", curie=NMDC_SFAS_BRCS.curie('other_programs'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__other_programs, domain=None, range=Optional[Union[dict[Union[str, OtherProgramId], Union[dict, OtherProgram]], list[Union[dict, OtherProgram]]]])

slots.researchProgramCollection__ai_projects = Slot(uri=NMDC_SFAS_BRCS.ai_projects, name="researchProgramCollection__ai_projects", curie=NMDC_SFAS_BRCS.curie('ai_projects'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__ai_projects, domain=None, range=Optional[Union[dict[Union[str, ArtificialIntelligenceProjectId], Union[dict, ArtificialIntelligenceProject]], list[Union[dict, ArtificialIntelligenceProject]]]])

slots.researchProgramCollection__sites = Slot(uri=NMDC_SFAS_BRCS.sites, name="researchProgramCollection__sites", curie=NMDC_SFAS_BRCS.curie('sites'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__sites, domain=None, range=Optional[Union[dict[Union[str, FieldSiteId], Union[dict, FieldSite]], list[Union[dict, FieldSite]]]])

slots.researchProgramCollection__metadata = Slot(uri=NMDC_SFAS_BRCS.metadata, name="researchProgramCollection__metadata", curie=NMDC_SFAS_BRCS.curie('metadata'),
                   model_uri=NMDC_SFAS_BRCS.researchProgramCollection__metadata, domain=None, range=Optional[Union[dict, CollectionMetadata]])

slots.collectionMetadata__compiled_date = Slot(uri=NMDC_SFAS_BRCS.compiled_date, name="collectionMetadata__compiled_date", curie=NMDC_SFAS_BRCS.curie('compiled_date'),
                   model_uri=NMDC_SFAS_BRCS.collectionMetadata__compiled_date, domain=None, range=Optional[str])

slots.collectionMetadata__sources = Slot(uri=NMDC_SFAS_BRCS.sources, name="collectionMetadata__sources", curie=NMDC_SFAS_BRCS.curie('sources'),
                   model_uri=NMDC_SFAS_BRCS.collectionMetadata__sources, domain=None, range=Optional[Union[str, list[str]]])

slots.collectionMetadata__notes = Slot(uri=NMDC_SFAS_BRCS.notes, name="collectionMetadata__notes", curie=NMDC_SFAS_BRCS.curie('notes'),
                   model_uri=NMDC_SFAS_BRCS.collectionMetadata__notes, domain=None, range=Optional[str])

slots.fundingInfo__agency = Slot(uri=NMDC_SFAS_BRCS.agency, name="fundingInfo__agency", curie=NMDC_SFAS_BRCS.curie('agency'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__agency, domain=None, range=Optional[str])

slots.fundingInfo__program = Slot(uri=NMDC_SFAS_BRCS.program, name="fundingInfo__program", curie=NMDC_SFAS_BRCS.curie('program'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__program, domain=None, range=Optional[str])

slots.fundingInfo__division = Slot(uri=NMDC_SFAS_BRCS.division, name="fundingInfo__division", curie=NMDC_SFAS_BRCS.curie('division'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__division, domain=None, range=Optional[str])

slots.fundingInfo__subprogram = Slot(uri=NMDC_SFAS_BRCS.subprogram, name="fundingInfo__subprogram", curie=NMDC_SFAS_BRCS.curie('subprogram'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__subprogram, domain=None, range=Optional[str])

slots.fundingInfo__area = Slot(uri=NMDC_SFAS_BRCS.area, name="fundingInfo__area", curie=NMDC_SFAS_BRCS.curie('area'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__area, domain=None, range=Optional[str])

slots.fundingInfo__contract = Slot(uri=NMDC_SFAS_BRCS.contract, name="fundingInfo__contract", curie=NMDC_SFAS_BRCS.curie('contract'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__contract, domain=None, range=Optional[str])

slots.fundingInfo__grant = Slot(uri=NMDC_SFAS_BRCS.grant, name="fundingInfo__grant", curie=NMDC_SFAS_BRCS.curie('grant'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__grant, domain=None, range=Optional[str])

slots.fundingInfo__total_funding = Slot(uri=NMDC_SFAS_BRCS.total_funding, name="fundingInfo__total_funding", curie=NMDC_SFAS_BRCS.curie('total_funding'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__total_funding, domain=None, range=Optional[str])

slots.fundingInfo__amount = Slot(uri=NMDC_SFAS_BRCS.amount, name="fundingInfo__amount", curie=NMDC_SFAS_BRCS.curie('amount'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__amount, domain=None, range=Optional[str])

slots.fundingInfo__award_2017 = Slot(uri=NMDC_SFAS_BRCS.award_2017, name="fundingInfo__award_2017", curie=NMDC_SFAS_BRCS.curie('award_2017'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__award_2017, domain=None, range=Optional[str])

slots.fundingInfo__current_period = Slot(uri=NMDC_SFAS_BRCS.current_period, name="fundingInfo__current_period", curie=NMDC_SFAS_BRCS.curie('current_period'),
                   model_uri=NMDC_SFAS_BRCS.fundingInfo__current_period, domain=None, range=Optional[str])

slots.location__address = Slot(uri=NMDC_SFAS_BRCS.address, name="location__address", curie=NMDC_SFAS_BRCS.curie('address'),
                   model_uri=NMDC_SFAS_BRCS.location__address, domain=None, range=Optional[str])

slots.location__city = Slot(uri=NMDC_SFAS_BRCS.city, name="location__city", curie=NMDC_SFAS_BRCS.curie('city'),
                   model_uri=NMDC_SFAS_BRCS.location__city, domain=None, range=Optional[str])

slots.location__state = Slot(uri=NMDC_SFAS_BRCS.state, name="location__state", curie=NMDC_SFAS_BRCS.curie('state'),
                   model_uri=NMDC_SFAS_BRCS.location__state, domain=None, range=Optional[str])

slots.location__country = Slot(uri=NMDC_SFAS_BRCS.country, name="location__country", curie=NMDC_SFAS_BRCS.curie('country'),
                   model_uri=NMDC_SFAS_BRCS.location__country, domain=None, range=Optional[str])

slots.webResources__main = Slot(uri=NMDC_SFAS_BRCS.main, name="webResources__main", curie=NMDC_SFAS_BRCS.curie('main'),
                   model_uri=NMDC_SFAS_BRCS.webResources__main, domain=None, range=Optional[Union[str, URI]])

slots.webResources__doe_page = Slot(uri=NMDC_SFAS_BRCS.doe_page, name="webResources__doe_page", curie=NMDC_SFAS_BRCS.curie('doe_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__doe_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__award_list = Slot(uri=NMDC_SFAS_BRCS.award_list, name="webResources__award_list", curie=NMDC_SFAS_BRCS.curie('award_list'),
                   model_uri=NMDC_SFAS_BRCS.webResources__award_list, domain=None, range=Optional[Union[str, URI]])

slots.webResources__ornl_page = Slot(uri=NMDC_SFAS_BRCS.ornl_page, name="webResources__ornl_page", curie=NMDC_SFAS_BRCS.curie('ornl_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__ornl_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__llnl_page = Slot(uri=NMDC_SFAS_BRCS.llnl_page, name="webResources__llnl_page", curie=NMDC_SFAS_BRCS.curie('llnl_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__llnl_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__data_portal = Slot(uri=NMDC_SFAS_BRCS.data_portal, name="webResources__data_portal", curie=NMDC_SFAS_BRCS.curie('data_portal'),
                   model_uri=NMDC_SFAS_BRCS.webResources__data_portal, domain=None, range=Optional[Union[str, URI]])

slots.webResources__data_hub = Slot(uri=NMDC_SFAS_BRCS.data_hub, name="webResources__data_hub", curie=NMDC_SFAS_BRCS.curie('data_hub'),
                   model_uri=NMDC_SFAS_BRCS.webResources__data_hub, domain=None, range=Optional[Union[str, URI]])

slots.webResources__data_page = Slot(uri=NMDC_SFAS_BRCS.data_page, name="webResources__data_page", curie=NMDC_SFAS_BRCS.curie('data_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__data_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__atlas = Slot(uri=NMDC_SFAS_BRCS.atlas, name="webResources__atlas", curie=NMDC_SFAS_BRCS.curie('atlas'),
                   model_uri=NMDC_SFAS_BRCS.webResources__atlas, domain=None, range=Optional[Union[str, URI]])

slots.webResources__github = Slot(uri=NMDC_SFAS_BRCS.github, name="webResources__github", curie=NMDC_SFAS_BRCS.curie('github'),
                   model_uri=NMDC_SFAS_BRCS.webResources__github, domain=None, range=Optional[Union[str, URI]])

slots.webResources__kbase = Slot(uri=NMDC_SFAS_BRCS.kbase, name="webResources__kbase", curie=NMDC_SFAS_BRCS.curie('kbase'),
                   model_uri=NMDC_SFAS_BRCS.webResources__kbase, domain=None, range=Optional[Union[str, URI]])

slots.webResources__ess_dive = Slot(uri=NMDC_SFAS_BRCS.ess_dive, name="webResources__ess_dive", curie=NMDC_SFAS_BRCS.curie('ess_dive'),
                   model_uri=NMDC_SFAS_BRCS.webResources__ess_dive, domain=None, range=Optional[Union[str, URI]])

slots.webResources__ideas_watersheds = Slot(uri=NMDC_SFAS_BRCS.ideas_watersheds, name="webResources__ideas_watersheds", curie=NMDC_SFAS_BRCS.curie('ideas_watersheds'),
                   model_uri=NMDC_SFAS_BRCS.webResources__ideas_watersheds, domain=None, range=Optional[Union[str, URI]])

slots.webResources__czen = Slot(uri=NMDC_SFAS_BRCS.czen, name="webResources__czen", curie=NMDC_SFAS_BRCS.curie('czen'),
                   model_uri=NMDC_SFAS_BRCS.webResources__czen, domain=None, range=Optional[Union[str, URI]])

slots.webResources__publications = Slot(uri=NMDC_SFAS_BRCS.publications, name="webResources__publications", curie=NMDC_SFAS_BRCS.curie('publications'),
                   model_uri=NMDC_SFAS_BRCS.webResources__publications, domain=None, range=Optional[Union[str, URI]])

slots.webResources__highlights = Slot(uri=NMDC_SFAS_BRCS.highlights, name="webResources__highlights", curie=NMDC_SFAS_BRCS.curie('highlights'),
                   model_uri=NMDC_SFAS_BRCS.webResources__highlights, domain=None, range=Optional[Union[str, URI]])

slots.webResources__documentation = Slot(uri=NMDC_SFAS_BRCS.documentation, name="webResources__documentation", curie=NMDC_SFAS_BRCS.curie('documentation'),
                   model_uri=NMDC_SFAS_BRCS.webResources__documentation, domain=None, range=Optional[Union[str, URI]])

slots.webResources__bacterial_strains = Slot(uri=NMDC_SFAS_BRCS.bacterial_strains, name="webResources__bacterial_strains", curie=NMDC_SFAS_BRCS.curie('bacterial_strains'),
                   model_uri=NMDC_SFAS_BRCS.webResources__bacterial_strains, domain=None, range=Optional[Union[str, URI]])

slots.webResources__bfi_portal = Slot(uri=NMDC_SFAS_BRCS.bfi_portal, name="webResources__bfi_portal", curie=NMDC_SFAS_BRCS.curie('bfi_portal'),
                   model_uri=NMDC_SFAS_BRCS.webResources__bfi_portal, domain=None, range=Optional[Union[str, URI]])

slots.webResources__ssrl_page = Slot(uri=NMDC_SFAS_BRCS.ssrl_page, name="webResources__ssrl_page", curie=NMDC_SFAS_BRCS.curie('ssrl_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__ssrl_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__anl_page = Slot(uri=NMDC_SFAS_BRCS.anl_page, name="webResources__anl_page", curie=NMDC_SFAS_BRCS.curie('anl_page'),
                   model_uri=NMDC_SFAS_BRCS.webResources__anl_page, domain=None, range=Optional[Union[str, URI]])

slots.webResources__team = Slot(uri=NMDC_SFAS_BRCS.team, name="webResources__team", curie=NMDC_SFAS_BRCS.curie('team'),
                   model_uri=NMDC_SFAS_BRCS.webResources__team, domain=None, range=Optional[Union[str, URI]])

slots.webResources__phytozome = Slot(uri=NMDC_SFAS_BRCS.phytozome, name="webResources__phytozome", curie=NMDC_SFAS_BRCS.curie('phytozome'),
                   model_uri=NMDC_SFAS_BRCS.webResources__phytozome, domain=None, range=Optional[Union[str, URI]])

slots.dataset__primary_reference_info = Slot(uri=NMDC_SFAS_BRCS.primary_reference_info, name="dataset__primary_reference_info", curie=NMDC_SFAS_BRCS.curie('primary_reference_info'),
                   model_uri=NMDC_SFAS_BRCS.dataset__primary_reference_info, domain=None, range=Optional[Union[dict, PrimaryReferenceInfo]])

slots.variable__roles = Slot(uri=NMDC_SFAS_BRCS.roles, name="variable__roles", curie=NMDC_SFAS_BRCS.curie('roles'),
                   model_uri=NMDC_SFAS_BRCS.variable__roles, domain=None, range=Optional[Union[Union[str, "VariableRole"], list[Union[str, "VariableRole"]]]])

slots.variable__value_type = Slot(uri=NMDC_SFAS_BRCS.value_type, name="variable__value_type", curie=NMDC_SFAS_BRCS.curie('value_type'),
                   model_uri=NMDC_SFAS_BRCS.variable__value_type, domain=None, range=Optional[Union[str, "VariableValueType"]])

slots.variable__units = Slot(uri=NMDC_SFAS_BRCS.units, name="variable__units", curie=NMDC_SFAS_BRCS.curie('units'),
                   model_uri=NMDC_SFAS_BRCS.variable__units, domain=None, range=Optional[str])

slots.variable__unit_term = Slot(uri=NMDC_SFAS_BRCS.unit_term, name="variable__unit_term", curie=NMDC_SFAS_BRCS.curie('unit_term'),
                   model_uri=NMDC_SFAS_BRCS.variable__unit_term, domain=None, range=Optional[Union[dict, OntologyTerm]])

slots.variable__bervo_term = Slot(uri=NMDC_SFAS_BRCS.bervo_term, name="variable__bervo_term", curie=NMDC_SFAS_BRCS.curie('bervo_term'),
                   model_uri=NMDC_SFAS_BRCS.variable__bervo_term, domain=None, range=Optional[Union[dict, BERVOTerm]])

slots.variable__mixs_terms = Slot(uri=NMDC_SFAS_BRCS.mixs_terms, name="variable__mixs_terms", curie=NMDC_SFAS_BRCS.curie('mixs_terms'),
                   model_uri=NMDC_SFAS_BRCS.variable__mixs_terms, domain=None, range=Optional[Union[dict[Union[str, MIXSTermId], Union[dict, MIXSTerm]], list[Union[dict, MIXSTerm]]]])

slots.variable__ontology_mappings = Slot(uri=NMDC_SFAS_BRCS.ontology_mappings, name="variable__ontology_mappings", curie=NMDC_SFAS_BRCS.curie('ontology_mappings'),
                   model_uri=NMDC_SFAS_BRCS.variable__ontology_mappings, domain=None, range=Optional[Union[dict[Union[str, OntologyTermId], Union[dict, OntologyTerm]], list[Union[dict, OntologyTerm]]]])

slots.variable__measured_entity = Slot(uri=NMDC_SFAS_BRCS.measured_entity, name="variable__measured_entity", curie=NMDC_SFAS_BRCS.curie('measured_entity'),
                   model_uri=NMDC_SFAS_BRCS.variable__measured_entity, domain=None, range=Optional[str])

slots.variable__material_or_matrix = Slot(uri=NMDC_SFAS_BRCS.material_or_matrix, name="variable__material_or_matrix", curie=NMDC_SFAS_BRCS.curie('material_or_matrix'),
                   model_uri=NMDC_SFAS_BRCS.variable__material_or_matrix, domain=None, range=Optional[str])

slots.variable__method = Slot(uri=NMDC_SFAS_BRCS.method, name="variable__method", curie=NMDC_SFAS_BRCS.curie('method'),
                   model_uri=NMDC_SFAS_BRCS.variable__method, domain=None, range=Optional[str])

slots.variable__time_series = Slot(uri=NMDC_SFAS_BRCS.time_series, name="variable__time_series", curie=NMDC_SFAS_BRCS.curie('time_series'),
                   model_uri=NMDC_SFAS_BRCS.variable__time_series, domain=None, range=Optional[Union[bool, Bool]])

slots.variable__temporal_resolution = Slot(uri=NMDC_SFAS_BRCS.temporal_resolution, name="variable__temporal_resolution", curie=NMDC_SFAS_BRCS.curie('temporal_resolution'),
                   model_uri=NMDC_SFAS_BRCS.variable__temporal_resolution, domain=None, range=Optional[str])

slots.variable__spatial_resolution = Slot(uri=NMDC_SFAS_BRCS.spatial_resolution, name="variable__spatial_resolution", curie=NMDC_SFAS_BRCS.curie('spatial_resolution'),
                   model_uri=NMDC_SFAS_BRCS.variable__spatial_resolution, domain=None, range=Optional[str])

slots.variable__levels = Slot(uri=NMDC_SFAS_BRCS.levels, name="variable__levels", curie=NMDC_SFAS_BRCS.curie('levels'),
                   model_uri=NMDC_SFAS_BRCS.variable__levels, domain=None, range=Optional[Union[str, list[str]]])

slots.variable__source_field_names = Slot(uri=NMDC_SFAS_BRCS.source_field_names, name="variable__source_field_names", curie=NMDC_SFAS_BRCS.curie('source_field_names'),
                   model_uri=NMDC_SFAS_BRCS.variable__source_field_names, domain=None, range=Optional[Union[str, list[str]]])

slots.variable__notes = Slot(uri=NMDC_SFAS_BRCS.notes, name="variable__notes", curie=NMDC_SFAS_BRCS.curie('notes'),
                   model_uri=NMDC_SFAS_BRCS.variable__notes, domain=None, range=Optional[str])

slots.ontologyTerm__id = Slot(uri=NMDC_SFAS_BRCS.id, name="ontologyTerm__id", curie=NMDC_SFAS_BRCS.curie('id'),
                   model_uri=NMDC_SFAS_BRCS.ontologyTerm__id, domain=None, range=URIRef)

slots.ontologyTerm__label = Slot(uri=NMDC_SFAS_BRCS.label, name="ontologyTerm__label", curie=NMDC_SFAS_BRCS.curie('label'),
                   model_uri=NMDC_SFAS_BRCS.ontologyTerm__label, domain=None, range=str)

slots.ontologyTerm__mapping_relation = Slot(uri=NMDC_SFAS_BRCS.mapping_relation, name="ontologyTerm__mapping_relation", curie=NMDC_SFAS_BRCS.curie('mapping_relation'),
                   model_uri=NMDC_SFAS_BRCS.ontologyTerm__mapping_relation, domain=None, range=Optional[Union[str, "OntologyMappingRelation"]])

slots.ontologyTerm__mapping_note = Slot(uri=NMDC_SFAS_BRCS.mapping_note, name="ontologyTerm__mapping_note", curie=NMDC_SFAS_BRCS.curie('mapping_note'),
                   model_uri=NMDC_SFAS_BRCS.ontologyTerm__mapping_note, domain=None, range=Optional[str])

slots.finding__reference = Slot(uri=NMDC_SFAS_BRCS.reference, name="finding__reference", curie=NMDC_SFAS_BRCS.curie('reference'),
                   model_uri=NMDC_SFAS_BRCS.finding__reference, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.primaryReferenceInfo__reference = Slot(uri=NMDC_SFAS_BRCS.reference, name="primaryReferenceInfo__reference", curie=NMDC_SFAS_BRCS.curie('reference'),
                   model_uri=NMDC_SFAS_BRCS.primaryReferenceInfo__reference, domain=None, range=Union[dict, Reference])

slots.primaryReferenceInfo__relationship_note = Slot(uri=NMDC_SFAS_BRCS.relationship_note, name="primaryReferenceInfo__relationship_note", curie=NMDC_SFAS_BRCS.curie('relationship_note'),
                   model_uri=NMDC_SFAS_BRCS.primaryReferenceInfo__relationship_note, domain=None, range=Optional[str])

slots.programOutputs__publication_count = Slot(uri=NMDC_SFAS_BRCS.publication_count, name="programOutputs__publication_count", curie=NMDC_SFAS_BRCS.curie('publication_count'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__publication_count, domain=None, range=Optional[str])

slots.programOutputs__patent_applications = Slot(uri=NMDC_SFAS_BRCS.patent_applications, name="programOutputs__patent_applications", curie=NMDC_SFAS_BRCS.curie('patent_applications'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__patent_applications, domain=None, range=Optional[int])

slots.programOutputs__invention_disclosures = Slot(uri=NMDC_SFAS_BRCS.invention_disclosures, name="programOutputs__invention_disclosures", curie=NMDC_SFAS_BRCS.curie('invention_disclosures'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__invention_disclosures, domain=None, range=Optional[int])

slots.programOutputs__licenses_options = Slot(uri=NMDC_SFAS_BRCS.licenses_options, name="programOutputs__licenses_options", curie=NMDC_SFAS_BRCS.curie('licenses_options'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__licenses_options, domain=None, range=Optional[int])

slots.programOutputs__patents = Slot(uri=NMDC_SFAS_BRCS.patents, name="programOutputs__patents", curie=NMDC_SFAS_BRCS.curie('patents'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__patents, domain=None, range=Optional[int])

slots.programOutputs__startups = Slot(uri=NMDC_SFAS_BRCS.startups, name="programOutputs__startups", curie=NMDC_SFAS_BRCS.curie('startups'),
                   model_uri=NMDC_SFAS_BRCS.programOutputs__startups, domain=None, range=Optional[int])

slots.researchResource__resource_type = Slot(uri=NMDC_SFAS_BRCS.resource_type, name="researchResource__resource_type", curie=NMDC_SFAS_BRCS.curie('resource_type'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__resource_type, domain=None, range=Optional[Union[str, "ResourceType"]])

slots.researchResource__identifiers = Slot(uri=NMDC_SFAS_BRCS.identifiers, name="researchResource__identifiers", curie=NMDC_SFAS_BRCS.curie('identifiers'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__identifiers, domain=None, range=Optional[Union[Union[dict, ResourceIdentifier], list[Union[dict, ResourceIdentifier]]]])

slots.researchResource__provider = Slot(uri=NMDC_SFAS_BRCS.provider, name="researchResource__provider", curie=NMDC_SFAS_BRCS.curie('provider'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__provider, domain=None, range=Optional[str])

slots.researchResource__url = Slot(uri=NMDC_SFAS_BRCS.url, name="researchResource__url", curie=NMDC_SFAS_BRCS.curie('url'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__url, domain=None, range=Optional[Union[str, URI]])

slots.researchResource__count = Slot(uri=NMDC_SFAS_BRCS.count, name="researchResource__count", curie=NMDC_SFAS_BRCS.curie('count'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__count, domain=None, range=Optional[str])

slots.researchResource__members = Slot(uri=NMDC_SFAS_BRCS.members, name="researchResource__members", curie=NMDC_SFAS_BRCS.curie('members'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__members, domain=None, range=Optional[Union[str, list[str]]])

slots.researchResource__member_count = Slot(uri=NMDC_SFAS_BRCS.member_count, name="researchResource__member_count", curie=NMDC_SFAS_BRCS.curie('member_count'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__member_count, domain=None, range=Optional[int])

slots.researchResource__primary_reference_info = Slot(uri=NMDC_SFAS_BRCS.primary_reference_info, name="researchResource__primary_reference_info", curie=NMDC_SFAS_BRCS.curie('primary_reference_info'),
                   model_uri=NMDC_SFAS_BRCS.researchResource__primary_reference_info, domain=None, range=Optional[Union[dict, PrimaryReferenceInfo]])

slots.resourceIdentifier__registry = Slot(uri=NMDC_SFAS_BRCS.registry, name="resourceIdentifier__registry", curie=NMDC_SFAS_BRCS.curie('registry'),
                   model_uri=NMDC_SFAS_BRCS.resourceIdentifier__registry, domain=None, range=str)

slots.resourceIdentifier__accession = Slot(uri=NMDC_SFAS_BRCS.accession, name="resourceIdentifier__accession", curie=NMDC_SFAS_BRCS.curie('accession'),
                   model_uri=NMDC_SFAS_BRCS.resourceIdentifier__accession, domain=None, range=str)

slots.resourceIdentifier__url = Slot(uri=NMDC_SFAS_BRCS.url, name="resourceIdentifier__url", curie=NMDC_SFAS_BRCS.curie('url'),
                   model_uri=NMDC_SFAS_BRCS.resourceIdentifier__url, domain=None, range=Optional[Union[str, URI]])

slots.resourceIdentifier__citation = Slot(uri=NMDC_SFAS_BRCS.citation, name="resourceIdentifier__citation", curie=NMDC_SFAS_BRCS.curie('citation'),
                   model_uri=NMDC_SFAS_BRCS.resourceIdentifier__citation, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.isolateCollection__organism_types = Slot(uri=NMDC_SFAS_BRCS.organism_types, name="isolateCollection__organism_types", curie=NMDC_SFAS_BRCS.curie('organism_types'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__organism_types, domain=None, range=Optional[Union[Union[str, "OrganismType"], list[Union[str, "OrganismType"]]]])

slots.isolateCollection__isolate_count = Slot(uri=NMDC_SFAS_BRCS.isolate_count, name="isolateCollection__isolate_count", curie=NMDC_SFAS_BRCS.curie('isolate_count'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__isolate_count, domain=None, range=Optional[int])

slots.isolateCollection__genome_count = Slot(uri=NMDC_SFAS_BRCS.genome_count, name="isolateCollection__genome_count", curie=NMDC_SFAS_BRCS.curie('genome_count'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__genome_count, domain=None, range=Optional[int])

slots.isolateCollection__source_environments = Slot(uri=NMDC_SFAS_BRCS.source_environments, name="isolateCollection__source_environments", curie=NMDC_SFAS_BRCS.curie('source_environments'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__source_environments, domain=None, range=Optional[Union[str, list[str]]])

slots.isolateCollection__isolation_methods = Slot(uri=NMDC_SFAS_BRCS.isolation_methods, name="isolateCollection__isolation_methods", curie=NMDC_SFAS_BRCS.curie('isolation_methods'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__isolation_methods, domain=None, range=Optional[Union[str, list[str]]])

slots.isolateCollection__host_organisms = Slot(uri=NMDC_SFAS_BRCS.host_organisms, name="isolateCollection__host_organisms", curie=NMDC_SFAS_BRCS.curie('host_organisms'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__host_organisms, domain=None, range=Optional[Union[str, list[str]]])

slots.isolateCollection__culture_collection_url = Slot(uri=NMDC_SFAS_BRCS.culture_collection_url, name="isolateCollection__culture_collection_url", curie=NMDC_SFAS_BRCS.curie('culture_collection_url'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__culture_collection_url, domain=None, range=Optional[Union[str, URI]])

slots.isolateCollection__genome_catalog_url = Slot(uri=NMDC_SFAS_BRCS.genome_catalog_url, name="isolateCollection__genome_catalog_url", curie=NMDC_SFAS_BRCS.curie('genome_catalog_url'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__genome_catalog_url, domain=None, range=Optional[Union[str, URI]])

slots.isolateCollection__kbase_narrative_id = Slot(uri=NMDC_SFAS_BRCS.kbase_narrative_id, name="isolateCollection__kbase_narrative_id", curie=NMDC_SFAS_BRCS.curie('kbase_narrative_id'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__kbase_narrative_id, domain=None, range=Optional[str])

slots.isolateCollection__primary_reference = Slot(uri=NMDC_SFAS_BRCS.primary_reference, name="isolateCollection__primary_reference", curie=NMDC_SFAS_BRCS.curie('primary_reference'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__primary_reference, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.isolateCollection__primary_reference_info = Slot(uri=NMDC_SFAS_BRCS.primary_reference_info, name="isolateCollection__primary_reference_info", curie=NMDC_SFAS_BRCS.curie('primary_reference_info'),
                   model_uri=NMDC_SFAS_BRCS.isolateCollection__primary_reference_info, domain=None, range=Optional[Union[dict, PrimaryReferenceInfo]])

slots.fieldSite__location = Slot(uri=NMDC_SFAS_BRCS.location, name="fieldSite__location", curie=NMDC_SFAS_BRCS.curie('location'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__location, domain=None, range=Optional[str])

slots.fieldSite__site_type = Slot(uri=NMDC_SFAS_BRCS.site_type, name="fieldSite__site_type", curie=NMDC_SFAS_BRCS.curie('site_type'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__site_type, domain=None, range=Optional[str])

slots.fieldSite__pi = Slot(uri=NMDC_SFAS_BRCS.pi, name="fieldSite__pi", curie=NMDC_SFAS_BRCS.curie('pi'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__pi, domain=None, range=Optional[str])

slots.fieldSite__institution = Slot(uri=NMDC_SFAS_BRCS.institution, name="fieldSite__institution", curie=NMDC_SFAS_BRCS.curie('institution'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__institution, domain=None, range=Optional[str])

slots.fieldSite__relevance = Slot(uri=NMDC_SFAS_BRCS.relevance, name="fieldSite__relevance", curie=NMDC_SFAS_BRCS.curie('relevance'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__relevance, domain=None, range=Optional[Union[str, list[str]]])

slots.fieldSite__contaminants = Slot(uri=NMDC_SFAS_BRCS.contaminants, name="fieldSite__contaminants", curie=NMDC_SFAS_BRCS.curie('contaminants'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__contaminants, domain=None, range=Optional[Union[str, list[str]]])

slots.fieldSite__contamination_source = Slot(uri=NMDC_SFAS_BRCS.contamination_source, name="fieldSite__contamination_source", curie=NMDC_SFAS_BRCS.curie('contamination_source'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__contamination_source, domain=None, range=Optional[str])

slots.fieldSite__elevation_m = Slot(uri=NMDC_SFAS_BRCS.elevation_m, name="fieldSite__elevation_m", curie=NMDC_SFAS_BRCS.curie('elevation_m'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__elevation_m, domain=None, range=Optional[int])

slots.fieldSite__mean_annual_temp_c = Slot(uri=NMDC_SFAS_BRCS.mean_annual_temp_c, name="fieldSite__mean_annual_temp_c", curie=NMDC_SFAS_BRCS.curie('mean_annual_temp_c'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__mean_annual_temp_c, domain=None, range=Optional[float])

slots.fieldSite__mean_annual_precip_cm = Slot(uri=NMDC_SFAS_BRCS.mean_annual_precip_cm, name="fieldSite__mean_annual_precip_cm", curie=NMDC_SFAS_BRCS.curie('mean_annual_precip_cm'),
                   model_uri=NMDC_SFAS_BRCS.fieldSite__mean_annual_precip_cm, domain=None, range=Optional[float])

slots.webReference__url = Slot(uri=NMDC_SFAS_BRCS.url, name="webReference__url", curie=NMDC_SFAS_BRCS.curie('url'),
                   model_uri=NMDC_SFAS_BRCS.webReference__url, domain=None, range=Union[str, URI])

slots.webReference__title = Slot(uri=NMDC_SFAS_BRCS.title, name="webReference__title", curie=NMDC_SFAS_BRCS.curie('title'),
                   model_uri=NMDC_SFAS_BRCS.webReference__title, domain=None, range=str)

slots.webReference__summary = Slot(uri=NMDC_SFAS_BRCS.summary, name="webReference__summary", curie=NMDC_SFAS_BRCS.curie('summary'),
                   model_uri=NMDC_SFAS_BRCS.webReference__summary, domain=None, range=Optional[str])

slots.studyDesign__design_types = Slot(uri=NMDC_SFAS_BRCS.design_types, name="studyDesign__design_types", curie=NMDC_SFAS_BRCS.curie('design_types'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__design_types, domain=None, range=Optional[Union[dict[Union[str, OntologyTermId], Union[dict, OntologyTerm]], list[Union[dict, OntologyTerm]]]])

slots.studyDesign__factor_panels = Slot(uri=NMDC_SFAS_BRCS.factor_panels, name="studyDesign__factor_panels", curie=NMDC_SFAS_BRCS.curie('factor_panels'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__factor_panels, domain=None, range=Optional[Union[str, list[str]]])

slots.studyDesign__experimental_units = Slot(uri=NMDC_SFAS_BRCS.experimental_units, name="studyDesign__experimental_units", curie=NMDC_SFAS_BRCS.curie('experimental_units'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__experimental_units, domain=None, range=Optional[Union[str, list[str]]])

slots.studyDesign__observational_units = Slot(uri=NMDC_SFAS_BRCS.observational_units, name="studyDesign__observational_units", curie=NMDC_SFAS_BRCS.curie('observational_units'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__observational_units, domain=None, range=Optional[Union[str, list[str]]])

slots.studyDesign__sampling_strategy = Slot(uri=NMDC_SFAS_BRCS.sampling_strategy, name="studyDesign__sampling_strategy", curie=NMDC_SFAS_BRCS.curie('sampling_strategy'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__sampling_strategy, domain=None, range=Optional[str])

slots.studyDesign__replication = Slot(uri=NMDC_SFAS_BRCS.replication, name="studyDesign__replication", curie=NMDC_SFAS_BRCS.curie('replication'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__replication, domain=None, range=Optional[str])

slots.studyDesign__randomization = Slot(uri=NMDC_SFAS_BRCS.randomization, name="studyDesign__randomization", curie=NMDC_SFAS_BRCS.curie('randomization'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__randomization, domain=None, range=Optional[str])

slots.studyDesign__blocking = Slot(uri=NMDC_SFAS_BRCS.blocking, name="studyDesign__blocking", curie=NMDC_SFAS_BRCS.curie('blocking'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__blocking, domain=None, range=Optional[str])

slots.studyDesign__controls = Slot(uri=NMDC_SFAS_BRCS.controls, name="studyDesign__controls", curie=NMDC_SFAS_BRCS.curie('controls'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__controls, domain=None, range=Optional[str])

slots.studyDesign__notes = Slot(uri=NMDC_SFAS_BRCS.notes, name="studyDesign__notes", curie=NMDC_SFAS_BRCS.curie('notes'),
                   model_uri=NMDC_SFAS_BRCS.studyDesign__notes, domain=None, range=Optional[str])

slots.nMDCStudyReference__pi = Slot(uri=NMDC_SFAS_BRCS.pi, name="nMDCStudyReference__pi", curie=NMDC_SFAS_BRCS.curie('pi'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__pi, domain=None, range=Optional[str])

slots.nMDCStudyReference__bioproject_ids = Slot(uri=NMDC_SFAS_BRCS.bioproject_ids, name="nMDCStudyReference__bioproject_ids", curie=NMDC_SFAS_BRCS.curie('bioproject_ids'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__bioproject_ids, domain=None, range=Optional[Union[str, list[str]]])

slots.nMDCStudyReference__gold_study_id = Slot(uri=NMDC_SFAS_BRCS.gold_study_id, name="nMDCStudyReference__gold_study_id", curie=NMDC_SFAS_BRCS.curie('gold_study_id'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__gold_study_id, domain=None, range=Optional[str])

slots.nMDCStudyReference__jgi_proposal_id = Slot(uri=NMDC_SFAS_BRCS.jgi_proposal_id, name="nMDCStudyReference__jgi_proposal_id", curie=NMDC_SFAS_BRCS.curie('jgi_proposal_id'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__jgi_proposal_id, domain=None, range=Optional[str])

slots.nMDCStudyReference__brc_dataset_ids = Slot(uri=NMDC_SFAS_BRCS.brc_dataset_ids, name="nMDCStudyReference__brc_dataset_ids", curie=NMDC_SFAS_BRCS.curie('brc_dataset_ids'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__brc_dataset_ids, domain=None, range=Optional[Union[str, list[str]]])

slots.nMDCStudyReference__nmdc_ingest_target = Slot(uri=NMDC_SFAS_BRCS.nmdc_ingest_target, name="nMDCStudyReference__nmdc_ingest_target", curie=NMDC_SFAS_BRCS.curie('nmdc_ingest_target'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__nmdc_ingest_target, domain=None, range=Optional[Union[bool, Bool]])

slots.nMDCStudyReference__nmdc_ingest_priority = Slot(uri=NMDC_SFAS_BRCS.nmdc_ingest_priority, name="nMDCStudyReference__nmdc_ingest_priority", curie=NMDC_SFAS_BRCS.curie('nmdc_ingest_priority'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__nmdc_ingest_priority, domain=None, range=Optional[Union[str, "NMDCIngestPriority"]])

slots.nMDCStudyReference__data_modalities = Slot(uri=NMDC_SFAS_BRCS.data_modalities, name="nMDCStudyReference__data_modalities", curie=NMDC_SFAS_BRCS.curie('data_modalities'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__data_modalities, domain=None, range=Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]])

slots.nMDCStudyReference__sample_count = Slot(uri=NMDC_SFAS_BRCS.sample_count, name="nMDCStudyReference__sample_count", curie=NMDC_SFAS_BRCS.curie('sample_count'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__sample_count, domain=None, range=Optional[int])

slots.nMDCStudyReference__organism = Slot(uri=NMDC_SFAS_BRCS.organism, name="nMDCStudyReference__organism", curie=NMDC_SFAS_BRCS.curie('organism'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__organism, domain=None, range=Optional[str])

slots.nMDCStudyReference__preprocessed_data_available = Slot(uri=NMDC_SFAS_BRCS.preprocessed_data_available, name="nMDCStudyReference__preprocessed_data_available", curie=NMDC_SFAS_BRCS.curie('preprocessed_data_available'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__preprocessed_data_available, domain=None, range=Optional[Union[Union[str, "PreprocessedDataType"], list[Union[str, "PreprocessedDataType"]]]])

slots.nMDCStudyReference__preprocessed_data_counts = Slot(uri=NMDC_SFAS_BRCS.preprocessed_data_counts, name="nMDCStudyReference__preprocessed_data_counts", curie=NMDC_SFAS_BRCS.curie('preprocessed_data_counts'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__preprocessed_data_counts, domain=None, range=Optional[str])

slots.nMDCStudyReference__ncbi_data_quality_notes = Slot(uri=NMDC_SFAS_BRCS.ncbi_data_quality_notes, name="nMDCStudyReference__ncbi_data_quality_notes", curie=NMDC_SFAS_BRCS.curie('ncbi_data_quality_notes'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__ncbi_data_quality_notes, domain=None, range=Optional[str])

slots.nMDCStudyReference__primary_reference_info = Slot(uri=NMDC_SFAS_BRCS.primary_reference_info, name="nMDCStudyReference__primary_reference_info", curie=NMDC_SFAS_BRCS.curie('primary_reference_info'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__primary_reference_info, domain=None, range=Optional[Union[dict, PrimaryReferenceInfo]])

slots.nMDCStudyReference__source_reference = Slot(uri=NMDC_SFAS_BRCS.source_reference, name="nMDCStudyReference__source_reference", curie=NMDC_SFAS_BRCS.curie('source_reference'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__source_reference, domain=None, range=Optional[Union[dict, WebReference]])

slots.nMDCStudyReference__synthetic_communities = Slot(uri=NMDC_SFAS_BRCS.synthetic_communities, name="nMDCStudyReference__synthetic_communities", curie=NMDC_SFAS_BRCS.curie('synthetic_communities'),
                   model_uri=NMDC_SFAS_BRCS.nMDCStudyReference__synthetic_communities, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.analysis__analysis_type = Slot(uri=NMDC_SFAS_BRCS.analysis_type, name="analysis__analysis_type", curie=NMDC_SFAS_BRCS.curie('analysis_type'),
                   model_uri=NMDC_SFAS_BRCS.analysis__analysis_type, domain=None, range=Optional[Union[str, "AnalysisType"]])

slots.analysis__input_data_description = Slot(uri=NMDC_SFAS_BRCS.input_data_description, name="analysis__input_data_description", curie=NMDC_SFAS_BRCS.curie('input_data_description'),
                   model_uri=NMDC_SFAS_BRCS.analysis__input_data_description, domain=None, range=Optional[str])

slots.analysis__output_data_types = Slot(uri=NMDC_SFAS_BRCS.output_data_types, name="analysis__output_data_types", curie=NMDC_SFAS_BRCS.curie('output_data_types'),
                   model_uri=NMDC_SFAS_BRCS.analysis__output_data_types, domain=None, range=Optional[Union[Union[str, "DataType"], list[Union[str, "DataType"]]]])

slots.analysis__primary_reference_info = Slot(uri=NMDC_SFAS_BRCS.primary_reference_info, name="analysis__primary_reference_info", curie=NMDC_SFAS_BRCS.curie('primary_reference_info'),
                   model_uri=NMDC_SFAS_BRCS.analysis__primary_reference_info, domain=None, range=Optional[Union[dict, PrimaryReferenceInfo]])

slots.kBaseNarrative__kbase_narrative_id = Slot(uri=NMDC_SFAS_BRCS.kbase_narrative_id, name="kBaseNarrative__kbase_narrative_id", curie=NMDC_SFAS_BRCS.curie('kbase_narrative_id'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__kbase_narrative_id, domain=None, range=Optional[str])

slots.kBaseNarrative__kbase_narrative_url = Slot(uri=NMDC_SFAS_BRCS.kbase_narrative_url, name="kBaseNarrative__kbase_narrative_url", curie=NMDC_SFAS_BRCS.curie('kbase_narrative_url'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__kbase_narrative_url, domain=None, range=Optional[Union[str, URI]])

slots.kBaseNarrative__kbase_workspace_id = Slot(uri=NMDC_SFAS_BRCS.kbase_workspace_id, name="kBaseNarrative__kbase_workspace_id", curie=NMDC_SFAS_BRCS.curie('kbase_workspace_id'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__kbase_workspace_id, domain=None, range=Optional[str])

slots.kBaseNarrative__osti_doi = Slot(uri=NMDC_SFAS_BRCS.osti_doi, name="kBaseNarrative__osti_doi", curie=NMDC_SFAS_BRCS.curie('osti_doi'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__osti_doi, domain=None, range=Optional[str])

slots.kBaseNarrative__is_static = Slot(uri=NMDC_SFAS_BRCS.is_static, name="kBaseNarrative__is_static", curie=NMDC_SFAS_BRCS.curie('is_static'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__is_static, domain=None, range=Optional[Union[bool, Bool]])

slots.kBaseNarrative__genome_count = Slot(uri=NMDC_SFAS_BRCS.genome_count, name="kBaseNarrative__genome_count", curie=NMDC_SFAS_BRCS.curie('genome_count'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__genome_count, domain=None, range=Optional[int])

slots.kBaseNarrative__sample_count = Slot(uri=NMDC_SFAS_BRCS.sample_count, name="kBaseNarrative__sample_count", curie=NMDC_SFAS_BRCS.curie('sample_count'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__sample_count, domain=None, range=Optional[int])

slots.kBaseNarrative__related_narratives = Slot(uri=NMDC_SFAS_BRCS.related_narratives, name="kBaseNarrative__related_narratives", curie=NMDC_SFAS_BRCS.curie('related_narratives'),
                   model_uri=NMDC_SFAS_BRCS.kBaseNarrative__related_narratives, domain=None, range=Optional[Union[str, list[str]]])

slots.flagshipGenome__common_name = Slot(uri=NMDC_SFAS_BRCS.common_name, name="flagshipGenome__common_name", curie=NMDC_SFAS_BRCS.curie('common_name'),
                   model_uri=NMDC_SFAS_BRCS.flagshipGenome__common_name, domain=None, range=Optional[str])

slots.flagshipGenome__year = Slot(uri=NMDC_SFAS_BRCS.year, name="flagshipGenome__year", curie=NMDC_SFAS_BRCS.curie('year'),
                   model_uri=NMDC_SFAS_BRCS.flagshipGenome__year, domain=None, range=Optional[int])

slots.referenceData__microbial_genomes = Slot(uri=NMDC_SFAS_BRCS.microbial_genomes, name="referenceData__microbial_genomes", curie=NMDC_SFAS_BRCS.curie('microbial_genomes'),
                   model_uri=NMDC_SFAS_BRCS.referenceData__microbial_genomes, domain=None, range=Optional[str])

slots.referenceData__plant_genomes = Slot(uri=NMDC_SFAS_BRCS.plant_genomes, name="referenceData__plant_genomes", curie=NMDC_SFAS_BRCS.curie('plant_genomes'),
                   model_uri=NMDC_SFAS_BRCS.referenceData__plant_genomes, domain=None, range=Optional[str])

slots.referenceData__biolog_media = Slot(uri=NMDC_SFAS_BRCS.biolog_media, name="referenceData__biolog_media", curie=NMDC_SFAS_BRCS.curie('biolog_media'),
                   model_uri=NMDC_SFAS_BRCS.referenceData__biolog_media, domain=None, range=Optional[str])

slots.referenceData__reactions_compounds = Slot(uri=NMDC_SFAS_BRCS.reactions_compounds, name="referenceData__reactions_compounds", curie=NMDC_SFAS_BRCS.curie('reactions_compounds'),
                   model_uri=NMDC_SFAS_BRCS.referenceData__reactions_compounds, domain=None, range=Optional[str])

slots.capability__capability_type = Slot(uri=NMDC_SFAS_BRCS.capability_type, name="capability__capability_type", curie=NMDC_SFAS_BRCS.curie('capability_type'),
                   model_uri=NMDC_SFAS_BRCS.capability__capability_type, domain=None, range=Optional[Union[str, "CapabilityType"]])

slots.capability__instruments = Slot(uri=NMDC_SFAS_BRCS.instruments, name="capability__instruments", curie=NMDC_SFAS_BRCS.curie('instruments'),
                   model_uri=NMDC_SFAS_BRCS.capability__instruments, domain=None, range=Optional[Union[Union[dict, Instrument], list[Union[dict, Instrument]]]])

slots.capability__access_mode = Slot(uri=NMDC_SFAS_BRCS.access_mode, name="capability__access_mode", curie=NMDC_SFAS_BRCS.curie('access_mode'),
                   model_uri=NMDC_SFAS_BRCS.capability__access_mode, domain=None, range=Optional[str])

slots.capability__throughput = Slot(uri=NMDC_SFAS_BRCS.throughput, name="capability__throughput", curie=NMDC_SFAS_BRCS.curie('throughput'),
                   model_uri=NMDC_SFAS_BRCS.capability__throughput, domain=None, range=Optional[str])

slots.capability__year_established = Slot(uri=NMDC_SFAS_BRCS.year_established, name="capability__year_established", curie=NMDC_SFAS_BRCS.curie('year_established'),
                   model_uri=NMDC_SFAS_BRCS.capability__year_established, domain=None, range=Optional[int])

slots.capability__url = Slot(uri=NMDC_SFAS_BRCS.url, name="capability__url", curie=NMDC_SFAS_BRCS.curie('url'),
                   model_uri=NMDC_SFAS_BRCS.capability__url, domain=None, range=Optional[Union[str, URI]])

slots.capability__applications = Slot(uri=NMDC_SFAS_BRCS.applications, name="capability__applications", curie=NMDC_SFAS_BRCS.curie('applications'),
                   model_uri=NMDC_SFAS_BRCS.capability__applications, domain=None, range=Optional[Union[str, list[str]]])

slots.capability__data_products = Slot(uri=NMDC_SFAS_BRCS.data_products, name="capability__data_products", curie=NMDC_SFAS_BRCS.curie('data_products'),
                   model_uri=NMDC_SFAS_BRCS.capability__data_products, domain=None, range=Optional[Union[str, list[str]]])

slots.capability__status = Slot(uri=NMDC_SFAS_BRCS.status, name="capability__status", curie=NMDC_SFAS_BRCS.curie('status'),
                   model_uri=NMDC_SFAS_BRCS.capability__status, domain=None, range=Optional[Union[str, "CapabilityStatus"]])

slots.capability__commissioned_date = Slot(uri=NMDC_SFAS_BRCS.commissioned_date, name="capability__commissioned_date", curie=NMDC_SFAS_BRCS.curie('commissioned_date'),
                   model_uri=NMDC_SFAS_BRCS.capability__commissioned_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.capability__leader = Slot(uri=NMDC_SFAS_BRCS.leader, name="capability__leader", curie=NMDC_SFAS_BRCS.curie('leader'),
                   model_uri=NMDC_SFAS_BRCS.capability__leader, domain=None, range=Optional[str])

slots.capability__future_expansion = Slot(uri=NMDC_SFAS_BRCS.future_expansion, name="capability__future_expansion", curie=NMDC_SFAS_BRCS.curie('future_expansion'),
                   model_uri=NMDC_SFAS_BRCS.capability__future_expansion, domain=None, range=Optional[str])

slots.instrument__instrument_type = Slot(uri=NMDC_SFAS_BRCS.instrument_type, name="instrument__instrument_type", curie=NMDC_SFAS_BRCS.curie('instrument_type'),
                   model_uri=NMDC_SFAS_BRCS.instrument__instrument_type, domain=None, range=Optional[Union[str, "InstrumentType"]])

slots.instrument__manufacturer = Slot(uri=NMDC_SFAS_BRCS.manufacturer, name="instrument__manufacturer", curie=NMDC_SFAS_BRCS.curie('manufacturer'),
                   model_uri=NMDC_SFAS_BRCS.instrument__manufacturer, domain=None, range=Optional[str])

slots.instrument__model = Slot(uri=NMDC_SFAS_BRCS.model, name="instrument__model", curie=NMDC_SFAS_BRCS.curie('model'),
                   model_uri=NMDC_SFAS_BRCS.instrument__model, domain=None, range=Optional[str])

slots.instrument__count = Slot(uri=NMDC_SFAS_BRCS.count, name="instrument__count", curie=NMDC_SFAS_BRCS.curie('count'),
                   model_uri=NMDC_SFAS_BRCS.instrument__count, domain=None, range=Optional[int])

slots.instrument__specifications = Slot(uri=NMDC_SFAS_BRCS.specifications, name="instrument__specifications", curie=NMDC_SFAS_BRCS.curie('specifications'),
                   model_uri=NMDC_SFAS_BRCS.instrument__specifications, domain=None, range=Optional[str])

slots.ResearchProgram_id = Slot(uri=SCHEMA.identifier, name="ResearchProgram_id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.ResearchProgram_id, domain=ResearchProgram, range=Union[str, ResearchProgramId],
                   pattern=re.compile(r'^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$'))

slots.ResearchProgram_name = Slot(uri=SCHEMA.name, name="ResearchProgram_name", curie=SCHEMA.curie('name'),
                   model_uri=NMDC_SFAS_BRCS.ResearchProgram_name, domain=ResearchProgram, range=str)

slots.BioenergyResearchCenter_program_type = Slot(uri=NMDC_SFAS_BRCS.program_type, name="BioenergyResearchCenter_program_type", curie=NMDC_SFAS_BRCS.curie('program_type'),
                   model_uri=NMDC_SFAS_BRCS.BioenergyResearchCenter_program_type, domain=BioenergyResearchCenter, range=Optional[Union[str, "ProgramType"]])

slots.ScientificFocusArea_program_type = Slot(uri=NMDC_SFAS_BRCS.program_type, name="ScientificFocusArea_program_type", curie=NMDC_SFAS_BRCS.curie('program_type'),
                   model_uri=NMDC_SFAS_BRCS.ScientificFocusArea_program_type, domain=ScientificFocusArea, range=Optional[Union[str, "ProgramType"]])

slots.OtherProgram_program_type = Slot(uri=NMDC_SFAS_BRCS.program_type, name="OtherProgram_program_type", curie=NMDC_SFAS_BRCS.curie('program_type'),
                   model_uri=NMDC_SFAS_BRCS.OtherProgram_program_type, domain=OtherProgram, range=Optional[Union[str, "ProgramType"]])

slots.ArtificialIntelligenceProject_program_type = Slot(uri=NMDC_SFAS_BRCS.program_type, name="ArtificialIntelligenceProject_program_type", curie=NMDC_SFAS_BRCS.curie('program_type'),
                   model_uri=NMDC_SFAS_BRCS.ArtificialIntelligenceProject_program_type, domain=ArtificialIntelligenceProject, range=Optional[Union[str, "ProgramType"]])

slots.Variable_name = Slot(uri=SCHEMA.name, name="Variable_name", curie=SCHEMA.curie('name'),
                   model_uri=NMDC_SFAS_BRCS.Variable_name, domain=Variable, range=str)

slots.BERVOTerm_id = Slot(uri=SCHEMA.identifier, name="BERVOTerm_id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.BERVOTerm_id, domain=BERVOTerm, range=Union[str, BERVOTermId],
                   pattern=re.compile(r'^BERVO:\d+$'))

slots.MIXSTerm_id = Slot(uri=SCHEMA.identifier, name="MIXSTerm_id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.MIXSTerm_id, domain=MIXSTerm, range=Union[str, MIXSTermId],
                   pattern=re.compile(r'^MIXS:\d{7}$'))

slots.Reference_id = Slot(uri=SCHEMA.identifier, name="Reference_id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.Reference_id, domain=Reference, range=Union[str, ReferenceId])

slots.FieldSite_id = Slot(uri=SCHEMA.identifier, name="FieldSite_id", curie=SCHEMA.curie('identifier'),
                   model_uri=NMDC_SFAS_BRCS.FieldSite_id, domain=FieldSite, range=Union[str, FieldSiteId])

slots.FieldSite_name = Slot(uri=SCHEMA.name, name="FieldSite_name", curie=SCHEMA.curie('name'),
                   model_uri=NMDC_SFAS_BRCS.FieldSite_name, domain=FieldSite, range=str)
