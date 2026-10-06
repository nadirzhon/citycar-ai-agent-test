# CityCar — AI Agent Architecture Case Study

**A production-oriented design for evidence-based sales analytics with AI agents.**

This repository demonstrates how I would design an AI system that answers a manager's request:

> «Проанализируй работу отдела продаж за последние 30 дней».

The system combines CRM data and call analysis, separates deterministic metrics from model-generated interpretation, and routes sensitive or low-confidence conclusions through human review.

## Architecture

```
Manager
   ↓
AI Orchestrator
   ├── CRM Agent ─────────→ amoCRM API
   ├── Telephony Agent ──→ calls / recordings
   ├── Analytics Agent
   └── Report Generator
            ↓
      Confidence / Impact Gate
         ↙           ↘
   auto-delivery    human review
```

## Agent responsibilities

### AI Orchestrator
- interprets the request and time range;
- starts the required agents;
- tracks execution state and confidence;
- combines structured and unstructured evidence.

### CRM Agent
Collects deals, pipeline state, responsible managers, values, tasks and overdue work through amoCRM API v4.

### Telephony Agent
Collects call metadata and recordings, sends required audio through speech-to-text, and stores transcript metadata. Raw recordings should not be exposed to the model unless necessary.

### Analytics Agent
Uses deterministic calculations for KPIs and AI analysis for qualitative signals such as objections, communication patterns and coaching opportunities.

### Report Generator
Produces an evidence-backed report with:

1. executive summary;
2. KPI table;
3. funnel and manager analysis;
4. problems with evidence;
5. call-quality findings;
6. recommendations;
7. confidence and data-quality notes.

## Human-in-the-loop

AI should not silently make high-impact employment decisions.

Human review is required for:
- disciplinary conclusions;
- compensation or target changes;
- customer-impacting actions;
- ambiguous cases;
- incomplete or low-quality evidence;
- low-confidence recommendations.

The design separates **what the data shows** from **what the model infers**.

## Data architecture

**PostgreSQL**
- normalized CRM snapshots
- call metadata
- transcripts
- KPI results
- analysis results
- report versions
- provenance

**S3-compatible object storage**
- permitted audio
- generated artifacts

**Redis**
- short-lived job state
- caching
- rate-limit coordination

Secrets remain outside source control.

## Data flow

```
request
  ↓
fixed time interval
  ↓
CRM + telephony ingestion
  ↓
normalization / transcription
  ↓
deterministic KPI calculation
  ↓
qualitative AI analysis
  ↓
evidence-backed report
  ↓
confidence / policy gate
  ↓
human review when required
```

## Integration example

The repository includes a Python amoCRM example in `src/amocrm_overdue_deals.py`.

It demonstrates:
- `GET /api/v4/leads`;
- task lookup through `GET /api/v4/tasks`;
- detection of deals without tasks;
- detection of overdue incomplete tasks;
- environment-based credentials.

For production I would add pagination, retry/backoff, rate-limit handling, batching where supported, structured logging and metrics.

## Production evolution

A production implementation should add:

- OAuth/token refresh;
- webhook-driven incremental sync;
- idempotent ingestion and job IDs;
- asynchronous workers/queue;
- encrypted object storage;
- STT and LLM provider abstractions;
- PII redaction before model calls;
- RBAC and audit logs;
- evaluation datasets;
- human-review queue;
- confidence calibration;
- monitoring for latency, coverage, failures, cost and report quality;
- automated tests and CI.

## Related engineering work

This case study reflects patterns used in my other AI systems: agent orchestration, API integrations, asynchronous services, event-driven processing, observability and human-in-the-loop controls.

## Repository structure

```
citycar-ai-agent-test/
├── README.md
├── architecture/
├── docs/
├── src/
├── requirements.txt
└── .env.example
```

## License

Educational / technical case study.
