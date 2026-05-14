# Coremagna Chatbot v2 — Setup Guide (RAG + Voice)

Two deliverables: an upgraded n8n workflow (adds Google Drive RAG) and a new chat widget (adds Voice tab). Existing lead capture — Google Sheets, Gmail, Calendar — is **untouched**.

---

## 1. Upload the knowledge base to Google Drive

1. Open Google Drive → your Coremagna workspace folder.
2. Upload `coremagna-knowledge-base.txt` (from this folder).
3. Open the file → copy the file ID from the URL:
   `https://drive.google.com/file/d/**1AbCdEfGhIjKlMnOpQrStUvWx**/view`
4. Keep the ID — you'll paste it as an n8n env var in step 3.

**Updating the knowledge base later:** Just edit the file in Google Drive. No workflow changes needed — the workflow downloads it fresh on every message.

---

## 2. Import the updated n8n workflow

### Option A — Replace entire workflow (clean import)
1. Sign in to `https://adriens.app.n8n.cloud`.
2. Open your existing chatbot workflow → click ⋯ → **Deactivate**.
3. **Workflows** → **Import from file** → select `coremagna-chatbot-v2.json`.
4. The new workflow imports as inactive. Wire credentials + env vars (steps 3–4 below), then activate.
5. Delete or keep the old workflow for reference.

### Option B — Add RAG nodes to existing workflow manually
If you've made customizations you want to keep:
1. Open your existing chatbot workflow in n8n.
2. Add a **Google Drive** node after the `Set Fields` node:
   - Resource: `File` / Operation: `Download`
   - File ID: `={{ $env.KNOWLEDGE_BASE_FILE_ID }}`
   - Credentials: your Google Drive OAuth2
3. Add a **Code** node after the Google Drive node. Paste the JavaScript from `RAG Search` node in `coremagna-chatbot-v2.json` (lines starting with `// Keyword-based RAG`).
4. Update your AI Agent/OpenAI node's system prompt: prepend the knowledge base context block (see `AI Agent` node in the workflow JSON — copy the system prompt from there).
5. Reconnect: `Set Fields → Google Drive Download KB → RAG Search → [your AI node]`.

---

## 3. Set environment variables

Cloud → avatar top-right → **Settings** → **Variables**:

```
KNOWLEDGE_BASE_FILE_ID=1AbCdEfGhIjKlMnOpQrStUvWx   ← from step 1
LEADS_SHEET_ID=your-google-sheets-id                 ← existing, if used
NOTIFICATION_EMAIL=ferit1@coremagna.com               ← who gets lead alerts
```

---

## 4. Wire credentials in the imported workflow

Click each flagged node → assign or create:

| Node | Credential type |
|---|---|
| `Google Drive — Download KB` | Google Drive OAuth2 (`googleDriveOAuth2Api`) |
| `AI Agent` | OpenAI API (`openAiApi`) |
| `Save Lead — Google Sheets` | Google Sheets OAuth2 (`googleSheetsOAuth2Api`) |
| `Gmail — Lead Notification` | Gmail OAuth2 (`gmailOAuth2`) |

All these credentials likely already exist in your n8n instance from the existing workflow — just re-select them.

---

## 5. Activate the workflow

Toggle the workflow from inactive → active. The webhook path remains `/webhook/chatbot` — no widget changes needed for this step.

---

## 6. Replace the chat widget

The new `chat-widget.js` is a drop-in replacement. It uses the **same webhook URL** and **same form gate** as the old widget.

### 6a. Copy the file
```bash
cp chatbot-upgrade/chat-widget.js /path/to/your/site/chat-widget.js
```

Or on the server, replace `widget.js` with `chat-widget.js` contents — they're both IIFE JS files.

### 6b. Update the script tag in index.html

The **existing** tag (line 1541 in `index.html`):
```html
<script src="widget.js" defer></script>
```

Change to:
```html
<script src="chat-widget.js" data-webhook="https://adriens.app.n8n.cloud/webhook/chatbot" defer></script>
```

The `data-webhook` attribute lets you override the URL per-page if needed. If omitted it defaults to the hardcoded production URL.

