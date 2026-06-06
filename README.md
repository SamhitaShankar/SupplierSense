# SupplierSense: AI-Powered Supply Chain Resilience Intelligence Platform

## Overview

SupplierSense is an AI-driven supply chain intelligence platform designed to detect supplier disruptions early, assess their downstream impact, and recommend actionable response strategies.

The system continuously analyzes external signals such as news events, weather alerts, financial indicators, and logistics disruptions to help organizations proactively manage supplier risk.

This project is being developed as an academic and research prototype using a multi-agent architecture powered by LangGraph and AWS Bedrock.

---

## Key Features

* Real-time disruption signal monitoring
* Multi-agent workflow orchestration using LangGraph
* Supplier risk assessment and scoring
* SKU impact analysis and inventory simulation
* Automated response playbook generation
* Redis-backed execution state management
* PostgreSQL persistence layer
* Interactive frontend dashboard for monitoring runs
* Cloud-native LLM integration using AWS Bedrock

---

## System Architecture

```text
External Data Sources
    ├── NewsAPI
    ├── NOAA Weather Alerts
    ├── Alpha Vantage
    └── Shipping Signal Providers
                │
                ▼
      A1: Signal Harvester
                │
                ▼
      A2: Supplier Analyzer
                │
                ▼
      A3: Impact Modeler
                │
                ▼
      A4: Inventory Optimizer
                │
                ▼
      A5: Response Planner
                │
                ▼
      A6: Orchestrator
                │
                ▼
    FastAPI + Redis + PostgreSQL
                │
                ▼
        React Frontend Dashboard
```

---

## Technology Stack

### AI & Agent Frameworks

* LangGraph
* LangChain
* AWS Bedrock
* Anthropic Claude (Bedrock-hosted)

### Backend

* FastAPI
* Python 3.10+
* Redis
* PostgreSQL
* Celery

### Frontend

* React
* TypeScript
* Vite
* Zustand

### Infrastructure

* Docker
* Docker Compose
* AWS

### Monitoring

* LangSmith

---

## Repository Structure

```text
SupplierSense/
├── agents/
├── api/
├── core/
├── data/
├── frontend/
├── graph/
├── tests/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/SamhitaShankar/SupplierSense.git
cd SupplierSense
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Configuration

Copy:

```bash
.env.example
```

to:

```bash
.env
```

and populate the required credentials.

---

## Running the Development Environment

Start infrastructure services:

```bash
docker compose up
```

Services:

* PostgreSQL → localhost:5432
* Redis → localhost:6379
* FastAPI Stub → localhost:8000

---

## Testing

Run pipeline validation:

```bash
python -m graph.pipeline
```

Run automated tests:

```bash
pytest
```

---

## Current Development Status

Completed components include:

* Shared state interfaces
* Mock data fixtures
* LangGraph workflow skeleton
* Dockerized development environment
* AWS Bedrock integration
* Signal Harvester foundation
* Supplier Analyzer implementation
* Impact Modeler implementation
* Inventory Optimizer implementation
* FastAPI backend skeleton
* Frontend dashboard prototype
* Redis-backed execution state management

Additional agents and integrations are under active development.

---

## Branching Strategy

* `main` → Stable public snapshot
* `dev` → Integration branch
* `feature/*` → Individual feature development

Examples:

* `feature/agent-signal-harvester`
* `feature/agent-supplier-analyzer`
* `feature/frontend`
* `feature/full-integration`

---

## Future Enhancements

* Live shipping data integrations
* Advanced supplier knowledge retrieval
* Enhanced scenario simulations
* Slack and email notifications
* Production deployment pipeline

---

## Contributors

Developed as part of an academic AI engineering initiative focused on building resilient and intelligent supply chain systems.

