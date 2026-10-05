# AI Agents

| Agent | Responsibility | Mode |
|---|---|---|
| Orchestrator | Plans and coordinates analysis | Mostly deterministic |
| CRM Agent | Retrieves and normalizes amoCRM data | Deterministic |
| Telephony Agent | Retrieves recordings and transcripts | Deterministic + STT |
| Analytics Agent | KPI calculations and qualitative analysis | Deterministic + LLM |
| Report Generator | Produces the manager report | LLM over structured inputs |

## Narrow tool boundaries

Each agent receives only the tools required for its job:

- list_deals(from_ts, to_ts)
- list_tasks(deal_ids, from_ts, to_ts)
- list_calls(from_ts, to_ts)
- transcribe(call_id)
- calculate_kpis(dataset)
- generate_report(validated_findings)

Provider-specific API code stays behind adapters. This makes testing and provider replacement easier.
