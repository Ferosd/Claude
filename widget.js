/**
 * Coremagna Chat Widget
 * Self-contained — injects its own CSS, no external deps.
 * All classes prefixed .cm- to avoid conflicts.
 */
(function () {
  'use strict';

  /* ── Constants ── */
  const WEBHOOK_URL = 'https://sarahxs.app.n8n.cloud/webhook/chatbot-webhook';
  const BOOKING_URL = 'https://calendar.app.google/XDGM8XJ9zEdqugKr9';
  const TIMEOUT_MS  = 10000;
  const WELCOME_MSG = 'Hi! 👋 I\'m Coremagna\'s AI assistant.\nI can help you learn about our services — web design, AI chatbots, and automation.\nWhat brings you here today?';

  /* ── Inject CSS ── */
  const style = document.createElement('style');
  style.textContent = `
    .cm-widget{position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;flex-direction:column;align-items:flex-end;gap:12px;font-family:'DM Sans','Segoe UI',sans-serif}

    /* Trigger button */
    .cm-trigger{width:56px;height:56px;border-radius:50%;background:#00D4AA;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 4px 16px rgba(0,212,170,0.35),0 2px 6px rgba(0,0,0,0.3);transition:transform 0.25s cubic-bezier(0.34,1.56,0.64,1),box-shadow 0.25s cubic-bezier(0.4,0,0.2,1);flex-shrink:0}
    .cm-trigger:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(0,212,170,0.45),0 2px 8px rgba(0,0,0,0.3)}
    .cm-trigger:active{transform:scale(0.96)}
    .cm-trigger svg{width:24px;height:24px;fill:none;stroke:#060a0e;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
    /* Pulse ring */
    .cm-trigger::before{content:'';position:absolute;inset:-4px;border-radius:50%;border:2px solid rgba(0,212,170,0.45);animation:cm-pulse 2.2s ease-out infinite;pointer-events:none}
    .cm-trigger::after{content:'';position:absolute;inset:-10px;border-radius:50%;border:1px solid rgba(0,212,170,0.2);animation:cm-pulse 2.2s ease-out 0.5s infinite;pointer-events:none}
    @keyframes cm-pulse{0%{transform:scale(1);opacity:1}100%{transform:scale(1.45);opacity:0}}

    /* Panel */
    .cm-panel{width:380px;height:520px;background:#0d1317;border:0.5px solid rgba(0,212,170,0.15);border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.4),0 2px 8px rgba(0,212,170,0.06);display:flex;flex-direction:column;overflow:hidden;transform-origin:bottom right;opacity:0;transform:scale(0.92) translateY(12px);transition:opacity 0.28s cubic-bezier(0.4,0,0.2,1),transform 0.28s cubic-bezier(0.34,1.56,0.64,1);pointer-events:none}
    .cm-panel.cm-open{opacity:1;transform:scale(1) translateY(0);pointer-events:all}

    /* Header */
    .cm-header{background:#111920;border-bottom:0.5px solid rgba(0,212,170,0.1);padding:14px 16px;display:flex;align-items:center;gap:10px;flex-shrink:0}
    .cm-header-info{display:flex;align-items:center;gap:8px;flex:1;min-width:0}
    .cm-online-dot{width:8px;height:8px;border-radius:50%;background:#00D4AA;flex-shrink:0;animation:cm-dot-pulse 2s ease-in-out infinite}
    @keyframes cm-dot-pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.55;transform:scale(0.85)}}
    .cm-agent-name{font-size:14px;font-weight:600;color:#F0F4F3;letter-spacing:-0.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .cm-close{width:28px;height:28px;border-radius:6px;background:none;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;color:rgba(240,244,243,0.45);font-size:18px;line-height:1;transition:color 0.2s cubic-bezier(0.4,0,0.2,1),background 0.2s cubic-bezier(0.4,0,0.2,1);flex-shrink:0}
    .cm-close:hover{color:#F0F4F3;background:rgba(255,255,255,0.06)}

    /* Messages */
    .cm-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
    .cm-messages::-webkit-scrollbar{width:4px}
    .cm-messages::-webkit-scrollbar-track{background:transparent}
    .cm-messages::-webkit-scrollbar-thumb{background:rgba(0,212,170,0.2);border-radius:2px}

    /* Bubbles */
    .cm-msg-row{display:flex;flex-direction:column;gap:4px}
    .cm-msg-row.cm-user{align-items:flex-end}
    .cm-bubble{max-width:85%;font-size:14px;line-height:1.6;padding:10px 14px;word-break:break-word;white-space:pre-wrap}
    .cm-bubble-bot{background:#111920;border:0.5px solid rgba(0,212,170,0.1);border-radius:4px 16px 16px 16px;color:#F0F4F3}
    .cm-bubble-user{background:#00D4AA;border-radius:16px 16px 4px 16px;color:#060a0e;font-weight:500}

    /* Booking button */
    .cm-book-btn{display:block;width:100%;padding:11px 16px;background:#00D4AA;color:#060a0e;border:none;border-radius:8px;font-size:13px;font-weight:700;letter-spacing:0.02em;cursor:pointer;text-align:center;text-decoration:none;margin-top:6px;transition:background 0.2s cubic-bezier(0.4,0,0.2,1),transform 0.2s cubic-bezier(0.34,1.56,0.64,1)}
    .cm-book-btn:hover{background:#00f0c4;transform:translateY(-1px)}
    .cm-book-btn:active{transform:translateY(0)}

    /* Typing indicator */
    .cm-typing{display:flex;align-items:center;gap:4px;padding:12px 14px;background:#111920;border:0.5px solid rgba(0,212,170,0.1);border-radius:4px 16px 16px 16px;width:fit-content}
    .cm-typing span{width:6px;height:6px;border-radius:50%;background:rgba(0,212,170,0.5);display:block;animation:cm-dot-bounce 1.2s ease-in-out infinite}
    .cm-typing span:nth-child(2){animation-delay:0.18s}
    .cm-typing span:nth-child(3){animation-delay:0.36s}
    @keyframes cm-dot-bounce{0%,80%,100%{transform:scale(0.75);opacity:0.5}40%{transform:scale(1.1);opacity:1}}

    /* Input */
    .cm-input-area{border-top:0.5px solid rgba(0,212,170,0.1);background:#111920;padding:12px 16px;display:flex;align-items:center;gap:10px;flex-shrink:0}
    .cm-input{flex:1;background:transparent;border:none;outline:none;color:#F0F4F3;font-size:14px;font-family:inherit;line-height:1.5;resize:none;min-height:24px;max-height:80px;overflow-y:auto}
    .cm-input::placeholder{color:rgba(240,244,243,0.3)}
    .cm-send{width:36px;height:36px;border-radius:50%;background:#00D4AA;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background 0.2s cubic-bezier(0.4,0,0.2,1),transform 0.2s cubic-bezier(0.34,1.56,0.64,1)}
    .cm-send:hover{background:#00f0c4;transform:scale(1.07)}
    .cm-send:active{transform:scale(0.95)}
    .cm-send:disabled{background:rgba(0,212,170,0.3);cursor:not-allowed;transform:none}
    .cm-send svg{width:16px;height:16px;fill:none;stroke:#060a0e;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}

    /* Mobile */
    @media(max-width:480px){
      .cm-widget{bottom:16px;right:16px;left:16px;align-items:flex-end}
      .cm-trigger{width:48px;height:48px}
      .cm-trigger svg{width:20px;height:20px}
      .cm-panel{width:100%;height:100%;position:fixed;inset:0;border-radius:0;transform-origin:bottom center}
    }
  `;
  document.head.appendChild(style);

  /* ── Build HTML ── */
  const widget = document.createElement('div');
  widget.className = 'cm-widget';
  widget.setAttribute('role', 'region');
  widget.setAttribute('aria-label', 'Chat with Coremagna AI');
  widget.innerHTML = `
    <div class="cm-panel" id="cmPanel" aria-live="polite" aria-hidden="true">
      <div class="cm-header">
        <div class="cm-header-info">
          <span class="cm-online-dot" aria-hidden="true"></span>
          <span class="cm-agent-name">Coremagna AI</span>
        </div>
        <button class="cm-close" id="cmClose" aria-label="Close chat">×</button>
      </div>
      <div class="cm-messages" id="cmMessages" role="log" aria-relevant="additions"></div>
      <div class="cm-input-area">
        <textarea class="cm-input" id="cmInput" placeholder="Type a message..." rows="1" aria-label="Chat message"></textarea>
        <button class="cm-send" id="cmSend" aria-label="Send message">
          <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
    </div>
    <button class="cm-trigger" id="cmTrigger" aria-label="Open chat" aria-expanded="false">
      <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    </button>
  `;
  document.body.appendChild(widget);

  /* ── State ── */
  const panel    = document.getElementById('cmPanel');
  const trigger  = document.getElementById('cmTrigger');
  const closeBtn = document.getElementById('cmClose');
  const messages = document.getElementById('cmMessages');
  const input    = document.getElementById('cmInput');
  const sendBtn  = document.getElementById('cmSend');

  let isOpen       = false;
  let hasWelcomed  = false;
  let isSending    = false;
  let typingEl     = null;

  /* ── Helpers ── */
  function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  function appendBubble(text, role) {
    const row = document.createElement('div');
    row.className = 'cm-msg-row' + (role === 'user' ? ' cm-user' : '');
    const bubble = document.createElement('div');
    bubble.className = 'cm-bubble ' + (role === 'user' ? 'cm-bubble-user' : 'cm-bubble-bot');
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    scrollToBottom();
    return row;
  }

  function appendBookingBtn(parentRow) {
    const btn = document.createElement('a');
    btn.className = 'cm-book-btn';
    btn.href      = BOOKING_URL;
    btn.target    = '_blank';
    btn.rel       = 'noopener noreferrer';
    btn.textContent = 'Book a Free Call →';
    parentRow.appendChild(btn);
    scrollToBottom();
  }

  function showTyping() {
    typingEl = document.createElement('div');
    typingEl.className = 'cm-typing';
    typingEl.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(typingEl);
    scrollToBottom();
  }

  function hideTyping() {
    if (typingEl) { typingEl.remove(); typingEl = null; }
  }

  function setLoading(loading) {
    isSending     = loading;
    sendBtn.disabled = loading;
    input.disabled   = loading;
  }

  /* ── Open / Close ── */
  function openPanel() {
    isOpen = true;
    panel.classList.add('cm-open');
    panel.setAttribute('aria-hidden', 'false');
    trigger.setAttribute('aria-expanded', 'true');
    if (!hasWelcomed) {
      hasWelcomed = true;
      appendBubble(WELCOME_MSG, 'bot');
    }
    setTimeout(() => input.focus(), 300);
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('cm-open');
    panel.setAttribute('aria-hidden', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.focus();
  }

  trigger.addEventListener('click', () => isOpen ? closePanel() : openPanel());
  closeBtn.addEventListener('click', closePanel);

  /* ── Send message ── */
  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isSending) return;

    input.value = '';
    input.style.height = '';
    appendBubble(text, 'user');
    setLoading(true);
    showTyping();

    const controller = new AbortController();
    const timeoutId  = setTimeout(() => controller.abort(), TIMEOUT_MS);

    let botRow;
    try {
      const res = await fetch(WEBHOOK_URL, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ message: text }),
        signal:  controller.signal
      });
      clearTimeout(timeoutId);
      const raw = await res.text();

      let data;
      try { data = JSON.parse(raw); } catch (_) { data = { message: raw }; }

      hideTyping();
      const reply = (data && (data.reply || data.message || data.text || data.output)) || raw || 'Got your message!';
      botRow = appendBubble(reply, 'bot');

      if (data && data.show_booking) {
        appendBookingBtn(botRow);
      }
    } catch (err) {
      clearTimeout(timeoutId);
      hideTyping();
      const msg = err.name === 'AbortError'
        ? 'Taking longer than usual. Please try again.'
        : 'Connection issue. Please try again.';
      appendBubble(msg, 'bot');
    } finally {
      setLoading(false);
      input.focus();
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  /* Auto-resize textarea */
  input.addEventListener('input', () => {
    input.style.height = '';
    input.style.height = Math.min(input.scrollHeight, 80) + 'px';
  });

  /* Close on Escape */
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) closePanel();
  });

})();
