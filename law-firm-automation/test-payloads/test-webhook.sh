#!/usr/bin/env bash
# Fire each test intake at the n8n webhook.
# Usage:
#   ./test-webhook.sh                         # uses production URL
#   ./test-webhook.sh https://.../webhook-test/law-firm-intake   # test mode
#   ./test-webhook.sh <url> personal-injury   # only one payload

set -euo pipefail

DEFAULT_URL="https://adriens.app.n8n.cloud/webhook/law-firm-intake"
URL="${1:-$DEFAULT_URL}"
ONLY="${2:-}"

DIR="$(cd "$(dirname "$0")" && pwd)"
PAYLOADS=("personal-injury" "immigration" "family-law")

post() {
  local name="$1"
  local file="$DIR/test-${name}.json"
  echo "── POST ${name} → ${URL} ──"
  curl -sS -X POST "$URL" \
    -H "Content-Type: application/json" \
    --data-binary "@${file}" \
    -w "\nHTTP %{http_code} in %{time_total}s\n\n"
}

if [[ -n "$ONLY" ]]; then
  post "$ONLY"
  exit 0
fi

for name in "${PAYLOADS[@]}"; do
  post "$name"
  sleep 2  # avoid hammering credit-limited APIs (OpenAI, Google) during a back-to-back test
done
