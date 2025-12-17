#!/usr/bin/env python3
"""Generate interactive chord diagram visualizations for keyword/datatype associations.

Extracts co-occurrence relationships from the SFAs/BRCs database and generates
an interactive D3.js visualization showing:
- Keyword-keyword co-occurrence (which keywords appear together in studies)
- Datatype-datatype co-occurrence (which data modalities are generated together)
- Keyword-datatype associations (which keywords link to which data types)
"""

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "db" / "sfas-brcs.yaml"
TEMPLATE_DIR = SCRIPT_DIR / "templates"
OUTPUT_PATH = SCRIPT_DIR.parent / "docs" / "associations.html"


def load_db() -> dict:
    """Load the YAML database."""
    with open(DB_PATH) as f:
        return yaml.safe_load(f)


def extract_study_associations(db: dict) -> dict[str, list[dict[str, Any]]]:
    """Extract keyword and datatype associations from studies.

    Returns dict with:
    - 'studies': list of study records with keywords and data_modalities
    - 'programs': list of program records with keywords and data_types
    """
    studies = []
    programs = []

    # Process all program types
    program_collections = [
        ('bioenergy_research_centers', 'BRC'),
        ('genomic_science_sfas', 'GS-SFA'),
        ('environmental_system_science_sfas', 'ESS-SFA'),
        ('user_facilities', 'Facility'),
        ('other_programs', 'Other'),
    ]

    for collection_key, program_type in program_collections:
        for program in db.get(collection_key, []):
            program_name = program.get('acronym') or program.get('name', 'Unknown')

            # Program-level keywords and data types
            program_keywords = program.get('keywords', [])
            program_data_types = program.get('data_types', [])

            if program_keywords or program_data_types:
                programs.append({
                    'name': program_name,
                    'type': program_type,
                    'keywords': program_keywords,
                    'data_types': program_data_types,
                })

            # Study-level keywords and data modalities
            for study in program.get('studies', []):
                study_name = study.get('name', 'Unnamed study')
                study_keywords = study.get('keywords', [])
                study_modalities = study.get('data_modalities', [])

                # Inherit program keywords if study has none
                if not study_keywords:
                    study_keywords = program_keywords[:3]  # Take top 3 from program

                if study_keywords or study_modalities:
                    studies.append({
                        'name': study_name,
                        'program': program_name,
                        'program_type': program_type,
                        'keywords': study_keywords,
                        'data_modalities': study_modalities,
                    })

    return {'studies': studies, 'programs': programs}


def build_cooccurrence_matrix(items: list[list[str]], min_count: int = 1) -> dict:
    """Build co-occurrence matrix from lists of items.

    Args:
        items: List of lists, where each inner list contains co-occurring items
        min_count: Minimum co-occurrence count to include

    Returns:
        Dict with 'nodes' (unique items) and 'links' (co-occurrence counts)
    """
    cooccurrence = defaultdict(int)
    item_counts = defaultdict(int)

    for item_list in items:
        # Count individual occurrences
        for item in item_list:
            item_counts[item] += 1

        # Count co-occurrences (pairs)
        for a, b in combinations(sorted(set(item_list)), 2):
            cooccurrence[(a, b)] += 1

    # Filter by minimum count
    links = [
        {'source': a, 'target': b, 'value': count}
        for (a, b), count in cooccurrence.items()
        if count >= min_count
    ]

    # Get nodes that appear in links
    nodes_in_links = set()
    for link in links:
        nodes_in_links.add(link['source'])
        nodes_in_links.add(link['target'])

    nodes = [
        {'name': name, 'count': item_counts[name]}
        for name in sorted(nodes_in_links)
    ]

    return {'nodes': nodes, 'links': links}


