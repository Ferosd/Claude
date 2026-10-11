from parts import ic, graph, offer, faq_html, table, SITE

SLUG = 'ai-visibility'
TITLE = 'AI Visibility Audit and Fixes for Local Firms | Coremagna'
DESC = ('We ask ChatGPT, Gemini and Perplexity the questions your clients ask, count how often your firm is named, '
        'and fix what decides it. Free 15-answer check.')

CSS = r'''
/* ── AI Visibility: hero answer mock ── */
.chat-body{padding:20px;display:flex;flex-direction:column;gap:14px}
.chat-q{align-self:flex-end;max-width:88%;padding:10px 16px;border-radius:16px 16px 4px 16px;background:var(--accent-dim);border:1px solid var(--border-hover);font-size:15px;font-weight:500;line-height:1.4;color:var(--text)}
.chat-lead{font-size:14px;color:var(--text-muted)}
.chat-list li{display:grid;grid-template-columns:32px minmax(0,1fr);gap:14px;align-items:center;padding:12px 0;border-top:1px solid var(--border)}
.chat-n{width:32px;height:32px;border-radius:50%;border:1px solid var(--border-hover);color:var(--accent);font-family:'JetBrains Mono',monospace;font-size:13px;display:grid;place-items:center}
.chat-list strong{display:block;font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:19px;line-height:1.2;letter-spacing:-0.01em}
.chat-why{display:block;font-size:14px;color:var(--text-muted);line-height:1.4}
.chat-miss{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 16px;border-radius:12px;background:var(--red-dim);border:1px solid var(--red)}
.chat-miss strong{font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:19px;letter-spacing:-0.01em}
.chat-miss span{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--red);white-space:nowrap}
/* The answer builds line by line on load. CSS only, so it never depends on a script. */
@keyframes chatIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.chat-lead,.chat-list li,.chat-miss{animation:chatIn 0.7s var(--ease) both}
.chat-lead{animation-delay:0.35s}
.chat-list li:nth-child(1){animation-delay:0.6s}
.chat-list li:nth-child(2){animation-delay:0.85s}
.chat-list li:nth-child(3){animation-delay:1.1s}
.chat-miss{animation-delay:1.6s}

/* ── Repeat runs grid ── */
.runs{display:grid;grid-template-columns:auto repeat(5,minmax(0,1fr));gap:8px;align-items:center}
.runs-lab{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text-muted);padding-right:8px;white-space:nowrap}
.runs-col{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text-fine);text-align:center}
.run{aspect-ratio:1;border-radius:10px;border:1px solid var(--border);background:var(--surface-2);display:grid;place-items:center;font-size:20px}
.run.hit{border-color:var(--border-hover);background:var(--accent-dim);color:var(--accent)}
.run.miss::before{content:'';width:26%;height:2px;border-radius:2px;background:var(--text-fine)}
.runs-result{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-top:20px;padding-top:20px;border-top:1px solid var(--border)}
.runs-big{font-family:'JetBrains Mono',monospace;font-size:clamp(2.2rem,4.5vw,3.5rem);font-weight:500;line-height:1;letter-spacing:-0.03em;color:var(--text)}
.runs-result p{font-size:15px;color:var(--text-muted)}

/* ── Sample report ── */
.rep-block{padding-top:18px;margin-top:18px;border-top:1px solid var(--border)}
.rep-h{font-family:'Cabinet Grotesk',sans-serif;font-size:13px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px}
.bar-row{display:grid;grid-template-columns:104px minmax(0,1fr) 88px;gap:12px;align-items:center;font-size:14px;color:var(--text-secondary);padding:5px 0}
.bar-row b{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:13px;text-align:right;color:var(--text)}
.bar-row.is-you{color:var(--text)}
.bar-row.is-you .bar i{background:var(--accent)}
.fix-row{display:grid;grid-template-columns:22px minmax(0,1fr) auto;gap:10px;align-items:start;font-size:14px;line-height:1.45;color:var(--text-secondary);padding:9px 0;border-top:1px solid var(--border)}
.fix-row:first-of-type{border-top:0}
.fix-row .mono{font-size:12px;color:var(--text-fine);padding-top:2px}
.prio{font-family:'JetBrains Mono',monospace;font-size:11px;padding:2px 8px;border-radius:99px;border:1px solid var(--border);color:var(--text-muted);white-space:nowrap}
.prio.hi{color:var(--red);border-color:var(--red)}
.prio.mid{color:var(--yellow);border-color:var(--yellow)}

/* ── Free check form ── */
.lead{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:32px}
.lead-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field label{font-size:12px;font-weight:500;letter-spacing:0.04em;text-transform:uppercase;color:var(--text-muted)}
.field input{min-height:48px;width:100%;background:var(--surface-2);border:1px solid var(--border);border-radius:8px;padding:0 14px;color:var(--text);font:inherit;font-size:16px}
.field input::placeholder{color:var(--text-fine)}
.field input:focus-visible{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.lead .btn-primary{width:100%;margin-top:20px}
.lead-fine{margin-top:12px;font-size:13px;color:var(--text-muted)}
.lead-fine a{text-decoration:underline;text-underline-offset:3px}
.lead-err{display:none;margin-top:12px;font-size:14px;color:var(--red)}
.lead-err.is-on{display:block}
.lead-err a{text-decoration:underline}
.lead-ok h3{font-size:22px;margin-bottom:8px}
.lead-ok p{font-size:15px;color:var(--text-muted)}
.check-list{display:flex;flex-direction:column;gap:12px;margin-top:var(--space-lg)}
.check-list li{display:grid;grid-template-columns:20px minmax(0,1fr);gap:12px;font-size:15px;line-height:1.5;color:var(--text-secondary)}
.check-list .ic{font-size:20px;color:var(--accent);margin-top:1px}

@media(max-width:768px){
  .lead{padding:28px 20px}
  .lead-grid{grid-template-columns:1fr}
  .bar-row{grid-template-columns:84px minmax(0,1fr) 78px;gap:8px}
  .chat-list strong,.chat-miss strong{font-size:17px}
}
@media(prefers-reduced-motion:reduce){
  .chat-lead,.chat-list li,.chat-miss{animation:none}
}
'''

