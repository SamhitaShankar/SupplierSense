import json
import os

import boto3
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse


load_dotenv()


def make_bedrock_llm(
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 1200,
):
    model_id = model or os.getenv(
        "BEDROCK_LLM_MODEL_ID",
        "anthropic.claude-3-haiku-20240307-v1:0",
    )

    return ChatBedrockConverse(
        model=model_id,
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        temperature=temperature,
        max_tokens=max_tokens,
    )


def make_agent(tools, system_prompt: str):
    llm = make_bedrock_llm()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent


def _bedrock_runtime_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def embed_text_bedrock(
    text: str,
    model_id: str | None = None,
    dimensions: int | None = None,
) -> list[float]:
    """
    Generate a single dense embedding vector using Amazon Titan Text Embeddings V2.
    """
    if not text or not text.strip():
        raise ValueError("Input text for embedding cannot be empty.")

    model_id = model_id or os.getenv(
        "BEDROCK_EMBED_MODEL_ID",
        "amazon.titan-embed-text-v2:0",
    )
    dimensions = dimensions or int(os.getenv("BEDROCK_EMBED_DIMENSIONS", "1024"))

    client = _bedrock_runtime_client()

    body = {
        "inputText": text,
        "dimensions": dimensions,
        "normalize": True,
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    result = json.loads(response["body"].read())

    if "embedding" in result and result["embedding"]:
        return result["embedding"]

    embeddings_by_type = result.get("embeddingsByType", {})
    if "float" in embeddings_by_type and embeddings_by_type["float"]:
        return embeddings_by_type["float"]

    raise ValueError(f"Unexpected embedding response format: {result}")