# Law Firm Document Automation — Setup Guide

End-to-end setup for the n8n workflow at `adriens.app.n8n.cloud`. Two workflows ship in `document-automation.json`:

1. **Law Firm — Document Automation v1** — main intake → docs → DocuSign flow
2. **Law Firm — DocuSign Signed Handler v1** — async webhook that fires when each envelope is signed

Plan for ~3–4 hours of first-time setup. Subsequent firms onboard in a day once your templates are stable.

---

## 1. Import the workflow into n8n cloud

1. Sign in to `https://adriens.app.n8n.cloud`.
2. Top-right **Workflows** → **Import from file** → select `document-automation.json`.
3. n8n imports both workflows because the file is a JSON array. You'll see them in the list as inactive.
4. Open each workflow in turn — every node will show a red badge until credentials and env vars are wired up. That's expected.

> If your n8n version refuses an array, split the file: keep `[0]` as `main.json` and `[1]` as `handler.json`, import each separately.

---

## 2. Environment variables

Cloud → top-right avatar → **Settings** → **Variables** (or **Environment**, depending on plan). Add every key. Values shown are examples.

```
FIRM_NAME=Smith & Partners LLP
FIRM_ADDRESS=123 Oxford Street, London W1D 2HG
FIRM_PHONE=+44 20 1234 5678
ATTORNEY_NAME=Sarah Jenkins
ADMIN_EMAIL=ops@smithpartners.example

# Google Drive folder IDs (from the URL: drive.google.com/drive/folders/<ID>)
GDRIVE_TEMPLATES_PI=1AbC...
GDRIVE_TEMPLATES_IMMIGRATION=1AbD...
GDRIVE_TEMPLATES_FAMILY=1AbE...
GDRIVE_TEMPLATES_RE=1AbF...
GDRIVE_TEMPLATES_ESTATE=1AbG...
GDRIVE_TEMPLATES_DEFAULT=1AbH...
GDRIVE_CLIENT_CASES_FOLDER=1AbI...

# Slack
SLACK_APPROVAL_CHANNEL=case-intake-approvals
SLACK_PIPELINE_CHANNEL=case-pipeline

# Airtable
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_CASES_TABLE=Cases

# DocuSign
DOCUSIGN_BASE_URL=https://demo.docusign.net
DOCUSIGN_ACCOUNT_ID=00000000-0000-0000-0000-000000000000
DOCUSIGN_ACCESS_TOKEN=... # bearer; rotated by your token-refresh workflow

# Tier flags
CLIO_ENABLED=false
STRIPE_ENABLED=false
MULTI_ATTORNEY_ENABLED=false

# Optional: only when CLIO_ENABLED=true
CLIO_ACCESS_TOKEN=...
```

After saving, **redeploy the workflows** so the env values rebind.

---

## 3. Google Drive — templates and case folders

### 3a. Folder structure

```
📁 Law Firm Workspace/
├── 📁 Templates/
│   ├── 📁 Personal Injury/        ← GDRIVE_TEMPLATES_PI
│   ├── 📁 Immigration/            ← GDRIVE_TEMPLATES_IMMIGRATION
│   ├── 📁 Family Law/             ← GDRIVE_TEMPLATES_FAMILY
│   ├── 📁 Real Estate/            ← GDRIVE_TEMPLATES_RE
│   ├── 📁 Estate Planning/        ← GDRIVE_TEMPLATES_ESTATE
│   └── 📁 Default/                ← GDRIVE_TEMPLATES_DEFAULT
└── 📁 Client Cases/               ← GDRIVE_CLIENT_CASES_FOLDER (one subfolder per client)
```

### 3b. Template documents

Templates **must be Google Docs** (not Word). Naming convention is critical because the workflow searches for templates by `documentKey`:

