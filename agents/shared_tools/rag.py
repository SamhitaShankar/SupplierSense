import os

from dotenv import load_dotenv
from langchain.tools import tool
from pinecone import Pinecone

from agents.base import embed_text_bedrock


load_dotenv()


def _get_index():
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "supplier-knowledge")

    if not api_key:
        raise ValueError("Missing PINECONE_API_KEY in environment.")

    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)


@tool
def rag_similarity_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Search Pinecone for suppliers semantically similar to the given query.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    index = _get_index()
    vector = embed_text_bedrock(query)

    result = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        namespace="suppliers",
    )

    matches = []
    raw_matches = getattr(result, "matches", []) or []

    for match in raw_matches:
        matches.append(
            {
                "id": getattr(match, "id", None),
                "score": getattr(match, "score", None),
                "metadata": getattr(match, "metadata", {}) or {},
            }
        )

    return matches