FAQ = [
    ('Can you guarantee that ChatGPT will recommend us?',
     'No, and be careful with anyone who says they can. An assistant builds each answer fresh from sources it picks at that moment, and the same question returns a different list almost every time. What we commit to is the work on your website, your profile and your listings, and an honest before and after count that includes the questions where nothing moved.'),
    ('Is this different from SEO?',
     'Mostly it is the same work with a different measurement. Google says so itself: optimising for its AI answers &ldquo;is still SEO&rdquo;, and a page has to be indexed and eligible for a normal search snippet before it can appear in one. What changes is what we count, which is how often you are named in an answer, and where we look, which includes ChatGPT and Perplexity as well as Google.'),
    ('Which assistants do you check?',
     'ChatGPT, Gemini and Perplexity, each with web search switched on and the location set to your town where the assistant allows it. For Google&rsquo;s AI Overviews and AI Mode we also read the generative AI report in your Search Console, which Google opened to every site in August 2026. That report shows impressions by page. It does not show the questions people asked or whether they clicked.'),
    ('Why do you ask every question five times?',
     'Because one answer is close to random. In a SparkToro and Gumshoe study, the same prompt gave the same list of brands less than once in 100 tries. Asking each question five times on three assistants gives 15 answers per question, which is enough to see whether you are named often, sometimes or never.'),
    ('Are the answers you collect the same ones my clients see?',
     'Close, but not identical. We collect answers through each assistant&rsquo;s API so that every run is logged with a date and can be repeated. A person using the app can get a slightly different answer because of their location, their history and the app version. We check a sample by hand in the apps and note any gap in the report.'),
    ('How long before a fix shows up in the answers?',
     'There is no fixed delay and we will not invent one. A change to a Google Business Profile can show in Google&rsquo;s own results within days. An assistant that relies on its own index can take weeks. That is why the second measurement comes 30 days after the sprint ends, and why the report also lists what did not move.'),
    ('What access do we need to give you?',
     'None for the free check. For the sprint: manager access to your Google Business Profile, an editor login for your website or the name of your developer, and one person who can approve wording. Search Console access is optional. We never need your case files, your practice management system or your inbox.'),
    ('Does this clash with our SEO agency?',
     'It should not. If your agency manages the website, we send them the fix list and they make the changes. Most of the sprint covers things a monthly SEO retainer rarely includes: asking the assistants, the services section of your Google Business Profile, fee and FAQ wording, and replies to recent reviews.'),
    ('Do you work with firms outside the UK?',
     'Yes. We work in English with firms in the UK, Ireland, Australia, New Zealand, Canada and the United States. The questions are written the way people in your country ask them, so solicitor, attorney or lawyer as it applies, and the location is set to your town.'),
    ('Do you use AI to do this work?',
     'Yes, for collecting and sorting the answers and for first drafts of wording. A person reads the results, decides what belongs on the fix list and edits every draft. Nothing is published on your website or profile until someone at your firm has approved it.'),
]