### 6c. Add to other pages
To embed on `rag-chatbot.html`, `automation.html`, etc.:
```html
<script src="/chat-widget.js" data-webhook="https://adriens.app.n8n.cloud/webhook/chatbot" defer></script>
```

---

## 7. Test chat mode

```bash
cd chatbot-upgrade && ./test-chat.sh
```

Expected response: `{"reply":"..."}` with Magna's text response.

Manual test:
1. Open the site.
2. The widget auto-opens after 5 seconds (or click the teal FAB).
3. Enter a name + email → click **Start Chatting**.
4. Type a question (e.g. "What's the Growth plan price?").
5. Magna should reply within a few seconds with pricing from the knowledge base.

Check n8n execution log: you should see `Google Drive — Download KB` download the file and `RAG Search` return relevant chunks in `rag_context`.

---

## 8. Test voice mode

1. Open the site in **Chrome or Edge** (voice requires Web Speech API).
2. Open the widget → enter name/email → **Start Chatting**.
3. Click the **🎤 Voice** tab.
4. Tap the microphone button — browser will ask for mic permission → **Allow**.
5. Speak a question (e.g. "What are your prices?").
6. You'll see the transcript appear, then "Thinking…", then Magna's response read aloud in a UK English voice.
7. The response also saves to chat history — switch to the **💬 Chat** tab to see it.

**Voice not working?**
- Must be Chrome or Edge (Firefox lacks `SpeechRecognition`).
- Must be on HTTPS (localhost:// works for local dev, plain http does not).
- Mic permission must be allowed — check the lock icon in the browser address bar.
- If voices don't load, reload the page once (browser sometimes needs a second pass to enumerate voices).

---

## 9. Browser compatibility for voice

| Browser | Speech-to-Text | Text-to-Speech |
|---|---|---|
| Chrome (desktop) | ✅ | ✅ |
| Edge (desktop) | ✅ | ✅ |
| Safari 16.4+ (desktop) | ✅ | ✅ |
| Firefox | ❌ | ✅ |
| Chrome (Android) | ✅ | ✅ |
| Safari (iOS) | Partial | ✅ |

When voice is not supported, the Voice tab shows a clear message: "Voice mode requires Chrome or Edge." The Chat tab continues to work normally on all browsers.

---

## 10. Updating the knowledge base

1. Open `coremagna-knowledge-base.txt` in Google Drive.
2. Edit the file — add new sections, update prices, add case studies.
3. Each section must:
   - Be separated by `---` on its own line
   - Be at least 20 characters
4. Save. No workflow restart needed — the workflow downloads the file fresh on every chat message.

**Best practice for adding a new industry section:**
```
---
INDUSTRY: ACCOUNTANCY FIRMS
We help UK accountancy firms automate client onboarding, document collection, and...
---
```

---

## 11. What the RAG Search actually does

1. Downloads the full knowledge base text from Google Drive.
2. Splits it by `---` into ~25 chunks (one per topic).
3. Takes the user's message and extracts words > 2 characters.
4. Scores each chunk: how many user words appear in the chunk text?
5. Takes the **top 3 chunks** with a score > 0.
6. Injects their text into the AI's system prompt as `KNOWLEDGE BASE CONTEXT`.
7. If no chunks score > 0 (very generic message), sends a fallback: "No specific context found. Answer based on general Coremagna knowledge."

This means Magna answers precisely from your business data without hallucinating services or prices that don't exist.

---

## 12. Architecture summary

```
Widget (Chat/Voice)
   │
   └─POST /webhook/chatbot
        │  { message, session_id, visitor_name, visitor_email, page_url, mode }
        │
        ▼
   Webhook → Set Fields → [Google Drive Download KB] → [RAG Search] → AI Agent
                                 ↑ NEW                    ↑ NEW         ↑ updated prompt
        │
        └─ Parse AI Response → Is Lead Complete?
                                      │
                               Yes ───┤── Save → Google Sheets
                                      │── Gmail notification
                                      └── Respond { reply }
                               No  ───└── Respond { reply }
```

Widget returns `reply` as either a chat bubble (Chat mode) or reads it aloud (Voice mode).
