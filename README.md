🇩🇪 [Deutsche Version](README_DE.md)

# Ticket Classification (Structured Output)

## Problem
Support teams receive tickets as free text. Without structure, there is no way
to prioritize them or to analyze which categories/urgency levels dominate.
Goal: reliably convert free text into a fixed JSON format (category,
urgency, sentiment).

## PM Decision
The first version used plain enum values without definitions — the model
categorized login problems with identical content inconsistently and rated
almost everything as "high" as soon as the tone sounded frustrated. Instead of
working with few-shot examples (more tokens, less generalizable), I gave every
enum value an explicit condition in the tool schema — including the constraint
that tone must play no role in urgency. Details: docs/decisions.md.

## Architecture Sketch
Free-text ticket → Claude Haiku 4.5 with forced tool call (tool_choice) →
validated JSON (category, urgency, sentiment). No framework, direct use of
the anthropic Python package.

## Evaluation Results
6 synthetic test tickets, 3 iterations:
1. Enums without descriptions: category inconsistency on login topics, urgency inflation (4/6 "high")
2. + enum descriptions: categories consistent, urgency still skewed by tone
3. + tone-independent urgency definition: all 6 classifications plausible

## Cost & Latency
- Cost per 1000 requests: $1.37 (Haiku 4.5, $1/$5 per million tokens, as of Sept 2026)
- Avg. latency: 0.88s, p95: 0.96s (indicative only, n=6)
- Avg. input tokens: 1030, avg. output tokens: 68

## Learnings
Enum values alone are not enough — without a definition, the model interprets
them inconsistently. The biggest lever was not a different model or a longer
prompt, but precise conditions directly in the tool schema. Tone and urgency
are easy to confuse unless you explicitly rule it out.

## What I Would Do Differently
With only 6 test cases, calibration cannot really be verified — that belongs
structurally in UC2 (Evaluation Harness) with a larger goldset instead of
spot-check eyeballing.
