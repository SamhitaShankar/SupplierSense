import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.shared_tools.rag import rag_similarity_search


if __name__ == "__main__":
    results = rag_similarity_search.invoke(
        {
            "query": "suppliers in Southeast Asia with electronics or semiconductor exposure and past disruption risk",
            "top_k": 3,
        }
    )
    print(results)