(function () {
  const WEBHOOK = 'https://sarahxs.app.n8n.cloud/webhook/chatbot-webhook';
  const ACCENT = '#00D4AA';
  const DARK = '#0d1317';
  const SURFACE = '#111920';
  const TEXT = '#F0F4F3';
  const MUTED = 'rgba(240,244,243,0.5)';

  let visitorName = '';
  let visitorEmail = '';
  let chatStarted = false;

  const css = `
    .cm-btn {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${ACCENT}; border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; transition: transform 0.2s;
    }
    .cm-btn:hover { transform: scale(1.08); }
    .cm-btn svg { width: 24px; height: 24px; }
    .cm-pulse {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${ACCENT}; opacity: 0.3;
      z-index: 99998; animation: cm-pulse 2s ease-out infinite;
      pointer-events: none;
    }
    @keyframes cm-pulse {
      0% { transform: scale(1); opacity: 0.3; }
      100% { transform: scale(1.8); opacity: 0; }
    }
    .cm-panel {
      position: fixed; bottom: 90px; right: 24px;
      width: 380px; height: 520px;
      background: ${DARK}; border-radius: 16px;
      border: 0.5px solid rgba(0,212,170,0.15);
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      display: flex; flex-direction: column;
      z-index: 99999; overflow: hidden;
      transform: translateY(20px) scale(0.95); opacity: 0;
      transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1),
                  opacity 0.3s ease;
      pointer-events: none;
    }
    .cm-panel.cm-open {
      transform: translateY(0) scale(1); opacity: 1;
      pointer-events: all;
    }
    .cm-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 14px 16px;
      background: ${SURFACE};
      border-bottom: 0.5px solid rgba(0,212,170,0.1);
      flex-shrink: 0;
    }
    .cm-header-left {
      display: flex; align-items: center; gap: 8px;
    }
    .cm-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: ${ACCENT};
      animation: cm-dot-pulse 2s ease-in-out infinite;
    }
    @keyframes cm-dot-pulse {
      0%,100% { opacity: 1; } 50% { opacity: 0.4; }
    }
    .cm-title {
      color: ${TEXT}; font-size: 14px; font-weight: 600;
      font-family: 'Cabinet Grotesk', sans-serif;
    }
    .cm-close {
      background: none; border: none; cursor: pointer;
      color: ${MUTED}; font-size: 18px; line-height: 1;
      padding: 4px; transition: color 0.2s;
    }
    .cm-close:hover { color: ${TEXT}; }

    /* ── FORM ── */
    .cm-form-wrap {
      flex: 1; display: flex; flex-direction: column;
      justify-content: center; padding: 28px 24px;
      gap: 0;
    }
    .cm-form-heading {
      color: ${TEXT}; font-size: 16px; font-weight: 600;
      font-family: 'Cabinet Grotesk', sans-serif;
      margin-bottom: 6px;
    }
    .cm-form-sub {
      color: ${MUTED}; font-size: 13px; margin-bottom: 24px;
      line-height: 1.5;
    }
    .cm-field { margin-bottom: 16px; }
    .cm-label {
      display: block; color: ${MUTED}; font-size: 12px;
      margin-bottom: 6px;
    }
    .cm-input {
      width: 100%; background: ${SURFACE};
      border: 0.5px solid rgba(0,212,170,0.15);
      border-radius: 8px; padding: 10px 14px;
      color: ${TEXT}; font-size: 14px; outline: none;
      transition: border-color 0.2s; box-sizing: border-box;
      font-family: inherit;
    }
    .cm-input:focus { border-color: ${ACCENT}; }
    .cm-input::placeholder { color: ${MUTED}; }
    .cm-error {
      color: #ff6b6b; font-size: 12px; margin-top: 4px;
      display: none;
    }
    .cm-submit {
      width: 100%; background: ${ACCENT};
      color: #060a0e; font-size: 14px; font-weight: 700;
      border: none; border-radius: 8px; padding: 12px;
      cursor: pointer; margin-top: 8px;
      font-family: 'Cabinet Grotesk', sans-serif;
      transition: filter 0.2s, transform 0.1s;
    }
    .cm-submit:hover { filter: brightness(1.1); }
    .cm-submit:active { transform: scale(0.98); }
    .cm-submit:disabled {
      opacity: 0.5; cursor: not-allowed; filter: none;
    }

    /* ── CHAT ── */
    .cm-messages {
      flex: 1; overflow-y: auto; padding: 16px;
      display: flex; flex-direction: column; gap: 12px;
    }
    .cm-messages::-webkit-scrollbar { width: 4px; }
    .cm-messages::-webkit-scrollbar-thumb {
      background: rgba(0,212,170,0.2); border-radius: 2px;
    }
    .cm-bot-row { display: flex; justify-content: flex-start; }
    .cm-user-row { display: flex; justify-content: flex-end; }
    .cm-bot-bubble {
      background: ${SURFACE};
      border: 0.5px solid rgba(0,212,170,0.1);
      border-radius: 4px 16px 16px 16px;
      color: ${TEXT}; font-size: 14px; line-height: 1.6;
      padding: 10px 14px; max-width: 85%;
    }
    .cm-user-bubble {
      background: ${ACCENT}; color: #060a0e;
      border-radius: 16px 16px 4px 16px;
      font-size: 14px; font-weight: 500; line-height: 1.6;
      padding: 10px 14px; max-width: 85%;
    }
    .cm-typing {
      display: flex; gap: 4px; align-items: center;
      padding: 10px 14px;
    }
    .cm-typing span {
      width: 6px; height: 6px; border-radius: 50%;
      background: ${ACCENT}; opacity: 0.6;
      animation: cm-bounce 1.2s ease-in-out infinite;
    }
    .cm-typing span:nth-child(2) { animation-delay: 0.2s; }
    .cm-typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes cm-bounce {
      0%,80%,100% { transform: scale(0.7); opacity: 0.4; }
      40% { transform: scale(1); opacity: 1; }
    }
    .cm-input-area {
      display: flex; align-items: flex-end; gap: 10px;
      padding: 12px 16px;
      border-top: 0.5px solid rgba(0,212,170,0.1);
      background: ${SURFACE}; flex-shrink: 0;
    }
    .cm-textarea {
      flex: 1; background: transparent; border: none;
      color: ${TEXT}; font-size: 14px; outline: none;
      resize: none; max-height: 80px; line-height: 1.5;
      font-family: inherit; padding: 4px 0;
    }
    .cm-textarea::placeholder { color: ${MUTED}; }
    .cm-send {
      width: 36px; height: 36px; border-radius: 50%;
      background: ${ACCENT}; border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; transition: filter 0.2s;
    }
    .cm-send:hover { filter: brightness(1.1); }
    .cm-send svg { width: 16px; height: 16px; }

    @media (max-width: 480px) {
      .cm-panel {
        inset: 0; bottom: 0; right: 0;
        width: 100%; height: 100%;
        border-radius: 0;
      }
      .cm-btn, .cm-pulse { bottom: 16px; right: 16px; }
      .cm-btn { width: 48px; height: 48px; }
      .cm-pulse { width: 48px; height: 48px; }
    }
  `;

  // ── INJECT CSS ──
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  // ── PULSE RING ──
  const pulse = document.createElement('div');
  pulse.className = 'cm-pulse';
  document.body.appendChild(pulse);

  // ── TRIGGER BUTTON ──
  const btn = document.createElement('button');
  btn.className = 'cm-btn';
  btn.setAttribute('aria-label', 'Open chat');
  btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="#060a0e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`;
  document.body.appendChild(btn);

  // ── PANEL ──
  const panel = document.createElement('div');
  panel.className = 'cm-panel';
  panel.innerHTML = `
    <div class="cm-header">
      <div class="cm-header-left">
        <div class="cm-dot"></div>
        <span class="cm-title">Coremagna AI</span>
      </div>
      <button class="cm-close" aria-label="Close">×</button>
    </div>

    <div class="cm-form-wrap" id="cm-form-wrap">
      <div class="cm-form-heading">Before we start</div>
      <div class="cm-form-sub">We'll personalize your experience.</div>
      <div class="cm-field">
        <label class="cm-label" for="cm-name">Your name</label>
        <input class="cm-input" id="cm-name" type="text" 
               placeholder="John Smith" autocomplete="name">
        <div class="cm-error" id="cm-name-err">Please enter your name.</div>
      </div>
      <div class="cm-field">
        <label class="cm-label" for="cm-email">Your email</label>
        <input class="cm-input" id="cm-email" type="email" 
               placeholder="john@company.com" autocomplete="email">
        <div class="cm-error" id="cm-email-err">Please enter a valid email.</div>
      </div>
      <button class="cm-submit" id="cm-submit" disabled>Start Chat →</button>
    </div>

    <div class="cm-messages" id="cm-messages" style="display:none"></div>

    <div class="cm-input-area" id="cm-input-area" style="display:none">
      <textarea class="cm-textarea" id="cm-textarea" 
                placeholder="Type a message..." rows="1"></textarea>
      <button class="cm-send" id="cm-send" aria-label="Send">
        <svg viewBox="0 0 24 24" fill="none" stroke="#060a0e" 
             stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"/>
          <polygon points="22 2 15 22 11 13 2 9 22 2"/>
        </svg>
      </button>
    </div>
  `;
  document.body.appendChild(panel);

  // ── REFS ──
  const closeBtn = panel.querySelector('.cm-close');
  const formWrap = panel.querySelector('#cm-form-wrap');
  const nameInput = panel.querySelector('#cm-name');
  const emailInput = panel.querySelector('#cm-email');
  const nameErr = panel.querySelector('#cm-name-err');
  const emailErr = panel.querySelector('#cm-email-err');
  const submitBtn = panel.querySelector('#cm-submit');
  const messages = panel.querySelector('#cm-messages');
  const inputArea = panel.querySelector('#cm-input-area');
  const textarea = panel.querySelector('#cm-textarea');
  const sendBtn = panel.querySelector('#cm-send');

  // ── OPEN / CLOSE ──
  function openPanel() {
    panel.classList.add('cm-open');
    pulse.style.display = 'none';
    if (!chatStarted) nameInput.focus();
    else textarea.focus();
  }
  function closePanel() {
    panel.classList.remove('cm-open');
    pulse.style.display = 'block';
  }

  btn.addEventListener('click', openPanel);
  closeBtn.addEventListener('click', closePanel);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && panel.classList.contains('cm-open')) {
      closePanel();
      btn.focus();
    }
  });

  // ── FORM VALIDATION ──
  function validateName() {
    const v = nameInput.value.trim();
    if (v.length < 2) {
      nameErr.style.display = 'block';
      return false;
    }
    nameErr.style.display = 'none';
    return true;
  }
  function validateEmail() {
    const v = emailInput.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) {
      emailErr.style.display = 'block';
      return false;
    }
    emailErr.style.display = 'none';
    return true;
  }
  function checkSubmit() {
    const n = nameInput.value.trim().length >= 2;
    const e = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim());
    submitBtn.disabled = !(n && e);
  }

  nameInput.addEventListener('input', checkSubmit);
  emailInput.addEventListener('input', checkSubmit);
  nameInput.addEventListener('blur', validateName);
  emailInput.addEventListener('blur', validateEmail);

  // ── START CHAT ──
  submitBtn.addEventListener('click', startChat);

  function startChat() {
    if (!validateName() || !validateEmail()) return;
    visitorName = nameInput.value.trim();
    visitorEmail = emailInput.value.trim();
    chatStarted = true;

    formWrap.style.display = 'none';
    messages.style.display = 'flex';
    inputArea.style.display = 'flex';

    const first = visitorName.split(' ')[0];
    appendBot(`Hi ${first}! 👋 I'm Coremagna's AI assistant. I can help you with web design, AI chatbots, and automation. What brings you here today?`);
    textarea.focus();
  }

  // ── MESSAGES ──
  function appendBot(text) {
    const row = document.createElement('div');
    row.className = 'cm-bot-row';
    const bubble = document.createElement('div');
    bubble.className = 'cm-bot-bubble';
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }

  function appendUser(text) {
    const row = document.createElement('div');
    row.className = 'cm-user-row';
    const bubble = document.createElement('div');
    bubble.className = 'cm-user-bubble';
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }

  function showTyping() {
    const row = document.createElement('div');
    row.className = 'cm-bot-row';
    row.id = 'cm-typing';
    row.innerHTML = `<div class="cm-bot-bubble cm-typing">
      <span></span><span></span><span></span>
    </div>`;
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
    return row;
  }

  function removeTyping() {
    const t = document.getElementById('cm-typing');
    if (t) t.remove();
  }

  // ── SEND MESSAGE ──
  async function sendMessage() {
    const text = textarea.value.trim();
    if (!text) return;

    textarea.value = '';
    textarea.style.height = 'auto';
    appendUser(text);

    const typing = showTyping();

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);

      const res = await fetch(WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          visitor_name: visitorName,
          visitor_email: visitorEmail
        }),
        signal: controller.signal
      });

      clearTimeout(timeout);
      removeTyping();

      const raw = await res.text();
      let reply = '';

      try {
        const data = JSON.parse(raw);
        reply = data.reply || data.message || data.text || data.output || raw;
      } catch {
        reply = raw;
      }

      appendBot(reply || 'Got your message!');

    } catch (err) {
      removeTyping();
      if (err.name === 'AbortError') {
        appendBot('Taking longer than usual. Please try again.');
      } else {
        appendBot('Connection issue. Please try again.');
      }
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 80) + 'px';
  });
})();