| documentKey | Filename in folder |
|---|---|
| `engagement_letter` | Engagement Letter |
| `hipaa_authorization` | HIPAA Authorization |
| `medical_records_release` | Medical Records Release |
| `conflict_check` | Conflict Check |
| `fee_agreement` | Fee Agreement |
| `retainer_agreement` | Retainer Agreement |
| `g28_authorization` | G-28 Authorization |
| `immigration_questionnaire` | Immigration Questionnaire |
| `financial_disclosure` | Financial Disclosure |
| `parenting_plan` | Parenting Plan |
| `custody_agreement` | Custody Agreement |
| `deed_transfer` | Deed Transfer |
| `title_search` | Title Search |
| `will_template` | Will |
| `trust_template` | Trust |
| `power_of_attorney` | Power of Attorney |

The Google Drive search uses partial matching, so `engagement_letter` matches a doc named "Engagement Letter v3 (UK)". Keep filenames distinct **within each folder** so the right template wins.

### 3c. Placeholder syntax

Inside each template, use this exact syntax (case-sensitive, double curly braces):

```
{{CLIENT_NAME}}        {{CLIENT_EMAIL}}    {{CLIENT_PHONE}}
{{CASE_TYPE}}          {{INCIDENT_DATE}}   {{INCIDENT_LOCATION}}
{{INJURY_DETAILS}}     {{INSURANCE_PROVIDER}}  {{INSURANCE_POLICY}}
{{DATE_TODAY}}         {{FIRM_NAME}}       {{FIRM_ADDRESS}}
{{ATTORNEY_NAME}}      {{CASE_ID}}
```

The `Replace Placeholders (Google Docs API)` node iterates `placeholders` and runs one `replaceAllText` request per key. See `template-examples/` for ready-to-paste samples.

### 3d. DocuSign anchor

At every signature spot, place the literal string `/sn1/` in white 1pt text. DocuSign auto-detects it and drops a sign-here tab there. (Configurable in the `Create DocuSign Envelope` node body.)

---

## 4. Configure n8n credentials

Open each workflow → click any flagged node → **Create new credential**.

| Node uses | Credential type | Notes |
|---|---|---|
| Classify Case Type | OpenAI API (`openAiApi`) | API key from `platform.openai.com/api-keys`. |
| Find Template File / Copy / Create Folder / Export PDF / Upload Signed | Google Drive OAuth2 (`googleDriveOAuth2Api`) | OAuth via Google Cloud Console. Add `https://app.n8n.cloud/rest/oauth2-credential/callback` to the Authorized redirect URIs. |
| Replace Placeholders (Google Docs API) | Google Docs OAuth2 (`googleDocsOAuth2Api`) | Same Google Cloud project; enable **Google Docs API**. |
| Welcome Email — Initial / Welcome Email — Case Active | Gmail OAuth2 (`gmailOAuth2`) | Send-as access on the firm address. |
| Send Slack Approval Request, Notify Pipeline, etc. | Slack OAuth2 (`slackOAuth2Api`) | Bot token with `chat:write`, `channels:read`. |
| Create Airtable Case / Lookup / Update | Airtable Personal Access Token (`airtableTokenApi`) | Scoped to the base. |
| Create DocuSign Envelope / Download Signed PDF | HTTP Header Auth (`httpHeaderAuth`) | Header name: `Authorization`. Value: `Bearer {{ $env.DOCUSIGN_ACCESS_TOKEN }}` — or hard-code the token here and skip the env var. |
| Create Clio Contact / Matter | HTTP Header Auth (`httpHeaderAuth`) | `Authorization: Bearer <CLIO_TOKEN>`. Only used when `CLIO_ENABLED=true`. |

After each credential is saved, the node's red badge clears.

---

## 5. DocuSign developer setup

1. Sign up at `https://developers.docusign.com/` and grab the **demo account ID** + **base URL** (`https://demo.docusign.net`).
2. **Apps and Keys** → **Add App** → keep the **Integration Key**.
3. **JWT Grant** flow recommended:
   - Generate an RSA keypair, paste the public key into the app config.
   - Service-account user grants application consent once: `https://account-d.docusign.com/oauth/auth?response_type=code&scope=signature%20impersonation&client_id=<INTEGRATION_KEY>&redirect_uri=https://adriens.app.n8n.cloud/`
