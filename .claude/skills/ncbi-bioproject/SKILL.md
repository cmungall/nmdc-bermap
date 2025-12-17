---
name: ncbi-bioproject
description: Skills for enriching study entries with NCBI BioProject metadata. Use this when you see studies with bioproject_ids (PRJNA...) that could be enriched with sample counts, publication DOIs, or organism information.
---

# NCBI BioProject Enrichment

This skill helps enrich study entries in `db/sfas-brcs.yaml` with metadata from NCBI BioProject.

## When to Use

Use this skill when:
- A study has `bioproject_ids` but is missing `sample_count`, `primary_reference`, or `organism`
- You need to verify or supplement study metadata
- The user asks to enrich studies from NCBI

## Command Line Tool

The script `scripts/enrich_from_ncbi.py` fetches metadata from NCBI.

### Fetch full metadata

```bash
uv run scripts/enrich_from_ncbi.py PRJNA561781
```

Output (YAML):
```yaml
bioproject_id: PRJNA561781
title: Native Miscanthus rhizosphere and endophytic microbiome
description: Survey of the native Miscanthus rhizosphere...
organism: soil metagenome
sample_count: 466
submitter_organization: University of Illinois at Urbana-Champaign
project_data_type: Targeted loci environmental
inferred_data_modality: AMPLICON_16S
```

### Get enrichment suggestions

```bash
uv run scripts/enrich_from_ncbi.py suggest PRJNA561781
```

This outputs only fields that would add new information to a study entry.

### Multiple BioProjects

```bash
uv run scripts/enrich_from_ncbi.py PRJNA561781 PRJNA733109 --format json
```

## Available Metadata

| Field | Description | Maps to Schema |
|-------|-------------|----------------|
| `sample_count` | Number of SRA runs | `Study.sample_count` |
| `primary_reference` | First linked publication DOI | `Study.primary_reference` |
| `organism` | Target organism | `Study.organism` |
| `inferred_data_modality` | Data type (AMPLICON, METAGENOMICS, etc.) | `Study.data_modalities` |
| `description` | Project description | `Study.description` |

## Data Modality Mapping

The script maps NCBI project data types to schema `DataModalityType`:

| NCBI Data Type | Schema Modality |
|----------------|-----------------|
| Metagenome | METAGENOMICS |
| Targeted loci / Targeted loci environmental | AMPLICON_16S |
| Genome sequencing | GENOMICS |
| Transcriptome | TRANSCRIPTOMICS |
| Metatranscriptome | METATRANSCRIPTOMICS |

## Example Workflow

1. Find a study with bioproject_ids but missing metadata:
   ```yaml
   - name: Native Miscanthus Rhizosphere Microbiome
     bioproject_ids:
     - PRJNA561781
     nmdc_ingest_priority: HIGH
   ```

2. Run enrichment:
   ```bash
   uv run scripts/enrich_from_ncbi.py suggest PRJNA561781
   ```

3. Update the study entry with suggested fields:
   ```yaml
   - name: Native Miscanthus Rhizosphere Microbiome
     bioproject_ids:
     - PRJNA561781
     sample_count: 466
     data_modalities:
     - AMPLICON_16S
     nmdc_ingest_priority: HIGH
   ```

## Rate Limits

NCBI E-utilities has rate limits:
- Without API key: 3 requests/second
- With API key: 10 requests/second

The script includes appropriate delays. For bulk operations, consider adding an API key.

## Direct API Access (Alternative)

If you need quick lookups without the script:

```bash
# BioProject summary
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=561781&retmode=json" | jq .

# SRA run count
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=PRJNA561781&retmode=json" | jq '.esearchresult.count'

# Linked PubMed articles
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=bioproject&db=pubmed&id=561781&retmode=json" | jq .
```
