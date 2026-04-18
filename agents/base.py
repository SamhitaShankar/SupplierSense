from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse


load_dotenv()


def make_bedrock_llm(
    model: str = "anthropic.claude-3-haiku-20240307-v1:0",
    temperature: float = 0.1,
    max_tokens: int = 1200,
):
    return ChatBedrockConverse(
        model=model,
        region_name="us-east-1",
        temperature=temperature,
        max_tokens=max_tokens,
    )