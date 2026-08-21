# LeadFlow — Python-Native Rebuild

A raw-Python rebuild of two production automations I originally built in n8n: **LeadFlow** (ICP-based lead scoring) and **IntentIQ** (AI reply classification). Built to prove I can operate at the code level, not just the no-code/UI level.

## What it does

`pipeline.py` runs an end-to-end GTM workflow:

1. **Score & tier leads** — reads a CSV of leads and applies a multi-condition ICP scoring function (industry, company size, geography, decision-maker title, and source), assigning each lead to Tier 1 (priority), Tier 2 (secondary), or Tier 3 (disqualified — held for manual review).
2. **Draft outreach copy** — for each Tier 1 lead, calls the Claude API directly (no automation platform) to generate a short, personalized cold outreach opener.
3. **Write back to CRM** — updates each Tier 1 lead's tier property in HubSpot via the CRM API. *(Currently simulated — prints the exact API call that would be made, since this repo isn't connected to a live HubSpot account.)*

## Why this exists

The n8n versions of LeadFlow and IntentIQ are real, in-production systems I built for Furniture Arte. This rebuild exists to demonstrate the underlying logic without the no-code UI doing the wiring — API calls, authentication, error handling, and data transformation, written and understood line by line.

## Stack

- **Python 3.9**
- **pandas** — CSV loading, filtering, scoring, sorting
- **requests** — direct HTTP calls to the Claude API
- Environment variables for API key management (no secrets in code)

## Example output

```
Lead: Acme Sofas
Outreach: I came across Acme Sofas and wanted to reach out because we think we
can add real value to your production line. Furniture Arte specializes in
premium leather sofa covers, crafted with a fast turnaround so your
manufacturing schedule never skips a beat.

[SIMULATED HUBSPOT WRITE] Would update Acme Sofas — set Lead Tier = Tier 1
```

## Setup

```bash
pip3 install pandas requests
export ANTHROPIC_API_KEY="your-key-here"
python3 pipeline.py
```

## Files

| File | Purpose |
|---|---|
| `pipeline.py` | Main script — scoring, outreach drafting, simulated CRM write |
| `leads2.csv` | Sample lead data matching the ICP schema |
| `qualified_leads.csv` | Output — Tier 1/2 leads after scoring |

## What's simulated vs. real

- **Real:** CSV parsing, ICP scoring logic, live Claude API calls generating actual outreach copy
- **Simulated:** the HubSpot write — the function is structured exactly like the real API call (endpoint, auth header, payload shape) but doesn't execute against a live account

## Background

Built as part of a self-directed Python sprint to develop a second portfolio artifact alongside the original n8n-based systems, targeting GTM Engineer roles.
