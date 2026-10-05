# CityCar — AI Operator / AI Agent Test Assignment

## Goal

Design an AI system that can answer a manager's request:

> «Проанализируй работу отдела продаж за последние 30 дней».

The system combines CRM data from amoCRM and call recordings from the telephony provider, produces an evidence-based sales analysis, and escalates low-confidence or high-impact conclusions to a human.

## 1. Architecture

~~~mermaid
flowchart LR
    M[Manager] --> O[AI Orchestrator]
    O --> C[CRM Agent]
    O --> T[Telephony Agent]
    O --> A[Analytics Agent]
    O --> R[Report Generator]
    C --> AMO[amoCRM API v4]
    T --> TEL[Telephony API]
    TEL --> S[(Call recordings)]
    S --> STT[Speech-to-Text]
    STT --> LLM[LLM analysis]
    AMO --> D[(PostgreSQL)]
    LLM --> D
    A --> D
    D --> R
    R --> H{Confidence / impact check}
    H -->|High confidence| M
    H -->|Low confidence / sensitive| REV[Human review]
    REV --> M
    CACHE[(Redis / cache)] -.-> C
    CACHE -.-> T
~~~

### Components

**AI Orchestrator**
- Receives the natural-language request.
- Resolves the time range: last 30 days.
- Starts the required agents.
- Tracks execution status and confidence.
- Combines structured CRM metrics and call-analysis results.

**CRM Agent**
- Reads deals and tasks from amoCRM API v4.
- Collects pipeline, status, responsible manager, value, task completion and overdue-task information.
- Stores normalized snapshots for reproducible analysis.

**Telephony Agent**
- Gets call metadata and recordings through the telephony provider API.
- Downloads audio only when required.
- Sends audio through Speech-to-Text.
- Stores transcript, timestamps and call metadata.
- Does not expose raw recordings to the LLM unless necessary.

**Analytics Agent**
- Calculates deterministic KPIs first: number of deals, conversion, revenue/value, overdue tasks, activity and response speed.
- Uses an LLM for qualitative analysis: objections, communication quality, recurring failure patterns and coaching opportunities.
- Separates measured facts from model-generated interpretations.

**Report Generator**
Produces:
1. Executive summary.
2. KPI table.
3. Funnel and manager-level analysis.
4. Problems and evidence.
5. Call-quality findings.
6. Recommended actions.
7. Confidence and data-quality notes.

### Data flow

1. Manager asks for a 30-day sales analysis.
2. Orchestrator creates a report job with a fixed from/to interval.
3. CRM Agent pulls relevant deals/tasks from amoCRM.
4. Telephony Agent pulls calls for the same period.
5. Calls are transcribed and classified.
6. Analytics Agent combines deterministic metrics with transcript-derived signals.
7. Report Generator produces the final report.
8. Confidence and policy checks decide whether the report can be delivered automatically or requires human review.
9. The final report and provenance are stored.

### Storage

**PostgreSQL**
- normalized CRM snapshots
- call metadata
- transcripts
- KPI results
- analysis results
- report versions
- source/provenance references

**Object storage (S3-compatible)**
- original audio when retention is permitted
- generated artifacts

**Redis**
- short-lived job state
- caching
- rate-limit coordination

Secrets and API tokens are stored in a secrets manager/environment, never in source control.

---

## 2. What the system does itself vs. human-in-the-loop

### Automated

The system can automatically:
- collect data;
- normalize CRM and telephony records;
- transcribe calls;
- calculate deterministic KPIs;
- identify overdue/missing tasks;
- detect recurring patterns in calls;
- compare managers and periods;
- generate a draft report;
- attach evidence and source references;
- assign confidence scores.

### Human review

A human should remain responsible for:
- personnel decisions;
- disciplinary conclusions;
- changing compensation or targets;
- customer-impacting actions;
- conclusions based on incomplete/low-quality recordings;
- ambiguous cases where the model confidence is low;
- approving recommendations that can materially affect an employee or customer.

The AI should recommend and explain, not silently make high-impact employment decisions.

---

## 3. Main risks and limitations

### 1. Data quality and completeness
CRM records can be incomplete, calls can be missing, tasks can be incorrectly linked, and different systems can use different identifiers. The report must expose coverage and data-quality warnings.

