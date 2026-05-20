from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )

    @model_serializer(mode='wrap', when_used='unless-none')
    def treat_empty_lists_as_none(
            self, handler: SerializerFunctionWrapHandler,
            info: SerializationInfo) -> dict[str, Any]:
        if info.exclude_none:
            _instance = self.model_copy()
            for field, field_info in type(_instance).model_fields.items():
                if getattr(_instance, field) == [] and not(
                        field_info.is_required()):
                    setattr(_instance, field, None)
        else:
            _instance = self
        return handler(_instance, info)



class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'nmdc_sfas_brcs',
     'default_range': 'string',
     'description': 'A LinkML schema for representing DOE BER (Biological and '
                    'Environmental Research)\n'
                    'funded Scientific Focus Areas (SFAs) and Bioenergy Research '
                    'Centers (BRCs),\n'
                    'including their metadata, datasets, publications, and '
                    'organizational structure.',
     'id': 'https://w3id.org/nmdc/sfas-brcs',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'nmdc-sfas-brcs',
     'prefixes': {'BERVO': {'prefix_prefix': 'BERVO',
                            'prefix_reference': 'https://w3id.org/bervo/BERVO_'},
                  'EFO': {'prefix_prefix': 'EFO',
                          'prefix_reference': 'http://www.ebi.ac.uk/efo/EFO_'},
                  'IAO': {'prefix_prefix': 'IAO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/IAO_'},
                  'MIXS': {'prefix_prefix': 'MIXS',
                           'prefix_reference': 'https://w3id.org/mixs/'},
                  'NCBITaxon': {'prefix_prefix': 'NCBITaxon',
                                'prefix_reference': 'http://purl.obolibrary.org/obo/NCBITaxon_'},
                  'OBI': {'prefix_prefix': 'OBI',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/OBI_'},
                  'STATO': {'prefix_prefix': 'STATO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/STATO_'},
                  'communitymech': {'prefix_prefix': 'communitymech',
                                    'prefix_reference': 'https://w3id.org/communitymech/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'doi': {'prefix_prefix': 'doi',
                          'prefix_reference': 'https://doi.org/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'nmdc_sfas_brcs': {'prefix_prefix': 'nmdc_sfas_brcs',
                                     'prefix_reference': 'https://w3id.org/nmdc/sfas-brcs/'},
                  'obo': {'prefix_prefix': 'obo',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/'},
                  'orcid': {'prefix_prefix': 'orcid',
                            'prefix_reference': 'https://orcid.org/'},
                  'pmid': {'prefix_prefix': 'pmid',
                           'prefix_reference': 'https://www.ncbi.nlm.nih.gov/pubmed/'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'ror': {'prefix_prefix': 'ror',
                          'prefix_reference': 'https://ror.org/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'see_also': ['https://www.genomicscience.energy.gov',
                  'https://ess.science.energy.gov',
                  'https://science.osti.gov/ber'],
     'source_file': 'src/nmdc_sfas_brcs/schema/nmdc_sfas_brcs.yaml',
     'title': 'NMDC SFAs and BRCs Schema'} )

class ProgramType(str, Enum):
    """
    Types of DOE BER research programs
    """
    BIOENERGY_RESEARCH_CENTER = "BIOENERGY_RESEARCH_CENTER"
    """
    A Bioenergy Research Center (BRC) - large-scale, multi-institutional center focused on biofuels and bioproducts from plant biomass
    """
    SCIENTIFIC_FOCUS_AREA = "SCIENTIFIC_FOCUS_AREA"
    """
    A Scientific Focus Area (SFA) - integrated research program at DOE national laboratories
    """
    USER_FACILITY = "USER_FACILITY"
    """
    A DOE BER User Facility providing resources to the scientific community
    """
    DATA_REPOSITORY = "DATA_REPOSITORY"
    """
    A data repository or archive
    """
    DATA_COLLABORATIVE = "DATA_COLLABORATIVE"
    """
    A collaborative data initiative
    """
    BIOPREPAREDNESS_INITIATIVE = "BIOPREPAREDNESS_INITIATIVE"
    """
    A biopreparedness research initiative such as BRaVE (Biopreparedness Research Virtual Environment) - typically cross-cutting, time-limited projects spanning multiple DOE offices
    """
    AI_PILOT_PROJECT = "AI_PILOT_PROJECT"
    """
    Artificial intelligence pilot project or AI-enabled science initiative, typically cross-cutting and often involving BER and ASCR.
    """
    FIELD_CAMPAIGN = "FIELD_CAMPAIGN"
    """
    Time-limited coordinated field campaign, often associated with an SFA or other BER program, producing campaign-specific observations and datasets.
    """
    OTHER_INITIATIVE = "OTHER_INITIATIVE"
    """
    Other research initiatives that don't fit traditional categories
    """


class SFAType(str, Enum):
    """
    Types of Scientific Focus Areas by program area
    """
    GENOMIC_SCIENCE_SFA = "GENOMIC_SCIENCE_SFA"
    """
    SFA within the Genomic Science Program focusing on plant and microbial systems biology
    """
    ENVIRONMENTAL_SYSTEM_SCIENCE_SFA = "ENVIRONMENTAL_SYSTEM_SCIENCE_SFA"
    """
    SFA within the Environmental System Science program focusing on watershed and ecosystem processes
    """
    ENVIRONMENTAL_MICROBIOME_SCIENCE = "ENVIRONMENTAL_MICROBIOME_SCIENCE"
    """
    SFA focused on environmental microbiome research
    """
    SECURE_BIOSYSTEMS_DESIGN = "SECURE_BIOSYSTEMS_DESIGN"
    """
    SFA focused on secure biosystems design and biocontainment
    """


class InstitutionType(str, Enum):
    """
    Types of research institutions
    """
    NATIONAL_LABORATORY = "NATIONAL_LABORATORY"
    """
    A DOE National Laboratory
    """
    UNIVERSITY = "UNIVERSITY"
    """
    A university or academic institution
    """
    RESEARCH_INSTITUTE = "RESEARCH_INSTITUTE"
    """
    A research institute
    """
    FEDERAL_AGENCY = "FEDERAL_AGENCY"
    """
    A federal government agency
    """
    PRIVATE_SECTOR = "PRIVATE_SECTOR"
    """
    A private sector organization
    """


class PreprocessedDataType(str, Enum):
    """
    Types of preprocessed or derived data products available in public repositories. Used to identify studies with analysis-ready data for NMDC consideration.
    """
    MAGS = "MAGS"
    """
    Metagenome-assembled genomes - draft genomes reconstructed from metagenomic data through binning and assembly
    """
    GENOME_ASSEMBLIES = "GENOME_ASSEMBLIES"
    """
    Assembled genome sequences (contigs, scaffolds, or complete)
    """
    GENE_ANNOTATIONS = "GENE_ANNOTATIONS"
    """
    Predicted gene calls and functional annotations
    """
    FUNCTIONAL_ANNOTATIONS = "FUNCTIONAL_ANNOTATIONS"
    """
    Functional annotations (COG, KEGG, Pfam, etc.)
    """
    TAXONOMIC_CLASSIFICATIONS = "TAXONOMIC_CLASSIFICATIONS"
    """
    Taxonomic assignments for sequences or bins
    """
    READ_QC = "READ_QC"
    """
    Quality-controlled sequencing reads
    """
    ASSEMBLY_QC = "ASSEMBLY_QC"
    """
    Assembly quality metrics (CheckM, QUAST, etc.)
    """
    METABOLIC_MODELS = "METABOLIC_MODELS"
    """
    Genome-scale metabolic reconstructions
    """
    PHYLOGENETIC_TREES = "PHYLOGENETIC_TREES"
    """
    Phylogenetic trees or placements
    """


class DataType(str, Enum):
    """
    Types of scientific data
    """
    DNA_sequencing_assay = "GENOMICS"
    """
    Genomic sequence data
    """
    whole_metagenome_sequencing_assay = "METAGENOMICS"
    """
    Metagenomic sequence data
    """
    transcription_profiling_assay = "TRANSCRIPTOMICS"
    """
    Transcriptomic expression data
    """
    METATRANSCRIPTOMICS = "METATRANSCRIPTOMICS"
    """
    Metatranscriptomic data
    """
    number_16s_ribosomal_gene_sequencing_assay = "AMPLICON_16S"
    """
    16S rRNA gene amplicon sequencing for bacterial/archaeal profiling
    """
    ITS_rRNA_gene_sequencing_assay = "AMPLICON_ITS"
    """
    ITS amplicon sequencing for fungal profiling
    """
    AMPLICON_18S = "AMPLICON_18S"
    """
    18S rRNA gene amplicon sequencing for eukaryotic profiling
    """
    protein_expression_profiling_assay = "PROTEOMICS"
    """
    Proteomic data
    """
    metabolite_profiling_assay = "METABOLOMICS"
    """
    Metabolomic data
    """
    EXOMETABOLOMICS = "EXOMETABOLOMICS"
    """
    Exometabolomic data (extracellular metabolites)
    """
    GEOSPATIAL = "GEOSPATIAL"
    """
    Geospatial or GIS data
    """
    PHENOTYPIC_DATA = "PHENOTYPIC_DATA"
    """
    Phenotypic measurement data
    """
    IMAGING_DATA = "IMAGING_DATA"
    """
    Various imaging data
    """
    ENVIRONMENTAL_SENSOR_DATA = "ENVIRONMENTAL_SENSOR_DATA"
    """
    Environmental sensor time series data
    """
    HYDROLOGICAL_DATA = "HYDROLOGICAL_DATA"
    """
    Hydrological measurements
    """
    BIOGEOCHEMICAL_DATA = "BIOGEOCHEMICAL_DATA"
    """
    Biogeochemical measurements
    """
    STABLE_ISOTOPE_DATA = "STABLE_ISOTOPE_DATA"
    """
    Stable isotope measurements
    """
    SYNTHETIC_BIOLOGY_CONSTRUCTS = "SYNTHETIC_BIOLOGY_CONSTRUCTS"
    """
    Synthetic biology parts and constructs
    """
    FIELD_TRIAL_DATA = "FIELD_TRIAL_DATA"
    """
    Data from field trials
    """
    CROP_YIELD_DATA = "CROP_YIELD_DATA"
    """
    Crop yield measurements
    """
    SOIL_MICROBIOME_DATA = "SOIL_MICROBIOME_DATA"
    """
    Soil microbiome characterization data
    """
    ENZYME_ACTIVITY_DATA = "ENZYME_ACTIVITY_DATA"
    """
    Enzyme activity measurements
    """
    ENZYME_KINETICS = "ENZYME_KINETICS"
    """
    Enzyme kinetics data
    """
    STRUCTURAL_BIOLOGY = "STRUCTURAL_BIOLOGY"
    """
    Structural biology data
    """
    GWAS_DATA = "GWAS_DATA"
    """
    Genome-wide association study data
    """
    ISOLATE_COLLECTIONS = "ISOLATE_COLLECTIONS"
    """
    Microbial isolate collection data
    """
    WATER_CHEMISTRY = "WATER_CHEMISTRY"
    """
    Water chemistry measurements
    """
    GROUNDWATER_CHEMISTRY = "GROUNDWATER_CHEMISTRY"
    """
    Groundwater chemistry data
    """
    MERCURY_SPECIATION = "MERCURY_SPECIATION"
    """
    Mercury speciation data
    """
    RADIOCARBON_DATA = "RADIOCARBON_DATA"
    """
    Radiocarbon dating data
    """
    REMOTE_SENSING = "REMOTE_SENSING"
    """
    Remote sensing imagery
    """
    SATELLITE_IMAGERY = "SATELLITE_IMAGERY"
    """
    Satellite imagery data
    """
    ECONOMIC_MODELING_DATA = "ECONOMIC_MODELING_DATA"
    """
    Techno-economic modeling outputs
    """
    LIFE_CYCLE_ASSESSMENT_DATA = "LIFE_CYCLE_ASSESSMENT_DATA"
    """
    Life cycle assessment data
    """
    FITNESS_DATA = "FITNESS_DATA"
    """
    Organism fitness data
    """
    CONTAINMENT_EFFICACY_DATA = "CONTAINMENT_EFFICACY_DATA"
    """
    Biocontainment efficacy measurements
    """
    FISH_IMAGING = "FISH_IMAGING"
    """
    Fluorescence in situ hybridization imaging data
    """
    SIDEROPHORE_DATA = "SIDEROPHORE_DATA"
    """
    Siderophore profile and iron-chelating compound data
    """
    ENDOHYPHAL_MICROBIOME_DATA = "ENDOHYPHAL_MICROBIOME_DATA"
    """
    Data on microorganisms living within fungal hyphae
    """
    BACTERIAL_FUNGAL_INTERACTION_DATA = "BACTERIAL_FUNGAL_INTERACTION_DATA"
    """
    Curated bacterial-fungal interaction records from literature or experiments
    """
    FUNGAL_HIGHWAY_DATA = "FUNGAL_HIGHWAY_DATA"
    """
    Data from fungal highway column experiments on bacterial dispersal via mycelia
    """


class DataCollectionModality(str, Enum):
    """
    Methods and modalities for data collection
    """
    FIELD_EXPERIMENTS = "FIELD_EXPERIMENTS"
    """
    Field-based experimental studies
    """
    FIELD_TRIALS = "FIELD_TRIALS"
    """
    Agricultural or ecological field trials
    """
    GREENHOUSE_STUDIES = "GREENHOUSE_STUDIES"
    """
    Greenhouse-based studies
    """
    LABORATORY_EXPERIMENTS = "LABORATORY_EXPERIMENTS"
    """
    Laboratory-based experiments
    """
    LABORATORY_FERMENTATION = "LABORATORY_FERMENTATION"
    """
    Laboratory-scale fermentation studies
    """
    HIGH_THROUGHPUT_SCREENING = "HIGH_THROUGHPUT_SCREENING"
    """
    High-throughput screening methods
    """
    HIGH_THROUGHPUT_SEQUENCING = "HIGH_THROUGHPUT_SEQUENCING"
    """
    High-throughput DNA/RNA sequencing
    """
    HIGH_THROUGHPUT_PHENOTYPING = "HIGH_THROUGHPUT_PHENOTYPING"
    """
    High-throughput phenotyping methods
    """
    GENOME_SEQUENCING = "GENOME_SEQUENCING"
    """
    Whole genome sequencing
    """
    METAGENOMICS = "METAGENOMICS"
    """
    Metagenomic sequencing and analysis
    """
    TARGETED_METAGENOMICS = "TARGETED_METAGENOMICS"
    """
    Targeted metagenomic approaches
    """
    MULTI_OMICS = "MULTI_OMICS"
    """
    Integrated multi-omics approaches
    """
    REMOTE_SENSING = "REMOTE_SENSING"
    """
    Remote sensing and satellite imagery
    """
    MASS_SPECTROMETRY = "MASS_SPECTROMETRY"
    """
    Mass spectrometry analysis
    """
    NMR_SPECTROSCOPY = "NMR_SPECTROSCOPY"
    """
    Nuclear magnetic resonance spectroscopy
    """
    IMAGING = "IMAGING"
    """
    Various imaging techniques
    """
    BIOIMAGING = "BIOIMAGING"
    """
    Biological imaging techniques
    """
    CHEMICAL_IMAGING = "CHEMICAL_IMAGING"
    """
    Chemical imaging methods
    """
    LIVE_CELL_IMAGING = "LIVE_CELL_IMAGING"
    """
    Live cell imaging
    """
    NANOSIMS = "NANOSIMS"
    """
    NanoSIMS imaging
    """
    SYNCHROTRON_METHODS = "SYNCHROTRON_METHODS"
    """
    Synchrotron-based analytical methods
    """
    COMPUTATIONAL_MODELING = "COMPUTATIONAL_MODELING"
    """
    Computational and mathematical modeling
    """
    ECOSYSTEM_MODELING = "ECOSYSTEM_MODELING"
    """
    Ecosystem-scale modeling
    """
    STABLE_ISOTOPE_PROBING = "STABLE_ISOTOPE_PROBING"
    """
    Quantitative stable isotope probing (qSIP)
    """
    RADIOISOTOPE_APPROACHES = "RADIOISOTOPE_APPROACHES"
    """
    Radioisotope tracer methods
    """
    GENOME_WIDE_ASSOCIATION = "GENOME_WIDE_ASSOCIATION"
    """
    Genome-wide association studies
    """
    COMMON_GARDEN_EXPERIMENTS = "COMMON_GARDEN_EXPERIMENTS"
    """
    Common garden experimental designs
    """
    FERMENTATION_STUDIES = "FERMENTATION_STUDIES"
    """
    Fermentation process studies
    """
    METABOLIC_FLUX_ANALYSIS = "METABOLIC_FLUX_ANALYSIS"
    """
    Metabolic flux analysis
    """
    TECHNO_ECONOMIC_ANALYSIS = "TECHNO_ECONOMIC_ANALYSIS"
    """
    Techno-economic analysis
    """
    ROBOTIC_AUTOMATION = "ROBOTIC_AUTOMATION"
    """
    Robotic/automated laboratory systems
    """
    GENOME_SCALE_ENGINEERING = "GENOME_SCALE_ENGINEERING"
    """
    Genome-scale engineering approaches
    """
    CRISPR_GENE_EDITING = "CRISPR_GENE_EDITING"
    """
    CRISPR-based gene editing
    """
    BACTERIAL_ISOLATION = "BACTERIAL_ISOLATION"
    """
    Bacterial isolation and culturing
    """
    FIELD_SENSORS = "FIELD_SENSORS"
    """
    Field-deployed environmental sensors
    """
    STREAM_SAMPLING = "STREAM_SAMPLING"
    """
    Stream and water body sampling
    """
    GROUNDWATER_MONITORING = "GROUNDWATER_MONITORING"
    """
    Groundwater monitoring
    """
    LONG_TERM_ECOLOGICAL_RESEARCH = "LONG_TERM_ECOLOGICAL_RESEARCH"
    """
    Long-term ecological research sites
    """
    FABRICATED_ECOSYSTEMS = "FABRICATED_ECOSYSTEMS"
    """
    Fabricated/controlled ecosystem platforms (e.g., EcoFAB)
    """
    FUNGAL_HIGHWAY_COLUMNS = "FUNGAL_HIGHWAY_COLUMNS"
    """
    Fungal highway column devices for studying bacterial dispersal via mycelia
    """
    FISH_MICROSCOPY = "FISH_MICROSCOPY"
    """
    Fluorescence in situ hybridization microscopy
    """
    COCULTURE_EXPERIMENTS = "COCULTURE_EXPERIMENTS"
    """
    Bacterial-fungal co-culture experiments
    """
    SEQUENCE_ENRICHMENT = "SEQUENCE_ENRICHMENT"
    """
    Sequence-based enrichment techniques for detecting endosymbionts
    """


class VariableRole(str, Enum):
    """
    Roles that a variable can play in a study design, dataset, or analysis. Where possible, roles are aligned to OBI, STATO, or EFO terms. Use the narrower study-design roles when the variable's role is known from the experimental design; use MEASURED_VARIABLE for observed data fields when no dependent/independent interpretation is intended.
    """
    study_design_independent_variable = "STUDY_DESIGN_INDEPENDENT_VARIABLE"
    """
    Study design variable that is varied, selected, or otherwise used to explain or predict changes in another variable.
    """
    study_design_dependent_variable = "STUDY_DESIGN_DEPENDENT_VARIABLE"
    """
    Study design variable whose value is expected to vary as a result of other variables.
    """
    study_design_controlled_variable = "STUDY_DESIGN_CONTROLLED_VARIABLE"
    """
    Study design variable held constant or constrained by the study design.
    """
    experimental_factor = "EXPERIMENTAL_FACTOR"
    """
    Variable representing an experimental factor or condition.
    """
    blocking_variable = "BLOCKING_VARIABLE"
    """
    Variable used to form blocks or strata in a study design or analysis.
    """
    MEASURED_VARIABLE = "MEASURED_VARIABLE"
    """
    Directly observed or measured variable.
    """
    COVARIATE = "COVARIATE"
    """
    Additional contextual or adjustment variable included in an analysis.
    """
    DERIVED = "DERIVED"
    """
    Variable computed, transformed, or inferred from other variables
    """
    date_Time_variable = "DATE_TIME_VARIABLE"
    """
    Variable whose values represent dates or times.
    """
    time_to_event_variable = "TIME_TO_EVENT_VARIABLE"
    """
    Variable whose values represent elapsed time until an event.
    """
    SPATIAL_INDEX = "SPATIAL_INDEX"
    """
    Location, plot, coordinate, depth, transect, or other spatial index
    """
    GROUPING = "GROUPING"
    """
    Replicate group, block, batch, genotype group, or other grouping variable
    """
    IDENTIFIER = "IDENTIFIER"
    """
    Sample, subject, feature, file, or other identifier field
    """
    QUALITY_CONTROL = "QUALITY_CONTROL"
    """
    Quality flag, censoring flag, uncertainty estimate, or QC metric
    """


class VariableValueType(str, Enum):
    """
    Basic value shape for variables
    """
    NUMERIC = "NUMERIC"
    """
    Numeric value that may include decimals
    """
    INTEGER = "INTEGER"
    """
    Integer count or whole-number value
    """
    CATEGORICAL = "CATEGORICAL"
    """
    Value drawn from a finite set of categories or levels
    """
    BOOLEAN = "BOOLEAN"
    """
    True/false value
    """
    DATETIME = "DATETIME"
    """
    Date, time, or timestamp value
    """
    TEXT = "TEXT"
    """
    Free-text string value
    """
    IDENTIFIER = "IDENTIFIER"
    """
    Identifier or accession value
    """
    ONTOLOGY_TERM = "ONTOLOGY_TERM"
    """
    Ontology CURIE, URI, or controlled vocabulary term
    """
    ARRAY = "ARRAY"
    """
    Ordered list, vector, spectrum, profile, or other repeated values
    """
    OBJECT = "OBJECT"
    """
    Structured object or nested record
    """


class OntologyMappingRelation(str, Enum):
    """
    SSSOM/SKOS mapping predicate used to qualify how a local variable, field, or data-dictionary entry maps to an ontology term.
    """
    exact_match = "EXACT_MATCH"
    """
    The local variable and ontology term can be used interchangeably in this context.
    """
    close_match = "CLOSE_MATCH"
    """
    The local variable and ontology term are sufficiently similar for many uses but should not be treated as exact equivalents.
    """
    broad_match = "BROAD_MATCH"
    """
    The ontology term is broader than the local variable.
    """
    narrow_match = "NARROW_MATCH"
    """
    The ontology term is narrower than the local variable.
    """
    related_match = "RELATED_MATCH"
    """
    The local variable and ontology term are associated but not equivalent or hierarchical.
    """


class StudyDesignTerm(str):
    """
    OBI study design terms
    """
    pass


class MIXSVariableTerm(str, Enum):
    """
    MIxS terms commonly useful when mapping catalogued study or dataset variables to sample, host, environment, and sequencing metadata fields.
    """
    experimental_factor = "EXPERIMENTAL_FACTOR"
    collection_date = "COLLECTION_DATE"
    broad_scale_environmental_context = "ENV_BROAD_SCALE"
    local_environmental_context = "ENV_LOCAL_SCALE"
    environmental_medium = "ENV_MEDIUM"
    depth = "DEPTH"
    water_content = "WATER_CONTENT"
    host_common_name = "HOST_COMMON_NAME"
    host_taxid = "HOST_TAXID"
    host_genotype = "HOST_GENOTYPE"
    fertilizer_regimen = "FERTILIZER_REGIMEN"
    watering_regimen = "WATERING_REGIMEN"
    chemical_administration = "CHEMICAL_ADMINISTRATION"
    perturbation = "PERTURBATION"
    season = "SEASON"
    plant_growth_medium = "PLANT_GROWTH_MEDIUM"
    sample_name = "SAMPLE_NAME"
    soil_temperature = "SOIL_TEMPERATURE"


class Keyword(str, Enum):
    """
    Keywords describing research focus areas with hierarchical organization
    """
    BIOENERGY = "BIOENERGY"
    """
    Bioenergy research focus area
    """
    FEEDSTOCK_CROP = "FEEDSTOCK_CROP"
    """
    Bioenergy feedstock crops
    """
    CARBON_AND_NUTRIENT_CYCLING = "CARBON_AND_NUTRIENT_CYCLING"
    """
    Carbon and nutrient cycling processes
    """
    SOIL_MICROBIOME = "SOIL_MICROBIOME"
    """
    Soil microbiome research
    """
    PLANT_MICROBE_INTERACTIONS = "PLANT_MICROBE_INTERACTIONS"
    """
    Plant-microbe interactions
    """
    WATERSHED_SCIENCE = "WATERSHED_SCIENCE"
    """
    Watershed and hydrology science
    """
    BIOGEOCHEMISTRY = "BIOGEOCHEMISTRY"
    """
    Biogeochemical processes
    """
    CONTAMINANT_SCIENCE = "CONTAMINANT_SCIENCE"
    """
    Contaminant fate and transport
    """
    SYNTHETIC_BIOLOGY = "SYNTHETIC_BIOLOGY"
    """
    Synthetic biology and engineering
    """
    OMICS_METHODS = "OMICS_METHODS"
    """
    Omics methods and approaches
    """
    WETLAND_SCIENCE = "WETLAND_SCIENCE"
    """
    Wetland ecosystem science
    """
    TECHNOLOGY_PLATFORM = "TECHNOLOGY_PLATFORM"
    """
    Technology platforms and tools
    """
    BIOFUELS = "BIOFUELS"
    """
    Biofuel production
    """
    BIOPRODUCTS = "BIOPRODUCTS"
    """
    Bio-based products
    """
    SUSTAINABLE_AVIATION_FUEL = "SUSTAINABLE_AVIATION_FUEL"
    """
    Sustainable aviation fuel production
    """
    LIGNOCELLULOSE = "LIGNOCELLULOSE"
    """
    Lignocellulosic biomass
    """
    CELLULOSIC_BIOMASS = "CELLULOSIC_BIOMASS"
    """
    Cellulosic biomass conversion
    """
    LIGNIN = "LIGNIN"
    """
    Lignin structure and valorization
    """
    LIGNIN_VALORIZATION = "LIGNIN_VALORIZATION"
    """
    Lignin valorization for products
    """
    BIOMASS_RECALCITRANCE = "BIOMASS_RECALCITRANCE"
    """
    Biomass recalcitrance and deconstruction
    """
    MICROBIAL_CONVERSION = "MICROBIAL_CONVERSION"
    """
    Microbial conversion of biomass
    """
    SUSTAINABILITY = "SUSTAINABILITY"
    """
    Sustainability aspects of bioenergy
    """
    MARGINAL_LANDS = "MARGINAL_LANDS"
    """
    Marginal lands for bioenergy production
    """
    LIFE_CYCLE_ASSESSMENT = "LIFE_CYCLE_ASSESSMENT"
    """
    Life cycle assessment for sustainability
    """
    IONIC_LIQUIDS = "IONIC_LIQUIDS"
    """
    Ionic liquids for biomass pretreatment
    """
    LIPID_ACCUMULATION = "LIPID_ACCUMULATION"
    """
    Lipid accumulation in plants
    """
    OIL_CROPS = "OIL_CROPS"
    """
    Oil crops for biofuel production
    """
    TERPENES = "TERPENES"
    """
    Terpene-based biofuels
    """
    FATTY_ACIDS = "FATTY_ACIDS"
    """
    Fatty acid-based biofuels
    """
    SWITCHGRASS = "SWITCHGRASS"
    """
    Panicum virgatum (switchgrass)
    """
    POPLAR = "POPLAR"
    """
    Populus species (poplar/cottonwood)
    """
    POPULUS = "POPULUS"
    """
    Populus genus
    """
    MISCANTHUS = "MISCANTHUS"
    """
    Miscanthus grass
    """
    SORGHUM = "SORGHUM"
    """
    Sorghum species
    """
    ENERGY_SORGHUM = "ENERGY_SORGHUM"
    """
    Energy sorghum varieties
    """
    SUGARCANE = "SUGARCANE"
    """
    Sugarcane
    """
    BRACHYPODIUM = "BRACHYPODIUM"
    """
    Brachypodium distachyon model grass
    """
    TALL_WHEATGRASS = "TALL_WHEATGRASS"
    """
    Tall wheatgrass
    """
    PERENNIAL_CROPS = "PERENNIAL_CROPS"
    """
    Perennial bioenergy crops
    """
    PLANT_CELL_WALLS = "PLANT_CELL_WALLS"
    """
    Plant cell wall composition and deconstruction
    """
    CARBON_CYCLING = "CARBON_CYCLING"
    """
    Carbon cycling processes
    """
    SOIL_CARBON = "SOIL_CARBON"
    """
    Soil carbon dynamics
    """
    CARBON_PERSISTENCE = "CARBON_PERSISTENCE"
    """
    Soil carbon persistence mechanisms
    """
    CARBON_FLUX = "CARBON_FLUX"
    """
    Carbon flux measurements
    """
    CARBON_USE_EFFICIENCY = "CARBON_USE_EFFICIENCY"
    """
    Carbon use efficiency in microbes
    """
    NUTRIENT_CYCLING = "NUTRIENT_CYCLING"
    """
    Nutrient cycling processes
    """
    DENITRIFICATION = "DENITRIFICATION"
    """
    Microbial denitrification
    """
    NITRATE = "NITRATE"
    """
    Nitrate cycling
    """
    DECOMPOSITION = "DECOMPOSITION"
    """
    Decomposition processes
    """
    SOIL_ORGANIC_MATTER = "SOIL_ORGANIC_MATTER"
    """
    Soil organic matter dynamics
    """
    RHIZOSPHERE = "RHIZOSPHERE"
    """
    Rhizosphere microbial communities
    """
    MICROBIAL_ECOSYSTEMS = "MICROBIAL_ECOSYSTEMS"
    """
    Microbial ecosystem dynamics
    """
    MICROBIAL_INTERACTIONS = "MICROBIAL_INTERACTIONS"
    """
    Microbial community interactions
    """
    VIROME = "VIROME"
    """
    Soil viral communities
    """
    PHAGE = "PHAGE"
    """
    Bacteriophages in soil
    """
    BACTERIAL_FUNGAL_INTERACTIONS = "BACTERIAL_FUNGAL_INTERACTIONS"
    """
    Bacterial-fungal interactions in soil
    """
    ENDOHYPHAL_BACTERIA = "ENDOHYPHAL_BACTERIA"
    """
    Bacteria living within fungal hyphae
    """
    FUNGAL_HIGHWAYS = "FUNGAL_HIGHWAYS"
    """
    Bacterial dispersal via fungal mycelial networks
    """
    SIDEROPHORES = "SIDEROPHORES"
    """
    Iron-chelating compounds mediating microbial interactions
    """
    SUBSURFACE_MICROBIOLOGY = "SUBSURFACE_MICROBIOLOGY"
    """
    Subsurface microbial communities
    """
    METAPHENOME = "METAPHENOME"
    """
    Metaphenome and community phenotypes
    """
    PLANT_PRODUCTIVITY = "PLANT_PRODUCTIVITY"
    """
    Plant productivity impacts
    """
    MOISTURE_EFFECTS = "MOISTURE_EFFECTS"
    """
    Moisture effects on microbiomes
    """
    MOISTURE_REGIMES = "MOISTURE_REGIMES"
    """
    Moisture regime effects
    """
    ENDOPHYTES = "ENDOPHYTES"
    """
    Endophytic microorganisms
    """
    MYCORRHIZAE = "MYCORRHIZAE"
    """
    Mycorrhizal associations
    """
    BIOENERGY_CROPS = "BIOENERGY_CROPS"
    """
    Plant-microbe interactions in bioenergy crops
    """
    PLANT_GROWTH_PROMOTING_BACTERIA = "PLANT_GROWTH_PROMOTING_BACTERIA"
    """
    Plant growth promoting bacteria
    """
    CO_EVOLUTION = "CO_EVOLUTION"
    """
    Co-evolution of plants and microbes
    """
    WATERSHED_HYDROLOGY = "WATERSHED_HYDROLOGY"
    """
    Watershed hydrological processes
    """
    WATERSHED_DYNAMICS = "WATERSHED_DYNAMICS"
    """
    Watershed dynamics and evolution
    """
    MOUNTAIN_HYDROLOGY = "MOUNTAIN_HYDROLOGY"
    """
    Mountain watershed hydrology
    """
    HYDROLOGIC_CONNECTIVITY = "HYDROLOGIC_CONNECTIVITY"
    """
    Hydrological connectivity
    """
    SNOWMELT = "SNOWMELT"
    """
    Snowmelt hydrology
    """
    DROUGHT = "DROUGHT"
    """
    Drought impacts
    """
    STREAM_NETWORKS = "STREAM_NETWORKS"
    """
    Stream network structure and function
    """
    RIVER_CORRIDORS = "RIVER_CORRIDORS"
    """
    River corridor processes
    """
    GROUNDWATER_QUALITY = "GROUNDWATER_QUALITY"
    """
    Groundwater quality
    """
    UPPER_COLORADO_RIVER_BASIN = "UPPER_COLORADO_RIVER_BASIN"
    """
    Upper Colorado River Basin study site
    """
    TENNESSEE_RIVER_BASIN = "TENNESSEE_RIVER_BASIN"
    """
    Tennessee River Basin study site
    """
    YAKIMA_RIVER_BASIN = "YAKIMA_RIVER_BASIN"
    """
    Yakima River Basin study site
    """
    LAND_COVER = "LAND_COVER"
    """
    Land cover effects on watersheds
    """
    WILDFIRE = "WILDFIRE"
    """
    Wildfire impacts on watersheds
    """
    STREAM_DRYING = "STREAM_DRYING"
    """
    Stream drying processes
    """
    HYDRO_BIOGEOCHEMISTRY = "HYDRO_BIOGEOCHEMISTRY"
    """
    Hydro-biogeochemical processes
    """
    SEDIMENT_WATER_INTERFACE = "SEDIMENT_WATER_INTERFACE"
    """
    Sediment-water interface processes
    """
    SUBSURFACE_INTERFACES = "SUBSURFACE_INTERFACES"
    """
    Subsurface interface processes
    """
    REDOX_CYCLING = "REDOX_CYCLING"
    """
    Redox cycling processes
    """
    METAL_REDUCTION = "METAL_REDUCTION"
    """
    Microbial metal reduction
    """
    INTERFACES = "INTERFACES"
    """
    Interface-mediated processes
    """
    MERCURY = "MERCURY"
    """
    Mercury contamination and cycling
    """
    METHYLMERCURY = "METHYLMERCURY"
    """
    Mercury methylation
    """
    MERCURY_METHYLATION = "MERCURY_METHYLATION"
    """
    Mercury methylation processes
    """
    HGCA = "HGCA"
    """
    hgcA gene for mercury methylation
    """
    HGCB = "HGCB"
    """
    hgcB gene for mercury methylation
    """
    URANIUM = "URANIUM"
    """
    Uranium contamination
    """
    ACTINIDES = "ACTINIDES"
    """
    Actinide behavior
    """
    CONTAMINANT_TRANSPORT = "CONTAMINANT_TRANSPORT"
    """
    Contaminant transport processes
    """
    COLLOID_TRANSPORT = "COLLOID_TRANSPORT"
    """
    Colloid-facilitated transport
    """
    METABOLIC_ENGINEERING = "METABOLIC_ENGINEERING"
    """
    Metabolic engineering approaches
    """
    GENOME_ENGINEERING = "GENOME_ENGINEERING"
    """
    Genome engineering technologies
    """
    CRISPR = "CRISPR"
    """
    CRISPR-based gene editing
    """
    GENOMIC_SELECTION = "GENOMIC_SELECTION"
    """
    Genomic selection methods
    """
    MICROBIAL_CHASSIS = "MICROBIAL_CHASSIS"
    """
    Microbial chassis organisms
    """
    SHEWANELLA = "SHEWANELLA"
    """
    Shewanella as chassis organism
    """
    BIOCONTAINMENT = "BIOCONTAINMENT"
    """
    Biocontainment strategies
    """
    BIOSECURITY = "BIOSECURITY"
    """
    Biosecurity considerations
    """
    BIODEFENSE = "BIODEFENSE"
    """
    Biodefense applications
    """
    BIOSYSTEMS_DESIGN = "BIOSYSTEMS_DESIGN"
    """
    Biosystems design approaches
    """
    ECOSYSTEM_ENGINEERING = "ECOSYSTEM_ENGINEERING"
    """
    Ecosystem engineering
    """
    MICROBIAL_INVASION = "MICROBIAL_INVASION"
    """
    Microbial invasion dynamics
    """
    FUNGAL_PATHOGENS = "FUNGAL_PATHOGENS"
    """
    Fungal pathogens
    """
    SYSTEMS_BIOLOGY = "SYSTEMS_BIOLOGY"
    """
    Systems biology approaches
    """
    MACHINE_LEARNING = "MACHINE_LEARNING"
    """
    Machine learning for biological design
    """
    DNA_BARCODING = "DNA_BARCODING"
    """
    DNA barcoding for tracking
    """
    COMBIGEM = "COMBIGEM"
    """
    CombiGEM combinatorial engineering
    """
    METAGENOMICS = "METAGENOMICS"
    """
    Metagenomic approaches
    """
    STABLE_ISOTOPES = "STABLE_ISOTOPES"
    """
    Stable isotope approaches
    """
    QSIP = "QSIP"
    """
    Quantitative stable isotope probing
    """
    NANOSIMS = "NANOSIMS"
    """
    NanoSIMS imaging
    """
    MODEX = "MODEX"
    """
    Model-experiment integration
    """
    WHONDRS = "WHONDRS"
    """
    WHONDRS consortium
    """
    WETLAND_BIOGEOCHEMISTRY = "WETLAND_BIOGEOCHEMISTRY"
    """
    Wetland biogeochemistry
    """
    WETLAND_RESILIENCE = "WETLAND_RESILIENCE"
    """
    Wetland resilience
    """
    RIPARIAN_WETLAND = "RIPARIAN_WETLAND"
    """
    Riparian wetland ecosystems
    """
    FLOODPLAIN = "FLOODPLAIN"
    """
    Floodplain ecosystems
    """
    CAPILLARY_FRINGE = "CAPILLARY_FRINGE"
    """
    Capillary fringe processes
    """
    SAVANNAH_RIVER_SITE = "SAVANNAH_RIVER_SITE"
    """
    Savannah River Site study location
    """
    ENVIRONMENTAL_CHANGE = "ENVIRONMENTAL_CHANGE"
    """
    Environmental change impacts
    """
    ENVIRONMENTAL_SYSTEMS = "ENVIRONMENTAL_SYSTEMS"
    """
    Environmental systems
    """
    FABRICATED_ECOSYSTEMS = "FABRICATED_ECOSYSTEMS"
    """
    Fabricated ecosystem platforms
    """
    ECOFAB = "ECOFAB"
    """
    EcoFAB platform
    """
    LONG_TERM_ECOLOGICAL_RESEARCH = "LONG_TERM_ECOLOGICAL_RESEARCH"
    """
    Long-term ecological research sites (e.g., LTER network)
    """


class CapabilityType(str, Enum):
    """
    Types of scientific capabilities provided by user facilities
    """
    SEQUENCING = "SEQUENCING"
    """
    DNA/RNA sequencing capabilities
    """
    SYNTHESIS = "SYNTHESIS"
    """
    DNA/protein synthesis capabilities
    """
    MASS_SPECTROMETRY = "MASS_SPECTROMETRY"
    """
    Mass spectrometry capabilities
    """
    NMR = "NMR"
    """
    Nuclear magnetic resonance capabilities
    """
    IMAGING = "IMAGING"
    """
    Imaging and microscopy capabilities
    """
    PHENOTYPING = "PHENOTYPING"
    """
    Phenotyping and functional characterization
    """
    COMPUTATIONAL = "COMPUTATIONAL"
    """
    Computational and data analysis capabilities
    """
    SAMPLE_PREPARATION = "SAMPLE_PREPARATION"
    """
    Sample preparation and processing
    """
    SHORT_READ_SEQUENCING = "SHORT_READ_SEQUENCING"
    """
    Short-read sequencing (Illumina, etc.)
    """
    LONG_READ_SEQUENCING = "LONG_READ_SEQUENCING"
    """
    Long-read sequencing (PacBio, Oxford Nanopore)
    """
    SINGLE_CELL_SEQUENCING = "SINGLE_CELL_SEQUENCING"
    """
    Single-cell genomics and transcriptomics
    """
    METAGENOME_SEQUENCING = "METAGENOME_SEQUENCING"
    """
    Metagenomic sequencing
    """
    RNASEQ = "RNASEQ"
    """
    RNA sequencing and transcriptomics
    """
    DNA_SYNTHESIS = "DNA_SYNTHESIS"
    """
    DNA synthesis and assembly
    """
    GENE_SYNTHESIS = "GENE_SYNTHESIS"
    """
    Gene synthesis
    """
    PATHWAY_SYNTHESIS = "PATHWAY_SYNTHESIS"
    """
    Pathway and construct synthesis
    """
    PROTEIN_EXPRESSION = "PROTEIN_EXPRESSION"
    """
    Protein expression systems
    """
    METABOLOMICS_MS = "METABOLOMICS_MS"
    """
    Mass spectrometry for metabolomics
    """
    PROTEOMICS_MS = "PROTEOMICS_MS"
    """
    Mass spectrometry for proteomics
    """
    LIPIDOMICS_MS = "LIPIDOMICS_MS"
    """
    Mass spectrometry for lipidomics
    """
    NATIVE_MS = "NATIVE_MS"
    """
    Native mass spectrometry for intact complexes
    """
    MS_IMAGING = "MS_IMAGING"
    """
    Mass spectrometry imaging
    """
    GC_MS = "GC_MS"
    """
    Gas chromatography-mass spectrometry
    """
    LC_MS = "LC_MS"
    """
    Liquid chromatography-mass spectrometry
    """
    FTICR_MS = "FTICR_MS"
    """
    Fourier-transform ion cyclotron resonance MS
    """
    LIQUID_STATE_NMR = "LIQUID_STATE_NMR"
    """
    Liquid-state NMR spectroscopy
    """
    SOLID_STATE_NMR = "SOLID_STATE_NMR"
    """
    Solid-state NMR spectroscopy
    """
    METABOLOMICS_NMR = "METABOLOMICS_NMR"
    """
    NMR for metabolomics
    """
    CRYO_EM = "CRYO_EM"
    """
    Cryogenic electron microscopy
    """
    CRYO_ET = "CRYO_ET"
    """
    Cryogenic electron tomography
    """
    CRYO_FIB_SEM = "CRYO_FIB_SEM"
    """
    Cryogenic focused ion beam-SEM
    """
    LIGHT_MICROSCOPY = "LIGHT_MICROSCOPY"
    """
    Light and fluorescence microscopy
    """
    SUPER_RESOLUTION_MICROSCOPY = "SUPER_RESOLUTION_MICROSCOPY"
    """
    Super-resolution microscopy
    """
    CHEMICAL_IMAGING = "CHEMICAL_IMAGING"
    """
    Chemical imaging methods
    """
    NANOSIMS_IMAGING = "NANOSIMS_IMAGING"
    """
    NanoSIMS imaging
    """
    SYNCHROTRON_IMAGING = "SYNCHROTRON_IMAGING"
    """
    Synchrotron-based imaging
    """
    MICROBIAL_PHENOTYPING = "MICROBIAL_PHENOTYPING"
    """
    Microbial phenotyping platforms
    """
    ANAEROBIC_PHENOTYPING = "ANAEROBIC_PHENOTYPING"
    """
    Anaerobic microbial phenotyping (AMP2)
    """
    HIGH_THROUGHPUT_PHENOTYPING = "HIGH_THROUGHPUT_PHENOTYPING"
    """
    High-throughput phenotyping
    """
    GROWTH_PHENOTYPING = "GROWTH_PHENOTYPING"
    """
    Growth and fitness phenotyping
    """
    FLOW_CYTOMETRY = "FLOW_CYTOMETRY"
    """
    Flow cytometry analysis
    """
    GENOME_ANNOTATION = "GENOME_ANNOTATION"
    """
    Genome annotation services
    """
    METABOLIC_MODELING = "METABOLIC_MODELING"
    """
    Metabolic modeling and simulation
    """
    METAGENOME_ANALYSIS = "METAGENOME_ANALYSIS"
    """
    Metagenome analysis pipelines
    """
    AI_ML_ANALYSIS = "AI_ML_ANALYSIS"
    """
    AI/ML-based analysis
    """
    HIGH_PERFORMANCE_COMPUTING = "HIGH_PERFORMANCE_COMPUTING"
    """
    High-performance computing resources
    """


class CapabilityStatus(str, Enum):
    """
    Operational status of a capability
    """
    OPERATIONAL = "OPERATIONAL"
    """
    Fully operational and available to users
    """
    COMING_ONLINE = "COMING_ONLINE"
    """
    Being commissioned, coming online soon
    """
    PILOT = "PILOT"
    """
    In pilot phase with limited access
    """
    UNDER_DEVELOPMENT = "UNDER_DEVELOPMENT"
    """
    Under development, not yet available
    """
    DECOMMISSIONED = "DECOMMISSIONED"
    """
    No longer available
    """


class InstrumentType(str, Enum):
    """
    Types of scientific instruments
    """
    ILLUMINA_SEQUENCER = "ILLUMINA_SEQUENCER"
    """
    Illumina short-read sequencer
    """
    PACBIO_SEQUENCER = "PACBIO_SEQUENCER"
    """
    PacBio long-read sequencer
    """
    OXFORD_NANOPORE = "OXFORD_NANOPORE"
    """
    Oxford Nanopore sequencer
    """
    ORBITRAP = "ORBITRAP"
    """
    Orbitrap mass spectrometer
    """
    TRIPLE_QUADRUPOLE = "TRIPLE_QUADRUPOLE"
    """
    Triple quadrupole mass spectrometer
    """
    FTICR = "FTICR"
    """
    Fourier-transform ion cyclotron resonance MS
    """
    TOF = "TOF"
    """
    Time-of-flight mass spectrometer
    """
    NMR_SPECTROMETER = "NMR_SPECTROMETER"
    """
    NMR spectrometer
    """
    CRYO_TEM = "CRYO_TEM"
    """
    Cryogenic transmission electron microscope
    """
    CRYO_SEM = "CRYO_SEM"
    """
    Cryogenic scanning electron microscope
    """
    FIB_SEM = "FIB_SEM"
    """
    Focused ion beam-SEM
    """
    FLOW_CYTOMETER = "FLOW_CYTOMETER"
    """
    Flow cytometer
    """
    LIQUID_HANDLER = "LIQUID_HANDLER"
    """
    Automated liquid handler
    """
    PLATE_READER = "PLATE_READER"
    """
    Microplate reader
    """
    HPLC = "HPLC"
    """
    High-performance liquid chromatography
    """
    GC = "GC"
    """
    Gas chromatograph
    """
    ANAEROBIC_CHAMBER = "ANAEROBIC_CHAMBER"
    """
    Anaerobic chamber or glove box
    """
    INCUBATOR = "INCUBATOR"
    """
    Microbial cultivation incubator
    """
    ELECTROPORATOR = "ELECTROPORATOR"
    """
    Electroporation device for cell transformation
    """


class AnalysisType(str, Enum):
    """
    Types of computational analyses
    """
    KBASE_NARRATIVE = "KBASE_NARRATIVE"
    """
    KBase reproducible analysis workflow - a Jupyter-like notebook combining data, analysis steps, and documentation
    """
    NMDC_WORKFLOW = "NMDC_WORKFLOW"
    """
    NMDC standardized bioinformatics workflow (e.g., metagenome annotation, MAG assembly)
    """
    CUSTOM_PIPELINE = "CUSTOM_PIPELINE"
    """
    Custom analysis pipeline not in KBase or NMDC
    """


class KBaseCollection(str, Enum):
    """
    Available KBase genome collections (as of 2024). Collections are curated datasets searchable by sequence similarity, taxonomy (GTDB), and functional traits (microTrait).
    """
    GTDB = "GTDB"
    """
    Genome Taxonomy Database reference collection - standardized microbial taxonomy based on genome phylogeny
    """
    ENIGMA = "ENIGMA"
    """
    ENIGMA SFA subsurface microbiome genomes from Oak Ridge Reservation contaminated site studies
    """
    PMI = "PMI"
    """
    Plant Microbe Interfaces SFA rhizosphere genomes - plant-host associated microbial genomes showing Populus rhizosphere diversity
    """
    GROW = "GROW"
    """
    Genome Resolved Open Watersheds (GROWdb) river microbiome MAGs from WHONDRS worldwide river sampling
    """


class NMDCIngestPriority(str, Enum):
    """
    Priority level for considering a study/dataset for NMDC ingest. Used to help prioritize which external datasets should be targeted for ingestion into the National Microbiome Data Collaborative.
    """
    HIGH = "HIGH"
    """
    High priority - dataset has rich microbiome data (metagenomes, amplicon sequences) with good metadata, ready for NMDC processing. Should be prioritized for ingest.
    """
    MEDIUM = "MEDIUM"
    """
    Medium priority - dataset has relevant microbiome data but may need metadata enrichment or format conversion before ingest.
    """
    LOW = "LOW"
    """
    Low priority - dataset has some microbiome relevance but is either small, has limited metadata, or is a marginal candidate.
    """


class ResourceType(str, Enum):
    """
    Coarse type of a research resource, used as a discriminator on the ResearchResource class. Lets the catalog represent isolate collections, mutant libraries, phage banks, knowledgebases, and similar large-grain reagent or data resources without proliferating subclasses.
    """
    ISOLATE_COLLECTION = "ISOLATE_COLLECTION"
    """
    A collection of cultured microbial isolates.
    """
    MUTANT_LIBRARY = "MUTANT_LIBRARY"
    """
    A pooled mutant library, e.g. a randomly-barcoded transposon (RB-TnSeq) insertion library or a CRISPRi library.
    """
    PHAGE_BANK = "PHAGE_BANK"
    """
    A collection of bacteriophage isolates maintained as a reagent bank.
    """
    REFERENCE_GENOME_SET = "REFERENCE_GENOME_SET"
    """
    A curated set of reference genomes maintained by a program.
    """
    PLASMID_COLLECTION = "PLASMID_COLLECTION"
    """
    A collection of plasmids or other genetic constructs.
    """
    SYNTHETIC_COMMUNITY = "SYNTHETIC_COMMUNITY"
    """
    A defined synthetic microbial community maintained as a reagent.
    """
    ORGANISM_PANEL = "ORGANISM_PANEL"
    """
    A defined set of organisms used as an experimental factor across one or more studies (e.g., the LBNL Fitness Browser organism set).
    """
    CONDITION_PANEL = "CONDITION_PANEL"
    """
    A defined set of growth conditions, media, stressors, or selective agents used as an experimental factor across one or more studies.
    """
    KNOWLEDGEBASE = "KNOWLEDGEBASE"
    """
    A versioned data resource or knowledgebase produced and maintained by the program (e.g., the LBNL Fitness Browser, the Phage Foundry Knowledge-Base).
    """
    SOFTWARE = "SOFTWARE"
    """
    A software tool or pipeline produced as a research resource.
    """
    OTHER = "OTHER"
    """
    A research resource not covered by the above categories.
    """


class OrganismType(str, Enum):
    """
    Types of organisms in a microbial isolate collection. Used to characterize the taxonomic breadth of culture collections maintained by research programs.
    """
    BACTERIA = "BACTERIA"
    """
    Bacterial isolates
    """
    ARCHAEA = "ARCHAEA"
    """
    Archaeal isolates
    """
    FUNGI = "FUNGI"
    """
    Fungal isolates including yeasts and filamentous fungi
    """
    PHAGE = "PHAGE"
    """
    Bacteriophages and archaeal viruses
    """
    OTHER_VIRUS = "OTHER_VIRUS"
    """
    Other viruses (not phage)
    """
    PROTIST = "PROTIST"
    """
    Protist/microeukaryote isolates
    """
    MICROALGAE = "MICROALGAE"
    """
    Microalgae isolates
    """


class PhenotypeAssayType(str, Enum):
    """
    Types of phenotype assays performed by research programs. Used to catalog what phenotyping capabilities and data types each SFA/BRC generates.
    """
    GROWTH_CURVES = "GROWTH_CURVES"
    """
    Growth rate measurements in liquid culture
    """
    BIOLOG_PHENOTYPING = "BIOLOG_PHENOTYPING"
    """
    Biolog plate carbon/nitrogen source utilization profiling
    """
    ANAEROBIC_GROWTH = "ANAEROBIC_GROWTH"
    """
    Growth characterization under anaerobic conditions
    """
    STRESS_TOLERANCE = "STRESS_TOLERANCE"
    """
    Growth under stress conditions (pH, temperature, osmotic, metal)
    """
    ANTIBIOTIC_RESISTANCE = "ANTIBIOTIC_RESISTANCE"
    """
    Antibiotic susceptibility/resistance profiling
    """
    RBTSEQ_FITNESS = "RBTSEQ_FITNESS"
    """
    Random barcode transposon sequencing (RB-TnSeq) for genome-wide fitness profiling across conditions
    """
    TRANSPOSON_MUTAGENESIS = "TRANSPOSON_MUTAGENESIS"
    """
    Transposon insertion sequencing for gene essentiality/fitness
    """
    CRISPR_SCREENS = "CRISPR_SCREENS"
    """
    CRISPR-based genetic screens (CRISPRi, knockout libraries)
    """
    TNSEQ = "TNSEQ"
    """
    Transposon sequencing for fitness profiling
    """
    COCULTURE_INTERACTIONS = "COCULTURE_INTERACTIONS"
    """
    Pairwise or multi-species co-culture interaction assays
    """
    BACTERIAL_FUNGAL_INTERACTION_ASSAY = "BACTERIAL_FUNGAL_INTERACTION_ASSAY"
    """
    Bacterial-fungal co-culture or proximity interaction assays
    """
    FUNGAL_HIGHWAY_ASSAY = "FUNGAL_HIGHWAY_ASSAY"
    """
    Fungal highway column assays for bacterial dispersal via mycelia
    """
    ENDOHYPHAL_SCREENING = "ENDOHYPHAL_SCREENING"
    """
    Screening for endohyphal bacteria within fungal isolates
    """
    INTERNALIZATION_ASSAY = "INTERNALIZATION_ASSAY"
    """
    In vitro bacterial internalization into fungal cells
    """
    SIDEROPHORE_ASSAY = "SIDEROPHORE_ASSAY"
    """
    Siderophore production and iron chelation assays
    """
    PLANT_COLONIZATION = "PLANT_COLONIZATION"
    """
    Plant root or leaf colonization assays
    """
    PHAGE_HOST_RANGE = "PHAGE_HOST_RANGE"
    """
    Phage-host infection range and specificity testing
    """
    SYNTHETIC_COMMUNITY = "SYNTHETIC_COMMUNITY"
    """
    Defined synthetic community assembly and dynamics
    """
    COMPETITION_ASSAYS = "COMPETITION_ASSAYS"
    """
    Competitive fitness assays between strains
    """
    EXOMETABOLOMICS = "EXOMETABOLOMICS"
    """
    Extracellular metabolite profiling (spent media analysis)
    """
    ENZYME_ACTIVITY_ASSAY = "ENZYME_ACTIVITY_ASSAY"
    """
    Enzyme activity measurements
    """
    SUBSTRATE_UTILIZATION = "SUBSTRATE_UTILIZATION"
    """
    Carbon/nitrogen substrate utilization profiling
    """
    METABOLIC_FLUX = "METABOLIC_FLUX"
    """
    Metabolic flux analysis (13C labeling)
    """
    RESPIRATION = "RESPIRATION"
    """
    Respiration rate measurements (O2 consumption, CO2 production)
    """
    LIVE_CELL_IMAGING = "LIVE_CELL_IMAGING"
    """
    Time-lapse microscopy of live cells
    """
    FLOW_CYTOMETRY_PHENOTYPING = "FLOW_CYTOMETRY_PHENOTYPING"
    """
    Single-cell phenotyping via flow cytometry
    """
    NANOSIMS_ACTIVITY = "NANOSIMS_ACTIVITY"
    """
    NanoSIMS stable isotope incorporation for activity measurement
    """
    CELL_MORPHOLOGY = "CELL_MORPHOLOGY"
    """
    Cell morphology and size measurements
    """
    BIOFILM_ASSAYS = "BIOFILM_ASSAYS"
    """
    Biofilm formation and structure assays
    """
    SOIL_INCUBATION = "SOIL_INCUBATION"
    """
    Soil microcosm incubation experiments
    """
    QSIP_ACTIVITY = "QSIP_ACTIVITY"
    """
    Quantitative stable isotope probing for in-situ activity
    """
    ECOFAB_PHENOTYPING = "ECOFAB_PHENOTYPING"
    """
    EcoFAB fabricated ecosystem phenotyping
    """


class InteractionType(str, Enum):
    """
    Types of bacterial-fungal interactions based on ecological outcome
    """
    MUTUALISM = "MUTUALISM"
    """
    Win-win interaction where bacteria and fungi achieve functional complementarity through resource sharing (e.g., mycorrhizal symbiosis, lichen symbiosis)
    """
    ANTAGONISM = "ANTAGONISM"
    """
    Reciprocal inhibition including pathogen infection, antibiotic production, and biological control mechanisms
    """
    COMPETITION = "COMPETITION"
    """
    Resource and spatial rivalry maintaining community stability through niche differentiation (e.g., iron, biotin, adhesion sites)
    """
    COMMENSALISM = "COMMENSALISM"
    """
    Interaction where one partner benefits while the other is unaffected
    """
    PARASITISM = "PARASITISM"
    """
    Interaction where one partner benefits at the expense of the other
    """
    ENDOSYMBIOSIS = "ENDOSYMBIOSIS"
    """
    Obligate or facultative intracellular association where bacteria live within fungal cells (endohyphal bacteria)
    """


class InteractionMode(str, Enum):
    """
    Physical or chemical mode of bacterial-fungal interaction
    """
    PHYSICAL_ATTACHMENT = "PHYSICAL_ATTACHMENT"
    """
    External attachment of bacteria to fungal surfaces (hyphae, spores)
    """
    ENDOHYPHAL = "ENDOHYPHAL"
    """
    Bacteria residing within fungal hyphae
    """
    BIOFILM_FORMATION = "BIOFILM_FORMATION"
    """
    Biofilm formation on fungal structures
    """
    FUNGAL_HIGHWAY = "FUNGAL_HIGHWAY"
    """
    Bacterial dispersal using fungal mycelia as transport networks
    """
    QUORUM_SENSING = "QUORUM_SENSING"
    """
    Chemical signaling via quorum sensing molecules
    """
    VOLATILE_METABOLITES = "VOLATILE_METABOLITES"
    """
    Interaction mediated by volatile organic compounds
    """
    SIDEROPHORE_MEDIATED = "SIDEROPHORE_MEDIATED"
    """
    Iron competition via siderophore production
    """
    ANTIBIOTIC_PRODUCTION = "ANTIBIOTIC_PRODUCTION"
    """
    Interaction mediated by antibiotic secretion
    """
    NUTRIENT_EXCHANGE = "NUTRIENT_EXCHANGE"
    """
    Metabolite exchange including carbon, nitrogen, vitamins
    """
    CHEMOTAXIS = "CHEMOTAXIS"
    """
    Directed movement in response to chemical gradients
    """



class ResearchProgramCollection(ConfiguredBaseModel):
    """
    A container for DOE BER funded research programs including Bioenergy Research Centers (BRCs), Scientific Focus Areas (SFAs), and User Facilities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs', 'tree_root': True})

    bioenergy_research_centers: Optional[list[BioenergyResearchCenter]] = Field(default=[], description="""Collection of DOE Bioenergy Research Centers""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    genomic_science_sfas: Optional[list[ScientificFocusArea]] = Field(default=[], description="""Collection of Genomic Science Program Scientific Focus Areas""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    environmental_system_science_sfas: Optional[list[ScientificFocusArea]] = Field(default=[], description="""Collection of Environmental System Science Scientific Focus Areas""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    user_facilities: Optional[list[UserFacility]] = Field(default=[], description="""Collection of DOE BER User Facilities""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    other_programs: Optional[list[OtherProgram]] = Field(default=[], description="""Other DOE research programs and initiatives that don't fit the traditional SFA/BRC/Facility categories (e.g., BRaVE, cross-cutting initiatives, time-limited projects)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    ai_projects: Optional[list[ArtificialIntelligenceProject]] = Field(default=[], description="""DOE artificial intelligence pilot projects and related AI-enabled science initiatives, including BER/ASCR-supported projects.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    sites: Optional[list[FieldSite]] = Field(default=[], description="""Canonical collection of field sites referenced by programs and studies. Sites are modeled once here and linked by identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })
    metadata: Optional[CollectionMetadata] = Field(default=None, description="""Metadata about this collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgramCollection']} })


class CollectionMetadata(ConfiguredBaseModel):
    """
    Metadata about the research program collection
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    compiled_date: Optional[str] = Field(default=None, description="""Date this collection was compiled (ISO 8601 format)""", json_schema_extra = { "linkml_meta": {'domain_of': ['CollectionMetadata']} })
    sources: Optional[list[str]] = Field(default=[], description="""Sources used to compile this collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['CollectionMetadata']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes about the collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['CollectionMetadata', 'Variable', 'StudyDesign']} })


class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'schema:Thing',
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    id: str = Field(default=..., description="""A unique identifier for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class ResearchProgram(NamedThing):
    """
    A DOE BER funded research program. This is the common parent class for Bioenergy Research Centers (BRCs) and Scientific Focus Areas (SFAs). Both program types share common attributes including funding, institutions, personnel, research focus, and outputs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'id': {'description': 'A unique identifier for the research '
                                              'program (e.g., nmdc_sfas_brcs:glbrc)',
                               'name': 'id',
                               'pattern': '^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$'},
                        'name': {'description': 'The full official name of the '
                                                'research program',
                                 'name': 'name',
                                 'required': True}}})

    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=None, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    partner_institutions: Optional[list[str]] = Field(default=[], description="""Partner institutions participating in the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    principal_investigators: Optional[list[Person]] = Field(default=[], description="""Principal investigators leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    location: Optional[Location] = Field(default=None, description="""Geographic location of the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    scientific_questions: Optional[list[str]] = Field(default=[], description="""Key scientific questions addressed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data collected or generated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    data_collection_modalities: Optional[list[DataCollectionModality]] = Field(default=[], description="""Methods and modalities used for data collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    nmdc_umbrella_study: Optional[str] = Field(default=None, description="""The NMDC umbrella study identifier for this research program. This is the top-level study that child studies link to via part_of.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    studies: Optional[list[NMDCStudyReference]] = Field(default=[], description="""NMDC studies associated with this research program. These are individual research studies that are part of the program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    analyses: Optional[list[KBaseNarrative]] = Field(default=[], description="""Computational analyses associated with this research program, including KBase narratives and other workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    kbase_genome_collection: Optional[KBaseCollection] = Field(default=None, description="""If this program has a curated genome collection in KBase Collections (e.g., ENIGMA, PMI, GROW), the collection identifier. Collections are searchable curated datasets with GTDB taxonomy and microTrait annotations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    datasets: Optional[list[Dataset]] = Field(default=[], description="""Datasets produced by or associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    key_publications: Optional[list[Reference]] = Field(default=[], description="""Key publications from the program with their findings""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    established: Optional[int] = Field(default=None, description="""Year the program was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    collaborators: Optional[str] = Field(default=None, description="""Description of collaborators""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    isolate_collections: Optional[list[IsolateCollection]] = Field(default=[], description="""Microbial isolate collections maintained by this research program. Provides catalog-level information about available cultures and genomes. For new entries that are not isolate collections (mutant libraries, phage banks, knowledgebases, reference genome sets), use research_resources instead. Both slots reference subtypes of ResearchResource, so a single query against the class hierarchy returns every resource a program maintains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    phenotype_assays: Optional[list[PhenotypeAssayType]] = Field(default=[], description="""Types of phenotype assays performed by this research program. Catalogs the phenotyping capabilities and data types generated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    id: str = Field(default=..., description="""A unique identifier for the research program (e.g., nmdc_sfas_brcs:glbrc)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The full official name of the research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })

    @field_validator('nmdc_umbrella_study')
    def pattern_nmdc_umbrella_study(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_umbrella_study format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_umbrella_study format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class BioenergyResearchCenter(ResearchProgram):
    """
    A DOE Bioenergy Research Center (BRC). BRCs are large-scale, multi-institutional research centers focused on developing sustainable biofuels and bioproducts from plant biomass. The BRC program is part of the Genomic Science portfolio within DOE's Office of Science Office of Biological and Environmental Research.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'OBI:0000835',
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'program_type': {'ifabsent': 'string(BIOENERGY_RESEARCH_CENTER)',
                                         'name': 'program_type'}}})

    outputs: Optional[ProgramOutputs] = Field(default=None, description="""Summary of program outputs""", json_schema_extra = { "linkml_meta": {'domain_of': ['BioenergyResearchCenter']} })
    predecessor: Optional[str] = Field(default=None, description="""Predecessor program that this program builds upon""", json_schema_extra = { "linkml_meta": {'domain_of': ['BioenergyResearchCenter']} })
    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=ProgramType.BIOENERGY_RESEARCH_CENTER, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'ifabsent': 'string(BIOENERGY_RESEARCH_CENTER)'} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    partner_institutions: Optional[list[str]] = Field(default=[], description="""Partner institutions participating in the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    principal_investigators: Optional[list[Person]] = Field(default=[], description="""Principal investigators leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    location: Optional[Location] = Field(default=None, description="""Geographic location of the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    scientific_questions: Optional[list[str]] = Field(default=[], description="""Key scientific questions addressed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data collected or generated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    data_collection_modalities: Optional[list[DataCollectionModality]] = Field(default=[], description="""Methods and modalities used for data collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    nmdc_umbrella_study: Optional[str] = Field(default=None, description="""The NMDC umbrella study identifier for this research program. This is the top-level study that child studies link to via part_of.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    studies: Optional[list[NMDCStudyReference]] = Field(default=[], description="""NMDC studies associated with this research program. These are individual research studies that are part of the program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    analyses: Optional[list[KBaseNarrative]] = Field(default=[], description="""Computational analyses associated with this research program, including KBase narratives and other workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    kbase_genome_collection: Optional[KBaseCollection] = Field(default=None, description="""If this program has a curated genome collection in KBase Collections (e.g., ENIGMA, PMI, GROW), the collection identifier. Collections are searchable curated datasets with GTDB taxonomy and microTrait annotations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    datasets: Optional[list[Dataset]] = Field(default=[], description="""Datasets produced by or associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    key_publications: Optional[list[Reference]] = Field(default=[], description="""Key publications from the program with their findings""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    established: Optional[int] = Field(default=None, description="""Year the program was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    collaborators: Optional[str] = Field(default=None, description="""Description of collaborators""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    isolate_collections: Optional[list[IsolateCollection]] = Field(default=[], description="""Microbial isolate collections maintained by this research program. Provides catalog-level information about available cultures and genomes. For new entries that are not isolate collections (mutant libraries, phage banks, knowledgebases, reference genome sets), use research_resources instead. Both slots reference subtypes of ResearchResource, so a single query against the class hierarchy returns every resource a program maintains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    phenotype_assays: Optional[list[PhenotypeAssayType]] = Field(default=[], description="""Types of phenotype assays performed by this research program. Catalogs the phenotyping capabilities and data types generated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    id: str = Field(default=..., description="""A unique identifier for the research program (e.g., nmdc_sfas_brcs:glbrc)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The full official name of the research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })

    @field_validator('nmdc_umbrella_study')
    def pattern_nmdc_umbrella_study(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_umbrella_study format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_umbrella_study format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ScientificFocusArea(ResearchProgram):
    """
    A DOE Scientific Focus Area (SFA). SFAs are integrated research programs at DOE national laboratories focused on specific scientific areas within BER's portfolio. SFAs conduct coordinated, team-oriented research taking advantage of national laboratory strengths.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'program_type': {'ifabsent': 'string(SCIENTIFIC_FOCUS_AREA)',
                                         'name': 'program_type'}}})

    sfa_type: Optional[SFAType] = Field(default=None, description="""The specific type of Scientific Focus Area""", json_schema_extra = { "linkml_meta": {'domain_of': ['ScientificFocusArea']} })
    technologies_developed: Optional[list[Technology]] = Field(default=[], description="""Technologies or tools developed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ScientificFocusArea']} })
    co_investigators: Optional[list[Person]] = Field(default=[], description="""Co-investigators on the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ScientificFocusArea']} })
    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=ProgramType.SCIENTIFIC_FOCUS_AREA, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'ifabsent': 'string(SCIENTIFIC_FOCUS_AREA)'} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    partner_institutions: Optional[list[str]] = Field(default=[], description="""Partner institutions participating in the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    principal_investigators: Optional[list[Person]] = Field(default=[], description="""Principal investigators leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    location: Optional[Location] = Field(default=None, description="""Geographic location of the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    scientific_questions: Optional[list[str]] = Field(default=[], description="""Key scientific questions addressed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data collected or generated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    data_collection_modalities: Optional[list[DataCollectionModality]] = Field(default=[], description="""Methods and modalities used for data collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    nmdc_umbrella_study: Optional[str] = Field(default=None, description="""The NMDC umbrella study identifier for this research program. This is the top-level study that child studies link to via part_of.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    studies: Optional[list[NMDCStudyReference]] = Field(default=[], description="""NMDC studies associated with this research program. These are individual research studies that are part of the program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    analyses: Optional[list[KBaseNarrative]] = Field(default=[], description="""Computational analyses associated with this research program, including KBase narratives and other workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    kbase_genome_collection: Optional[KBaseCollection] = Field(default=None, description="""If this program has a curated genome collection in KBase Collections (e.g., ENIGMA, PMI, GROW), the collection identifier. Collections are searchable curated datasets with GTDB taxonomy and microTrait annotations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    datasets: Optional[list[Dataset]] = Field(default=[], description="""Datasets produced by or associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    key_publications: Optional[list[Reference]] = Field(default=[], description="""Key publications from the program with their findings""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    established: Optional[int] = Field(default=None, description="""Year the program was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    collaborators: Optional[str] = Field(default=None, description="""Description of collaborators""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    isolate_collections: Optional[list[IsolateCollection]] = Field(default=[], description="""Microbial isolate collections maintained by this research program. Provides catalog-level information about available cultures and genomes. For new entries that are not isolate collections (mutant libraries, phage banks, knowledgebases, reference genome sets), use research_resources instead. Both slots reference subtypes of ResearchResource, so a single query against the class hierarchy returns every resource a program maintains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    phenotype_assays: Optional[list[PhenotypeAssayType]] = Field(default=[], description="""Types of phenotype assays performed by this research program. Catalogs the phenotyping capabilities and data types generated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    id: str = Field(default=..., description="""A unique identifier for the research program (e.g., nmdc_sfas_brcs:glbrc)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The full official name of the research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })

    @field_validator('nmdc_umbrella_study')
    def pattern_nmdc_umbrella_study(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_umbrella_study format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_umbrella_study format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class OtherProgram(ResearchProgram):
    """
    Other DOE research programs and initiatives that don't fit the traditional SFA/BRC/Facility categories. Examples include BRaVE (Biopreparedness Research Virtual Environment) projects, cross-cutting initiatives, and time-limited collaborative projects spanning multiple DOE offices.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'program_type': {'ifabsent': 'string(OTHER_INITIATIVE)',
                                         'name': 'program_type'}}})

    initiative_name: Optional[str] = Field(default=None, description="""Name of the parent initiative this program belongs to (e.g., BRaVE for Biopreparedness Research Virtual Environment projects)""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    funding_period: Optional[str] = Field(default=None, description="""The funding period for time-limited initiatives (e.g., \"2023-2026\" or \"FY2023-FY2025\")""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    participating_offices: Optional[list[str]] = Field(default=[], description="""DOE offices participating in funding this initiative (e.g., BER, ASCR, BES)""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=ProgramType.OTHER_INITIATIVE, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'ifabsent': 'string(OTHER_INITIATIVE)'} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    partner_institutions: Optional[list[str]] = Field(default=[], description="""Partner institutions participating in the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    principal_investigators: Optional[list[Person]] = Field(default=[], description="""Principal investigators leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    location: Optional[Location] = Field(default=None, description="""Geographic location of the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    scientific_questions: Optional[list[str]] = Field(default=[], description="""Key scientific questions addressed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data collected or generated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    data_collection_modalities: Optional[list[DataCollectionModality]] = Field(default=[], description="""Methods and modalities used for data collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    nmdc_umbrella_study: Optional[str] = Field(default=None, description="""The NMDC umbrella study identifier for this research program. This is the top-level study that child studies link to via part_of.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    studies: Optional[list[NMDCStudyReference]] = Field(default=[], description="""NMDC studies associated with this research program. These are individual research studies that are part of the program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    analyses: Optional[list[KBaseNarrative]] = Field(default=[], description="""Computational analyses associated with this research program, including KBase narratives and other workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    kbase_genome_collection: Optional[KBaseCollection] = Field(default=None, description="""If this program has a curated genome collection in KBase Collections (e.g., ENIGMA, PMI, GROW), the collection identifier. Collections are searchable curated datasets with GTDB taxonomy and microTrait annotations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    datasets: Optional[list[Dataset]] = Field(default=[], description="""Datasets produced by or associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    key_publications: Optional[list[Reference]] = Field(default=[], description="""Key publications from the program with their findings""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    established: Optional[int] = Field(default=None, description="""Year the program was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    collaborators: Optional[str] = Field(default=None, description="""Description of collaborators""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    isolate_collections: Optional[list[IsolateCollection]] = Field(default=[], description="""Microbial isolate collections maintained by this research program. Provides catalog-level information about available cultures and genomes. For new entries that are not isolate collections (mutant libraries, phage banks, knowledgebases, reference genome sets), use research_resources instead. Both slots reference subtypes of ResearchResource, so a single query against the class hierarchy returns every resource a program maintains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    phenotype_assays: Optional[list[PhenotypeAssayType]] = Field(default=[], description="""Types of phenotype assays performed by this research program. Catalogs the phenotyping capabilities and data types generated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    id: str = Field(default=..., description="""A unique identifier for the research program (e.g., nmdc_sfas_brcs:glbrc)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The full official name of the research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })

    @field_validator('nmdc_umbrella_study')
    def pattern_nmdc_umbrella_study(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_umbrella_study format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_umbrella_study format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ArtificialIntelligenceProject(OtherProgram):
    """
    A DOE artificial intelligence project or pilot initiative using AI/ML, agentic systems, data lakehouses, autonomous laboratories, or related computational methods to advance BER-relevant biological and environmental science.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'program_type': {'ifabsent': 'string(AI_PILOT_PROJECT)',
                                         'name': 'program_type'}}})

    initiative_name: Optional[str] = Field(default=None, description="""Name of the parent initiative this program belongs to (e.g., BRaVE for Biopreparedness Research Virtual Environment projects)""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    funding_period: Optional[str] = Field(default=None, description="""The funding period for time-limited initiatives (e.g., \"2023-2026\" or \"FY2023-FY2025\")""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    participating_offices: Optional[list[str]] = Field(default=[], description="""DOE offices participating in funding this initiative (e.g., BER, ASCR, BES)""", json_schema_extra = { "linkml_meta": {'domain_of': ['OtherProgram']} })
    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=ProgramType.AI_PILOT_PROJECT, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'ifabsent': 'string(AI_PILOT_PROJECT)'} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    partner_institutions: Optional[list[str]] = Field(default=[], description="""Partner institutions participating in the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    principal_investigators: Optional[list[Person]] = Field(default=[], description="""Principal investigators leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    location: Optional[Location] = Field(default=None, description="""Geographic location of the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    scientific_questions: Optional[list[str]] = Field(default=[], description="""Key scientific questions addressed by the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data collected or generated""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    data_collection_modalities: Optional[list[DataCollectionModality]] = Field(default=[], description="""Methods and modalities used for data collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    nmdc_umbrella_study: Optional[str] = Field(default=None, description="""The NMDC umbrella study identifier for this research program. This is the top-level study that child studies link to via part_of.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    studies: Optional[list[NMDCStudyReference]] = Field(default=[], description="""NMDC studies associated with this research program. These are individual research studies that are part of the program.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    analyses: Optional[list[KBaseNarrative]] = Field(default=[], description="""Computational analyses associated with this research program, including KBase narratives and other workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    kbase_genome_collection: Optional[KBaseCollection] = Field(default=None, description="""If this program has a curated genome collection in KBase Collections (e.g., ENIGMA, PMI, GROW), the collection identifier. Collections are searchable curated datasets with GTDB taxonomy and microTrait annotations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    datasets: Optional[list[Dataset]] = Field(default=[], description="""Datasets produced by or associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    key_publications: Optional[list[Reference]] = Field(default=[], description="""Key publications from the program with their findings""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    established: Optional[int] = Field(default=None, description="""Year the program was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    collaborators: Optional[str] = Field(default=None, description="""Description of collaborators""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    isolate_collections: Optional[list[IsolateCollection]] = Field(default=[], description="""Microbial isolate collections maintained by this research program. Provides catalog-level information about available cultures and genomes. For new entries that are not isolate collections (mutant libraries, phage banks, knowledgebases, reference genome sets), use research_resources instead. Both slots reference subtypes of ResearchResource, so a single query against the class hierarchy returns every resource a program maintains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    phenotype_assays: Optional[list[PhenotypeAssayType]] = Field(default=[], description="""Types of phenotype assays performed by this research program. Catalogs the phenotyping capabilities and data types generated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram']} })
    id: str = Field(default=..., description="""A unique identifier for the research program (e.g., nmdc_sfas_brcs:glbrc)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The full official name of the research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })

    @field_validator('nmdc_umbrella_study')
    def pattern_nmdc_umbrella_study(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_umbrella_study format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_umbrella_study format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^([a-z][a-z0-9_]*:)?[a-z][a-z0-9_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class UserFacility(NamedThing):
    """
    A DOE BER User Facility providing resources and capabilities to the broader scientific community. Examples include JGI, EMSL, and KBase.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    acronym: Optional[str] = Field(default=None, description="""Short acronym or abbreviation for the program (e.g., GLBRC, ENIGMA)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility'],
         'slot_uri': 'schema:alternateName'} })
    program_type: Optional[ProgramType] = Field(default=None, description="""The type of research program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    start_date: Optional[str] = Field(default=None, description="""Date or year when the program started. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    end_date: Optional[str] = Field(default=None, description="""Date or year when the program ended. Leave empty for ongoing programs. Prefer ISO 8601 dates when known; use a year-only value when the exact date is not known.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institution: Optional[str] = Field(default=None, description="""The primary institution leading the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    lead_institutions: Optional[list[str]] = Field(default=[], description="""Multiple lead institutions (for collaborative programs)""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    funding: Optional[FundingInfo] = Field(default=None, description="""Funding information for the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    websites: Optional[WebResources] = Field(default=None, description="""Web resources associated with the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    services: Optional[list[str]] = Field(default=[], description="""Services provided by a facility""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    capabilities: Optional[list[Capability]] = Field(default=[], description="""Scientific capabilities provided by the facility""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    flagship_genomes: Optional[list[FlagshipGenome]] = Field(default=[], description="""Flagship genomes sequenced by the facility""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    reference_data: Optional[ReferenceData] = Field(default=None, description="""Reference data maintained by the facility""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    supported_data_types: Optional[list[str]] = Field(default=[], description="""Data types supported by a facility""", json_schema_extra = { "linkml_meta": {'domain_of': ['UserFacility']} })
    research_resources: Optional[list[ResearchResource]] = Field(default=[], description="""Research resources maintained or produced by this program at catalog grain (mutant libraries, phage banks, reference genome sets, plasmid collections, synthetic communities, knowledgebases, software). Use this slot for resource kinds other than isolate collections; existing isolate collections remain under the isolate_collections slot for back-compatibility but are also instances of ResearchResource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'UserFacility']} })
    id: str = Field(default=..., description="""A unique identifier for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class Institution(ConfiguredBaseModel):
    """
    A research institution such as a national laboratory, university, or research institute.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Organization',
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    ror_id: Optional[str] = Field(default=None, description="""Research Organization Registry identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['Institution']} })
    institution_type: Optional[InstitutionType] = Field(default=None, description="""The type of institution""", json_schema_extra = { "linkml_meta": {'domain_of': ['Institution']} })

    @field_validator('ror_id')
    def pattern_ror_id(cls, v):
        pattern=re.compile(r"^ror:\d{9}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ror_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ror_id format: {v}"
            raise ValueError(err_msg)
        return v


class Person(ConfiguredBaseModel):
    """
    A person involved in a research program, such as a principal investigator, co-investigator, or other key personnel.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person', 'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    role: Optional[str] = Field(default=None, description="""Role of a person in the program (e.g., Director, Principal Investigator)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    affiliation: Optional[str] = Field(default=None, description="""Institutional affiliation of a person""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    email: Optional[str] = Field(default=None, description="""Email address""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'schema:email'} })
    orcid: Optional[str] = Field(default=None, description="""ORCID identifier for a person""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })
    expertise: Optional[str] = Field(default=None, description="""Area of expertise""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person']} })

    @field_validator('orcid')
    def pattern_orcid(cls, v):
        pattern=re.compile(r"^orcid:\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid orcid format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid orcid format: {v}"
            raise ValueError(err_msg)
        return v


class FundingInfo(ConfiguredBaseModel):
    """
    Information about funding for a research program including agency, program, and award details.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    agency: Optional[str] = Field(default=None, description="""The funding agency (e.g., DOE BER)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    program: Optional[str] = Field(default=None, description="""The specific funding program (e.g., Genomic Science Program)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    division: Optional[str] = Field(default=None, description="""The division within the agency""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    subprogram: Optional[str] = Field(default=None, description="""Subprogram or area within the program""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    area: Optional[str] = Field(default=None, description="""Research area designation""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    contract: Optional[str] = Field(default=None, description="""Contract number""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    grant: Optional[str] = Field(default=None, description="""Grant number or identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    total_funding: Optional[str] = Field(default=None, description="""Total funding amount (may include period)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    amount: Optional[str] = Field(default=None, description="""Specific funding amount""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    award_2017: Optional[str] = Field(default=None, description="""Award amount for 2017 funding cycle""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })
    current_period: Optional[str] = Field(default=None, description="""Current funding period (e.g., 2023-2028)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FundingInfo']} })


class Location(ConfiguredBaseModel):
    """
    Geographic location information for a research program
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    address: Optional[str] = Field(default=None, description="""Street address or building name""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location']} })
    city: Optional[str] = Field(default=None, description="""City name""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location']} })
    state: Optional[str] = Field(default=None, description="""State or province""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location']} })
    country: Optional[str] = Field(default="USA", description="""Country name""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location'], 'ifabsent': 'string(USA)'} })


class WebResources(ConfiguredBaseModel):
    """
    Collection of web resources associated with a research program
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    main: Optional[str] = Field(default=None, description="""Main website URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    doe_page: Optional[str] = Field(default=None, description="""DOE program page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    award_list: Optional[str] = Field(default=None, description="""DOE award list, funding announcement, or award summary URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    ornl_page: Optional[str] = Field(default=None, description="""ORNL project page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    llnl_page: Optional[str] = Field(default=None, description="""LLNL project page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    data_portal: Optional[str] = Field(default=None, description="""Data portal URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    data_hub: Optional[str] = Field(default=None, description="""Data hub URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    data_page: Optional[str] = Field(default=None, description="""Data page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    atlas: Optional[str] = Field(default=None, description="""Atlas or mapping portal URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    github: Optional[str] = Field(default=None, description="""GitHub organization or repository URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    kbase: Optional[str] = Field(default=None, description="""KBase collaboration page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    ess_dive: Optional[str] = Field(default=None, description="""ESS-DIVE data portal URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    ideas_watersheds: Optional[str] = Field(default=None, description="""IDEAS-Watersheds page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    czen: Optional[str] = Field(default=None, description="""Critical Zone Exploration Network page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    publications: Optional[str] = Field(default=None, description="""Publications page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    highlights: Optional[str] = Field(default=None, description="""Research highlights page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    documentation: Optional[str] = Field(default=None, description="""Documentation URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    bacterial_strains: Optional[str] = Field(default=None, description="""Bacterial strains collection URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    bfi_portal: Optional[str] = Field(default=None, description="""BFI research portal URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    ssrl_page: Optional[str] = Field(default=None, description="""SSRL page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    anl_page: Optional[str] = Field(default=None, description="""ANL page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    team: Optional[str] = Field(default=None, description="""Team page URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })
    phytozome: Optional[str] = Field(default=None, description="""Phytozome plant genome portal URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebResources']} })


class Dataset(ConfiguredBaseModel):
    """
    A dataset produced by or associated with a research program.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    doi: Optional[str] = Field(default=None, description="""Digital Object Identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    url: Optional[str] = Field(default=None, description="""A URL""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability'],
         'slot_uri': 'schema:url'} })
    repository: Optional[str] = Field(default=None, description="""Data repository where a dataset is stored""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    data_type: Optional[str] = Field(default=None, description="""Type of data in a dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    size: Optional[str] = Field(default=None, description="""Size of a dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    version: Optional[str] = Field(default=None, description="""Version of a dataset or resource""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    years: Optional[str] = Field(default=None, description="""Years covered by a dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    reference: Optional[str] = Field(default=None, description="""Reference citation for a dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Finding', 'PrimaryReferenceInfo']} })
    count: Optional[str] = Field(default=None, description="""Count of items in a dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'ResearchResource', 'Instrument']} })
    osti_id: Optional[str] = Field(default=None, description="""OSTI (Office of Scientific and Technical Information) identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    doi_examples: Optional[list[str]] = Field(default=[], description="""Example DOIs for a dataset collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    nmdc_study_id: Optional[str] = Field(default=None, description="""National Microbiome Data Collaborative study identifier (e.g., nmdc:sty-11-ev70y104)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'NMDCStudyReference']} })
    jgi_project_id: Optional[str] = Field(default=None, description="""DOE Joint Genome Institute project identifier for sequence data (e.g., Gs0114663 or 1191516)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    ameriflux_site_id: Optional[str] = Field(default=None, description="""Ameriflux site identifier for flux tower data (e.g., US-KL1)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    lter_dataset_id: Optional[str] = Field(default=None, description="""Long Term Ecological Research Network dataset identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    pride_id: Optional[str] = Field(default=None, description="""ProteomeXchange/PRIDE Archive identifier for proteomics data (e.g., PXD049389)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    massive_id: Optional[str] = Field(default=None, description="""MassIVE repository identifier for mass spectrometry data (e.g., MSV000095714)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset']} })
    primary_reference: Optional[str] = Field(default=None, description="""DOI of the primary publication describing this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    additional_references: Optional[list[str]] = Field(default=[], description="""DOIs of additional publications associated with or derived from this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Analysis']} })
    interaction_types: Optional[list[InteractionType]] = Field(default=[], description="""Types of microbial interactions studied (e.g., mutualism, antagonism, competition)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    interaction_modes: Optional[list[InteractionMode]] = Field(default=[], description="""Physical or chemical modes of microbial interaction (e.g., endohyphal, siderophore-mediated)""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'Dataset']} })
    variables: Optional[list[Variable]] = Field(default=[], description="""Variables, factors, measurements, or data fields catalogued for a study or dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'NMDCStudyReference']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference slot - enables title and excerpt validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })

    @field_validator('nmdc_study_id')
    def pattern_nmdc_study_id(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_study_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_study_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('ameriflux_site_id')
    def pattern_ameriflux_site_id(cls, v):
        pattern=re.compile(r"^[A-Z]{2}-[A-Za-z0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ameriflux_site_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ameriflux_site_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('pride_id')
    def pattern_pride_id(cls, v):
        pattern=re.compile(r"^PXD\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid pride_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid pride_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('massive_id')
    def pattern_massive_id(cls, v):
        pattern=re.compile(r"^MSV\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid massive_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid massive_id format: {v}"
            raise ValueError(err_msg)
        return v


class Variable(ConfiguredBaseModel):
    """
    A variable, factor, measurement, or metadata field observed, manipulated, derived, or otherwise used in a study or dataset. Variables act as a lightweight data dictionary and can be tagged with analytical roles, time-series behavior, units, methods, and ontology mappings such as BERVO. Ontology references are modeled as id/label objects so linkml-term-validator can check both the identifier and the canonical label.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:PropertyValue',
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'name': {'description': 'Human-readable variable name or label '
                                                'used in the study or dataset',
                                 'name': 'name',
                                 'required': True}}})

    name: str = Field(default=..., description="""Human-readable variable name or label used in the study or dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    roles: Optional[list[VariableRole]] = Field(default=[], description="""Roles this variable plays in the study design or analysis. Multiple roles are allowed; for example, drought treatment may be both EXPERIMENTAL_FACTOR and STUDY_DESIGN_INDEPENDENT_VARIABLE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    value_type: Optional[VariableValueType] = Field(default=None, description="""Basic type or shape of values recorded for this variable""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    units: Optional[str] = Field(default=None, description="""Human-readable units for quantitative variables""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    unit_term: Optional[OntologyTerm] = Field(default=None, description="""Unit ontology term, if available""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    bervo_term: Optional[BERVOTerm] = Field(default=None, description="""Primary BERVO class mapping for this variable, when available""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    mixs_terms: Optional[list[MIXSTerm]] = Field(default=[], description="""MIxS metadata terms corresponding to this variable, when the variable represents a MIxS sample, environmental, host, or sequencing metadata field.""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'RECOMMENDED',
                       'range': 'MIXSVariableTerm'}],
         'domain_of': ['Variable']} })
    ontology_mappings: Optional[list[OntologyTerm]] = Field(default=[], description="""Additional ontology mappings for this variable, including ENVO, PATO, UO, OBI, or other relevant controlled vocabularies. Statistical or study-design roles should generally be represented in the roles slot rather than repeated here.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    measured_entity: Optional[str] = Field(default=None, description="""Entity, organism, environmental feature, process, or system being measured or manipulated by this variable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    material_or_matrix: Optional[str] = Field(default=None, description="""Material, sample matrix, compartment, or context for the variable (e.g., soil, rhizosphere, leaf tissue, porewater, bioreactor culture).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    method: Optional[str] = Field(default=None, description="""Measurement, manipulation, or derivation method""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    time_series: Optional[bool] = Field(default=None, description="""True when values for this variable are captured repeatedly through time""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    temporal_resolution: Optional[str] = Field(default=None, description="""Temporal grain or sampling interval for time-series variables""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    spatial_resolution: Optional[str] = Field(default=None, description="""Spatial grain, support, or resolution for spatial variables""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    levels: Optional[list[str]] = Field(default=[], description="""Known categorical levels, treatment levels, bins, or allowed values for this variable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    source_field_names: Optional[list[str]] = Field(default=[], description="""Column names, file field names, or source labels that map to this variable""", json_schema_extra = { "linkml_meta": {'domain_of': ['Variable']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes about the variable definition or usage""", json_schema_extra = { "linkml_meta": {'domain_of': ['CollectionMetadata', 'Variable', 'StudyDesign']} })


class OntologyTerm(ConfiguredBaseModel):
    """
    A reference to an ontology term, represented as an identifier plus the term label expected from the source ontology. The label field is marked as rdfs:label for linkml-term-validator label checks.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    id: str = Field(default=..., description="""CURIE or URI for the ontology term""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference']} })
    label: str = Field(default=..., description="""Human-readable ontology term label""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm'], 'implements': ['rdfs:label']} })
    mapping_relation: Optional[OntologyMappingRelation] = Field(default=None, description="""SSSOM/SKOS mapping predicate describing how the local variable or field maps to this ontology term. The local variable is the subject and the ontology term is the object; for example, NARROW_MATCH means the ontology term is narrower than the local variable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })
    mapping_note: Optional[str] = Field(default=None, description="""Curator note explaining the scope or uncertainty of this ontology mapping""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })


class BERVOTerm(OntologyTerm):
    """
    A BERVO ontology term represented with an identifier and label
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'id': {'description': 'BERVO CURIE for the ontology term',
                               'name': 'id',
                               'pattern': '^BERVO:\\d+$'}}})

    id: str = Field(default=..., description="""BERVO CURIE for the ontology term""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference']} })
    label: str = Field(default=..., description="""Human-readable ontology term label""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm'], 'implements': ['rdfs:label']} })
    mapping_relation: Optional[OntologyMappingRelation] = Field(default=None, description="""SSSOM/SKOS mapping predicate describing how the local variable or field maps to this ontology term. The local variable is the subject and the ontology term is the object; for example, NARROW_MATCH means the ontology term is narrower than the local variable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })
    mapping_note: Optional[str] = Field(default=None, description="""Curator note explaining the scope or uncertainty of this ontology mapping""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^BERVO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class MIXSTerm(OntologyTerm):
    """
    A MIxS metadata term represented with an identifier and label
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'id': {'description': 'MIxS CURIE for the metadata term',
                               'name': 'id',
                               'pattern': '^MIXS:\\d{7}$'}}})

    id: str = Field(default=..., description="""MIxS CURIE for the metadata term""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference']} })
    label: str = Field(default=..., description="""Human-readable ontology term label""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm'], 'implements': ['rdfs:label']} })
    mapping_relation: Optional[OntologyMappingRelation] = Field(default=None, description="""SSSOM/SKOS mapping predicate describing how the local variable or field maps to this ontology term. The local variable is the subject and the ontology term is the object; for example, NARROW_MATCH means the ontology term is narrower than the local variable.""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })
    mapping_note: Optional[str] = Field(default=None, description="""Curator note explaining the scope or uncertainty of this ontology mapping""", json_schema_extra = { "linkml_meta": {'domain_of': ['OntologyTerm']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^MIXS:\d{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Reference(ConfiguredBaseModel):
    """
    A publication reference with key findings. Minimal metadata is stored here; full bibliographic data can be fetched/cached via linkml-reference-validator.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'id': {'description': 'DOI of the publication (e.g., '
                                              'doi:10.1038/s41586-020-03127-1)',
                               'implements': ['linkml:authoritative_reference'],
                               'name': 'id'}}})

    id: str = Field(default=..., description="""DOI of the publication (e.g., doi:10.1038/s41586-020-03127-1)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'implements': ['linkml:authoritative_reference'],
         'slot_uri': 'schema:identifier'} })
    title: Optional[str] = Field(default=None, description="""Title of a publication or other work""", json_schema_extra = { "linkml_meta": {'domain_of': ['Reference', 'WebReference'], 'slot_uri': 'dcterms:title'} })
    findings: Optional[list[Finding]] = Field(default=[], description="""Key findings or claims extracted from a publication""", json_schema_extra = { "linkml_meta": {'domain_of': ['Reference']} })


class Finding(ConfiguredBaseModel):
    """
    A key finding or claim extracted from a publication
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    statement: str = Field(default=..., description="""A key finding or claim from the publication""", json_schema_extra = { "linkml_meta": {'domain_of': ['Finding']} })
    supporting_text: Optional[str] = Field(default=None, description="""Exact excerpt or quote from the publication supporting the finding""", json_schema_extra = { "linkml_meta": {'domain_of': ['Finding'], 'implements': ['linkml:excerpt']} })
    reference: Optional[str] = Field(default=None, description="""DOI of the publication this finding is from (for validation)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Finding', 'PrimaryReferenceInfo'],
         'implements': ['linkml:authoritative_reference']} })


class PrimaryReferenceInfo(ConfiguredBaseModel):
    """
    Container for a primary reference with its metadata. Provides a structured way to associate a publication reference with an entity (e.g., IsolateCollection, Dataset) while allowing future annotations about the relationship.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    reference: Reference = Field(default=..., description="""The primary publication reference""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Finding', 'PrimaryReferenceInfo']} })
    relationship_note: Optional[str] = Field(default=None, description="""Optional note describing the relationship between the reference and the entity it's attached to (e.g., \"Describes the isolation methods\", \"First report of these isolates\")""", json_schema_extra = { "linkml_meta": {'domain_of': ['PrimaryReferenceInfo']} })


class ProgramOutputs(ConfiguredBaseModel):
    """
    Summary of research outputs from a program
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    publication_count: Optional[str] = Field(default=None, description="""Number or description of publications""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })
    patent_applications: Optional[int] = Field(default=None, description="""Number of patent applications""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })
    invention_disclosures: Optional[int] = Field(default=None, description="""Number of invention disclosures""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })
    licenses_options: Optional[int] = Field(default=None, description="""Number of licenses or options""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })
    patents: Optional[int] = Field(default=None, description="""Number of patents granted""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })
    startups: Optional[int] = Field(default=None, description="""Number of startup companies formed""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProgramOutputs']} })


class ResearchResource(ConfiguredBaseModel):
    """
    A large-grain research resource maintained or produced by a research program: an isolate collection, mutant library, phage bank, reference genome set, plasmid collection, synthetic community, knowledgebase, or similar reagent or data resource. Catalog-level metadata only; detailed records are expected to live in external systems referenced via identifiers. IsolateCollection is a subtype; other resource kinds are distinguished by the resource_type discriminator rather than by proliferating subclasses.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    primary_reference: Optional[str] = Field(default=None, description="""DOI of the primary publication describing this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    resource_type: Optional[ResourceType] = Field(default=None, description="""Coarse classification of this resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    identifiers: Optional[list[ResourceIdentifier]] = Field(default=[], description="""Typed external identifiers for the resource — registry + accession tuples pointing to records in catalogs such as Addgene, BEI, ATCC, DSMZ, KBase narratives, NCBI:Assembly, the LBNL Fitness Browser, lab catalogs, or RRID-issuing registries.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    provider: Optional[str] = Field(default=None, description="""Organization or laboratory that maintains and distributes the resource (e.g., LBNL, EMSL, JGI, BEI Resources).""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    url: Optional[str] = Field(default=None, description="""Primary landing or catalog URL for the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability']} })
    count: Optional[str] = Field(default=None, description="""Approximate size of the resource (e.g., \"~10^5 mutants\", \"261 isolates\", \"135 Gbases\"). Free text so units travel with the value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'ResearchResource', 'Instrument']} })
    members: Optional[list[str]] = Field(default=[], description="""Members of the resource at human-readable grain (e.g., organism names with strain designators, condition or media descriptors). For panel resources this is the panel content. May be a representative subset when the full list is large; in that case the canonical list lives at the resource's url and member_count reflects the total.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    member_count: Optional[int] = Field(default=None, description="""Total number of members in the resource. Useful when members is a representative subset rather than a complete enumeration.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference for new entries.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })


class ResourceIdentifier(ConfiguredBaseModel):
    """
    A typed external identifier for a research resource: a {registry, accession} tuple with an optional resolvable URL and citation. Used to point at a resource's record in any external catalog or registry — examples include Addgene, BEI, ATCC, DSMZ, KBase narrative IDs, NCBI:Assembly accessions, a Fitness Browser organism ID, an RRID, or a lab catalog identifier.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    registry: str = Field(default=..., description="""Issuing registry or catalog (e.g., RRID, Addgene, BEI, ATCC, DSMZ, KBase, NCBI:Assembly, fit.genomics.lbl.gov, internal).""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResourceIdentifier']} })
    accession: str = Field(default=..., description="""Identifier assigned by the registry.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResourceIdentifier']} })
    url: Optional[str] = Field(default=None, description="""Resolvable URL for the identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability']} })
    citation: Optional[str] = Field(default=None, description="""DOI of a canonical publication describing this resource entry, when distinct from the resource's primary_reference.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResourceIdentifier']} })


class IsolateCollection(ResearchResource):
    """
    A collection of cultured microbial isolates maintained by a research program. Provides catalog-level metadata about the collection; detailed isolate records are maintained in external systems (KBase, JGI, culture collections). Subtype of ResearchResource; other resource kinds (mutant libraries, phage banks, knowledgebases) are modeled as ResearchResource directly using the resource_type discriminator.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    organism_types: Optional[list[OrganismType]] = Field(default=[], description="""Types of organisms in this collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    isolate_count: Optional[int] = Field(default=None, description="""Approximate number of isolates in the collection""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    genome_count: Optional[int] = Field(default=None, description="""Number of isolates with sequenced genomes""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection', 'KBaseNarrative']} })
    source_environments: Optional[list[str]] = Field(default=[], description="""Environments from which isolates were obtained (e.g., rhizosphere, subsurface, contaminated groundwater, phyllosphere)""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    isolation_methods: Optional[list[str]] = Field(default=[], description="""Brief description of isolation methods used (e.g., aerobic plating, anaerobic enrichment, single-cell sorting)""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    host_organisms: Optional[list[str]] = Field(default=[], description="""Host organisms if isolates are host-associated (e.g., Populus, Panicum virgatum)""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    culture_collection_url: Optional[str] = Field(default=None, description="""URL to browse or request live cultures""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    genome_catalog_url: Optional[str] = Field(default=None, description="""URL to genome data (KBase narrative, JGI, NCBI BioProject)""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection']} })
    kbase_narrative_id: Optional[str] = Field(default=None, description="""KBase narrative ID containing isolate genomes if applicable""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection', 'KBaseNarrative']} })
    primary_reference: Optional[str] = Field(default=None, description="""DOI of primary publication describing the collection. DEPRECATED: Use primary_reference_info for new entries to enable title validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference - enables title and excerpt validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })
    resource_type: Optional[ResourceType] = Field(default=None, description="""Coarse classification of this resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    identifiers: Optional[list[ResourceIdentifier]] = Field(default=[], description="""Typed external identifiers for the resource — registry + accession tuples pointing to records in catalogs such as Addgene, BEI, ATCC, DSMZ, KBase narratives, NCBI:Assembly, the LBNL Fitness Browser, lab catalogs, or RRID-issuing registries.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    provider: Optional[str] = Field(default=None, description="""Organization or laboratory that maintains and distributes the resource (e.g., LBNL, EMSL, JGI, BEI Resources).""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    url: Optional[str] = Field(default=None, description="""Primary landing or catalog URL for the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability']} })
    count: Optional[str] = Field(default=None, description="""Approximate size of the resource (e.g., \"~10^5 mutants\", \"261 isolates\", \"135 Gbases\"). Free text so units travel with the value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'ResearchResource', 'Instrument']} })
    members: Optional[list[str]] = Field(default=[], description="""Members of the resource at human-readable grain (e.g., organism names with strain designators, condition or media descriptors). For panel resources this is the panel content. May be a representative subset when the full list is large; in that case the canonical list lives at the resource's url and member_count reflects the total.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })
    member_count: Optional[int] = Field(default=None, description="""Total number of members in the resource. Useful when members is a representative subset rather than a complete enumeration.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchResource']} })


class FieldSite(NamedThing):
    """
    A field research site associated with a research program
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Place',
         'from_schema': 'https://w3id.org/nmdc/sfas-brcs',
         'slot_usage': {'id': {'description': 'A unique identifier for the field site',
                               'name': 'id',
                               'required': True},
                        'name': {'description': 'The canonical name of the field site',
                                 'name': 'name',
                                 'required': True}}})

    location: Optional[str] = Field(default=None, description="""Geographic location of the field site""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'FieldSite']} })
    site_type: Optional[str] = Field(default=None, description="""Type of field site (e.g., NEON, LTER, RESEARCH_STATION, NATIONAL_FOREST, NATIONAL_PARK, AGRICULTURAL, URBAN, COASTAL_WETLAND)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    pi: Optional[str] = Field(default=None, description="""Principal investigator leading research at this site""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite', 'NMDCStudyReference']} })
    institution: Optional[str] = Field(default=None, description="""Institution of the principal investigator""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    relevance: Optional[list[str]] = Field(default=[], description="""Research relevance categories for the site (e.g., BIOTECH, BIOENERGY, HAZARD_PREDICTION, WILDFIRE, CLIMATE_CHANGE, AGRICULTURE)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    contaminants: Optional[list[str]] = Field(default=[], description="""Contaminants present at the site (if applicable)""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    contamination_source: Optional[str] = Field(default=None, description="""Source of contamination at the site""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    elevation_m: Optional[int] = Field(default=None, description="""Elevation of the field site in meters above sea level""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    mean_annual_temp_c: Optional[float] = Field(default=None, description="""Mean annual temperature at the site in degrees Celsius""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    mean_annual_precip_cm: Optional[float] = Field(default=None, description="""Mean annual precipitation at the site in centimeters""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite']} })
    id: str = Field(default=..., description="""A unique identifier for the field site""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The canonical name of the field site""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class Technology(ConfiguredBaseModel):
    """
    A technology or tool developed by a research program
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class WebReference(ConfiguredBaseModel):
    """
    A reference to a web resource such as a project page, news article, or documentation. Used for citing non-DOI sources that document research activities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    url: str = Field(default=..., description="""URL of the web resource""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability']} })
    title: str = Field(default=..., description="""Title of the web page or resource""", json_schema_extra = { "linkml_meta": {'domain_of': ['Reference', 'WebReference']} })
    summary: Optional[str] = Field(default=None, description="""Brief description of what content can be found at this URL. Serves as an annotation to help users understand what information the source provides before clicking.""", json_schema_extra = { "linkml_meta": {'domain_of': ['WebReference']} })


class StudyDesign(ConfiguredBaseModel):
    """
    Study-level design metadata that applies across variables and datasets. This captures the design pattern, experimental or observational units, replication, blocking, randomization, and related notes separately from the data dictionary entries for individual variables.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    design_types: Optional[list[OntologyTerm]] = Field(default=[], description="""OBI or related ontology terms describing the study design""", json_schema_extra = { "linkml_meta": {'bindings': [{'binds_value_of': 'id',
                       'obligation_level': 'RECOMMENDED',
                       'range': 'StudyDesignTerm'}],
         'domain_of': ['StudyDesign']} })
    factor_panels: Optional[list[str]] = Field(default=[], description="""Names of panel ResearchResource entries (typically ORGANISM_PANEL or CONDITION_PANEL) that contribute the factor levels for this study. Lets multiple studies share a panel definition rather than redeclaring it; the cross-product of the referenced panels is implied by the study design and need not be enumerated cell by cell.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    experimental_units: Optional[list[str]] = Field(default=[], description="""Units assigned to treatments or interventions""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    observational_units: Optional[list[str]] = Field(default=[], description="""Units on which measurements are made""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    sampling_strategy: Optional[str] = Field(default=None, description="""Sampling strategy or sampling design used by the study""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    replication: Optional[str] = Field(default=None, description="""Description of biological, technical, field, or model replication""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    randomization: Optional[str] = Field(default=None, description="""Description of randomization, if used""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    blocking: Optional[str] = Field(default=None, description="""Description of blocking or stratification, if used""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    controls: Optional[str] = Field(default=None, description="""Description of control groups, baselines, or reference conditions""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDesign']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes about the study design""", json_schema_extra = { "linkml_meta": {'domain_of': ['CollectionMetadata', 'Variable', 'StudyDesign']} })


class NMDCStudyReference(ConfiguredBaseModel):
    """
    A reference to an NMDC study associated with a research program. Links BRC/SFA research to specific studies in the National Microbiome Data Collaborative. Can also represent studies that are candidates for NMDC ingest (nmdc_ingest_target=true).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    nmdc_study_id: Optional[str] = Field(default=None, description="""National Microbiome Data Collaborative study identifier (e.g., nmdc:sty-11-ev70y104)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'NMDCStudyReference']} })
    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    primary_reference: Optional[str] = Field(default=None, description="""DOI of the primary publication describing this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    keywords: Optional[list[Keyword]] = Field(default=[], description="""Keywords describing the research focus""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference'],
         'slot_uri': 'schema:keywords'} })
    field_site_ids: Optional[list[str]] = Field(default=[], description="""Identifiers of canonical field sites associated with the program or study. These reference entries in the top-level sites collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResearchProgram', 'NMDCStudyReference']} })
    study_design: Optional[StudyDesign] = Field(default=None, description="""Study design metadata associated with a study""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    variables: Optional[list[Variable]] = Field(default=[], description="""Variables, factors, measurements, or data fields catalogued for a study or dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'NMDCStudyReference']} })
    pi: Optional[str] = Field(default=None, description="""Principal investigator name for this study""", json_schema_extra = { "linkml_meta": {'domain_of': ['FieldSite', 'NMDCStudyReference']} })
    bioproject_ids: Optional[list[str]] = Field(default=[], description="""NCBI BioProject identifiers associated with this study""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    gold_study_id: Optional[str] = Field(default=None, description="""GOLD study identifier (e.g., gold:Gs0128851)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    jgi_proposal_id: Optional[str] = Field(default=None, description="""JGI proposal identifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    brc_dataset_ids: Optional[list[str]] = Field(default=[], description="""Dataset identifiers from the BRC API (api.bioenergy.org) associated with this study. These are the native identifiers which may be DOIs, BioProject IDs, or repository-specific IDs.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    nmdc_ingest_target: Optional[bool] = Field(default=None, description="""If true, indicates this study has data that should be targeted for ingest into NMDC but is not yet registered there.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    nmdc_ingest_priority: Optional[NMDCIngestPriority] = Field(default=None, description="""Priority level for NMDC ingest consideration. HIGH for datasets with rich microbiome data ready for processing, MEDIUM for datasets that need some preparation, LOW for marginal candidates.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    data_modalities: Optional[list[DataType]] = Field(default=[], description="""Types of data generated in this study (e.g., 16S_AMPLICON, METAGENOMICS)""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    sample_count: Optional[int] = Field(default=None, description="""Number of samples in the study""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference', 'KBaseNarrative']} })
    organism: Optional[str] = Field(default=None, description="""Primary organism studied""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    preprocessed_data_available: Optional[list[PreprocessedDataType]] = Field(default=[], description="""Types of preprocessed/derived data products available in public repositories (e.g., NCBI) for this study. Examples include MAGs (metagenome-assembled genomes), genome assemblies, gene annotations, etc. Used to identify studies with analysis-ready data that may meet NMDC quality standards.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    preprocessed_data_counts: Optional[str] = Field(default=None, description="""Counts of preprocessed data products available (e.g., \"28 MAGs\", \"135 Gbases\"). Free text to capture quantity and type.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    ncbi_data_quality_notes: Optional[str] = Field(default=None, description="""Notes about the quality or completeness of preprocessed data in NCBI. Used to track whether external data meets NMDC standards.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference slot - enables title and excerpt validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })
    source_reference: Optional[WebReference] = Field(default=None, description="""Web reference documenting this study (project page, news article, etc.) for studies without a primary DOI publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })
    synthetic_communities: Optional[list[str]] = Field(default=[], description="""CURIEs referencing synthetic community (SynCom) entries in the CommunityMech knowledge base that are associated with this study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference']} })

    @field_validator('nmdc_study_id')
    def pattern_nmdc_study_id(cls, v):
        pattern=re.compile(r"^nmdc:sty-[a-z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nmdc_study_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nmdc_study_id format: {v}"
            raise ValueError(err_msg)
        return v


class Analysis(NamedThing):
    """
    A computational analysis performed on research data. This is an abstract base class for different types of analyses including KBase narratives, pipeline runs, and other computational workflows.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    primary_reference: Optional[str] = Field(default=None, description="""DOI of the primary publication describing this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    additional_references: Optional[list[str]] = Field(default=[], description="""DOIs of additional publications associated with or derived from this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Analysis']} })
    analysis_type: Optional[AnalysisType] = Field(default=None, description="""Type of analysis performed""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    input_data_description: Optional[str] = Field(default=None, description="""Description of input data used""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    output_data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data objects produced""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference slot - enables title and excerpt validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })
    id: str = Field(default=..., description="""A unique identifier for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class KBaseNarrative(Analysis):
    """
    A KBase Narrative - a reproducible, shareable analysis workflow in the DOE Systems Biology Knowledgebase. Narratives combine data, analysis steps, and documentation in an executable Jupyter-like notebook format. Can be made public, shared, and assigned DOIs for citation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    kbase_narrative_id: Optional[str] = Field(default=None, description="""KBase narrative numeric ID (e.g., \"109073\"). This is the number that appears in URLs like kbase.us/n/109073/63/""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection', 'KBaseNarrative']} })
    kbase_narrative_url: Optional[str] = Field(default=None, description="""Full URL to the public narrative""", json_schema_extra = { "linkml_meta": {'domain_of': ['KBaseNarrative']} })
    kbase_workspace_id: Optional[str] = Field(default=None, description="""Workspace ID for programmatic access via KBase Workspace API""", json_schema_extra = { "linkml_meta": {'domain_of': ['KBaseNarrative']} })
    osti_doi: Optional[str] = Field(default=None, description="""DOI assigned by OSTI if narrative has been registered as a citable dataset (format: 10.25982/...)""", json_schema_extra = { "linkml_meta": {'domain_of': ['KBaseNarrative']} })
    is_static: Optional[bool] = Field(default=None, description="""Whether this is a static (snapshot) narrative suitable for citation""", json_schema_extra = { "linkml_meta": {'domain_of': ['KBaseNarrative']} })
    genome_count: Optional[int] = Field(default=None, description="""Number of genomes/MAGs in this narrative""", json_schema_extra = { "linkml_meta": {'domain_of': ['IsolateCollection', 'KBaseNarrative']} })
    sample_count: Optional[int] = Field(default=None, description="""Number of samples in this narrative""", json_schema_extra = { "linkml_meta": {'domain_of': ['NMDCStudyReference', 'KBaseNarrative']} })
    related_narratives: Optional[list[str]] = Field(default=[], description="""IDs of related KBase narratives""", json_schema_extra = { "linkml_meta": {'domain_of': ['KBaseNarrative']} })
    primary_reference: Optional[str] = Field(default=None, description="""DOI of the primary publication describing this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis'],
         'implements': ['linkml:authoritative_reference']} })
    additional_references: Optional[list[str]] = Field(default=[], description="""DOIs of additional publications associated with or derived from this dataset""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'Analysis']} })
    analysis_type: Optional[AnalysisType] = Field(default=None, description="""Type of analysis performed""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    input_data_description: Optional[str] = Field(default=None, description="""Description of input data used""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    output_data_types: Optional[list[DataType]] = Field(default=[], description="""Types of data objects produced""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analysis']} })
    primary_reference_info: Optional[PrimaryReferenceInfo] = Field(default=None, description="""Primary publication reference with structured metadata for validation. Preferred over primary_reference slot - enables title and excerpt validation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'IsolateCollection',
                       'NMDCStudyReference',
                       'Analysis']} })
    id: str = Field(default=..., description="""A unique identifier for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'OntologyTerm', 'Reference'],
         'slot_uri': 'schema:identifier'} })
    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })


class FlagshipGenome(ConfiguredBaseModel):
    """
    A flagship genome sequenced and maintained by a facility
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    common_name: Optional[str] = Field(default=None, description="""Common name of the organism""", json_schema_extra = { "linkml_meta": {'domain_of': ['FlagshipGenome']} })
    year: Optional[int] = Field(default=None, description="""Year the genome was sequenced""", json_schema_extra = { "linkml_meta": {'domain_of': ['FlagshipGenome']} })


class ReferenceData(ConfiguredBaseModel):
    """
    Reference data maintained by a facility
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    microbial_genomes: Optional[str] = Field(default=None, description="""Number/source of microbial genomes""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReferenceData']} })
    plant_genomes: Optional[str] = Field(default=None, description="""Number/source of plant genomes""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReferenceData']} })
    biolog_media: Optional[str] = Field(default=None, description="""Number of Biolog media formulations""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReferenceData']} })
    reactions_compounds: Optional[str] = Field(default=None, description="""Number/source of reactions and compounds""", json_schema_extra = { "linkml_meta": {'domain_of': ['ReferenceData']} })


class Capability(ConfiguredBaseModel):
    """
    A scientific capability or resource provided by a user facility, including instrumentation, platforms, and analytical services.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    capability_type: Optional[CapabilityType] = Field(default=None, description="""The type/category of capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    instruments: Optional[list[Instrument]] = Field(default=[], description="""Specific instruments or equipment supporting this capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    access_mode: Optional[str] = Field(default=None, description="""How users can access this capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    throughput: Optional[str] = Field(default=None, description="""Throughput or capacity metrics""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    year_established: Optional[int] = Field(default=None, description="""Year this capability was established""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    url: Optional[str] = Field(default=None, description="""URL for more information about this capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset',
                       'ResearchResource',
                       'ResourceIdentifier',
                       'WebReference',
                       'Capability']} })
    applications: Optional[list[str]] = Field(default=[], description="""Key applications or use cases for this capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    data_products: Optional[list[str]] = Field(default=[], description="""Types of data products generated by this capability""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    status: Optional[CapabilityStatus] = Field(default=None, description="""Current operational status""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    commissioned_date: Optional[date] = Field(default=None, description="""Date the capability was commissioned""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    leader: Optional[str] = Field(default=None, description="""Name of the capability lead or manager""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })
    future_expansion: Optional[str] = Field(default=None, description="""Notes on planned future expansion or related facilities""", json_schema_extra = { "linkml_meta": {'domain_of': ['Capability']} })


class Instrument(ConfiguredBaseModel):
    """
    A scientific instrument or piece of equipment that supports a capability.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nmdc/sfas-brcs'})

    name: Optional[str] = Field(default=None, description="""A human-readable name for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Person',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A human-readable description for an entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing',
                       'Institution',
                       'Dataset',
                       'Variable',
                       'ResearchResource',
                       'IsolateCollection',
                       'Technology',
                       'StudyDesign',
                       'NMDCStudyReference',
                       'FlagshipGenome',
                       'Capability',
                       'Instrument'],
         'slot_uri': 'schema:description'} })
    instrument_type: Optional[InstrumentType] = Field(default=None, description="""Type of instrument""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    manufacturer: Optional[str] = Field(default=None, description="""Manufacturer of the instrument""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    model: Optional[str] = Field(default=None, description="""Model name or number""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })
    count: Optional[int] = Field(default=None, description="""Number of instruments of this type""", json_schema_extra = { "linkml_meta": {'domain_of': ['Dataset', 'ResearchResource', 'Instrument']} })
    specifications: Optional[str] = Field(default=None, description="""Key specifications (e.g., resolution, sensitivity)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Instrument']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ResearchProgramCollection.model_rebuild()
CollectionMetadata.model_rebuild()
NamedThing.model_rebuild()
ResearchProgram.model_rebuild()
BioenergyResearchCenter.model_rebuild()
ScientificFocusArea.model_rebuild()
OtherProgram.model_rebuild()
ArtificialIntelligenceProject.model_rebuild()
UserFacility.model_rebuild()
Institution.model_rebuild()
Person.model_rebuild()
FundingInfo.model_rebuild()
Location.model_rebuild()
WebResources.model_rebuild()
Dataset.model_rebuild()
Variable.model_rebuild()
OntologyTerm.model_rebuild()
BERVOTerm.model_rebuild()
MIXSTerm.model_rebuild()
Reference.model_rebuild()
Finding.model_rebuild()
PrimaryReferenceInfo.model_rebuild()
ProgramOutputs.model_rebuild()
ResearchResource.model_rebuild()
ResourceIdentifier.model_rebuild()
IsolateCollection.model_rebuild()
FieldSite.model_rebuild()
Technology.model_rebuild()
WebReference.model_rebuild()
StudyDesign.model_rebuild()
NMDCStudyReference.model_rebuild()
Analysis.model_rebuild()
KBaseNarrative.model_rebuild()
FlagshipGenome.model_rebuild()
ReferenceData.model_rebuild()
Capability.model_rebuild()
Instrument.model_rebuild()
