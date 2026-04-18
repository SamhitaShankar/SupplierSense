import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from langchain.tools import tool

from agents.base import make_bedrock_llm


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@tool
def fetch_news_signals(query: str, date_range: str) -> List[Dict[str, Any]]:
    """Fetch news disruption signals. For now this returns realistic stubbed news items."""
    return [
        {
            "source": "NewsAPI-stub",
            "type": "geo",
            "headline": "Port workers strike threatens container movement in Chennai",
            "raw_text": "Labor unrest near Chennai port may delay exports for electronics and textiles suppliers.",
            "affected_region": "Chennai, India",
            "affected_commodities": ["electronics", "textiles"],
            "timestamp": _utc_now_iso(),
        },
        {
            "source": "NewsAPI-stub",
            "type": "geo",
            "headline": "Heavy rainfall warning issued for Tamil Nadu logistics corridors",
            "raw_text": "Transport corridors connecting supplier clusters face rain-related disruption risk.",
            "affected_region": "Tamil Nadu, India",
            "affected_commodities": ["packaged foods", "consumer goods"],
            "timestamp": _utc_now_iso(),
        },
    ]


@tool
def fetch_weather_alerts(geo_bbox: str) -> List[Dict[str, Any]]:
    """Fetch weather alerts. For now this returns realistic stubbed NOAA-shaped alerts."""
    return [
        {
            "source": "NOAA-stub",
            "type": "weather",
            "event": "Severe Rainfall Alert",
            "raw_text": "Severe rainfall may impact road movement and port handling operations.",
            "affected_region": "South India Coast",
            "affected_commodities": ["general cargo"],
            "timestamp": _utc_now_iso(),
        }
    ]


@tool
def fetch_shipping_delays(port_codes: str) -> List[Dict[str, Any]]:
    """Fetch shipping delays. For now this returns stubbed MarineTraffic-style port delay data."""
    return [
        {
            "source": "MarineTraffic-stub",
            "type": "shipping",
            "port_code": "INMAA",
            "raw_text": "Average vessel waiting time increased to 18 hours due to congestion.",
            "affected_region": "Chennai Port",
            "affected_commodities": ["electronics", "appliances"],
            "timestamp": _utc_now_iso(),
        }
    ]


@tool
def fetch_financial_signals(ticker_list: str) -> List[Dict[str, Any]]:
    """Fetch supplier financial signals. For now this returns stubbed Alpha Vantage-style data."""
    return [
        {
            "source": "AlphaVantage-stub",
            "type": "financial",
            "ticker": "SUPX",
            "raw_text": "Supplier stock declined 7% over 5 trading sessions amid margin pressure concerns.",
            "affected_region": "India",
            "affected_commodities": ["electronics components"],
            "timestamp": _utc_now_iso(),
        }
    ]


@tool
def normalize_signals(raw_list_json: str) -> List[Dict[str, Any]]:
    """Normalize mixed raw signals into the shared SignalEvent shape using Bedrock."""
    llm = make_bedrock_llm()

    prompt = f"""
You are a supply-chain signal normalizer.

Convert the raw input list into a JSON array.
Each item must contain exactly these keys:
id, type, source, raw_text, severity, affected_region, affected_commodities, timestamp, confidence

Rules:
- type must be one of: weather, financial, geo, shipping, regulatory, social
- severity must be a float from 0.0 to 1.0
- confidence must be a float from 0.0 to 1.0
- affected_commodities must be a list of strings
- timestamp must be an ISO-8601 string
- Return ONLY valid JSON array, no markdown

Raw input:
{raw_list_json}
""".strip()

    response = llm.invoke(prompt)
    text = response.content if isinstance(response.content, str) else "".join(
        block.get("text", "") for block in response.content if isinstance(block, dict)
    )

    return json.loads(text)


@tool
def score_signal_severity(signal_json: str) -> float:
    """Score one normalized signal from 0.0 to 1.0 using Bedrock."""
    llm = make_bedrock_llm()

    prompt = f"""
You are a supply-chain risk scoring assistant.

Given this signal, return ONLY a single number between 0.0 and 1.0.
No explanation. No markdown.

Signal:
{signal_json}
""".strip()

    response = llm.invoke(prompt)
    text = response.content if isinstance(response.content, str) else "".join(
        block.get("text", "") for block in response.content if isinstance(block, dict)
    )

    return float(text.strip())