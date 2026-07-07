# Coremagna AI Voice Agent — Kurulum Rehberi

Mimari: **Vapi** (telefon hattı + konuşma: STT Deepgram, LLM GPT-4o, TTS) ↔ **n8n** (takvim, CRM, bildirim).
Çağrı sırasında Vapi asistanı 3 aracı n8n webhook'una sorar; çağrı bitince özet raporu n8n'e düşer.

```
Arayan ──► Vapi (Max) ──tool-calls──► n8n /webhook/vapi-tools ──► Google Calendar + Sheets
                     └──end-of-call-report──► n8n /webhook/vapi-report ──► Sheets (Calls) + Gmail (Ferit'e özet)
```

Dosyalar:
- `automations/coremagna-voice-agent.json` — n8n workflow'u (import edilecek)
- `automations/vapi-assistant.json` — Vapi asistan tanımı (prompt + tool'lar)

---

## 0. Ön koşul: n8n dışarıdan erişilebilir olmalı

Vapi'nin sunucuları webhook'lara internetten ulaşacak; `localhost:5678` yetmez.
Tünel (ngrok sabit domain) veya Oracle/VPS kurulumu — hangisini seçtiysek onun HTTPS adresini not et.
Aşağıda her yerde `https://SENIN-N8N-ADRESIN` olarak geçiyor.

## 1. Google Sheet'i hazırla (2 dakika)

"Coremagna CRM" adında bir Sheet aç, **iki sekme** oluştur, başlık satırlarını birebir böyle yaz:

**Leads** sekmesi (1. satır):
```
Timestamp | Name | Phone | Email | Sector | Datetime | Notes | Status | Source
```

**Calls** sekmesi (1. satır):
```
Timestamp | Caller | DurationSec | EndedReason | Sector | Booked | Summary | Recording | Transcript
```

(Kolon adları workflow'daki otomatik eşlemeyle birebir aynı olmalı.)

## 2. n8n workflow'unu içe aktar

1. n8n → sol üst menü → **Import from File** → `automations/coremagna-voice-agent.json`
2. Kırmızı görünen node'lara tek tek gir ve kendi hesaplarını bağla:
   - **Get Day Events** ve **Create Calendar Event** → Google Calendar credential + takvim seç (dropdown)
   - **Log Booking / Log Lead / Log Call** → Google Sheets credential + "Coremagna CRM" dokümanını seç (sekme adları hazır: Leads / Calls)
   - **Email Ferit** → Gmail credential (alıcı ferit1@coremagna.com hazır)
3. Workflow'u **Active** yap. Webhook adreslerin şunlar olur:
   - `https://SENIN-N8N-ADRESIN/webhook/vapi-tools`
   - `https://SENIN-N8N-ADRESIN/webhook/vapi-report`

> Not: Test modunda URL `/webhook-test/...` olur ve sadece "Listen for test event" açıkken çalışır. Vapi'ye daima `/webhook/` (production) adresini ver ve workflow'u Active tut.

## 3. Vapi asistanını kur (dashboard.vapi.ai)

1. Hesap aç — deneme kredisi veriyorlar, kart istemeden test edebilirsin.
2. `automations/vapi-assistant.json` içindeki **iki `REPLACE-WITH-YOUR-N8N-DOMAIN`** kısmını kendi n8n adresinle değiştir (3 tool + 1 server URL).
3. Asistanı oluşturmanın iki yolu:
   - **API ile (önerilen, tek komut):**
     ```bash
     curl https://api.vapi.ai/assistant \
       -H "Authorization: Bearer VAPI_PRIVATE_KEY" \
       -H "Content-Type: application/json" \
       -d @automations/vapi-assistant.json
     ```
   - **Dashboard ile:** Assistants → Create → alanları dosyadan kopyala (System Prompt, First Message, model gpt-4o, ses). Tools sekmesinde 3 function tool'u tanımla (isim/parametre/Server URL dosyada hazır), sonra asistana ekle. Advanced → Server URL'e `/webhook/vapi-report` adresini yaz ve "end-of-call-report" mesajını işaretle.
4. Ses: `vapi / Elliot` ile başla; dashboard'da tek tıkla ElevenLabs seslerine geçebilirsin (İngiliz aksanlı profesyonel bir ses markaya daha çok yakışabilir — dinleyip seç).

## 4. Test — telefon numarası almadan

Dashboard'da asistanın sayfasındaki **"Talk to Assistant"** (web call) butonuyla ara:

- [ ] "What do you do and what does it cost?" → kilitli fiyatları doğru söylüyor mu?
- [ ] "Book me a call tomorrow" → müsaitlik soruyor, en fazla 2 slot öneriyor mu?
- [ ] İsim + telefon + e-posta verip onayla → **Sheets Leads'e satır düştü mü? Takvimde etkinlik var mı?**
- [ ] "Just have someone call me" → capture_lead çalışıp "Callback requested" satırı düştü mü?
- [ ] Çağrıyı kapat → **Calls sekmesine özet + sana Gmail geldi mi?**
- [ ] n8n → Executions ekranından her adımın yeşil olduğunu gör.

## 5. Telefon numarası

- **ABD numarası:** Vapi dashboard → Phone Numbers → ücretsiz US numarası al, asistana bağla. (Test ve ABD pazarı için yeterli.)
- **UK numarası:** Twilio'dan +44 numara al (~£1/ay) → Vapi → Phone Numbers → **Import from Twilio**. UK pazarına satışta siteye bu numara yazılır.

## 6. Maliyet gerçeği

Vapi dakika başı ücretlendirir (~$0.05-0.15/dk bileşen seçimine göre; STT+LLM+TTS dahil).
Ayda 100 çağrı × 3 dk ≈ $15-45 — müşteri demosu ve gelen lead için makul; sınırsız değil, dashboard'dan harcamayı izle.

## 7. Sonraki adım: siteye bağlama (hazır olunca söyle)

- demo.html'deki gizli "Voice Agent" kartını açarız → numarayı yazarız ("Call our AI right now").
- İstersek Vapi Web SDK ile sitede "Talk to our AI" butonu da eklenir (tarayıcıdan mikrofonla konuşma, numara gerektirmez) — bunu ben yaparım, tek script.

## Sorun giderme

| Belirti | Muhtemel sebep |
|---|---|
| Asistan "let me check" deyip donuyor | n8n workflow Active değil veya URL'de `/webhook-test/` kalmış |
| Tool cevabı geliyor ama asistan anlamıyor | Yanıt formatı bozuk — Respond node'una dokunulmuş; `results[].toolCallId` korunmalı |
| Sheets'e satır düşmüyor | Sekme adı/başlıklar rehberdekiyle birebir değil (autoMap başlığa göre eşler) |
| Takvim etkinliği yanlış saatte | Asistan datetime'ı UTC üretir; takvim saat dilimini kontrol et |
| Rapor maili gelmiyor | Vapi asistanında Server URL boş veya "end-of-call-report" işaretli değil |
