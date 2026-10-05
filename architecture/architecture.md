# Architecture

The system separates deterministic integrations and calculations from AI reasoning.

## Runtime

~~~text
Manager
  |
  v
AI Orchestrator
  |------------------|
  v                  v
CRM Agent        Telephony Agent
  |                  |
amoCRM API       Telephony API
  |                  |
  v                  v
PostgreSQL        Audio -> STT
                       |
                       v
                 LLM analysis
                       |
                       v
                 Analytics Agent
                       |
                       v
                 Report Generator
                       |
                       v
              Confidence / policy gate
                  |           |
                safe       review
                  |           |
                  +-----+-----+
                        v
                     Manager
~~~

## Agent responsibilities

### Orchestrator
Converts a natural-language request into a bounded report job, coordinates agents, tracks status and enforces the final validation gate.

### CRM Agent
Authenticates with amoCRM, retrieves deals/tasks, normalizes identifiers/timestamps and preserves source references.

### Telephony Agent
Retrieves call metadata and authorized recordings, sends audio to STT and attaches transcript segments to call IDs.

### Analytics Agent
Runs deterministic KPI calculations first, then performs semantic analysis over validated transcript data.

### Report Generator
Creates a manager-facing report from structured findings. Important conclusions retain source IDs or calculation provenance.

### Storage

PostgreSQL stores normalized records, transcripts, KPIs, analysis results and report versions. S3-compatible object storage holds audio where retention is permitted. Redis can hold job state and cache.

### Human review gate

Low-confidence findings and high-impact employment/customer actions are escalated to a human before being presented as approved recommendations.