BODY = r'''
<!-- ── HERO ── -->
<section id="hero" aria-labelledby="heroH1">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">AI Visibility</span></li></ol>
    </nav>
    <div class="hero-grid">
      <div class="hero-text">
        <p class="hero-kicker">AI Visibility</p>
        <h1 class="hero-h1" id="heroH1">Find out whether AI recommends your firm</h1>
        <p class="hero-sub">We ask ChatGPT, Gemini and Perplexity the questions your clients ask, count how often your firm is named, then fix the things those answers are built from.</p>
        <div class="hero-actions">
          <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="hero">Book a call
            ''' + ic('arrow-right') + r'''
          </a>
          <a href="#check" class="btn-ghost">Get the free check</a>
        </div>
        <p class="hero-fine">The free check is 15 answers on one page. It needs no access to anything of yours.</p>
        <p class="byline">By <a href="/about">Ferit Patefe</a>, founder of Coremagna. Updated <time datetime="{{TODAY}}">{{TODAY_LONG}}</time>.</p>
      </div>

      <figure class="mock chat">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>AI assistant</span>
          <span class="tag">Example answer</span>
        </div>
        <div class="chat-body">
          <p class="chat-q">Who is the best family law solicitor in Leeds?</p>
          <p class="chat-lead">Three firms come up most often for this:</p>
          <ol class="chat-list">
            <li><span class="chat-n" aria-hidden="true">1</span><div><strong>Firm A</strong><span class="chat-why">Fixed fees are listed on its website</span></div></li>
            <li><span class="chat-n" aria-hidden="true">2</span><div><strong>Firm B</strong><span class="chat-why">Hundreds of recent Google reviews</span></div></li>
            <li><span class="chat-n" aria-hidden="true">3</span><div><strong>Firm C</strong><span class="chat-why">A clear page for every service it offers</span></div></li>
          </ol>
          <div class="chat-miss"><strong>Your firm</strong><span>Not mentioned</span></div>
        </div>
        <figcaption class="sr-only">An example of an AI answer that names three competing firms and leaves yours out. The firm names are placeholders.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── DEFINITION ── -->
<section class="sec" id="what" aria-labelledby="whatTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="whatTitle">What is AI visibility?</h2>
      </div>
      <div class="answer rv">
        <p><strong>AI visibility is how often an AI assistant names your business when someone asks it for a recommendation.</strong> A person types a question such as &ldquo;who is the best family law solicitor in Leeds&rdquo; into ChatGPT, Gemini or Perplexity, and the assistant answers with two to four firms. If your firm is one of them, you are visible for that question. If it is not, that person never sees you, whatever your Google ranking is.</p>
        <p>It is measured as a share. We ask the same set of client questions many times on each assistant and count the answers that name you. A firm named in 15 of 150 answers has 10% visibility. One answer by itself tells you very little, because the same question returns a different list almost every time it is asked.</p>
        <p>An AI visibility audit measures that share, shows which competitors are named instead of you, and lists the sources the assistants relied on. A fix sprint then changes what those sources say about your firm.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── EXPLAINER VIDEO ── -->
<section class="sec" id="video" aria-labelledby="videoTitle">
  <div class="container">
    <div class="video-grid">
      <div>
        <h2 class="sec-h2" id="videoTitle">See the check in 38 seconds</h2>
        <p class="sec-sub">One client question, one example answer, and what we do about it. No sound needed.</p>
        <ol class="video-points">
          <li><span class="mono">0:00</span><span>A client asks an assistant for a solicitor</span></li>
          <li><span class="mono">0:05</span><span>Three firms are named and yours is not</span></li>
          <li><span class="mono">0:19</span><span>Why one answer proves nothing</span></li>
          <li><span class="mono">0:26</span><span>What the fix sprint changes</span></li>
        </ol>
      </div>
      <div class="rv">
        <div class="video-frame">
          <video controls playsinline preload="none" poster="/videos/services/ai-visibility-poster.jpg" data-video="ai-visibility" aria-label="38-second explainer of the AI visibility check">
            <source src="/videos/services/ai-visibility.mp4" type="video/mp4">
          </video>
        </div>
        <p class="video-cap">Firm names and the 4 of 15 count in the video are examples, not results.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── DATA ── -->
<section class="sec" id="data" aria-labelledby="dataTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="dataTitle">How many people ask AI for a recommendation?</h2>
      <p class="sec-sub">Enough to matter, and the number is moving fast. Here is what has been measured so far.</p>
    </div>
    <div class="stats rv">
      <div class="stat-row">
        <span class="stat-num">45%</span>
        <p>of US consumers used generative AI tools to get local business recommendations in the past year. One year earlier it was 6%.
          <span class="stat-src">Source: <a href="https://www.brightlocal.com/research/local-consumer-review-survey/" target="_blank" rel="noopener noreferrer">BrightLocal Local Consumer Review Survey</a>, February 2026, 1,002 US adults.</span></p>
      </div>
      <div class="stat-row">
        <span class="stat-num">42%</span>
        <p>of US consumers say they would use ChatGPT to research which lawyer to hire, up from 28% in 2025. Google is still first, at 72%.
          <span class="stat-src">Source: <a href="https://www.ilawyermarketing.com/what-online-sources-do-people-use-to-research-and-find-attorneys-in-2026/" target="_blank" rel="noopener noreferrer">iLawyerMarketing</a>, 2026, 1,110 US adults. A law firm marketing agency ran the survey, and it records what people say they would do.</span></p>
      </div>
      <div class="stat-row">
        <span class="stat-num">54%</span>
        <p>of UK adults now use AI tools such as ChatGPT, Copilot or Gemini. A year earlier it was 31%.
          <span class="stat-src">Source: <a href="https://www.ofcom.org.uk/media-use-and-attitudes/media-habits-adults/passive-social-media-use-ai-companionship-and-online-side-hustles-uk-adults-media-and-online-lives-revealed" target="_blank" rel="noopener noreferrer">Ofcom, Adults&rsquo; Media Use and Attitudes</a>, April 2026.</span></p>
      </div>
      <div class="stat-row">
        <span class="stat-num">66%</span>
        <p>of local searches on Google Maps showed the business being tracked. ChatGPT, Google AI Mode and AI Overviews named the same business in 32% to 38% of those searches.
          <span class="stat-src">Source: <a href="https://www.brightlocal.com/research/local-ai-visibility-study/" target="_blank" rel="noopener noreferrer">BrightLocal local AI visibility study</a>, September 2026, about 200,000 searches.</span></p>
      </div>
    </div>
    <div class="prose rv" style="margin-top:var(--space-xl)">
      <p><strong>Read these with care.</strong> Three of the four come from the United States, and two were published by companies that sell marketing services. Nobody has yet published good UK data on how many people choose a solicitor or a dentist through an AI assistant. The direction is clear. The size is not.</p>
    </div>
  </div>
</section>

<!-- ── WHY ONE ANSWER IS NOT ENOUGH ── -->
<section class="sec" id="repeat" aria-labelledby="repeatTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="repeatTitle">Why can't you just ask ChatGPT once?</h2>
        <div class="prose rv">
          <p>You can, and you should. But one answer is one draw from a hat. SparkToro and Gumshoe had 600 volunteers run the same 12 prompts nearly 3,000 times. The chance of getting the same list of brands twice was <strong>under 1 in 100</strong>.</p>
          <p>BrightLocal found the same thing for local businesses. Repeat a local search on an AI assistant and only <strong>21% to 33%</strong> of the businesses named are the ones named last time.</p>
          <p>So a screenshot of one answer proves very little, in either direction. What holds steady is how often a business is named across many runs. That share is the number we report.</p>
          <p class="stat-src">Sources: <a href="https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/" target="_blank" rel="noopener noreferrer">SparkToro and Gumshoe</a>, January 2026. <a href="https://www.brightlocal.com/research/local-ai-visibility-study/" target="_blank" rel="noopener noreferrer">BrightLocal</a>, September 2026.</p>
        </div>
      </div>
      <figure class="mock rv">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>One question, asked 15 times</span>
          <span class="tag">Example</span>
        </div>
        <div class="mock-body">
          <div class="runs" aria-hidden="true">
            <span></span><span class="runs-col">Run 1</span><span class="runs-col">Run 2</span><span class="runs-col">Run 3</span><span class="runs-col">Run 4</span><span class="runs-col">Run 5</span>
            <span class="runs-lab">ChatGPT</span><span class="run hit">''' + ic('check') + r'''</span><span class="run miss"></span><span class="run miss"></span><span class="run hit">''' + ic('check') + r'''</span><span class="run miss"></span>
            <span class="runs-lab">Gemini</span><span class="run miss"></span><span class="run miss"></span><span class="run hit">''' + ic('check') + r'''</span><span class="run miss"></span><span class="run miss"></span>
            <span class="runs-lab">Perplexity</span><span class="run miss"></span><span class="run hit">''' + ic('check') + r'''</span><span class="run miss"></span><span class="run miss"></span><span class="run miss"></span>
          </div>
          <div class="runs-result">
            <span class="runs-big">4 of 15</span>
            <p>answers named the firm, which is 27% visibility for this question</p>
          </div>
        </div>
        <figcaption class="sr-only">Example grid: the same question asked five times on ChatGPT, Gemini and Perplexity. The firm is named in 4 of the 15 answers.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── WHAT DECIDES IT ── -->
<section class="sec" id="signals" aria-labelledby="signalsTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="signalsTitle">What decides whether your firm is named?</h2>
      <p class="sec-sub">Assistants do not have a secret list. They read public sources and repeat what they find. These are the sources, and what we do to each one.</p>
    </div>
''' + table(
    'Citation shares are from BrightLocal&rsquo;s analysis of 1.9 million citations in local AI answers, September 2026, United States.',
    ['Source', 'Why it matters', 'What we do in the sprint'],
    [
        ['Your own website', '42% of the citations in local AI answers pointed to business websites, more than any other source.',
         'One clear page per service, with your location, your fees where you publish them, and answers to the questions we tested.'],
        ['Google Business Profile', '28.5% of citations. Google also says a profile helps a business show up in its AI answers.',
         'Categories, the services list, description, opening hours and the questions section, filled in and kept current.'],
        ['Reviews', 'Assistants quote review counts and what reviewers say when they explain a recommendation.',
         'A short review request you can send after a matter closes, and draft replies to your most recent reviews.'],
        ['Directories and registers', 'Sector directories and your regulator&rsquo;s register are where an assistant checks that a firm is real.',
         'The same name, address, phone number and service list on every listing the assistants cited in your baseline.'],
        ['Access for AI crawlers', 'A page an assistant cannot fetch cannot be cited. Some sites block these crawlers without knowing it.',
         'We check robots.txt and indexing, and open the door to the search crawlers of OpenAI, Perplexity and Anthropic.'],
        ['Structured data', 'Google says it is not required for AI answers. It still helps a machine read your address, hours and services correctly.',
         'We add the right schema for a law firm, a dental practice or a local business, and we do not oversell it.'],
    ], us=2) + r'''
    <div class="prose rv" style="margin-top:var(--space-xl)">
      <p><strong>What we leave out.</strong> We do not sell llms.txt files, paid mentions on forums or batches of AI-written articles as a route into AI answers. <a class="txt-link" href="https://developers.google.com/search/docs/fundamentals/ai-optimization-guide" target="_blank" rel="noopener noreferrer">Google&rsquo;s own guide</a> says none of them is needed, and that content people find unique and useful matters more than anything else on its list.</p>
    </div>
  </div>
</section>

<!-- ── HOW IT WORKS ── -->
<section class="sec" id="how" aria-labelledby="howTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="howTitle">How the check and the fix sprint work</h2>
        <p class="sec-sub">Five steps over about six weeks. Your part is one call and a few approvals.</p>
      </div>
      <ol class="steps rv">
        <li class="step">
          <span class="step-n" aria-hidden="true">01</span>
          <h3>Agree the questions</h3>
          <p>On a 30-minute call we settle ten questions real clients ask, in their words: by service, by town and by price.</p>
          <span class="step-meta">Day 1</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">02</span>
          <h3>Measure the baseline</h3>
          <p>Each question goes to three assistants, five times each. That is 150 answers. We record who was named, how often, and which sources each answer cited.</p>
          <span class="step-meta">Days 2 to 4</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">03</span>
          <h3>Run the fix sprint</h3>
          <p>Fourteen days of changes to your website, your Google Business Profile and your listings. You approve the wording before anything goes live.</p>
          <span class="step-meta">Days 5 to 18</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">04</span>
          <h3>Measure again</h3>
          <p>Thirty days after the sprint we run the same ten questions the same way, which gives another 150 answers. You get both sets of numbers side by side, including the ones that did not move.</p>
          <span class="step-meta">About day 48</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">05</span>
          <h3>Keep tracking if you want to</h3>
          <p>A monthly run of the same questions, a one-page report and small follow-up fixes. This part is optional.</p>
          <span class="step-meta">Monthly</span>
        </li>
      </ol>
    </div>
  </div>
</section>

<!-- ── SAMPLE REPORT ── -->
<section class="sec" id="report" aria-labelledby="reportTitle">
  <div class="container">
    <div class="split-wide">
      <figure class="mock rv">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>AI visibility report</span>
          <span class="tag">Sample with invented numbers</span>
        </div>
        <div class="mock-body">
          <p class="mock-meta"><span>Family law</span><span>Leeds</span><span>10 questions</span><span>150 answers</span></p>
          <div class="rep-block">
            <p class="rep-h">How often your firm was named</p>
            <div class="bar-row is-you"><span>ChatGPT</span><span class="bar"><i style="--v:16"></i></span><b>8 of 50</b></div>
            <div class="bar-row is-you"><span>Gemini</span><span class="bar"><i style="--v:10"></i></span><b>5 of 50</b></div>
            <div class="bar-row is-you"><span>Perplexity</span><span class="bar"><i style="--v:6"></i></span><b>3 of 50</b></div>
          </div>
          <div class="rep-block">
            <p class="rep-h">Who was named instead</p>
            <div class="bar-row"><span>Firm A</span><span class="bar"><i style="--v:61"></i></span><b>61%</b></div>
            <div class="bar-row"><span>Firm B</span><span class="bar"><i style="--v:44"></i></span><b>44%</b></div>
            <div class="bar-row"><span>Firm C</span><span class="bar"><i style="--v:38"></i></span><b>38%</b></div>
            <div class="bar-row is-you"><span>Your firm</span><span class="bar"><i style="--v:11"></i></span><b>11%</b></div>
          </div>
          <div class="rep-block">
            <p class="rep-h">Fix list in order</p>
            <div class="fix-row"><span class="mono">1</span><span>Add fees and what they cover to the family law page</span><span class="prio hi">High</span></div>
            <div class="fix-row"><span class="mono">2</span><span>Fill in the services list on the Google Business Profile</span><span class="prio hi">High</span></div>
            <div class="fix-row"><span class="mono">3</span><span>Answer six of the tested questions on the website</span><span class="prio mid">Medium</span></div>
            <div class="fix-row"><span class="mono">4</span><span>Reply to the last 20 reviews</span><span class="prio mid">Medium</span></div>
            <div class="fix-row"><span class="mono">5</span><span>Stop robots.txt blocking AI search crawlers</span><span class="prio">Low</span></div>
          </div>
        </div>
        <figcaption class="sr-only">A sample report with invented numbers: how often a firm was named on each assistant, which firms were named instead, and a fix list in priority order.</figcaption>
      </figure>
      <div>
        <h2 class="sec-h2" id="reportTitle">What the report looks like</h2>
        <div class="prose rv">
          <p>One page a partner can read in two minutes. It answers three questions: how often are we named, who is named instead of us, and what do we change first.</p>
          <p>Every number carries the date it was collected and the method behind it, so the second report can be compared with the first. The full list of 150 answers comes with it as a spreadsheet, with the sources each answer cited.</p>
          <p>The sample here uses invented numbers and placeholder firm names. Your report uses your town, your services and the firms that were really named.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── ACCESS ── -->
<section class="sec" id="access" aria-labelledby="accessTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="accessTitle">What we need from you</h2>
      <p class="sec-sub">The free check needs nothing. Every answer comes from public sources. The sprint needs a little access and one person who can say yes to wording.</p>
    </div>
    <div class="access rv">
      <div class="access-card">
        <h3>For the fix sprint</h3>
        <ul>
          <li>''' + ic('check-circle') + r'''<div>Manager access to your Google Business Profile</div></li>
          <li>''' + ic('check-circle') + r'''<div>An editor login for your website <span>or the name of your developer, and we send them the change list</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>One 30-minute call to agree the questions</div></li>
          <li>''' + ic('check-circle') + r'''<div>One person who approves wording before it goes live</div></li>
          <li>''' + ic('check-circle') + r'''<div>Search Console access as a restricted user <span>optional, for Google&rsquo;s AI impressions report</span></div></li>
        </ul>
      </div>
      <div class="access-card is-never">
        <h3>We never ask for</h3>
        <ul>
          <li>''' + ic('x-circle') + r'''<div>Client files or matter details</div></li>
          <li>''' + ic('x-circle') + r'''<div>Your practice or patient management system</div></li>
          <li>''' + ic('x-circle') + r'''<div>Your CRM or your inbox</div></li>
          <li>''' + ic('x-circle') + r'''<div>Owner rights on any account</div></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ── PROMISES ── -->
<section class="sec" id="promise" aria-labelledby="promiseTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="promiseTitle">What we cannot promise and what we can</h2>
      <p class="sec-sub">Nobody outside OpenAI, Google or Perplexity controls what their assistants say. So we promise the work and the measurement, and we put the limits in writing.</p>
    </div>
    <div class="guards rv">
      <div class="guard">''' + ic('prohibit') + r'''<h3>No ranking promises</h3><p>We will not tell you that an assistant will name your firm, or by when. We tell you what we changed and what the count was before and after.</p></div>
      <div class="guard">''' + ic('calendar-check') + r'''<h3>Dated numbers with the method</h3><p>Every figure shows the date, the questions and the number of runs, so anyone can repeat it.</p></div>
      <div class="guard">''' + ic('check-circle') + r'''<h3>You approve every change</h3><p>Nothing goes live on your website or your profile until someone at your firm has said yes.</p></div>
      <div class="guard">''' + ic('lock-simple') + r'''<h3>No client data</h3><p>The work uses public sources and your marketing accounts. We do not touch client records.</p></div>
      <div class="guard">''' + ic('arrows-clockwise') + r'''<h3>No lock-in</h3><p>The sprint is a one-time fee. Tracking runs month to month and stops with 30 days&rsquo; notice.</p></div>
      <div class="guard">''' + ic('key') + r'''<h3>Everything stays yours</h3><p>The pages, the profile, the question set and both reports belong to you, whether or not you keep working with us.</p></div>
    </div>
  </div>
</section>

<!-- ── PRICING ── -->
<section class="sec" id="pricing" aria-labelledby="pricingTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="pricingTitle">What it costs</h2>
      <p class="sec-sub">Published prices, because we ask the same of the firms we work with.</p>
    </div>
    <div class="price-grid rv">
      <div class="plan is-main">
        <div class="plan-top">
          <h3 class="plan-name">Fix sprint</h3>
          <span><span class="p-price">$997</span><span class="p-unit">one time</span></span>
        </div>
        <p>The full job: measure, fix, measure again. About six weeks from the first call to the second report.</p>
        <ul>
          <li>''' + ic('check-circle') + r'''Ten client questions agreed with you</li>
          <li>''' + ic('check-circle') + r'''A baseline of 150 answers across three assistants</li>
          <li>''' + ic('check-circle') + r'''14 days of fixes to your website, Google Business Profile and listings</li>
          <li>''' + ic('check-circle') + r'''Up to six new answers and two rewritten pages, sent to you for approval</li>
          <li>''' + ic('check-circle') + r'''A second measurement 30 days later</li>
          <li>''' + ic('check-circle') + r'''A one-page report each time, plus every answer in a spreadsheet</li>
        </ul>
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="pricing">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
      </div>
      <div class="plan-side">
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Free check</h3>
            <span><span class="p-price">$0</span></span>
          </div>
          <p>Five client questions on three assistants, asked once each. One page that shows where you were named and who was named instead. A snapshot, not a measurement.</p>
          <a href="#check" class="btn-ghost">Request the check</a>
        </div>
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Monthly tracking</h3>
            <span><span class="p-price">$297</span><span class="p-unit">a month</span></span>
          </div>
          <p>The same 150-answer run every month, a one-page report and up to two hours of follow-up fixes. Starts after a sprint.</p>
        </div>
      </div>
    </div>
    <p class="price-note">Prices are in US dollars. The cost of running the questions is included. There is no setup fee and no minimum term on tracking.</p>
  </div>
</section>

<!-- ── BREAK-EVEN ── -->
<section class="sec" id="worth" aria-labelledby="worthTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="worthTitle">How many new clients would cover it?</h2>
        <div class="prose rv">
          <p>We do not forecast how many clients a change in AI visibility brings. Nobody can yet: even Google&rsquo;s own report shows how often a page appeared in an AI answer, not whether anyone called.</p>
          <p>What you can work out is the other side of the sum. Move the slider to what one new client is worth to you, and see how many it takes to pay for the sprint.</p>
        </div>
      </div>
      <div class="calc rv">
        <div class="calc-row">
          <label for="feeRange"><span>Average fee from one new client</span><output id="feeOut" for="feeRange">$2,000</output></label>
          <input type="range" id="feeRange" min="300" max="10000" step="100" value="2000">
        </div>
        <div class="calc-out" aria-live="polite">
          <span class="calc-big" id="calcBig">1 client</span>
          <p id="calcText">One new client at that fee covers the sprint twice over.</p>
        </div>
        <p class="calc-fine">Sprint fee $997. This is arithmetic, not a forecast.</p>
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
        <p>For solicitors in England and Wales, part of this work overlaps with rules you already follow. The <a class="txt-link" href="https://www.sra.org.uk/solicitors/standards-regulations/transparency-rules/" target="_blank" rel="noopener noreferrer">SRA Transparency Rules</a> require price and service information for certain services, your complaints procedure, your SRA number and the SRA digital badge on your website. Those are the same pages an assistant reads when someone asks what a conveyancing solicitor costs.</p>
        <p>During the sprint we flag anything on those pages that looks missing or out of date. We write in plain English, we make no claim a regulator would call misleading, and nothing is published until someone at the firm has approved it.</p>
        <p>The same care applies to dental practices and to mortgage and financial advisers, who have their own advertising rules. We are not a law firm and this is not compliance advice. The decision stays with your compliance officer.</p>
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

<!-- ── FREE CHECK FORM ── -->
<section class="sec" id="check" aria-labelledby="checkTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="checkTitle">Get the free 15-answer check</h2>
        <p class="sec-sub">Tell us the firm, the town and the service you most want to be found for. We send one page back within three working days.</p>
        <ul class="check-list">
          <li>''' + ic('check-circle') + r'''Five questions your clients would ask, on ChatGPT, Gemini and Perplexity</li>
          <li>''' + ic('check-circle') + r'''Where your firm was named and which firms were named instead</li>
          <li>''' + ic('check-circle') + r'''No call needed and no access to anything of yours</li>
        </ul>
      </div>
      <div class="lead rv">
        <form id="checkForm">
          <div class="lead-grid">
            <div class="field"><label for="cfName">Your name</label><input id="cfName" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="cfEmail">Work email</label><input id="cfEmail" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="cfFirm">Firm or practice</label><input id="cfFirm" name="firm" type="text" autocomplete="organization" required></div>
            <div class="field"><label for="cfSite">Website</label><input id="cfSite" name="website" type="text" inputmode="url" placeholder="yourfirm.co.uk" required></div>
            <div class="field"><label for="cfTown">Town or city</label><input id="cfTown" name="town" type="text" placeholder="Leeds" required></div>
            <div class="field"><label for="cfArea">Main service</label><input id="cfArea" name="area" type="text" placeholder="Family law" required></div>
          </div>
          <div class="hp" aria-hidden="true"><label for="cfUrl2">Leave this empty</label><input id="cfUrl2" name="url2" type="text" tabindex="-1" autocomplete="off"></div>
          <button type="submit" class="btn-primary">Send me the check</button>
          <p class="lead-err" id="checkErr" role="alert">That did not go through. Email the same details to <a href="#" class="js-mail" data-subject="Free AI visibility check" rel="nofollow">ferit1@coremagna.com</a> and we will pick it up from there.</p>
          <p class="lead-fine">We use these details only to run the check and send it to you. <a href="/privacy">Privacy policy</a>.</p>
        </form>
        <div class="lead-ok" id="checkOk" tabindex="-1" hidden>
          <h3>Request received</h3>
          <p>Your one-page check will be in your inbox within three working days.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── RELATED ── -->
<section class="sec" id="next" aria-labelledby="nextTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="nextTitle">Where firms go next</h2>
    </div>
    <div class="related rv">
      <a class="rel-card" href="/expert-content">
        <span class="rel-kicker">Expert Content</span>
        <h3>Answer the questions the check found</h3>
        <p>The check shows which client questions your website does not answer. One recorded hour with a partner each month becomes the pages and short videos that answer them.</p>
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
        <p class="sec-sub">Every figure on this page, with where it came from. Checked on {{TODAY_LONG}}.</p>
      </div>
      <ol class="sources">
        <li><a href="https://www.brightlocal.com/research/local-consumer-review-survey/" target="_blank" rel="noopener noreferrer">BrightLocal, Local Consumer Review Survey 2026</a>. Use of generative AI for local business recommendations rose from 6% to 45%. 1,002 US adults, published February 2026.</li>
        <li><a href="https://www.ilawyermarketing.com/what-online-sources-do-people-use-to-research-and-find-attorneys-in-2026/" target="_blank" rel="noopener noreferrer">iLawyerMarketing, online sources people use to research attorneys in 2026</a>. Google 71.9%, ChatGPT 41.9% (28.1% in 2025). 1,110 US adults.</li>
        <li><a href="https://www.ofcom.org.uk/media-use-and-attitudes/media-habits-adults/passive-social-media-use-ai-companionship-and-online-side-hustles-uk-adults-media-and-online-lives-revealed" target="_blank" rel="noopener noreferrer">Ofcom, Adults&rsquo; Media Use and Attitudes 2026</a>. 54% of UK adults use AI tools. Published April 2026.</li>
        <li><a href="https://www.brightlocal.com/research/local-ai-visibility-study/" target="_blank" rel="noopener noreferrer">BrightLocal, local AI visibility study</a>. About 200,000 searches and 1.9 million citations across ChatGPT, Google AI Mode and AI Overviews. Published 16 September 2026.</li>
        <li><a href="https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/" target="_blank" rel="noopener noreferrer">SparkToro and Gumshoe, AI recommendation consistency</a>. 600 volunteers, 12 prompts, 2,961 runs. Published 28 January 2026. Not peer reviewed, and Gumshoe sells AI tracking.</li>
        <li><a href="https://developers.google.com/search/docs/fundamentals/ai-optimization-guide" target="_blank" rel="noopener noreferrer">Google Search Central, AI optimization guide</a>. Last updated 10 July 2026.</li>
        <li><a href="https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports" target="_blank" rel="noopener noreferrer">Google Search Central, generative AI performance reports in Search Console</a>. Announced 3 June 2026, available to all sites from 31 August 2026.</li>
        <li><a href="https://www.sra.org.uk/solicitors/standards-regulations/transparency-rules/" target="_blank" rel="noopener noreferrer">Solicitors Regulation Authority, Transparency Rules</a>.</li>
      </ol>
    </div>
  </div>
</section>

<!-- ── FINAL CTA ── -->
<section id="final-cta" aria-labelledby="ctaTitle">
  <div class="container">
    <div class="cta-wrap">
      <h2 id="ctaTitle">See what AI says about your firm</h2>
      <p>Book a call and we will run two of your questions live, or ask for the free check and get one page by email.</p>
      <div class="cta-actions">
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="final">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
        <a href="#check" class="btn-ghost">Get the free check</a>
      </div>
    </div>
  </div>
</section>
'''

