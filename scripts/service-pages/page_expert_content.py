from parts import ic, graph, offer, faq_html, table, SITE

SLUG = 'expert-content'
TITLE = 'Expert Content for Law Firms and Practices | Coremagna'
DESC = ('One recorded hour with a partner each month becomes four answer pages, eight short videos and eight posts. '
        'A real person on camera and sign-off on everything.')

CSS = r'''
/* ── Expert Content: hero recording mock ── */
.rec{padding:20px}
.rec-top{display:flex;align-items:center;gap:14px}
.rec-time{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:22px;line-height:1;padding:10px 14px;border-radius:10px;background:var(--accent);color:var(--on-accent);white-space:nowrap}
.rec-track{position:relative;flex:1;height:10px;border-radius:99px;background:var(--surface-2);overflow:hidden}
.rec-track i{position:absolute;top:0;bottom:0;left:calc(var(--a) * 1%);width:calc(var(--w) * 1%);border-radius:99px;background:var(--accent)}
.rec-lead{margin-top:16px;font-size:14px;color:var(--text-muted)}
.rec-list li{display:grid;grid-template-columns:32px minmax(0,1fr);gap:14px;align-items:center;padding:13px 0;border-top:1px solid var(--border)}
.rec-list li:first-child{margin-top:10px}
.rec-n{width:32px;height:32px;border-radius:50%;border:1px solid var(--border-hover);color:var(--accent);font-family:'JetBrains Mono',monospace;font-size:13px;display:grid;place-items:center}
.rec-list strong{display:block;font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:18px;line-height:1.2;letter-spacing:-0.01em}
.rec-out{display:block;margin-top:3px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text-muted)}
.rec-sum{display:flex;flex-wrap:wrap;gap:8px;padding-top:16px;border-top:1px solid var(--border)}
.rec-sum span{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:99px;background:var(--accent-dim);border:1px solid var(--border-hover);font-size:13px;font-weight:500;color:var(--text)}
.rec-sum .ic{font-size:16px;color:var(--accent)}
/* The list builds on load. CSS only, so it never depends on a script. */
@keyframes recIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.rec-lead,.rec-list li,.rec-sum{animation:recIn 0.7s var(--ease) both}
.rec-lead{animation-delay:0.3s}
.rec-list li:nth-child(1){animation-delay:0.5s}
.rec-list li:nth-child(2){animation-delay:0.7s}
.rec-list li:nth-child(3){animation-delay:0.9s}
.rec-list li:nth-child(4){animation-delay:1.1s}
.rec-sum{animation-delay:1.5s}

/* ── Evidence: two quotes beside the caveat ── */
.quote-wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:72px;align-items:start;margin-top:var(--space-xl)}
.quote-stack{display:flex;flex-direction:column;gap:36px}

/* ── Outputs ── */
.outs{border-top:1px solid var(--border)}
.out-row{display:grid;grid-template-columns:minmax(0,96px) minmax(0,1fr);gap:8px 24px;align-items:baseline;padding:24px 0;border-bottom:1px solid var(--border)}
.out-row .stat-num{font-size:clamp(2.2rem,4.5vw,3.5rem)}
.out-row h3{font-size:22px;line-height:1.15;margin-bottom:6px}
.out-row p{font-size:15px;line-height:1.65;color:var(--text-muted);max-width:56ch}
.card-fig{position:sticky;top:108px}
.card-fig img{width:100%;height:auto;border-radius:16px;border:1px solid var(--border);box-shadow:var(--shadow)}
.card-fig figcaption{margin-top:12px;font-size:13px;line-height:1.5;color:var(--text-muted)}

@media(max-width:1024px){
  .quote-wrap{grid-template-columns:minmax(0,1fr);gap:var(--space-xl)}
  .card-fig{position:static;max-width:420px}
}
@media(max-width:768px){
  .rec{padding:18px 16px}
  .rec-time{font-size:18px;padding:9px 12px}
  .rec-list strong{font-size:16px}
  .out-row{grid-template-columns:minmax(0,64px) minmax(0,1fr);gap:8px 16px;padding:22px 0}
  .out-row h3{font-size:18px}
}
@media(prefers-reduced-motion:reduce){
  .rec-lead,.rec-list li,.rec-sum{animation:none}
}
'''

