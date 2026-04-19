import json
from typing import Any, Dict, List

from agents.interfaces import SupplierSenseState
from agents.signal_harvester.tools import (
    fetch_financial_signals,
    fetch_news_signals,
    fetch_shipping_delays,
    fetch_weather_alerts,
    normalize_signals,
    score_signal_severity,
)

print("Running Signal Harvester")
def _generate_signal_summary(signals: List[Dict[str, Any]]) -> str:
    if not signals:
        return "No disruption signals detected."

    regions = sorted({signal["affected_region"] for signal in signals})
    max_severity = max(signal["severity"] for signal in signals)
    count = len(signals)

    return (
        f"Collected {count} disruption signals across {', '.join(regions)}. "
        f"Highest observed severity is {max_severity:.2f}."
    )


def signal_harvester_agent(state: SupplierSenseState) -> SupplierSenseState:
    """
    A1 Signal Harvester:
    - reads nothing from state
    - writes only raw_signals and signal_summary
    """
    raw_inputs: List[Dict[str, Any]] = []

    raw_inputs.extend(fetch_news_signals.invoke({
        "query": "supplier disruption OR port delay OR weather disruption",
        "date_range": "last_7_days",
    }))
    raw_inputs.extend(fetch_weather_alerts.invoke({
        "geo_bbox": "south_india_bbox",
    }))
    raw_inputs.extend(fetch_shipping_delays.invoke({
        "port_codes": "INMAA,INTUT",
    }))
    raw_inputs.extend(fetch_financial_signals.invoke({
        "ticker_list": "SUPX,SUPY",
    }))

    normalized_signals = normalize_signals.invoke({
        "raw_list_json": json.dumps(raw_inputs)
    })

    rescored_signals: List[Dict[str, Any]] = []
    for signal in normalized_signals:
        severity = score_signal_severity.invoke({
            "signal_json": json.dumps(signal)
        })
        updated_signal = {**signal, "severity": round(float(severity), 2)}
        rescored_signals.append(updated_signal)

    signal_summary = _generate_signal_summary(rescored_signals)

    return {
        **state,
        "raw_signals": rescored_signals,
        "signal_summary": signal_summary,
    }