4. **Token-refresh workflow (separate, not in this file).** Build a small n8n cron workflow that hits `https://account-d.docusign.com/oauth/token` with the JWT assertion every 50 minutes and writes the new access token into the `DOCUSIGN_ACCESS_TOKEN` env var via the n8n API. Or, simpler for a starter tier: paste a long-lived token manually each day.
5. **Connect (signed-handler webhook):**
   - Settings → **Connect** → **Add Configuration** → **Custom**.
   - URL: `https://adriens.app.n8n.cloud/webhook/docusign-signed` (production) or `/webhook-test/docusign-signed` (test mode while editing).
   - Trigger events: **Envelope Signed/Completed**.
   - Include: `Recipients`, `Custom Fields`.
   - Format: **JSON**.
6. Send a test envelope through the demo. The handler workflow should receive a webhook within 30 s.

---

## 6. Airtable schema — `Cases` table

Create one base, one table named exactly `Cases` (or change `AIRTABLE_CASES_TABLE`). Field types:

| Field | Type | Notes |
|---|---|---|
| Case ID | Single line text | Primary field, e.g. `PI-20260507-MW`. |
| Client Name | Single line text | |
| Email | Email | |
| Phone | Phone | |
| Case Type | Single line text | Free text from intake. |
| Sub Type | Single line text | AI-derived. |
| Status | Single select | Options: `Awaiting Signature`, `Partial Signed`, `Active Case`, `Rejected at Review`. |
| Documents Sent | Number | Integer. |
| Documents Signed | Number | Integer, defaults 0. |
| DocuSign Envelope IDs | Long text | One envelope per line. |
| Case Folder URL | URL | |
| Case Folder ID | Single line text | Optional — fills if you wire up a Set node. |
| Created At | Date (with time) | ISO timestamp. |
| Last Signed At | Date (with time) | |
| Attorney Assigned | Single line text | Filled from `ATTORNEY_NAME` env. |
| Priority | Single select | `HIGH`, `MEDIUM`, `LOW`. |

Copy the base ID from `airtable.com/<BASE_ID>/api/docs` → put it in `AIRTABLE_BASE_ID`.

---

## 7. Slack setup

1. Create a Slack app at `https://api.slack.com/apps` → **From scratch** → install to your workspace.
2. **OAuth & Permissions** scopes: `chat:write`, `channels:read`, `im:write`.
3. Install to workspace, copy **Bot User OAuth Token** into the n8n Slack credential.
4. Create the channels referenced by the env vars (`#case-intake-approvals`, `#case-pipeline`).
5. Invite the bot user to both channels (`/invite @YourBot`).
6. **Approval action buttons.** The workflow uses Slack's button **URL** field (not interactive payloads) so no Events API is required — the buttons hit the n8n Wait node's resume URL with `?status=approved|rejected`. This is the simplest pattern but means anyone with the URL can approve. For tighter control, switch to interactive payloads + a small `/slack/actions` webhook handler.

---

## 8. End-to-end test

```bash
cd test-payloads
./test-webhook.sh https://adriens.app.n8n.cloud/webhook-test/law-firm-intake
```

Expected sequence:

1. `Intake Webhook` fires → fields normalized.
2. `Classify Case Type` returns JSON like `{"category":"PERSONAL_INJURY","requiredDocuments":[...]}`.
3. `Route by Case Type` exits the **PERSONAL_INJURY** branch.
4. `Create Client Case Folder` creates `PI-20260507-MW - Marcus Williams` under `Client Cases`.
5. `Loop Over Documents` iterates ~5 times — one Google Doc copy + batchUpdate per doc.
6. `Send Slack Approval Request` posts to `#case-intake-approvals` — click **Approve & Send**.
7. `Loop For DocuSign` creates one envelope per doc; client receives DocuSign emails.
8. `Create Airtable Case` adds the row; `Welcome Email — Initial` lands in client inbox.
9. Sign each DocuSign envelope on the demo signer page.
10. `DocuSign Webhook` fires; handler downloads + uploads signed PDF, updates Airtable counter.
11. After the last envelope: `Welcome Email — Case Active` and `Notify Attorney — Case Open`.

