/**
 * Coremagna Chat Widget v2 — Chat + Voice
 * Drop-in replacement for widget.js
 * Embed: <script src="/chat-widget.js" data-webhook="https://..."></script>
 */
(function () {
  'use strict';

  // ── CONFIG ────────────────────────────────────────────────────
  const script = document.currentScript;
  const WEBHOOK = (script && script.dataset.webhook) || 'https://adriens.app.n8n.cloud/webhook/chatbot';
  const RATE_LIMIT_MS = 2000;
  const MAX_MESSAGES = 50;
  const GREETING_DELAY = 5000;

  const BOOK_URL = 'https://calendar.app.google/XDGM8XJ9zEdqugKr9';
  const BOOK_PHRASES = ['book', 'call', 'calendar', 'schedule', 'appointment', 'calendly', 'calendar.app'];

  // ── COLORS ────────────────────────────────────────────────────
  const C = {
    bg: '#0d1117',
    header: '#060a0e',
    surface: '#111920',
    accent: '#00D4AA',
    accentDim: 'rgba(0,212,170,0.12)',
    text: '#F0F4F3',
    muted: '#8a9ba8',
    userBubble: '#1a2530',
    botBubble: '#111920',
    border: 'rgba(255,255,255,0.07)',
    accentBorder: 'rgba(0,212,170,0.15)',
  };

  // ── STATE ─────────────────────────────────────────────────────
  let visitorName = '';
  let visitorEmail = '';
  let chatStarted = false;
  let isOpen = false;
  let activeTab = 'chat';
  let messageCount = 0;
  let lastSentAt = 0;
  let greetingTimer = null;
  let voiceState = 'idle'; // idle | listening | processing | speaking
  let recognition = null;
  let isSending = false;

  // Session + visitor IDs
  function uid() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2);
  }
  const sessionId = sessionStorage.getItem('cm_sid') || uid();
  sessionStorage.setItem('cm_sid', sessionId);
  const visitorId = localStorage.getItem('cm_vid') || uid();
  localStorage.setItem('cm_vid', visitorId);

  // Conversation history in sessionStorage
  function saveHistory(msgs) {
    try { sessionStorage.setItem('cm_history', JSON.stringify(msgs)); } catch (_) {}
  }
  function loadHistory() {
    try { return JSON.parse(sessionStorage.getItem('cm_history') || '[]'); } catch (_) { return []; }
  }

  // ── CSS ───────────────────────────────────────────────────────
  const css = `
    /* ── RESET & BASE ── */
    .cm-widget *, .cm-widget *::before, .cm-widget *::after {
      box-sizing: border-box; margin: 0; padding: 0;
    }

    /* ── PULSE RING ── */
    .cm-pulse-ring {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${C.accent}; opacity: 0; pointer-events: none;
      z-index: 99998;
      animation: cm-pulse-ring 5s ease-out 3s infinite;
    }
    @keyframes cm-pulse-ring {
      0%   { transform: scale(1); opacity: 0.35; }
      70%  { transform: scale(1.9); opacity: 0; }
      100% { opacity: 0; }
    }

    /* ── FAB ── */
    .cm-fab {
      position: fixed; bottom: 24px; right: 24px;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${C.accent}; border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      z-index: 99999;
      transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                  filter 0.2s ease;
      box-shadow: 0 4px 16px rgba(0,212,170,0.35);
    }
    .cm-fab:hover { transform: scale(1.1); filter: brightness(1.12); }
    .cm-fab:focus-visible { outline: 2px solid ${C.text}; outline-offset: 3px; }
    .cm-fab svg { width: 24px; height: 24px; transition: transform 0.25s; }

    /* ── PANEL ── */
    .cm-panel {
      position: fixed; bottom: 90px; right: 24px;
      width: 400px; height: 560px;
      background: ${C.bg}; border-radius: 20px;
      border: 0.5px solid ${C.accentBorder};
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      display: flex; flex-direction: column;
      z-index: 99999; overflow: hidden;
      transform: translateY(16px) scale(0.96); opacity: 0;
      transition: transform 0.35s cubic-bezier(0.34,1.56,0.64,1),
                  opacity 0.25s ease;
      pointer-events: none;
    }
    .cm-panel.cm-open {
      transform: translateY(0) scale(1); opacity: 1;
      pointer-events: all;
    }

    /* ── HEADER ── */
    .cm-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 14px 18px;
      background: ${C.header};
      border-bottom: 0.5px solid ${C.accentBorder};
      flex-shrink: 0;
    }
    .cm-header-left { display: flex; align-items: center; gap: 9px; }
    .cm-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: ${C.accent};
      animation: cm-dot-blink 2.5s ease-in-out infinite;
    }
    @keyframes cm-dot-blink {
      0%,100% { opacity: 1; } 50% { opacity: 0.35; }
    }
    .cm-title {
      color: ${C.text}; font-size: 14px; font-weight: 600;
      font-family: 'DM Sans', 'Cabinet Grotesk', sans-serif; letter-spacing: 0.01em;
    }
    .cm-minimize {
      background: none; border: none; cursor: pointer;
      color: ${C.muted}; font-size: 20px; line-height: 1;
      padding: 2px 6px; border-radius: 4px;
      transition: color 0.2s, background 0.2s;
    }
    .cm-minimize:hover { color: ${C.text}; background: ${C.accentDim}; }
    .cm-minimize:focus-visible { outline: 2px solid ${C.accent}; }

    /* ── FORM GATE ── */
    .cm-form-wrap {
      flex: 1; display: flex; flex-direction: column;
      justify-content: center; padding: 28px 24px; gap: 0;
      overflow-y: auto;
    }
    .cm-form-heading {
      color: ${C.text}; font-size: 17px; font-weight: 600;
      font-family: 'DM Sans', sans-serif; margin-bottom: 6px;
    }
    .cm-form-sub {
      color: ${C.muted}; font-size: 13px; margin-bottom: 22px; line-height: 1.55;
    }
    .cm-field { margin-bottom: 14px; }
    .cm-label {
      display: block; color: ${C.muted}; font-size: 12px;
      margin-bottom: 5px; font-family: 'DM Sans', sans-serif;
    }
    .cm-input {
      width: 100%; background: ${C.surface};
      border: 0.5px solid ${C.accentBorder};
      border-radius: 10px; padding: 10px 14px;
      color: ${C.text}; font-size: 14px; outline: none;
      transition: border-color 0.2s; font-family: inherit;
    }
    .cm-input:focus { border-color: ${C.accent}; }
    .cm-input::placeholder { color: ${C.muted}; }
    .cm-err {
      color: #ff6b6b; font-size: 11px; margin-top: 4px; display: none;
    }
    .cm-submit {
      width: 100%; background: ${C.accent};
      color: #060a0e; font-size: 14px; font-weight: 700;
      border: none; border-radius: 10px; padding: 12px;
      cursor: pointer; margin-top: 6px;
      font-family: 'DM Sans', sans-serif;
      transition: filter 0.2s, transform 0.12s;
    }
    .cm-submit:hover:not(:disabled) { filter: brightness(1.1); }
    .cm-submit:active:not(:disabled) { transform: scale(0.98); }
    .cm-submit:disabled { opacity: 0.45; cursor: not-allowed; }
    .cm-submit:focus-visible { outline: 2px solid ${C.text}; }

    /* ── CHAT INTERFACE ── */
    .cm-chat-interface {
      flex: 1; display: flex; flex-direction: column; overflow: hidden;
    }

    /* ── TABS ── */
    .cm-tabs {
      display: flex; border-bottom: 0.5px solid ${C.border};
      background: ${C.header}; flex-shrink: 0;
    }
    .cm-tab {
      flex: 1; padding: 11px 0; border: none; cursor: pointer;
      font-size: 13px; font-family: 'DM Sans', sans-serif; font-weight: 500;
      background: none; color: ${C.muted};
      border-bottom: 2px solid transparent;
      transition: color 0.2s, border-color 0.2s;
    }
    .cm-tab:hover { color: ${C.text}; }
    .cm-tab.cm-tab-active {
      color: ${C.accent}; border-bottom-color: ${C.accent};
    }
    .cm-tab:focus-visible { outline: 2px solid ${C.accent}; outline-offset: -2px; }

    /* ── MESSAGES ── */
    .cm-messages {
      flex: 1; overflow-y: auto; padding: 14px 16px;
      display: flex; flex-direction: column; gap: 10px;
    }
    .cm-messages::-webkit-scrollbar { width: 3px; }
    .cm-messages::-webkit-scrollbar-thumb {
      background: rgba(0,212,170,0.18); border-radius: 2px;
    }
    .cm-bot-row { display: flex; flex-direction: column; align-items: flex-start; gap: 3px; }
    .cm-user-row { display: flex; justify-content: flex-end; }
    .cm-sender-label {
      font-size: 11px; color: ${C.muted}; padding-left: 2px;
      font-family: 'DM Sans', sans-serif;
    }
    .cm-bot-bubble {
      background: ${C.botBubble};
      border: 0.5px solid ${C.accentBorder};
      border-left: 2px solid ${C.accent};
      border-radius: 4px 16px 16px 16px;
      color: ${C.text}; font-size: 14px; line-height: 1.65;
      padding: 10px 14px; max-width: 86%; word-break: break-word;
    }
    .cm-user-bubble {
      background: ${C.userBubble};
      border-radius: 16px 16px 4px 16px;
      color: ${C.text}; font-size: 14px; font-weight: 400;
      line-height: 1.65; padding: 10px 14px; max-width: 86%;
      word-break: break-word;
    }
    .cm-bot-bubble a { color: ${C.accent}; text-decoration: underline; }
    .cm-book-btn {
      display: inline-block; margin-top: 8px;
      background: ${C.accent}; color: #060a0e;
      font-size: 12px; font-weight: 700;
      border-radius: 8px; padding: 7px 14px;
      text-decoration: none; cursor: pointer; border: none;
      font-family: 'DM Sans', sans-serif;
      transition: filter 0.2s;
    }
    .cm-book-btn:hover { filter: brightness(1.1); }

    /* ── TYPING INDICATOR ── */
    .cm-typing {
      display: flex; gap: 5px; align-items: center;
      background: ${C.botBubble};
      border: 0.5px solid ${C.accentBorder};
      border-left: 2px solid ${C.accent};
      border-radius: 4px 16px 16px 16px;
      padding: 12px 16px; width: fit-content;
    }
    .cm-typing span {
      width: 6px; height: 6px; border-radius: 50%;
      background: ${C.accent}; opacity: 0.5;
      animation: cm-bounce 1.3s ease-in-out infinite;
    }
    .cm-typing span:nth-child(2) { animation-delay: 0.18s; }
    .cm-typing span:nth-child(3) { animation-delay: 0.36s; }
    @keyframes cm-bounce {
      0%,80%,100% { transform: translateY(0); opacity: 0.4; }
      40% { transform: translateY(-5px); opacity: 1; }
    }

    /* ── CHAT INPUT ── */
    .cm-input-bar {
      display: flex; align-items: flex-end; gap: 10px;
      padding: 12px 14px;
      border-top: 0.5px solid ${C.border};
      background: ${C.header}; flex-shrink: 0;
    }
    .cm-textarea {
      flex: 1; background: transparent; border: none;
      color: ${C.text}; font-size: 14px; outline: none;
      resize: none; max-height: 80px; line-height: 1.5;
      font-family: inherit; padding: 4px 0;
    }
    .cm-textarea::placeholder { color: ${C.muted}; }
    .cm-send-btn {
      width: 36px; height: 36px; border-radius: 50%;
      background: ${C.accent}; border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
      transition: filter 0.2s, transform 0.12s;
    }
    .cm-send-btn:hover { filter: brightness(1.1); }
    .cm-send-btn:active { transform: scale(0.92); }
    .cm-send-btn:focus-visible { outline: 2px solid ${C.text}; }
    .cm-send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .cm-send-btn svg { width: 15px; height: 15px; }

    /* ── VOICE PANEL ── */
    .cm-voice-panel {
      flex: 1; display: flex; flex-direction: column;
      align-items: center; justify-content: space-between;
      padding: 24px 20px 28px;
      overflow: hidden;
    }
    .cm-voice-transcript {
      width: 100%; min-height: 60px; max-height: 120px;
      overflow-y: auto; text-align: center;
      color: ${C.text}; font-size: 14px; line-height: 1.6;
      padding: 8px 12px;
      background: ${C.surface}; border-radius: 12px;
      border: 0.5px solid ${C.border};
      font-family: 'DM Sans', sans-serif;
    }
    .cm-voice-transcript:empty::before {
      content: 'Your words will appear here'; color: ${C.muted};
      font-style: italic;
    }
    .cm-voice-center {
      display: flex; flex-direction: column; align-items: center; gap: 16px;
    }
    .cm-mic-btn {
      width: 86px; height: 86px; border-radius: 50%; border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      position: relative; transition: transform 0.2s, filter 0.2s;
      background: ${C.surface};
      border: 2px solid ${C.accentBorder};
      box-shadow: 0 0 0 0 rgba(0,212,170,0.3);
    }
    .cm-mic-btn:hover { transform: scale(1.05); filter: brightness(1.1); }
    .cm-mic-btn:active { transform: scale(0.95); }
    .cm-mic-btn:focus-visible { outline: 2px solid ${C.accent}; outline-offset: 4px; }
    .cm-mic-btn svg { width: 36px; height: 36px; }
    .cm-mic-btn.cm-listening {
      background: rgba(220,38,38,0.15);
      border-color: rgba(220,38,38,0.5);
      animation: cm-mic-pulse 1.1s ease-in-out infinite;
    }
    @keyframes cm-mic-pulse {
      0%,100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.4); }
      50% { box-shadow: 0 0 0 16px rgba(220,38,38,0); }
    }
    .cm-mic-btn.cm-speaking {
      background: ${C.accentDim};
      border-color: ${C.accent};
      animation: cm-speak-pulse 1.4s ease-in-out infinite;
    }
    @keyframes cm-speak-pulse {
      0%,100% { box-shadow: 0 0 0 0 rgba(0,212,170,0.4); }
      50% { box-shadow: 0 0 0 16px rgba(0,212,170,0); }
    }

    /* ── WAVEFORM ── */
    .cm-waveform {
      display: flex; align-items: center; gap: 4px; height: 30px;
      opacity: 0; transition: opacity 0.3s;
    }
    .cm-waveform.cm-active { opacity: 1; }
    .cm-waveform span {
      display: block; width: 3px; border-radius: 2px;
      background: ${C.accent};
    }
    .cm-waveform.cm-bars-idle span { height: 8px; }
    .cm-waveform.cm-bars-on span {
      animation: cm-wave 0.9s ease-in-out infinite;
    }
    .cm-waveform.cm-bars-on span:nth-child(1) { animation-delay: 0s;    height: 12px; }
    .cm-waveform.cm-bars-on span:nth-child(2) { animation-delay: 0.12s; height: 20px; }
    .cm-waveform.cm-bars-on span:nth-child(3) { animation-delay: 0.24s; height: 28px; }
    .cm-waveform.cm-bars-on span:nth-child(4) { animation-delay: 0.12s; height: 20px; }
    .cm-waveform.cm-bars-on span:nth-child(5) { animation-delay: 0s;    height: 12px; }
    @keyframes cm-wave {
      0%,100% { transform: scaleY(0.4); opacity: 0.6; }
      50% { transform: scaleY(1); opacity: 1; }
    }
    .cm-waveform.cm-bars-speak span {
      background: ${C.accent};
      animation: cm-wave-speak 0.7s ease-in-out infinite;
    }
    .cm-waveform.cm-bars-speak span:nth-child(1) { animation-delay: 0s; }
    .cm-waveform.cm-bars-speak span:nth-child(2) { animation-delay: 0.1s; }
    .cm-waveform.cm-bars-speak span:nth-child(3) { animation-delay: 0.2s; }
    .cm-waveform.cm-bars-speak span:nth-child(4) { animation-delay: 0.1s; }
    .cm-waveform.cm-bars-speak span:nth-child(5) { animation-delay: 0s; }
    @keyframes cm-wave-speak {
      0%,100% { transform: scaleY(0.5); }
      50% { transform: scaleY(1); }
    }

    .cm-voice-status {
      color: ${C.muted}; font-size: 13px; font-family: 'DM Sans', sans-serif;
      text-align: center; min-height: 20px;
    }
    .cm-voice-status.cm-status-listening { color: #f87171; }
    .cm-voice-status.cm-status-speaking { color: ${C.accent}; }

    /* ── SPINNER ── */
    .cm-spinner {
      width: 36px; height: 36px; border-radius: 50%;
      border: 3px solid ${C.border};
      border-top-color: ${C.accent};
      animation: cm-spin 0.8s linear infinite;
    }
    @keyframes cm-spin { to { transform: rotate(360deg); } }

    /* ── NO SUPPORT NOTICE ── */
    .cm-no-voice {
      flex: 1; display: flex; flex-direction: column;
      align-items: center; justify-content: center; gap: 12px;
      padding: 32px 24px; text-align: center;
    }
    .cm-no-voice svg { width: 40px; height: 40px; opacity: 0.3; }
    .cm-no-voice p { color: ${C.muted}; font-size: 14px; line-height: 1.6; }
    .cm-no-voice strong { color: ${C.text}; }

    /* ── MOBILE ── */
    @media (max-width: 480px) {
      .cm-panel {
        inset: 0; width: 100%; height: 100%;
        border-radius: 0; bottom: 0; right: 0;
      }
      .cm-fab, .cm-pulse-ring { bottom: 16px; right: 16px; }
    }

    /* ── REDUCED MOTION ── */
    @media (prefers-reduced-motion: reduce) {
      .cm-pulse-ring, .cm-dot,
      .cm-typing span, .cm-waveform span,
      .cm-mic-btn, .cm-spinner { animation: none !important; }
      .cm-panel, .cm-fab { transition: none !important; }
    }
  `;

  // ── INJECT STYLE ──────────────────────────────────────────────
  const styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── PULSE RING ────────────────────────────────────────────────
  const pulseRing = document.createElement('div');
  pulseRing.className = 'cm-pulse-ring';
  document.body.appendChild(pulseRing);

  // ── FAB ───────────────────────────────────────────────────────
  const fab = document.createElement('button');
  fab.className = 'cm-fab';
  fab.setAttribute('aria-label', 'Open chat with Magna');
  fab.setAttribute('aria-expanded', 'false');
  fab.innerHTML = chatIcon();
  document.body.appendChild(fab);

  // ── PANEL HTML ────────────────────────────────────────────────
  const panel = document.createElement('div');
  panel.className = 'cm-panel cm-widget';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Magna AI chat assistant');
  panel.innerHTML = `
    <div class="cm-header">
      <div class="cm-header-left">
        <div class="cm-dot" aria-hidden="true"></div>
        <span class="cm-title">Magna</span>
      </div>
      <button class="cm-minimize" aria-label="Close chat">−</button>
    </div>

    <!-- FORM GATE -->
    <div class="cm-form-wrap" id="cm-form-wrap">
      <div class="cm-form-heading">Before we start 👋</div>
      <div class="cm-form-sub">Drop your details and I'll personalize my answers.</div>
      <div class="cm-field">
        <label class="cm-label" for="cm-name-inp">Your name</label>
        <input class="cm-input" id="cm-name-inp" type="text"
               placeholder="Jane Smith" autocomplete="name">
        <div class="cm-err" id="cm-name-err">Please enter your name (min 2 characters).</div>
      </div>
      <div class="cm-field">
        <label class="cm-label" for="cm-email-inp">Your email</label>
        <input class="cm-input" id="cm-email-inp" type="email"
               placeholder="jane@company.com" autocomplete="email">
        <div class="cm-err" id="cm-email-err">Please enter a valid email address.</div>
      </div>
      <button class="cm-submit" id="cm-submit-btn" disabled>Start Chatting →</button>
    </div>

    <!-- CHAT INTERFACE (hidden until form submitted) -->
    <div class="cm-chat-interface" id="cm-chat-interface" style="display:none;flex:1;flex-direction:column;overflow:hidden;">
      <div class="cm-tabs" role="tablist">
        <button class="cm-tab cm-tab-active" id="cm-tab-chat-btn"
                role="tab" aria-selected="true" aria-controls="cm-tab-chat-pane">💬 Chat</button>
        <button class="cm-tab" id="cm-tab-voice-btn"
                role="tab" aria-selected="false" aria-controls="cm-tab-voice-pane">🎤 Voice</button>
      </div>

      <!-- CHAT PANE -->
      <div id="cm-tab-chat-pane" role="tabpanel" style="flex:1;display:flex;flex-direction:column;overflow:hidden;">
        <div class="cm-messages" id="cm-messages" aria-live="polite" aria-label="Conversation"></div>
        <div class="cm-input-bar">
          <textarea class="cm-textarea" id="cm-textarea"
                    placeholder="Ask me anything…" rows="1"
                    aria-label="Type your message"></textarea>
          <button class="cm-send-btn" id="cm-send-btn" aria-label="Send message">
            <svg viewBox="0 0 24 24" fill="none" stroke="#060a0e"
                 stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- VOICE PANE -->
      <div id="cm-tab-voice-pane" role="tabpanel" style="display:none;flex:1;overflow:hidden;"></div>
    </div>
  `;
  document.body.appendChild(panel);

  // ── ELEMENT REFS ──────────────────────────────────────────────
  const formWrap     = panel.querySelector('#cm-form-wrap');
  const chatIface    = panel.querySelector('#cm-chat-interface');
  const nameInp      = panel.querySelector('#cm-name-inp');
  const emailInp     = panel.querySelector('#cm-email-inp');
  const nameErr      = panel.querySelector('#cm-name-err');
  const emailErr     = panel.querySelector('#cm-email-err');
  const submitBtn    = panel.querySelector('#cm-submit-btn');
  const tabChatBtn   = panel.querySelector('#cm-tab-chat-btn');
  const tabVoiceBtn  = panel.querySelector('#cm-tab-voice-btn');
  const chatPane     = panel.querySelector('#cm-tab-chat-pane');
  const voicePane    = panel.querySelector('#cm-tab-voice-pane');
  const messages     = panel.querySelector('#cm-messages');
  const textarea     = panel.querySelector('#cm-textarea');
  const sendBtn      = panel.querySelector('#cm-send-btn');
  const minimizeBtn  = panel.querySelector('.cm-minimize');

  // ── ICON HELPERS ──────────────────────────────────────────────
  function chatIcon() {
    return `<svg viewBox="0 0 24 24" fill="none" stroke="#060a0e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`;
  }
  function closeIcon() {
    return `<svg viewBox="0 0 24 24" fill="none" stroke="#060a0e" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;
  }
  function micIcon(color) {
    return `<svg viewBox="0 0 24 24" fill="none" stroke="${color || '#F0F4F3'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>`;
  }
  function speakerIcon() {
    return `<svg viewBox="0 0 24 24" fill="none" stroke="${C.accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>`;
  }
  function spinnerHTML() {
    return `<div class="cm-spinner" aria-label="Thinking"></div>`;
  }

  // ── OPEN / CLOSE ──────────────────────────────────────────────
  function openPanel() {
    isOpen = true;
    panel.classList.add('cm-open');
    fab.setAttribute('aria-expanded', 'true');
    fab.setAttribute('aria-label', 'Close chat');
    fab.innerHTML = closeIcon();
    pulseRing.style.animationPlayState = 'paused';
    pulseRing.style.opacity = '0';
    clearTimeout(greetingTimer);
    if (chatStarted) textarea.focus();
    else nameInp.focus();
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('cm-open');
    fab.setAttribute('aria-expanded', 'false');
    fab.setAttribute('aria-label', 'Open chat with Magna');
    fab.innerHTML = chatIcon();
    pulseRing.style.animationPlayState = 'running';
    pulseRing.style.opacity = '';
    if (recognition && voiceState === 'listening') {
      recognition.stop();
    }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  }

  fab.addEventListener('click', () => { isOpen ? closePanel() : openPanel(); });
  minimizeBtn.addEventListener('click', closePanel);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) { closePanel(); fab.focus(); }
  });

  // ── FORM VALIDATION ───────────────────────────────────────────
  function validName() {
    return nameInp.value.trim().length >= 2;
  }
  function validEmail() {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInp.value.trim());
  }
  function checkGate() {
    submitBtn.disabled = !(validName() && validEmail());
  }
  nameInp.addEventListener('input', checkGate);
  emailInp.addEventListener('input', checkGate);
  nameInp.addEventListener('blur', () => {
    nameErr.style.display = validName() ? 'none' : 'block';
  });
  emailInp.addEventListener('blur', () => {
    emailErr.style.display = validEmail() ? 'none' : 'block';
  });

  // ── START CHAT ────────────────────────────────────────────────
  submitBtn.addEventListener('click', startChat);
  nameInp.addEventListener('keydown', (e) => { if (e.key === 'Enter') emailInp.focus(); });
  emailInp.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !submitBtn.disabled) startChat();
  });

  function startChat() {
    if (!validName()) { nameErr.style.display = 'block'; nameInp.focus(); return; }
    if (!validEmail()) { emailErr.style.display = 'block'; emailInp.focus(); return; }
    visitorName = nameInp.value.trim();
    visitorEmail = emailInp.value.trim();
    chatStarted = true;

    formWrap.style.display = 'none';
    chatIface.style.display = 'flex';
    chatIface.style.flexDirection = 'column';
    chatIface.style.overflow = 'hidden';
    chatIface.style.flex = '1';

    // Restore history
    const history = loadHistory();
    history.forEach(m => {
      if (m.role === 'user') renderUser(m.text);
      else renderBot(m.text, false);
    });

    if (history.length === 0) {
      const first = visitorName.split(' ')[0];
      setTimeout(() => {
        renderBot(`Hi ${first}! 👋 I'm Magna, Coremagna's AI assistant. I can help you with AI chatbots, automation workflows, web design, and voice agents. What can I help you with today?`);
      }, 300);
    }

    buildVoicePane();
    textarea.focus();
  }

  // ── TABS ──────────────────────────────────────────────────────
  tabChatBtn.addEventListener('click', () => switchTab('chat'));
  tabVoiceBtn.addEventListener('click', () => switchTab('voice'));

  function switchTab(tab) {
    activeTab = tab;
    if (tab === 'chat') {
      tabChatBtn.classList.add('cm-tab-active');
      tabChatBtn.setAttribute('aria-selected', 'true');
      tabVoiceBtn.classList.remove('cm-tab-active');
      tabVoiceBtn.setAttribute('aria-selected', 'false');
      chatPane.style.display = 'flex';
      chatPane.style.flexDirection = 'column';
      voicePane.style.display = 'none';
      if (window.speechSynthesis) window.speechSynthesis.cancel();
      if (recognition && voiceState === 'listening') recognition.stop();
      textarea.focus();
    } else {
      tabVoiceBtn.classList.add('cm-tab-active');
      tabVoiceBtn.setAttribute('aria-selected', 'true');
      tabChatBtn.classList.remove('cm-tab-active');
      tabChatBtn.setAttribute('aria-selected', 'false');
      chatPane.style.display = 'none';
      voicePane.style.display = 'flex';
      voicePane.style.flexDirection = 'column';
      voicePane.style.overflow = 'hidden';
    }
  }

  // ── RENDER MESSAGES ───────────────────────────────────────────
  function renderBot(text, save = true) {
    const row = document.createElement('div');
    row.className = 'cm-bot-row';
    const label = document.createElement('div');
    label.className = 'cm-sender-label';
    label.textContent = 'Magna';
    const bubble = document.createElement('div');
    bubble.className = 'cm-bot-bubble';
    bubble.innerHTML = formatText(text);

    if (BOOK_PHRASES.some(p => text.toLowerCase().includes(p))) {
      const btn = document.createElement('a');
      btn.className = 'cm-book-btn';
      btn.href = BOOK_URL;
      btn.target = '_blank';
      btn.rel = 'noopener noreferrer';
      btn.textContent = '📅 Book a Free Call';
      bubble.appendChild(document.createElement('br'));
      bubble.appendChild(btn);
    }

    row.appendChild(label);
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
    if (save) saveToHistory('bot', text);
  }

  function renderUser(text, save = true) {
    const row = document.createElement('div');
    row.className = 'cm-user-row';
    const bubble = document.createElement('div');
    bubble.className = 'cm-user-bubble';
    bubble.textContent = text;
    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
    if (save) saveToHistory('user', text);
  }

  function formatText(text) {
    // Make URLs clickable
    const escaped = text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    return escaped.replace(
      /(https?:\/\/[^\s<>"]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
  }

  function saveToHistory(role, text) {
    const h = loadHistory();
    h.push({ role, text });
    if (h.length > 60) h.splice(0, h.length - 60);
    saveHistory(h);
  }

  function showTyping() {
    const row = document.createElement('div');
    row.className = 'cm-bot-row';
    row.id = 'cm-typing-row';
    row.innerHTML = `<div class="cm-sender-label">Magna</div><div class="cm-typing"><span></span><span></span><span></span></div>`;
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
  }
  function hideTyping() {
    const t = messages.querySelector('#cm-typing-row');
    if (t) t.remove();
  }

  // ── SEND MESSAGE (CHAT MODE) ──────────────────────────────────
  async function sendChatMessage(text) {
    if (!text || isSending) return;
    const now = Date.now();
    if (now - lastSentAt < RATE_LIMIT_MS) return;
    if (messageCount >= MAX_MESSAGES) {
      renderBot('We\'ve reached the message limit for this session. Please book a call to continue: ' + BOOK_URL);
      return;
    }
    lastSentAt = now;
    messageCount++;
    isSending = true;
    sendBtn.disabled = true;
    renderUser(text);
    showTyping();

    try {
      const res = await fetchWithTimeout(WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          visitor_name: visitorName,
          visitor_email: visitorEmail,
          page_url: window.location.href,
          mode: 'chat',
        }),
      }, 15000);
      hideTyping();
      const raw = await res.text();
      const reply = parseReply(raw);
      renderBot(reply);
    } catch (err) {
      hideTyping();
      renderBot(err.name === 'AbortError'
        ? 'Taking a bit longer than usual — please try again.'
        : 'Connection issue. Please check your internet and try again.');
    } finally {
      isSending = false;
      sendBtn.disabled = false;
    }
  }

  function parseReply(raw) {
    try {
      const d = JSON.parse(raw);
      return d.reply || d.message || d.text || d.output || raw;
    } catch (_) { return raw || '…'; }
  }

  async function fetchWithTimeout(url, opts, ms) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), ms);
    try {
      return await fetch(url, { ...opts, signal: ctrl.signal });
    } finally {
      clearTimeout(timer);
    }
  }

  // ── CHAT INPUT EVENTS ─────────────────────────────────────────
  sendBtn.addEventListener('click', () => {
    const t = textarea.value.trim();
    if (t) { textarea.value = ''; textarea.style.height = 'auto'; sendChatMessage(t); }
  });
  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const t = textarea.value.trim();
      if (t) { textarea.value = ''; textarea.style.height = 'auto'; sendChatMessage(t); }
    }
  });
  textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 80) + 'px';
  });

  // ── VOICE PANE ────────────────────────────────────────────────
  let micBtn, waveform, voiceStatus, voiceTranscript;

  function buildVoicePane() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const hasVoice = !!SR && !!window.speechSynthesis;

    if (!hasVoice) {
      voicePane.innerHTML = `
        <div class="cm-no-voice">
          <svg viewBox="0 0 24 24" fill="none" stroke="${C.muted}" stroke-width="1.5" stroke-linecap="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
          <p><strong>Voice mode unavailable</strong><br>Your browser doesn't support the Web Speech API. Please use <strong>Chrome or Edge</strong> on desktop, then refresh.</p>
        </div>`;
      return;
    }

    voicePane.innerHTML = `
      <div class="cm-voice-panel">
        <div class="cm-voice-transcript" id="cm-voice-transcript" aria-live="polite"></div>
        <div class="cm-voice-center">
          <button class="cm-mic-btn" id="cm-mic-btn" aria-label="Tap to speak">
            ${micIcon()}
          </button>
          <div class="cm-waveform cm-active cm-bars-idle" id="cm-waveform" aria-hidden="true">
            <span></span><span></span><span></span><span></span><span></span>
          </div>
        </div>
        <div class="cm-voice-status" id="cm-voice-status">Tap to speak</div>
      </div>`;

    micBtn       = voicePane.querySelector('#cm-mic-btn');
    waveform     = voicePane.querySelector('#cm-waveform');
    voiceStatus  = voicePane.querySelector('#cm-voice-status');
    voiceTranscript = voicePane.querySelector('#cm-voice-transcript');

    setupRecognition(SR);
    micBtn.addEventListener('click', handleMicClick);
  }

  function setupRecognition(SR) {
    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-GB';
    recognition.maxAlternatives = 1;

    let interimTranscript = '';
    let finalTranscript = '';

    recognition.onstart = () => {
      setVoiceState('listening');
      interimTranscript = '';
      finalTranscript = '';
    };

    recognition.onresult = (e) => {
      interimTranscript = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalTranscript += t;
        else interimTranscript += t;
      }
      if (voiceTranscript) {
        voiceTranscript.textContent = finalTranscript || interimTranscript;
      }
    };

    recognition.onerror = (e) => {
      setVoiceState('idle');
      if (voiceStatus) {
        if (e.error === 'not-allowed') {
          voiceStatus.textContent = 'Microphone access denied. Allow mic in browser settings.';
        } else if (e.error === 'no-speech') {
          voiceStatus.textContent = 'No speech detected — tap to try again.';
        } else {
          voiceStatus.textContent = 'Error: ' + e.error + '. Tap to try again.';
        }
      }
    };

    recognition.onend = () => {
      const text = (finalTranscript || interimTranscript).trim();
      if (text && voiceState === 'listening') {
        setVoiceState('processing');
        sendVoiceMessage(text);
      } else if (voiceState === 'listening') {
        setVoiceState('idle');
      }
    };
  }

  function handleMicClick() {
    if (!recognition) return;
    if (voiceState === 'idle') {
      recognition.start();
    } else if (voiceState === 'listening') {
      recognition.stop();
    } else if (voiceState === 'speaking') {
      window.speechSynthesis.cancel();
      setVoiceState('idle');
    }
  }

  async function sendVoiceMessage(text) {
    if (voiceTranscript) voiceTranscript.textContent = text;
    // Also add to chat history
    saveToHistory('user', text);

    // Replace mic icon with spinner for processing
    if (micBtn) micBtn.innerHTML = spinnerHTML();
    if (voiceStatus) {
      voiceStatus.textContent = 'Thinking…';
      voiceStatus.className = 'cm-voice-status';
    }
    if (waveform) {
      waveform.className = 'cm-waveform';
    }

    let reply = '';
    try {
      const res = await fetchWithTimeout(WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          visitor_name: visitorName,
          visitor_email: visitorEmail,
          page_url: window.location.href,
          mode: 'voice',
        }),
      }, 15000);
      const raw = await res.text();
      reply = parseReply(raw);
    } catch (err) {
      reply = err.name === 'AbortError'
        ? 'Sorry, that took too long. Could you try again?'
        : 'I had a connection issue. Please try again.';
    }

    // Save bot reply to shared history
    saveToHistory('bot', reply);

    // Update voice transcript with bot reply
    if (voiceTranscript) voiceTranscript.textContent = reply;
    setVoiceState('speaking');
    speakText(reply, () => setVoiceState('idle'));
  }

  function speakText(text, onDone) {
    if (!window.speechSynthesis) { if (onDone) onDone(); return; }
    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-GB';
    utter.rate = 1.0;
    utter.pitch = 1.0;

    // Pick best available UK female voice
    function doSpeak() {
      const voices = window.speechSynthesis.getVoices();
      const preferred =
        voices.find(v => v.name === 'Google UK English Female') ||
        voices.find(v => v.lang === 'en-GB' && v.name.toLowerCase().includes('female')) ||
        voices.find(v => v.lang === 'en-GB') ||
        voices.find(v => v.lang.startsWith('en'));
      if (preferred) utter.voice = preferred;
      window.speechSynthesis.speak(utter);
    }

    // Voices may not be loaded yet in some browsers
    if (window.speechSynthesis.getVoices().length > 0) {
      doSpeak();
    } else {
      window.speechSynthesis.onvoiceschanged = doSpeak;
    }

    utter.onend = () => { if (onDone) onDone(); };
    utter.onerror = () => { if (onDone) onDone(); };
  }

  function setVoiceState(state) {
    voiceState = state;
    if (!micBtn) return;
    micBtn.className = 'cm-mic-btn';
    waveform.className = 'cm-waveform';
    voiceStatus.className = 'cm-voice-status';

    if (state === 'idle') {
      micBtn.innerHTML = micIcon();
      micBtn.setAttribute('aria-label', 'Tap to speak');
      waveform.className = 'cm-waveform cm-active cm-bars-idle';
      voiceStatus.textContent = 'Tap to speak';
    } else if (state === 'listening') {
      micBtn.classList.add('cm-listening');
      micBtn.innerHTML = micIcon('#f87171');
      micBtn.setAttribute('aria-label', 'Listening — tap to stop');
      waveform.className = 'cm-waveform cm-active cm-bars-on';
      voiceStatus.classList.add('cm-status-listening');
      voiceStatus.textContent = 'Listening…';
    } else if (state === 'processing') {
      // spinner is already injected in sendVoiceMessage
      micBtn.setAttribute('aria-label', 'Processing');
    } else if (state === 'speaking') {
      micBtn.classList.add('cm-speaking');
      micBtn.innerHTML = speakerIcon();
      micBtn.setAttribute('aria-label', 'Speaking — tap to stop');
      waveform.className = 'cm-waveform cm-active cm-bars-speak';
      voiceStatus.classList.add('cm-status-speaking');
      voiceStatus.textContent = 'Speaking…';
    }
  }

  // ── AUTO-GREETING ─────────────────────────────────────────────
  greetingTimer = setTimeout(() => {
    if (!isOpen && !chatStarted) {
      openPanel();
    }
  }, GREETING_DELAY);

})();
