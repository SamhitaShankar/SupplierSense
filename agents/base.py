from dotenv import load_dotenv
from langchain.agents import create_agent
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


def make_agent(tools, system_prompt: str):
    llm = make_bedrock_llm()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent