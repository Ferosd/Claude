# Law Firm — Document Automation (n8n)

Production-ready n8n automation that takes a client intake submission, uses AI to classify the case, generates Google Doc deliverables from templates, runs a Slack approval flow, dispatches via DocuSign for e-signature, archives to Google Drive, and syncs to Airtable + (optional) Clio.

## Files

| File | Purpose |
|---|---|
| [`document-automation.json`](./document-automation.json) | Importable n8n export. Contains **two** workflows in one array: `Law Firm — Document Automation v1` (main) and `Law Firm — DocuSign Signed Handler v1` (post-signature webhook). |
| [`SETUP-GUIDE.md`](./SETUP-GUIDE.md) | Step-by-step setup: env vars, credentials, Google Drive/Docs, DocuSign Connect, Airtable schema, Slack bot, end-to-end test, 7-day per-firm onboarding playbook. |
| [`test-payloads/`](./test-payloads) | 3 sample intake JSONs (PI, Immigration, Family Law) + `test-webhook.sh` curl driver. |
| [`template-examples/`](./template-examples) | Markdown reference templates (engagement letter, HIPAA auth, fee agreement) with the `{{PLACEHOLDER}}` syntax that the Google Docs `replaceAllText` API expects. |

## Quick start

```bash
# 1. Import into n8n
#    Workflows → Import from file → document-automation.json

# 2. Set env vars (see SETUP-GUIDE.md §2)

# 3. Wire credentials (OpenAI, Google Drive/Docs, Gmail, Slack, Airtable, DocuSign)

# 4. Smoke test
cd test-payloads && ./test-webhook.sh https://adriens.app.n8n.cloud/webhook-test/law-firm-intake personal-injury
```

## Architecture

```
Webhook → Normalize → Build Placeholders → AI Classify
   → Switch (PI/IMM/FAM/RE/ESTATE/OTHER) → Set template folder
   → Create case folder → Loop docs (List → Copy → batchUpdate)
   → Aggregate → Slack approval → Wait (24h timeout)
   → IF approved
        ├ Yes → Loop DocuSign (Export PDF → Encode → Create envelope)
        │       → Aggregate envelopes → Airtable create → Welcome email → Slack pipeline
        └ No  → Slack reject → Airtable log
```

Separately (handler workflow):

```
DocuSign Connect webhook → Extract → Lookup case → Download signed PDF
   → Upload to Drive → Update Airtable counter
   → IF all signed
        ├ Yes → Welcome email + Slack notify + (Clio sync if enabled) → Ack
        └ No  → Log progress → Ack
```

## Tier flexibility

Same JSON serves all three tiers. Toggle via env vars:

- `MULTI_ATTORNEY_ENABLED` — Scale tier multi-attorney routing
- `STRIPE_ENABLED` — payment collection step
- `CLIO_ENABLED` — Clio sync in handler workflow

See `SETUP-GUIDE.md §10` for tier-by-tier configuration.
