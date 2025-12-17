#!/usr/bin/env python3
"""
Fetch metadata from NCBI BioProject to enrich study entries.

Usage:
    uv run scripts/enrich_from_ncbi.py PRJNA561781
    uv run scripts/enrich_from_ncbi.py PRJNA561781 PRJNA733109 --format yaml
"""

import json
import sys
import time
from typing import Optional

import typer
from Bio import Entrez

app = typer.Typer(help="Fetch NCBI BioProject metadata for study enrichment")

# Required by NCBI
Entrez.email = "nmdc-sfas-brcs@example.org"


def get_bioproject_uid(accession: str) -> Optional[str]:
    """Convert BioProject accession (PRJNA...) to UID."""
    handle = Entrez.esearch(db="bioproject", term=accession)
    result = Entrez.read(handle)
    handle.close()
    if result["IdList"]:
        return result["IdList"][0]
    return None


def fetch_bioproject_summary(uid: str) -> dict:
    """Fetch BioProject summary by UID."""
    import urllib.request
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id={uid}&retmode=json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data.get("result", {}).get(uid, {})


def fetch_sra_count(accession: str) -> int:
    """Get count of SRA runs linked to BioProject."""
    handle = Entrez.esearch(db="sra", term=accession, retmax=0)
    result = Entrez.read(handle)
    handle.close()
    return int(result.get("Count", 0))


def fetch_linked_pubmed(uid: str) -> list[str]:
    """Get PubMed IDs linked to BioProject."""
    handle = Entrez.elink(dbfrom="bioproject", db="pubmed", id=uid)
    result = Entrez.read(handle)
    handle.close()

    pmids = []
    for linkset in result:
        for linksetdb in linkset.get("LinkSetDb", []):
            if linksetdb.get("DbTo") == "pubmed":
                pmids.extend([link["Id"] for link in linksetdb.get("Link", [])])
    return pmids


def fetch_pubmed_doi(pmid: str) -> Optional[str]:
    """Get DOI from PubMed ID."""
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
    from Bio import Medline
    # Parse XML to get DOI
    import xml.etree.ElementTree as ET
    content = handle.read()
    handle.close()

    root = ET.fromstring(content)
    for article_id in root.findall(".//ArticleId"):
        if article_id.get("IdType") == "doi":
            return f"doi:{article_id.text}"
    return None


def infer_data_modality(project_data_type: str) -> Optional[str]:
    """Map NCBI project data type to schema DataModalityType."""
    mapping = {
        "metagenome": "METAGENOMICS",
        "targeted loci": "AMPLICON_16S",
        "targeted loci environmental": "AMPLICON_16S",
        "genome sequencing": "GENOMICS",
        "transcriptome": "TRANSCRIPTOMICS",
        "metatranscriptome": "METATRANSCRIPTOMICS",
        "raw sequence reads": "METAGENOMICS",
    }
    for key, value in mapping.items():
        if key in project_data_type.lower():
            return value
    return None


def enrich_from_bioproject(accession: str) -> dict:
    """
    Fetch all available metadata for a BioProject accession.

    Returns a dict with fields that can be used to enrich Study entries.
    """
    # Get UID from accession
    uid = get_bioproject_uid(accession)
    if not uid:
        return {"error": f"BioProject {accession} not found"}

    time.sleep(0.34)  # Rate limit: 3 requests/sec without API key

    # Fetch summary
    summary = fetch_bioproject_summary(uid)
    if not summary:
        return {"error": f"Could not fetch summary for {accession}"}

    time.sleep(0.34)

    # Fetch SRA count
    sra_count = fetch_sra_count(accession)

    time.sleep(0.34)

    # Fetch linked publications
    pmids = fetch_linked_pubmed(uid)
    dois = []
    for pmid in pmids[:3]:  # Limit to first 3
        time.sleep(0.34)
        doi = fetch_pubmed_doi(pmid)
        if doi:
            dois.append(doi)

    # Build enrichment data (field names from NCBI JSON use lowercase with underscores)
    result = {
        "bioproject_id": accession,
        "ncbi_uid": str(uid),
        "title": summary.get("project_title", ""),
        "description": summary.get("project_description", ""),
        "organism": summary.get("organism_name", ""),
        "taxid": summary.get("taxid"),
        "submitter_organization": summary.get("submitter_organization", ""),
        "registration_date": summary.get("registration_date", ""),
        "project_data_type": summary.get("project_data_type", ""),
    }

    # Add computed fields
    if sra_count > 0:
        result["sample_count"] = sra_count

    if dois:
        result["publication_dois"] = dois
        result["primary_reference"] = dois[0]

    modality = infer_data_modality(summary.get("project_data_type", ""))
    if modality:
        result["inferred_data_modality"] = modality

    return result


@app.command()
def enrich(
    bioproject_ids: list[str] = typer.Argument(..., help="BioProject accession(s) e.g. PRJNA561781"),
    format: str = typer.Option("yaml", "--format", "-f", help="Output format: yaml or json"),
):
    """Fetch NCBI metadata for one or more BioProject accessions."""
    results = []

    # Filter out empty strings
    bioproject_ids = [acc.strip() for acc in bioproject_ids if acc.strip()]

    for acc in bioproject_ids:
        typer.echo(f"Fetching {acc}...", err=True)
        data = enrich_from_bioproject(acc)
        results.append(data)
        time.sleep(0.5)  # Be nice to NCBI

    if format == "json":
        print(json.dumps(results if len(results) > 1 else results[0], indent=2))
    else:
        import yaml
        print(yaml.dump(results if len(results) > 1 else results[0],
                       default_flow_style=False, sort_keys=False))


@app.command()
def suggest(
    bioproject_id: str = typer.Argument(..., help="BioProject accession e.g. PRJNA561781"),
):
    """
    Suggest YAML snippet for enriching a Study entry.

    Outputs only fields that would add new information.
    """
    data = enrich_from_bioproject(bioproject_id)

    if "error" in data:
        typer.echo(f"Error: {data['error']}", err=True)
        raise typer.Exit(1)

    # Build suggestion with only useful fields
    suggestion = {}

    if data.get("sample_count"):
        suggestion["sample_count"] = data["sample_count"]

    if data.get("primary_reference"):
        suggestion["primary_reference"] = data["primary_reference"]

    if data.get("inferred_data_modality"):
        suggestion["# inferred_data_modality"] = data["inferred_data_modality"]

    if data.get("organism") and data["organism"] != "soil metagenome":
        suggestion["organism"] = data["organism"]

    typer.echo(f"\n# Suggested enrichments for {bioproject_id}:")
    typer.echo(f"# Title: {data.get('title', 'N/A')}")
    typer.echo(f"# Submitter: {data.get('submitter_organization', 'N/A')}")
    typer.echo(f"# Data type: {data.get('project_data_type', 'N/A')}")
    typer.echo()

    if suggestion:
        import yaml
        print(yaml.dump(suggestion, default_flow_style=False, sort_keys=False))
    else:
        typer.echo("# No additional enrichments found")


if __name__ == "__main__":
    app()
