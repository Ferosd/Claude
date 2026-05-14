#!/usr/bin/env bash
# Test the Coremagna chatbot webhook (chat + voice)
# Usage:
#   ./test-chat.sh                          # uses production URL
#   ./test-chat.sh https://.../webhook-test/chatbot   # test mode

set -euo pipefail

BASE="${1:-https://adriens.app.n8n.cloud/webhook/chatbot}"

sep() { echo; echo "── $1 ──"; }

sep "Basic greeting (chat)"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi, what does Coremagna do?","session_id":"test-001","visitor_name":"Jane Test","visitor_email":"jane@test.com","page_url":"https://coremagna.com/","mode":"chat"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

sleep 1

sep "Pricing question — should trigger RAG hit on PRICING chunks"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the price of the Growth plan?","session_id":"test-001","visitor_name":"Jane Test","visitor_email":"jane@test.com","page_url":"https://coremagna.com/","mode":"chat"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

sleep 1

sep "Industry question — should trigger dental/medical chunk"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{"message":"Do you work with dental clinics?","session_id":"test-002","visitor_name":"Bob Dent","visitor_email":"bob@dental.com","page_url":"https://coremagna.com/rag-chatbot.html","mode":"chat"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

sleep 1

sep "Voice mode message (same endpoint, mode=voice)"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{"message":"How long does setup take?","session_id":"test-003","visitor_name":"Alice Voice","visitor_email":"alice@voice.com","page_url":"https://coremagna.com/","mode":"voice"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

sleep 1

sep "Lead completion — provides name + email + interest (should trigger Google Sheets save)"
curl -sS -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{"message":"My name is Marcus Williams, email marcus@restaurant.com. I run a restaurant chain with 3 locations. I need AI chatbot + reservation automation.","session_id":"test-004","visitor_name":"Marcus Williams","visitor_email":"marcus@restaurant.com","page_url":"https://coremagna.com/","mode":"chat"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"

echo
echo "Done. Check n8n execution log for RAG context and lead_data fields."