If any step stalls, open the failed execution in n8n, expand the node, and read the error tab. The Code nodes have inline `console.log` that surfaces in the **Console** tab.

---

## 9. Per-firm onboarding (7-day playbook)

Reuse this workflow JSON for every new firm. The only changes are credentials, env vars, and templates.

| Day | Task |
|---|---|
| 1 | Discovery call. Capture firm letterhead, attorney names, case types they accept, signature anchor preferences. Provision Google Workspace + DocuSign demo + Slack workspace if firm doesn't have one. |
| 2 | Duplicate the workflows in n8n (Workflows → ⋯ → **Duplicate**). Rename to `<Firm Name> — Document Automation v1` etc. Create a new Airtable base from a template duplicate. |
| 3 | Build template Google Docs from firm letterhead. Insert all `{{PLACEHOLDERS}}`. Place in case-type subfolders. |
| 4 | Connect credentials (Google, Slack, Gmail, OpenAI, DocuSign). Fill env vars. Run a manual test with a fake client. |
| 5 | DocuSign Connect webhook configured + verified. Anchor `/sn1/` placement validated on every template. |
| 6 | UAT with 2-3 real intakes (with consent). Watch every execution. Fix template prose, tweak Slack copy. |
| 7 | Activate both workflows. Hand over the Airtable view + a 1-page admin doc describing the approval channel and how to revoke a sent envelope. |

---

## 10. Tier toggles (Starter / Growth / Scale)

Same JSON serves all tiers — branches are gated by env vars.

- **Starter** (single case type, email-only): set every `GDRIVE_TEMPLATES_*` to the same starter folder, `MULTI_ATTORNEY_ENABLED=false`, ignore Slack approval (deactivate `Send Slack Approval Request` + connect `Aggregate Documents → Loop Documents → DocuSign` directly). Skip Airtable by deactivating `Create Airtable Case`.
- **Growth** (Slack approval, Airtable sync, 3 case types): default state of the JSON.
- **Scale** (Clio sync, multi-attorney, Stripe payment): set `CLIO_ENABLED=true` and supply `CLIO_ACCESS_TOKEN`. The handler workflow's `Clio Sync Enabled?` IF node already routes to the Clio create-contact + create-matter chain. Add Stripe payment by inserting a `Stripe → Create Customer` node after `Create Airtable Case` gated on `STRIPE_ENABLED`.

---

## 11. Error handling

- Every external-API node has `continueOnFail: true` plus `retryOnFail: true` with 2–3 attempts and `waitBetweenTries` = 2–4 s. n8n's native retry uses exponential-ish backoff per attempt.
- For workflow-level failures, create one **Error Trigger** workflow:
  1. New workflow → add `Error Trigger` node.
  2. Add Slack → channel `automation-errors`, message `=⚠️ {{$json.execution.error.message}} in {{$json.workflow.name}}`.
  3. Add Gmail → recipient `={{ $env.ADMIN_EMAIL }}`.
  4. In the main workflow's **Settings → Error Workflow**, select this new workflow.
- DocuSign 401s usually mean an expired access token. Fix the token-refresh workflow rather than retrying.

---

## 12. Security checklist

- [ ] No credentials hard-coded in nodes — all use `{{ $env.X }}` or n8n credentials.
- [ ] Webhook paths use unguessable suffixes (n8n auto-appends a UUID in production mode — use the production URL, not `/webhook-test/`).
- [ ] DocuSign Connect set to **HMAC** with a shared secret if available; verify in a Code node before processing.
- [ ] Slack approval URLs expire when the Wait node resumes — they're single-use, but anyone with the URL can act on them. Consider switching to an Events API + signed-payload verifier for compliance-heavy firms.
- [ ] Airtable PAT scoped to a single base, single workspace.
- [ ] Restrict Google OAuth scopes to `drive.file` + `documents` rather than full `drive`.
