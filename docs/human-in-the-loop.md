# Human-in-the-Loop

The system uses a review gate instead of assuming that an LLM output is automatically correct.

## Automatic delivery

A report can be delivered automatically when:
- source coverage is sufficient;
- deterministic metrics pass validation;
- transcript quality is acceptable;
- no high-impact action is proposed;
- semantic findings meet the configured confidence threshold.

## Human review

Escalate when:
- source data is incomplete;
- recordings are missing or unintelligible;
- the model contradicts structured facts;
- confidence is below threshold;
- the conclusion concerns discipline, compensation, termination or another high-impact employment decision;
- a customer or contractual commitment could be affected.

The reviewer sees the finding, evidence, source IDs, confidence and model/version metadata before approval.