def build_bipartite_associations(
    items_a: list[str],
    items_b: list[str],
    records: list[dict],
    key_a: str,
    key_b: str,
    min_count: int = 1
) -> dict:
    """Build bipartite association data (e.g., keyword-datatype).

    Args:
        items_a: All possible items of type A
        items_b: All possible items of type B
        records: List of records containing both types
        key_a: Key to access type A items in records
        key_b: Key to access type B items in records
        min_count: Minimum association count to include

    Returns:
        Dict with 'nodes' and 'links' for bipartite visualization
    """
    associations = defaultdict(int)
    counts_a = defaultdict(int)
    counts_b = defaultdict(int)

    for record in records:
        a_items = record.get(key_a, [])
        b_items = record.get(key_b, [])

        for a in a_items:
            counts_a[a] += 1
            for b in b_items:
                associations[(a, b)] += 1

        for b in b_items:
            counts_b[b] += 1

    # Build links
    links = [
        {'source': a, 'target': b, 'value': count}
        for (a, b), count in associations.items()
        if count >= min_count
    ]

    # Get nodes that appear in links
    nodes_a_in_links = set()
    nodes_b_in_links = set()
    for link in links:
        nodes_a_in_links.add(link['source'])
        nodes_b_in_links.add(link['target'])

    nodes = []
    for name in sorted(nodes_a_in_links):
        nodes.append({'name': name, 'count': counts_a[name], 'group': 'keyword'})
    for name in sorted(nodes_b_in_links):
        nodes.append({'name': name, 'count': counts_b[name], 'group': 'datatype'})

    return {'nodes': nodes, 'links': links}


def generate_visualization_data(db: dict) -> dict:
    """Generate all visualization data from the database."""
    data = extract_study_associations(db)
    studies = data['studies']
    programs = data['programs']

    # Keyword-keyword co-occurrence (from studies)
    keyword_lists = [s['keywords'] for s in studies if s['keywords']]
    keyword_cooccurrence = build_cooccurrence_matrix(keyword_lists, min_count=1)

    # Datatype-datatype co-occurrence (from studies)
    datatype_lists = [s['data_modalities'] for s in studies if s['data_modalities']]
    datatype_cooccurrence = build_cooccurrence_matrix(datatype_lists, min_count=1)

    # Keyword-datatype associations (from studies)
    keyword_datatype = build_bipartite_associations(
        items_a=[],  # Will be populated from records
        items_b=[],
        records=studies,
        key_a='keywords',
        key_b='data_modalities',
        min_count=1
    )

    # Program-level data for context
    program_keyword_lists = [p['keywords'] for p in programs if p['keywords']]
    program_keyword_cooccurrence = build_cooccurrence_matrix(program_keyword_lists, min_count=1)

    return {
        'keyword_keyword': keyword_cooccurrence,
        'datatype_datatype': datatype_cooccurrence,
        'keyword_datatype': keyword_datatype,
        'program_keywords': program_keyword_cooccurrence,
        'stats': {
            'study_count': len(studies),
            'program_count': len(programs),
            'unique_keywords': len(set(k for s in studies for k in s.get('keywords', []))),
            'unique_datatypes': len(set(d for s in studies for d in s.get('data_modalities', []))),
        }
    }


def create_jinja_env() -> Environment:
    """Create and configure Jinja2 environment."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def generate_html(viz_data: dict) -> str:
    """Generate the HTML page from templates."""
    env = create_jinja_env()
    template = env.get_template("associations.html.j2")
    return template.render(
        viz_data_json=json.dumps(viz_data, indent=2),
        stats=viz_data['stats']
    )


def main():
    """Main entry point."""
    print(f"Loading database from {DB_PATH}")
    db = load_db()

    print("Extracting associations...")
    viz_data = generate_visualization_data(db)

    print(f"  Studies: {viz_data['stats']['study_count']}")
    print(f"  Programs: {viz_data['stats']['program_count']}")
    print(f"  Unique keywords: {viz_data['stats']['unique_keywords']}")
    print(f"  Unique datatypes: {viz_data['stats']['unique_datatypes']}")
    print(f"  Keyword-keyword links: {len(viz_data['keyword_keyword']['links'])}")
    print(f"  Datatype-datatype links: {len(viz_data['datatype_datatype']['links'])}")
    print(f"  Keyword-datatype links: {len(viz_data['keyword_datatype']['links'])}")

    print("Generating HTML visualization...")
    html = generate_html(viz_data)

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing to {OUTPUT_PATH}")
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)

    print(f"Done! Open {OUTPUT_PATH} in a browser.")


if __name__ == "__main__":
    main()