FAQ = [
    ('Does the partner need to prepare?',
     'No. They see the four questions a few days before and answer them the way they would on a client call. If an answer runs long or wanders, that is ours to fix in the edit.'),
    ('What if our partners do not want to be on camera?',
     'Then we record sound only. You still get the four answer pages and the eight posts, and the short videos are replaced by quote cards and captioned audio clips. The price is the same.'),
    ('Do you use AI to write the content?',
     'AI makes the transcript and a first rough draft from it, and helps find the best 40 seconds in an hour of video. A person edits every page against the recording. We do not use AI avatars, cloned voices or generated headshots, and we do not add a fact the partner did not say without marking it for review.'),
    ('Who checks that the content is accurate?',
     'Your partner does, and your compliance contact signs it off. We are not lawyers or clinicians. Our job is to make sure the page says what the partner said, clearly, and to flag anything that needs a date or a source.'),
    ('Can more than one partner take part?',
     'Yes. The hour can be split between two people, or rotate between departments from month to month. The monthly output stays the same.'),
    ('Who publishes the content?',
     'Either of us. With an editor login we publish the pages and schedule the profile posts ourselves. If your web team prefers to do it, they get each page as a formatted document with its title, description and links ready. LinkedIn posts go to the partner ready to paste.'),
    ('Will this bring in new clients?',
     'We cannot promise that, and nobody honestly can. What the evidence supports is narrower: assistants and search engines draw heavily on firm websites, and a page with a named expert and a clear answer is the kind Google says it wants to show. If you have monthly AI visibility tracking, the count will show whether the questions you answered start to name you.'),
    ('What happens to the recordings?',
     'They are stored privately, used only to make your content, and deleted whenever you ask. The raw recording and every finished file belong to the firm.'),
    ('Do you work with practices outside the UK?',
     'Yes. We work in English with firms and practices in the UK, Ireland, Australia, New Zealand, Canada and the United States, and follow the advertising rules of the regulator you answer to.'),
    ('Is there a minimum term?',
     'No. The monthly plan runs month to month and stops with 30 days&rsquo; notice. The single session carries no further commitment.'),
]

