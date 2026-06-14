"""Validate the per-study/-site LinkML profiles: load each via SchemaView (resolving
imports against base.yaml) and confirm every slot range resolves to a known
type/class/enum. Exits non-zero on any problem. Run with: just validate-profiles
"""

import glob
import sys
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

SCHEMAS = Path(__file__).resolve().parent
BUILTIN = {
    "string", "integer", "boolean", "float", "double", "decimal", "time", "date",
    "datetime", "uriorcurie", "curie", "uri", "ncname", "objectidentifier",
    "nodeidentifier", "jsonpointer", "jsonpath", "sparqlpath",
}


def main() -> int:
    files = sorted(glob.glob(str(SCHEMAS / "studies" / "*.yaml")) +
                   glob.glob(str(SCHEMAS / "sites" / "*.yaml")))
    problems = []
    for f in [str(SCHEMAS / "base.yaml")] + files:
        sv = SchemaView(f)
        known = set(sv.all_enums()) | set(sv.all_classes()) | set(sv.all_types()) | BUILTIN
        for sname, slot in sv.all_slots().items():
            if slot.range and slot.range not in known:
                problems.append(f"{Path(f).name}: slot '{sname}' has unresolved range '{slot.range}'")

    print(f"Checked base.yaml + {len(files)} profiles.")
    if problems:
        print(f"FAILED with {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("All profiles valid: load, imports resolve, ranges resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