JS = r'''
/* Break-even: how many new clients pay for the sprint */
(function(){
  const range=document.getElementById('feeRange');
  if(!range) return;
  const out=document.getElementById('feeOut'),big=document.getElementById('calcBig'),text=document.getElementById('calcText');
  const FEE=997;
  const money=n=>'$'+n.toLocaleString('en-US');
  function update(){
    const v=Number(range.value);
    const need=Math.ceil(FEE/v);
    out.textContent=money(v);
    big.textContent=need+(need===1?' client':' clients');
    const times=v/FEE;
    text.textContent=need===1
      ?(times>=1.5?'One new client at that fee covers the sprint '+(Math.round(times*10)/10)+' times over.':'One new client at that fee covers the sprint.')
      :'It takes '+need+' new clients at that fee to cover the sprint.';
  }
  range.addEventListener('input',update);
  update();
})();

/* Free check form. Same webhook and field names as the contact form on the home page. */
(function(){
  const form=document.getElementById('checkForm');
  if(!form) return;
  const WEBHOOK='https://melis.app.n8n.cloud/webhook/contact-form1';
  const btn=form.querySelector('button[type="submit"]');
  const ok=document.getElementById('checkOk');
  const err=document.getElementById('checkErr');
  const val=n=>form.elements[n].value.trim();
  form.addEventListener('submit',async e=>{
    e.preventDefault();
    err.classList.remove('is-on');
    const done=()=>{form.hidden=true;ok.hidden=false;ok.focus();};
    /* A filled hidden field means a bot: show success and send nothing */
    if(val('url2')){done();return;}
    const data={
      name:val('name'),email:val('email'),company:val('firm'),phone:'',
      service:'ai-visibility-check',budget:'',timeline:'',
      message:'Free AI visibility check. Website: '+val('website')+' | Town or city: '+val('town')+' | Main service: '+val('area'),
      source:'coremagna.com/ai-visibility',submitted_at:new Date().toISOString()
    };
    const label=btn.textContent;
    btn.disabled=true;btn.textContent='Sending';
    try{
      const res=await fetch(WEBHOOK,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      if(!res.ok) throw new Error('HTTP '+res.status);
      done();
      track('check_request',{page:PAGE});
    }catch(x){
      err.classList.add('is-on');
      btn.disabled=false;btn.textContent=label;
    }
  });
})();
'''

