from pprint import pprint

from agents.shared_tools.supplier_tools import (
    lookup_supplier_by_region,
    query_supplier_history,
    enrich_supplier_profile,
)


def main():
    print("\n=== SUPPLIERS IN TAMIL NADU ===")
    pprint(lookup_supplier_by_region("Tamil Nadu"))

    print("\n=== SUPPLIERS IN TAMIL NADU / electronics ===")
    pprint(lookup_supplier_by_region("Tamil Nadu", "electronics"))

    print("\n=== HISTORY FOR SUP001 ===")
    pprint(query_supplier_history("SUP001", limit=3))

    print("\n=== ENRICHED PROFILE FOR SUP001 ===")
    pprint(enrich_supplier_profile("SUP001"))


if __name__ == "__main__":
    main()