BODY = r'''
<!-- ── HERO ── -->
<section id="hero" aria-labelledby="heroH1">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">Expert Content</span></li></ol>
    </nav>
    <div class="hero-grid">
      <div class="hero-text">
        <p class="hero-kicker">Expert Content</p>
        <h1 class="hero-h1" id="heroH1">One hour with a partner becomes a month of content</h1>
        <p class="hero-sub">We interview one of your partners for an hour a month about the questions clients ask. That recording becomes answer pages for your website, short videos of the partner, and posts for LinkedIn and your Google Business Profile.</p>
        <div class="hero-actions">
          <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="hero">Book a call
            ''' + ic('arrow-right') + r'''
          </a>
          <a href="#how" class="btn-ghost">See how a month works</a>
        </div>
        <p class="hero-fine">About 90 minutes of a partner&rsquo;s time a month, review included.</p>
        <p class="byline">By <a href="/about">Ferit Patefe</a>, founder of Coremagna. Updated <time datetime="{{TODAY}}">{{TODAY_LONG}}</time>.</p>
      </div>

      <figure class="mock">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>One recorded interview</span>
          <span class="tag">Example</span>
        </div>
        <div class="rec">
          <div class="rec-top">
            <span class="rec-time">60:00</span>
            <span class="rec-track" aria-hidden="true"><i style="--a:4;--w:17"></i><i style="--a:28;--w:20"></i><i style="--a:54;--w:15"></i><i style="--a:76;--w:19"></i></span>
          </div>
          <p class="rec-lead">Four client questions, answered by a partner:</p>
          <ol class="rec-list">
            <li><span class="rec-n" aria-hidden="true">1</span><div><strong>How much does a divorce cost?</strong><span class="rec-out">1 page &middot; 2 videos &middot; 2 posts</span></div></li>
            <li><span class="rec-n" aria-hidden="true">2</span><div><strong>How long does probate take?</strong><span class="rec-out">1 page &middot; 2 videos &middot; 2 posts</span></div></li>
            <li><span class="rec-n" aria-hidden="true">3</span><div><strong>Do I need a solicitor to remortgage?</strong><span class="rec-out">1 page &middot; 2 videos &middot; 2 posts</span></div></li>
            <li><span class="rec-n" aria-hidden="true">4</span><div><strong>What happens at a first meeting?</strong><span class="rec-out">1 page &middot; 2 videos &middot; 2 posts</span></div></li>
          </ol>
          <div class="rec-sum">
            <span>''' + ic('file-text') + r'''4 answer pages</span>
            <span>''' + ic('video-camera') + r'''8 short videos</span>
            <span>''' + ic('chat-circle-dots') + r'''8 posts</span>
          </div>
        </div>
        <figcaption class="sr-only">An example of one recorded hour: four client questions, each turned into one answer page, two short videos and two posts.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── DEFINITION ── -->
<section class="sec" id="what" aria-labelledby="whatTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="whatTitle">What is expert content?</h2>
      </div>
      <div class="answer rv">
        <p><strong>Expert content is material that comes from the person who does the work: the solicitor, the dentist or the adviser, speaking from cases they have handled.</strong> It answers the questions clients really ask, in that person&rsquo;s own words, with their name on it and a date that shows when it was last checked.</p>
        <p>It is the opposite of the generic article. Any firm can publish &ldquo;five things to know about probate&rdquo;, and any AI tool can write it in a minute. Only your partner can say what goes wrong most often in a probate application, what it usually costs at your firm, and what they tell a client on the first call.</p>
        <p>The hard part has never been knowledge. It is time. A partner can answer a client question in two minutes of talking and will not find two hours to write the answer down. So we record the talking and do the writing.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── EXPLAINER VIDEO ── -->
<section class="sec" id="video" aria-labelledby="videoTitle">
  <div class="container">
    <div class="video-grid">
      <div>
        <h2 class="sec-h2" id="videoTitle">See the month in 28 seconds</h2>
        <p class="sec-sub">One question, one recorded hour, and what comes out of it. No sound needed.</p>
        <ol class="video-points">
          <li><span class="mono">0:00</span><span>A client types a question</span></li>
          <li><span class="mono">0:05</span><span>The answer is in a partner&rsquo;s head</span></li>
          <li><span class="mono">0:10</span><span>What one recorded hour becomes</span></li>
          <li><span class="mono">0:17</span><span>The two rules we do not bend</span></li>
        </ol>
      </div>
      <div class="rv">
        <div class="video-frame">
          <video controls playsinline preload="none" poster="/videos/services/expert-content-poster.jpg" data-video="expert-content" aria-label="28-second explainer of how one recorded hour becomes a month of content">
            <source src="/videos/services/expert-content.mp4" type="video/mp4">
          </video>
        </div>
        <p class="video-cap">The questions in the video are examples.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── EVIDENCE ── -->
<section class="sec" id="data" aria-labelledby="dataTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="dataTitle">Why does it have to come from the partner?</h2>
      <p class="sec-sub">Three reasons, each with a source you can check.</p>
    </div>
    <div class="stats rv">
      <div class="stat-row">
        <span class="stat-num">42%</span>
        <p>of the citations in local AI answers pointed to the business&rsquo;s own website, more than any other kind of source. What your site says in its own words is the first thing an assistant reads.
          <span class="stat-src">Source: <a href="https://www.brightlocal.com/research/local-ai-visibility-study/" target="_blank" rel="noopener noreferrer">BrightLocal local AI visibility study</a>, September 2026, 1.9 million citations, United States.</span></p>
      </div>
    </div>
    <div class="quote-wrap rv">
      <div class="quote-stack">
        <blockquote class="quote">
          <p>&ldquo;Is it self-evident to your visitors who authored your content? Do pages carry a byline, where one might be expected?&rdquo;</p>
          <cite><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener noreferrer">Google Search Central</a>, questions to ask about your own content</cite>
        </blockquote>
        <blockquote class="quote">
          <p>&ldquo;Fabricating creator profiles (such as by using AI-generated headshots, made-up names, or false credentials to make content appear as if it was written by human experts) is a form of deception.&rdquo;</p>
          <cite><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener noreferrer">Google Search Central</a>, the same page, updated 5 October 2026</cite>
        </blockquote>
      </div>
      <div class="prose">
        <p>Google asks three things of any page: who made it, how it was made, and why. It asks whether the content shows first-hand expertise, and it now names invented experts as deception that marks a page as low quality. A real partner with a real byline is the plainest answer to all of that.</p>
        <p>The third reason is your regulator. In August 2026 the Solicitors Regulation Authority issued a <a class="txt-link" href="https://www.sra.org.uk/solicitors/guidance/misuse-ai/" target="_blank" rel="noopener noreferrer">warning notice on the misuse of AI</a>. It deals with legal work and not with marketing, but its principle is the one we work to: the solicitor stays accountable for anything produced with AI.</p>
        <p><strong>Read this with care.</strong> No study shows that a partner&rsquo;s name on a page makes an assistant cite it. The evidence supports something narrower. Assistants lean on firm websites, Google asks who wrote a page, and regulators hold the firm responsible for what it publishes. A real expert, named and checked, meets all three.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── OUTPUTS ── -->
<section class="sec" id="outputs" aria-labelledby="outputsTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="outputsTitle">What one recorded hour becomes</h2>
      <p class="sec-sub">Everything below comes out of the same 60 minutes. None of it starts from a blank prompt.</p>
    </div>
    <div class="split-wide">
      <div class="outs rv">
        <div class="out-row">
          <span class="stat-num">4</span>
          <div><h3>Answer pages</h3><p>One page for each question, 600 to 900 words. The short answer comes first, then the detail, then fees or timescales where you publish them. Each page carries the partner&rsquo;s name, their role and the date it was last reviewed.</p></div>
        </div>
        <div class="out-row">
          <span class="stat-num">8</span>
          <div><h3>Short videos</h3><p>Two for each question, 30 to 60 seconds long, cut from the recording. The partner on camera, captions on screen, in vertical and square formats.</p></div>
        </div>
        <div class="out-row">
          <span class="stat-num">8</span>
          <div><h3>Posts</h3><p>Four for the partner&rsquo;s LinkedIn profile and four for your Google Business Profile. Each one points to an answer page.</p></div>
        </div>
        <div class="out-row">
          <span class="stat-num">4</span>
          <div><h3>Quote cards</h3><p>One graphic for each question in your firm&rsquo;s colours, for the feed and for the top of the page.</p></div>
        </div>
      </div>
      <figure class="card-fig rv">
        <img src="/images/services/quote-card-template.webp" alt="Quote card template: a client question as the headline, the partner&rsquo;s answer beneath it, and their name and role at the foot" loading="lazy" decoding="async" width="720" height="900">
        <figcaption>The quote card template with placeholder text. Yours carries the partner&rsquo;s words, their name and your firm&rsquo;s colours.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── HOW IT WORKS ── -->
<section class="sec" id="how" aria-labelledby="howTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="howTitle">How a month works</h2>
        <p class="sec-sub">Five steps. The partner is needed for two of them.</p>
      </div>
      <ol class="steps rv">
        <li class="step">
          <span class="step-n" aria-hidden="true">01</span>
          <h3>Choose the questions</h3>
          <p>We bring a shortlist from your AI visibility check, your intake calls and the searches that already reach your site. You pick four.</p>
          <span class="step-meta">Week 1</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">02</span>
          <h3>Record the hour</h3>
          <p>A video call with one partner. We ask, and they answer the way they would answer a client. There is no script and no preparation beyond seeing the questions.</p>
          <span class="step-meta">Week 1, 60 minutes of the partner&rsquo;s time</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">03</span>
          <h3>Draft and cut</h3>
          <p>We turn the recording into pages, clips and posts. AI makes the transcript and a first rough draft. A person edits every line against what was said.</p>
          <span class="step-meta">Week 2</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">04</span>
          <h3>Partner review</h3>
          <p>The partner reads the four pages and watches the clips. Changes come back as tracked edits, and your compliance contact signs off.</p>
          <span class="step-meta">Week 3, about 30 minutes of the partner&rsquo;s time</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">05</span>
          <h3>Publish</h3>
          <p>We publish to your site and profiles, or hand everything to your web team with instructions. The next recording is booked before the month ends.</p>
          <span class="step-meta">Week 4</span>
        </li>
      </ol>
    </div>
  </div>
</section>

<!-- ── COMPARISON ── -->
<section class="sec" id="compare" aria-labelledby="compareTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="compareTitle">How does this compare with other ways to get content?</h2>
      <p class="sec-sub">There are four ways a firm ends up with articles on its website. They differ most in where the knowledge comes from.</p>
    </div>
''' + table(
    'A general comparison, not survey data.',
    ['<span class="sr-only">Compared on</span>', 'AI-written articles', 'An agency writer', 'The partner writes', 'A recorded hour'],
    [
        ['Where the knowledge comes from', 'The model&rsquo;s training data, which is the same for every firm.',
         'A writer&rsquo;s research. The writer is rarely a lawyer or a clinician.', 'The partner.',
         'The partner, in their own spoken words.'],
        ['Partner time each month', 'A review, if anyone remembers to do one.', 'A briefing and several rounds of corrections.',
         'Hours for every article.', 'About 90 minutes.'],
        ['Named author', 'Often nobody, or a name on work that person did not do.', 'Usually the firm.', 'Yes.',
         'Yes, with their role and a review date.'],
        ['Main risk', 'It reads like every other site, and nobody checked the errors.', 'Accurate but generic.',
         'It does not get written.', 'It needs a partner who is willing to talk.'],
    ], us=4) + r'''
  </div>
</section>

<!-- ── ACCESS ── -->
<section class="sec" id="access" aria-labelledby="accessTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="accessTitle">What we need from you</h2>
      <p class="sec-sub">An hour of one person&rsquo;s time, somewhere quiet, and someone who can say yes.</p>
    </div>
    <div class="access rv">
      <div class="access-card">
        <h3>Each month</h3>
        <ul>
          <li>''' + ic('check-circle') + r'''<div>One partner for a 60-minute video call <span>and about 30 minutes to review</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>A laptop with a camera in a quiet room <span>we send a short setup guide</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>Your logo, colours and fonts</div></li>
          <li>''' + ic('check-circle') + r'''<div>An editor login for your website <span>or a web contact who will publish for you</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>One person who signs off for compliance</div></li>
        </ul>
      </div>
      <div class="access-card is-never">
        <h3>We never ask for</h3>
        <ul>
          <li>''' + ic('x-circle') + r'''<div>Client names or matter details</div></li>
          <li>''' + ic('x-circle') + r'''<div>Your practice or patient management system</div></li>
          <li>''' + ic('x-circle') + r'''<div>The partner&rsquo;s LinkedIn password <span>posts arrive ready to paste</span></div></li>
          <li>''' + ic('x-circle') + r'''<div>Owner rights on any account</div></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ── RULES ── -->
<section class="sec" id="promise" aria-labelledby="promiseTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="promiseTitle">The rules we work by</h2>
      <p class="sec-sub">The first two are not negotiable. They are the reason the content can carry a partner&rsquo;s name.</p>
    </div>
    <div class="guards rv">
      <div class="guard">''' + ic('user-circle') + r'''<h3>A real person on camera</h3><p>The partner appears as themselves. No avatars, no cloned voices and no generated headshots.</p></div>
      <div class="guard">''' + ic('check-circle') + r'''<h3>Nothing goes live without sign-off</h3><p>Every page, clip and post is approved by the partner and by whoever handles compliance at your firm.</p></div>
      <div class="guard">''' + ic('microphone') + r'''<h3>Only what was said</h3><p>Pages are built from the recording. If we add a fact the partner did not say, it is marked for them to check.</p></div>
      <div class="guard">''' + ic('lock-simple') + r'''<h3>No client details</h3><p>The questions are general ones. Anything that could identify a client is cut before the first draft.</p></div>
      <div class="guard">''' + ic('prohibit') + r'''<h3>No ranking promises</h3><p>We do not promise positions, citations or enquiries. We promise the content, on time and checked.</p></div>
      <div class="guard">''' + ic('key') + r'''<h3>Everything stays yours</h3><p>The recordings, pages, clips and posts belong to the firm, with no licence to renew.</p></div>
    </div>
  </div>
</section>

<!-- ── PRICING ── -->
<section class="sec" id="pricing" aria-labelledby="pricingTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="pricingTitle">What it costs</h2>
      <p class="sec-sub">One monthly price, or a single session to see the output first.</p>
    </div>
    <div class="price-grid rv">
      <div class="plan is-main">
        <div class="plan-top">
          <h3 class="plan-name">Monthly</h3>
          <span><span class="p-price">$1,497</span><span class="p-unit">a month</span></span>
        </div>
        <p>One recorded hour, turned into a month of content.</p>
        <ul>
          <li>''' + ic('check-circle') + r'''One 60-minute recorded interview</li>
          <li>''' + ic('check-circle') + r'''Four answer pages with the partner&rsquo;s byline</li>
          <li>''' + ic('check-circle') + r'''Eight short captioned videos</li>
          <li>''' + ic('check-circle') + r'''Eight posts for LinkedIn and Google Business Profile</li>
          <li>''' + ic('check-circle') + r'''Four quote cards in your firm&rsquo;s colours</li>
          <li>''' + ic('check-circle') + r'''Publishing, or a handover to your web team</li>
        </ul>
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="pricing">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
      </div>
      <div class="plan-side">
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Single session</h3>
            <span><span class="p-price">$997</span><span class="p-unit">one time</span></span>
          </div>
          <p>One recorded hour, two answer pages, four short videos and four posts. A way to see the output before you commit to a month.</p>
          <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-ghost" data-loc="pricing-single">Try one session</a>
        </div>
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Free AI visibility check</h3>
            <span><span class="p-price">$0</span></span>
          </div>
          <p>Five client questions on three assistants. It shows which questions your website does not answer, which is where the first recording starts.</p>
          <a href="/ai-visibility#check" class="btn-ghost">Get the free check</a>
        </div>
      </div>
    </div>
    <p class="price-note">Prices are in US dollars. Transcription and editing costs are included. There is no setup fee and no minimum term on the monthly plan.</p>
  </div>
</section>

<!-- ── BREAK-EVEN ── -->
<section class="sec" id="worth" aria-labelledby="worthTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="worthTitle">How many new clients would cover a month?</h2>
        <div class="prose rv">
          <p>We do not forecast enquiries from content, and you should be wary of anyone who does. Pages take time to be found, and nobody can tell you in advance which one a client will read before they call.</p>
          <p>What you can work out is how little it would take to pay for itself. Move the slider to what one new client is worth to your firm.</p>
        </div>
      </div>
      <div class="calc rv">
        <div class="calc-row">
          <label for="feeRange"><span>Average fee from one new client</span><output id="feeOut" for="feeRange">$2,000</output></label>
          <input type="range" id="feeRange" min="300" max="10000" step="100" value="2000">
        </div>
        <div class="calc-out" aria-live="polite">
          <span class="calc-big" id="calcBig">1 client</span>
          <p id="calcText">One new client at that fee covers the month.</p>
        </div>
        <p class="calc-fine">Monthly fee $1,497. This is arithmetic, not a forecast.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── REGULATED FIRMS ── -->
<section class="sec" id="regulated" aria-labelledby="regTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="regTitle">If your firm is regulated</h2>
      </div>
      <div class="prose rv">
        <p>For solicitors in England and Wales, the <a class="txt-link" href="https://www.sra.org.uk/solicitors/standards-regulations/transparency-rules/" target="_blank" rel="noopener noreferrer">SRA Transparency Rules</a> already require price and service information on your website for certain services. An answer page is a natural home for it, written in the plain English clients search in.</p>
        <p>Dental practices in the UK follow the General Dental Council&rsquo;s <a class="txt-link" href="https://www.gdc-uk.org/standards-guidance/standards-and-guidance/gdc-guidance-for-dental-professionals/guidance-on-advertising" target="_blank" rel="noopener noreferrer">guidance on advertising</a>. Health practitioners in Australia cannot use patient testimonials about clinical care under the <a class="txt-link" href="https://www.ahpra.gov.au/Resources/Advertising-hub/Advertising-guidelines-and-other-guidance/Advertising-guidelines.aspx" target="_blank" rel="noopener noreferrer">Ahpra advertising guidelines</a>, which is one more reason the practitioner speaks and patients do not.</p>
        <p>Every page goes to your compliance contact before it is published. We are not a law firm and this is not compliance advice. The decision stays with your compliance officer.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── FAQ ── -->
<section class="sec" id="faq" aria-labelledby="faqTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="faqTitle">Common questions</h2>
        <p class="sec-sub">Anything not covered here, ask on the call.</p>
      </div>
      <div class="faq-list">
''' + faq_html(FAQ) + r'''
      </div>
    </div>
  </div>
</section>

<!-- ── RELATED ── -->
<section class="sec" id="next" aria-labelledby="nextTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="nextTitle">Related services</h2>
    </div>
    <div class="related rv">
      <a class="rel-card" href="/ai-visibility">
        <span class="rel-kicker">AI Visibility</span>
        <h3>Find the questions first</h3>
        <p>We ask ChatGPT, Gemini and Perplexity the questions your clients ask and count how often your firm is named. The questions where you are missing are the ones worth recording.</p>
        <span class="rel-go">See how it works''' + ic('arrow-right') + r'''</span>
      </a>
      <a class="rel-card" href="/ad-creative-testing">
        <span class="rel-kicker">Ad Creative Testing</span>
        <h3>Selling products online?</h3>
        <p>For e-commerce brands: new ad concepts every month and a read on which one wins.</p>
        <span class="rel-go">See how it works''' + ic('arrow-right') + r'''</span>
      </a>
    </div>
  </div>
</section>

<!-- ── SOURCES ── -->
<section class="sec" id="sources" aria-labelledby="sourcesTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="sourcesTitle">Sources</h2>
        <p class="sec-sub">Every figure, quote and rule on this page, with where it came from. Checked on {{TODAY_LONG}}.</p>
      </div>
      <ol class="sources">
        <li><a href="https://www.brightlocal.com/research/local-ai-visibility-study/" target="_blank" rel="noopener noreferrer">BrightLocal, local AI visibility study</a>. Business websites made up 42% of the citations in local AI answers. About 200,000 searches and 1.9 million citations, United States. Published 16 September 2026.</li>
        <li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener noreferrer">Google Search Central, Creating helpful, reliable, people-first content</a>. The who, how and why questions, and the passage on fabricated creator profiles. Last updated 5 October 2026.</li>
        <li><a href="https://www.sra.org.uk/solicitors/guidance/misuse-ai/" target="_blank" rel="noopener noreferrer">Solicitors Regulation Authority, warning notice on the misuse of AI</a>. Issued 17 August 2026.</li>
        <li><a href="https://www.sra.org.uk/solicitors/standards-regulations/transparency-rules/" target="_blank" rel="noopener noreferrer">Solicitors Regulation Authority, Transparency Rules</a>.</li>
        <li><a href="https://www.gdc-uk.org/standards-guidance/standards-and-guidance/gdc-guidance-for-dental-professionals/guidance-on-advertising" target="_blank" rel="noopener noreferrer">General Dental Council, Guidance on advertising</a>.</li>
        <li><a href="https://www.ahpra.gov.au/Resources/Advertising-hub/Advertising-guidelines-and-other-guidance/Advertising-guidelines.aspx" target="_blank" rel="noopener noreferrer">Ahpra, Guidelines for advertising a regulated health service</a>.</li>
      </ol>
    </div>
  </div>
</section>

<!-- ── FINAL CTA ── -->
<section id="final-cta" aria-labelledby="ctaTitle">
  <div class="container">
    <div class="cta-wrap">
      <h2 id="ctaTitle">Find the questions worth an hour of a partner's time</h2>
      <p>The free AI visibility check shows which client questions your website does not answer. Start there, or book a call and we will plan the first recording.</p>
      <div class="cta-actions">
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="final">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
        <a href="/ai-visibility#check" class="btn-ghost">Get the free check</a>
      </div>
    </div>
  </div>
</section>
'''