SERVICE = {
    'name': 'AI visibility audit and fix sprint',
    'serviceType': 'AI search visibility audit',
    'description': ('Coremagna asks ChatGPT, Gemini and Perplexity the questions a local firm\'s clients ask, counts how often '
                    'the firm is named across repeated runs, then fixes the website, Google Business Profile and listings '
                    'those answers draw on and measures again.'),
    'audience': {'@type': 'BusinessAudience', 'name': 'Law firms, dental practices, estate agents and other local professional firms'},
    'offers': [
        offer('Free check', 0, 'Five client questions on three AI assistants, one run each, reported on one page.'),
        offer('Fix sprint', 997, 'Baseline of 150 answers, 14 days of fixes, and a second measurement 30 days later.'),
        offer('Monthly tracking', 297, 'The same 150-answer run every month with a one-page report and follow-up fixes.', 'month'),
    ],
}
VIDEO = {
    'name': 'How an AI visibility check works',
    'description': ('A client asks an AI assistant for a family law solicitor. Three firms are named and one is left out. '
                    'The video shows why a single answer proves little, how repeated runs are counted, and what a 14-day fix sprint changes.'),
    'thumbnailUrl': SITE + '/videos/services/ai-visibility-poster.jpg',
    'contentUrl': SITE + '/videos/services/ai-visibility.mp4',
    'duration': 'PT38S',
}

PAGE = {
    'n': 1,
    'slug': SLUG,
    'title': TITLE,
    'desc': DESC,
    'og_title': 'Find out whether AI recommends your firm',
    'og_desc': 'We ask ChatGPT, Gemini and Perplexity the questions your clients ask, count how often you are named, and fix what decides it.',
    'og_alt': 'Find out whether AI recommends your firm. Coremagna AI Visibility.',
    'css': CSS,
    'body': BODY,
    'js': JS,
    'icons': ['arrow-right', 'check-circle', 'x-circle', 'check', 'prohibit', 'calendar-check', 'lock-simple',
              'arrows-clockwise', 'key'],
    'mail_subject': 'AI visibility',
    'jsonld': graph(SLUG, 'AI Visibility', TITLE, DESC, SERVICE, VIDEO, 'AI Visibility'),
}