### 2. STT/LLM errors
Speech recognition can mishear names, numbers or objections. LLMs can over-interpret conversations. Deterministic KPIs therefore come from structured data, while qualitative findings must include evidence and confidence.

### 3. Security and privacy
Call recordings and transcripts may contain personal or confidential information. Access must be role-based, data retention must be limited, secrets must not enter prompts/logs, and sensitive data must be protected in transit and at rest.

---

## 4. amoCRM integration example

The repository contains a small Python example in src/amocrm_overdue_deals.py.

It:
- calls GET /api/v4/leads;
- checks tasks through GET /api/v4/tasks;
- identifies deals without tasks;
- identifies deals with incomplete tasks whose complete_till is in the past;
- reads the access token and base URL from environment variables.

amoCRM documents GET /api/v4/leads for listing deals and GET /api/v4/tasks with filters including entity_type, entity_id and is_completed; task deadlines are represented by complete_till as a Unix timestamp.

For a production implementation I would add pagination, retry/backoff, rate-limit handling, batching where supported, structured logging and metrics.

---

## 5. Real AI project

### HEAN — event-driven AI/algorithmic trading platform

**Task:** build an automated research and trading platform capable of collecting market signals, evaluating strategies, managing execution and risk, and exposing system state through an operational dashboard.

**Stack:**
- Python
- FastAPI
- asyncio
- WebSocket
- Redis
- PostgreSQL
- Docker
- React / Vite
- Pydantic
- pytest
- C++ / Rust components for performance-sensitive workloads

**Architecture:**
- event-driven services;
- market-perception adapters;
- strategy and hypothesis layer;
- decision memory;
- execution routing;
- risk controls / kill switch;
- telemetry and monitoring;
- web dashboard.

The project is private, so implementation details and credentials are intentionally not exposed in this test repository.

---

## 6. What I learned independently during the last six months

I focused on practical AI-agent and backend engineering rather than only model prompting.

### Main areas

- LLM and AI-agent architectures.
- Multi-agent orchestration and tool calling.
- MCP and external-system integrations.
- Async Python with FastAPI and WebSockets.
- Event-driven architecture.
- Docker and reproducible service environments.
- PostgreSQL and Redis in distributed applications.
- OAuth/API authentication patterns.
- Observability, telemetry and operational debugging.
- Git/GitHub workflows and CI/CD.

### Application

I applied these technologies directly while developing HEAN: agents/services communicate through events, external APIs are isolated behind adapters, state is persisted, and telemetry is exposed so failures can be diagnosed instead of hidden.

---

## 7. Example of a self-proposed improvement

In the trading platform, I identified that event floods and queue saturation could make the system appear alive while important processing was delayed.

Instead of treating this only as an isolated bug, I proposed and implemented an observability layer:
- periodic heartbeat;
- telemetry aggregation;
- WebSocket telemetry topics;
- REST telemetry endpoints;
- portfolio/system summaries;
- clearer operational signals for diagnosing bottlenecks.

The result was a system where queue pressure, service health and processing state became visible and measurable, making debugging and further optimization substantially more systematic.

---

## Production evolution

For a production CityCar implementation I would add:
- OAuth/token refresh for amoCRM.
- Webhooks for incremental synchronization.
- Idempotent ingestion and job IDs.
- Async workers/queue.
- S3-compatible encrypted audio storage.
- STT provider abstraction.
- LLM provider abstraction and prompt/version registry.
- PII redaction before LLM processing.
- RBAC and audit logs.
- Evaluation dataset for call classification.
- Human review queue.
- Confidence calibration.
- Monitoring for latency, coverage, STT failure rate, token cost, report quality and API errors.
- Automated tests and CI.

## Repository structure

~~~
citycar-ai-agent-test/
├── README.md
├── architecture/
│   └── architecture.md
├── docs/
│   ├── ai-agents.md
│   ├── human-in-the-loop.md
│   └── experience.md
├── src/
│   └── amocrm_overdue_deals.py
├── .gitignore
├── .env.example
└── requirements.txt
~~~

## References

- amoCRM Leads API: https://www.amocrm.ru/developers/content/crm_platform/leads-api
- amoCRM Tasks API: https://www.amocrm.ru/developers/content/crm_platform/tasks-api