JS = r'''
/* Break-even: how many new clients pay for a month */
(function(){
  const range=document.getElementById('feeRange');
  if(!range) return;
  const out=document.getElementById('feeOut'),big=document.getElementById('calcBig'),text=document.getElementById('calcText');
  const FEE=1497;
  const money=n=>'$'+n.toLocaleString('en-US');
  function update(){
    const v=Number(range.value);
    const need=Math.ceil(FEE/v);
    out.textContent=money(v);
    big.textContent=need+(need===1?' client':' clients');
    const times=v/FEE;
    text.textContent=need===1
      ?(times>=1.5?'One new client at that fee covers the month '+(Math.round(times*10)/10)+' times over.':'One new client at that fee covers the month.')
      :'It takes '+need+' new clients at that fee to cover the month.';
  }
  range.addEventListener('input',update);
  update();
})();
'''

SERVICE = {
    'name': 'Expert content from recorded partner interviews',
    'serviceType': 'Content production for professional firms',
    'description': ('Coremagna records a one-hour interview with a partner each month and turns it into four answer pages '
                    'for the firm\'s website, eight short videos of the partner, eight posts for LinkedIn and Google Business '
                    'Profile and four quote cards. A real person is on camera and the firm approves everything before it is published.'),
    'audience': {'@type': 'BusinessAudience', 'name': 'Law firms, dental practices and other professional firms'},
    'offers': [
        offer('Single session', 997, 'One recorded hour, two answer pages, four short videos and four posts.'),
        offer('Monthly', 1497, 'One recorded hour a month, four answer pages, eight short videos, eight posts and four quote cards.', 'month'),
    ],
}
VIDEO = {
    'name': 'How one recorded hour becomes a month of content',
    'description': ('A client types a question that a partner could answer in two minutes. The video shows how one recorded '
                    'hour a month becomes four answer pages, eight short videos and eight posts, and the two rules the work follows.'),
    'thumbnailUrl': SITE + '/videos/services/expert-content-poster.jpg',
    'contentUrl': SITE + '/videos/services/expert-content.mp4',
    'duration': 'PT28S',
}

PAGE = {
    'n': 3,
    'slug': SLUG,
    'title': TITLE,
    'desc': DESC,
    'og_title': 'One hour with a partner becomes a month of content',
    'og_desc': 'One recorded hour a month becomes four answer pages, eight short videos and eight posts. A real person on camera and sign-off on everything.',
    'og_alt': 'One hour with a partner becomes a month of content. Coremagna Expert Content.',
    'css': CSS,
    'body': BODY,
    'js': JS,
    'icons': ['arrow-right', 'check-circle', 'x-circle', 'user-circle', 'microphone', 'lock-simple', 'prohibit', 'key',
              'file-text', 'video-camera', 'chat-circle-dots'],
    'mail_subject': 'Expert content',
    'jsonld': graph(SLUG, 'Expert Content', TITLE, DESC, SERVICE, VIDEO, 'Expert Content'),
}
