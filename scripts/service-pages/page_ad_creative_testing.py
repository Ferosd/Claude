from parts import ic, graph, offer, faq_html, table, SITE

SLUG = 'ad-creative-testing'
TITLE = 'Ad Creative Testing for E-commerce Brands | Coremagna'
DESC = ('A monthly batch of new video ad concepts made from your product photos, set up as a clean test in your '
        'Meta account, with a one-page readout of what won.')

CSS = r'''
/* ── Ad Creative Testing: hero readout mock ── */
.ro{padding:6px 20px 18px}
.ro-head,.ro-row{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1.25fr) 64px;gap:14px;align-items:center}
.ro-head{padding:12px 0;font-size:12px;color:var(--text-muted);border-bottom:1px solid var(--border)}
.ro-head span:last-child,.ro-cost{text-align:right}
.ro-row{padding:14px 0;border-bottom:1px solid var(--border)}
.ro-row strong{display:block;font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:18px;line-height:1.2;letter-spacing:-0.01em}
.ro-verdict{display:block;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text-muted)}
.ro-hook{display:grid;grid-template-columns:minmax(0,1fr) 38px;gap:10px;align-items:center}
.ro-hook b,.ro-cost{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:14px;color:var(--text)}
.ro-hook b{text-align:right}
.ro-row.is-win{margin:0 -12px;padding:14px 12px;border-radius:10px;background:var(--accent-dim);border-bottom-color:transparent}
.ro-row.is-win .bar i{background:var(--accent)}
.ro-row.is-win .ro-verdict{color:var(--accent)}
.ro-row.is-out strong,.ro-row.is-out b{color:var(--text-muted)}
.ro-row.is-out .ro-verdict{color:var(--red)}
.ro-note{padding-top:14px;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.5;color:var(--text-muted)}
/* The rows arrive one by one on load. CSS only, so it never depends on a script. */
@keyframes roIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.ro-row,.ro-note{animation:roIn 0.7s var(--ease) both}
.ro-row:nth-of-type(2){animation-delay:0.35s}
.ro-row:nth-of-type(3){animation-delay:0.6s}
.ro-row:nth-of-type(4){animation-delay:0.85s}
.ro-row:nth-of-type(5){animation-delay:1.1s}
.ro-note{animation-delay:1.5s}

/* ── One month's batch ── */
.cg{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;margin-top:16px}
.cg-col{background:var(--surface-2);border:1px solid var(--border);border-radius:12px;padding:16px 16px 8px}
.cg-name{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:8px;font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:16px;letter-spacing:-0.01em;color:var(--text)}
.cg-name span{font-family:'JetBrains Mono',monospace;font-weight:400;font-size:11px;color:var(--accent);white-space:nowrap}
.cg-col li{padding:9px 0;border-top:1px solid var(--border);font-size:14px;line-height:1.4;color:var(--text-secondary)}

/* ── Readout terms ── */
.defs{border-top:1px solid var(--border)}
.defs > div{display:grid;grid-template-columns:minmax(0,190px) minmax(0,1fr);gap:6px 24px;padding:20px 0;border-bottom:1px solid var(--border)}
.defs dt{font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:18px;line-height:1.2;letter-spacing:-0.01em;color:var(--text)}
.defs dd{font-size:15px;line-height:1.65;color:var(--text-muted);max-width:58ch}
.defs dd b{display:block;margin-bottom:4px;font-family:'JetBrains Mono',monospace;font-weight:500;font-size:13px;color:var(--text-secondary)}

/* ── Portfolio stills ── */
.wall{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;padding-bottom:28px}
.wall-tile{display:block;transition:transform 0.3s var(--ease)}
.wall-tile:nth-child(even){transform:translateY(28px)}
.wall-tile:hover{transform:translateY(-4px)}
.wall-tile:nth-child(even):hover{transform:translateY(24px)}
.wall-tile:focus-visible{outline:2px solid var(--accent);outline-offset:4px;border-radius:14px}
.wall-img{display:block;aspect-ratio:9/16;border-radius:14px;overflow:hidden;border:1px solid var(--border);background:var(--media-bg)}
.wall-img img{width:100%;height:100%;object-fit:cover}
.wall-cap{display:block;margin-top:10px;font-size:13px;line-height:1.4;color:var(--text-muted)}
.wall-cap b{display:block;font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:15px;letter-spacing:-0.01em;color:var(--text)}
.wall-more{margin-top:var(--space-lg)}

.quote-wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:72px;align-items:start;margin-top:var(--space-xl)}

@media(max-width:1024px){
  .quote-wrap{grid-template-columns:minmax(0,1fr);gap:var(--space-lg)}
}
@media(max-width:768px){
  .wall{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;padding-bottom:20px}
  .wall-tile:nth-child(even){transform:translateY(20px)}
  .wall-tile:hover{transform:none}
  .wall-tile:nth-child(even):hover{transform:translateY(20px)}
  .defs > div{grid-template-columns:minmax(0,1fr)}
  .ro{padding:6px 16px 16px}
  .ro-head,.ro-row{grid-template-columns:minmax(0,1.1fr) minmax(0,1fr) 48px;gap:10px}
  .ro-row strong{font-size:16px}
}
@media(max-width:480px){
  .cg{grid-template-columns:minmax(0,1fr)}
}
@media(prefers-reduced-motion:reduce){
  .ro-row,.ro-note{animation:none}
  .wall-tile,.wall-tile:hover{transition:none}
}
'''

FAQ = [
    ('Can you promise a lower cost per purchase?',
     'No. A test can show that none of the new concepts beats what you already run, and sometimes it does. What we promise is four ideas that are different from each other, a test set up so the result can be read, and a readout that says plainly what won and what did not.'),
    ('How much ad spend do we need?',
     'For a pilot we suggest about $100 a day for the 14 days the test runs, paid by you to Meta. That is our working rule and not a Meta requirement. With less, the test still ranks concepts on hook rate and click rate, but cost per purchase will rest on too few purchases to trust, and the readout will say so.'),
    ('Do you manage our ad account?',
     'No. We set up the test, read it and tell you what to scale. Day-to-day buying stays with you or your media buyer. If an agency runs the account, we send them the files and a setup sheet and work from their numbers.'),
    ('Are the videos made with AI?',
     'Yes. We build them from your product photos and any footage you have, using AI video tools, and a person edits every one. You can see finished examples on the <a href="/product-videos">product videos</a> page. Where a real person is needed on camera, we say so and use footage from you or from a creator you choose.'),
    ('Which platforms do you cover?',
     'Meta first: Facebook and Instagram, in feed, Stories and Reels. The same files can be cut for TikTok and YouTube Shorts if you ask. The readout covers Meta.'),
    ('How is a concept different from a variation?',
     'A concept is a reason to buy: it solves this problem, it works this way, it beats that alternative. A variation is the same reason with a different opening line, caption or cut. Testing variations of one concept tells you which wording is best. Testing concepts tells you what your customers care about, which is the bigger question.'),
    ('What is a hook rate?',
     'The share of people who were shown the ad and watched at least three seconds of it: three-second video plays divided by impressions. It is the earliest sign of whether an opening works, and it needs far less budget to measure than cost per purchase.'),
    ('What happens if nothing wins?',
     'Then you have learned four things not to spend more on, which is worth knowing. The readout says so in plain words, and the next brief moves to different ground. We do not dress up a flat test as a win.'),
    ('Who owns the ads?',
     'You do. Every video, brief and readout is yours to keep and to keep running, whether or not you continue with us.'),
    ('What do you need to start a pilot?',
     'A link to the product, the photos and footage you have, a list of claims you can prove, and either partner access to the ad account or a media buyer who will launch the ads. A 30-minute call covers the rest.'),
]

BODY = r'''
<!-- ── HERO ── -->
<section id="hero" aria-labelledby="heroH1">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">Ad Creative Testing</span></li></ol>
    </nav>
    <div class="hero-grid">
      <div class="hero-text">
        <p class="hero-kicker">Ad Creative Testing</p>
        <h1 class="hero-h1" id="heroH1">New ad concepts every month and a read on which one wins</h1>
        <p class="hero-sub">We research the angles, produce a batch of short video ads from your product photos and footage, set up a clean test in your Meta ad account, and send a one-page readout two weeks later.</p>
        <div class="hero-actions">
          <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="hero">Book a call
            ''' + ic('arrow-right') + r'''
          </a>
          <a href="#how" class="btn-ghost">See how a month works</a>
        </div>
        <p class="hero-fine">It starts with a pilot of ten ads for $997. Ad spend stays on your own account.</p>
        <p class="byline">By <a href="/about">Ferit Patefe</a>, founder of Coremagna. Updated <time datetime="{{TODAY}}">{{TODAY_LONG}}</time>.</p>
      </div>

      <figure class="mock">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>Two-week readout</span>
          <span class="tag">Example data</span>
        </div>
        <div class="ro">
          <div class="ro-head"><span>Concept</span><span>Hook rate</span><span>Cost</span></div>
          <div class="ro-row is-win"><div><strong>Problem first</strong><span class="ro-verdict">Winner</span></div><div class="ro-hook"><span class="bar"><i style="--v:86"></i></span><b>31%</b></div><span class="ro-cost">$24</span></div>
          <div class="ro-row"><div><strong>Unboxing</strong><span class="ro-verdict">Try new hooks</span></div><div class="ro-hook"><span class="bar"><i style="--v:75"></i></span><b>27%</b></div><span class="ro-cost">$31</span></div>
          <div class="ro-row"><div><strong>How it works</strong><span class="ro-verdict">Try new hooks</span></div><div class="ro-hook"><span class="bar"><i style="--v:61"></i></span><b>22%</b></div><span class="ro-cost">$38</span></div>
          <div class="ro-row is-out"><div><strong>Comparison</strong><span class="ro-verdict">Dropped</span></div><div class="ro-hook"><span class="bar"><i style="--v:50"></i></span><b>18%</b></div><span class="ro-cost">$52</span></div>
          <p class="ro-note">Cost is cost per purchase. Next month keeps the winner and tests four new concepts against it.</p>
        </div>
        <figcaption class="sr-only">An example readout comparing four ad concepts on hook rate and cost per purchase. The numbers are invented to show the layout.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── DEFINITION ── -->
<section class="sec" id="what" aria-labelledby="whatTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="whatTitle">What is ad creative testing?</h2>
      </div>
      <div class="answer rv">
        <p><strong>Ad creative testing is running several different ads against the same audience and the same budget to see which idea sells, then putting the money behind the winner.</strong> The thing being tested is the concept, which is the reason a stranger should care. One ad opens on the problem. Another shows how the product works. A third compares it with the cheap alternative. Each concept gets a few different opening lines, called hooks, because the opening seconds decide whether anyone watches the rest.</p>
        <p>After a set period you compare the concepts on the same measures: how many people watched past three seconds, how many clicked, and what a purchase cost. The winner gets more budget. The losers are switched off, and what they taught you goes into the next batch.</p>
        <p>It is not the same as making more ads. Twenty versions of one idea with a new colour or caption tell you almost nothing. Four ideas that are really different tell you what your customers respond to.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── EXPLAINER VIDEO ── -->
<section class="sec" id="video" aria-labelledby="videoTitle">
  <div class="container">
    <div class="video-grid">
      <div>
        <h2 class="sec-h2" id="videoTitle">See the loop in 34 seconds</h2>
        <p class="sec-sub">A tired ad, four new concepts, and the readout two weeks later. No sound needed.</p>
        <ol class="video-points">
          <li><span class="mono">0:00</span><span>An ad that has run too long</span></li>
          <li><span class="mono">0:05</span><span>Why the idea is now the hard part</span></li>
          <li><span class="mono">0:10</span><span>Four concepts and three hooks for each</span></li>
          <li><span class="mono">0:17</span><span>The readout after two weeks</span></li>
        </ol>
      </div>
      <div class="rv">
        <div class="video-frame">
          <video controls playsinline preload="none" poster="/videos/services/ad-creative-testing-poster.jpg" data-video="ad-creative-testing" aria-label="34-second explainer of monthly ad creative testing">
            <source src="/videos/services/ad-creative-testing.mp4" type="video/mp4">
          </video>
        </div>
        <p class="video-cap">The product, the ads and every number in the video are examples, not results.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── DATA ── -->
<section class="sec" id="data" aria-labelledby="dataTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="dataTitle">Why does the creative matter more than the targeting?</h2>
      <p class="sec-sub">Because the platform now does most of the targeting for you, and anyone can make a video. Here is what has been measured or said on the record.</p>
    </div>
    <div class="stats rv">
      <div class="stat-row">
        <span class="stat-num">49%</span>
        <p>of the extra sales that advertising produced came from the quality of the creative. Targeting accounted for 11%.
          <span class="stat-src">Source: <a href="https://info.ncsolutions.com/hubfs/2023%20Five%20Keys%20to%20Advertising%20Effectiveness/NCS_Five_Keys_to_Advertising_Effectiveness_E-Book_08-23.pdf" target="_blank" rel="noopener noreferrer">NCSolutions, Five Keys to Advertising Effectiveness</a>, 2023 update, nearly 450 US consumer goods campaigns on TV and digital.</span></p>
      </div>
      <div class="stat-row">
        <span class="stat-num">15M</span>
        <p>ads were made with Meta&rsquo;s generative AI tools in a single month, by more than a million advertisers. That was in late 2024.
          <span class="stat-src">Source: <a href="https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/" target="_blank" rel="noopener noreferrer">Meta Engineering</a>, 2 December 2024.</span></p>
      </div>
    </div>
    <div class="quote-wrap rv">
      <blockquote class="quote">
        <p>&ldquo;Increased ad diversity can improve people&rsquo;s experience with ads and drive better advertiser outcomes.&rdquo;</p>
        <cite><a href="https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/" target="_blank" rel="noopener noreferrer">Meta Engineering</a>, on its Andromeda ad retrieval system, December 2024</cite>
      </blockquote>
      <div class="prose">
        <p>Meta&rsquo;s system now picks which ad to show each person from a far larger pool than it used to. That works in favour of an account with several different ideas in it, and against one that runs a single ad until it wears out.</p>
        <p>Making the video is no longer the hard part either. On 6 October 2026 Meta said that generating video from still images is now generally available inside Advantage+ creative. A competitor can turn a product photo into a video in the same afternoon you can. What they cannot copy as fast is knowing which idea works for your product.</p>
        <p><strong>Read these with care.</strong> The 49% comes from campaigns for groceries and household goods, measured by a company that sells ad measurement. It was not measured on Meta alone and it will not transfer exactly to your brand. Meta&rsquo;s statements are Meta&rsquo;s own. Meta has never published an official number for how many different ads an ad set should hold, so we do not quote one.</p>
        <p class="stat-src">Source for the October announcement: <a href="https://www.socialmediatoday.com/news/meta-introduces-new-ai-powered-tools-at-ad-week-2026/832288/" target="_blank" rel="noopener noreferrer">Social Media Today</a>, 6 October 2026.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── WHAT A BATCH LOOKS LIKE ── -->
<section class="sec" id="batch" aria-labelledby="batchTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="batchTitle">What a batch looks like</h2>
        <div class="prose rv">
          <p>Every batch starts from four concepts. Each one is a different reason to buy, written as one sentence you can argue with before any video is made.</p>
          <p>Each concept then gets three hooks, which are three different ways to open the same idea. That gives twelve video ads. If one concept wins, the hooks tell you which opening carried it.</p>
          <p>From the second month the batch also holds four new variations of the previous winner, so the ad that is working gets fresh versions before it wears out.</p>
        </div>
      </div>
      <figure class="mock rv">
        <div class="mock-head">
          <span class="mock-title"><i class="mock-dot"></i>One month&rsquo;s batch</span>
          <span class="tag">Example</span>
        </div>
        <div class="mock-body">
          <p class="mock-meta"><span>Insulated bottle</span><span>4 concepts</span><span>12 video ads</span></p>
          <div class="cg">
            <div class="cg-col"><p class="cg-name">Problem first<span>3 hooks</span></p><ul><li>Warm water by 10am?</li><li>Your bottle is lying to you</li><li>Three hours and it gave up</li></ul></div>
            <div class="cg-col"><p class="cg-name">How it works<span>3 hooks</span></p><ul><li>Two walls with no air between</li><li>Why the ice lasts 24 hours</li><li>Cut one in half and look</li></ul></div>
            <div class="cg-col"><p class="cg-name">Unboxing<span>3 hooks</span></p><ul><li>What is in the box</li><li>First fill, first sip</li><li>It arrived like this</li></ul></div>
            <div class="cg-col"><p class="cg-name">Comparison<span>3 hooks</span></p><ul><li>Ours against a $9 bottle</li><li>Same ice, six hours later</li><li>Which one would you carry?</li></ul></div>
          </div>
        </div>
        <figcaption class="sr-only">An example batch for an insulated bottle: four concepts, each with three opening lines. The product and the lines are invented.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ── COMPARISON ── -->
<section class="sec" id="compare" aria-labelledby="compareTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="compareTitle">How is this different from an AI video tool or a creator?</h2>
      <p class="sec-sub">Both are good at producing videos. Neither decides what to test or reads the result, and that is where most of the value sits.</p>
    </div>
''' + table(
    'A general comparison. Tools and creators differ, so check the one you are considering.',
    ['<span class="sr-only">Compared on</span>', 'AI video tool', 'Freelance creators', 'Coremagna creative testing'],
    [
        ['What you get', 'As many videos as you care to generate, within minutes.',
         'A handful of videos from real people, usually within a few weeks.',
         'A planned batch every month: four concepts with three hooks each, cut for feed, Stories and Reels.'],
        ['Who picks the concepts', 'You do.', 'You do, or the creator improvises.',
         'We do, from your reviews, your past results and the ads your competitors run. You approve them.'],
        ['Who sets up the test', 'You do.', 'You do.',
         'We do, in your ad account, or we hand a setup sheet to your media buyer.'],
        ['Who reads the result', 'You do.', 'You do.',
         'We send one page that says what to scale, what to switch off and what to test next.'],
        ['People on camera', 'Avatars or generated presenters.', 'Real people.',
         'Product shots and demos by default. Real people only from your own footage or a creator you choose.'],
        ['Your part', 'Planning, prompting, editing, launching and analysing.',
         'Briefing, chasing, editing, launching and analysing.',
         'Approve the concepts, then read one page.'],
    ], us=3) + r'''
  </div>
</section>

<!-- ── HOW IT WORKS ── -->
<section class="sec" id="how" aria-labelledby="howTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="howTitle">How a month works</h2>
        <p class="sec-sub">Five steps. The pilot runs the same way with a smaller batch.</p>
      </div>
      <ol class="steps rv">
        <li class="step">
          <span class="step-n" aria-hidden="true">01</span>
          <h3>Research</h3>
          <p>We read your reviews, your last three months of ad results and the ads your competitors are running in the Meta Ad Library. The output is four concepts, each with one sentence on why it might work.</p>
          <span class="step-meta">Days 1 to 3</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">02</span>
          <h3>Sign-off</h3>
          <p>You see the concepts, the hooks and every product claim before anything is produced. Anything you cannot stand behind comes out.</p>
          <span class="step-meta">Day 4</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">03</span>
          <h3>Produce</h3>
          <p>Twelve short video ads from your product photos and footage, plus four new variations of last month&rsquo;s winner. Each one is cut for feed, Stories and Reels.</p>
          <span class="step-meta">Days 5 to 10</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">04</span>
          <h3>Launch</h3>
          <p>We set the test up in your ad account, or hand the files and a setup sheet to your media buyer. Every concept gets the same audience and the same budget, so the difference you see comes from the creative.</p>
          <span class="step-meta">Day 11</span>
        </li>
        <li class="step">
          <span class="step-n" aria-hidden="true">05</span>
          <h3>Read</h3>
          <p>After 14 days you get one page: hook rate, click rate and cost per purchase for each concept, what to scale, what to switch off, and the brief for next month.</p>
          <span class="step-meta">Day 25</span>
        </li>
      </ol>
    </div>
  </div>
</section>

<!-- ── READOUT TERMS ── -->
<section class="sec" id="readout" aria-labelledby="readoutTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="readoutTitle">What the readout tells you</h2>
        <p class="sec-sub">Four numbers for each concept and one decision. Every number comes from your own Ads Manager, so you can check it.</p>
      </div>
      <dl class="defs rv">
        <div><dt>Hook rate</dt><dd><b>3-second video plays &divide; impressions</b>Whether the opening stops the scroll. It is the first number to settle, and it needs the least budget.</dd></div>
        <div><dt>Hold rate</dt><dd><b>ThruPlays &divide; 3-second video plays</b>Whether people who stopped kept watching. Meta counts a ThruPlay when a video plays to the end or for at least 15 seconds.</dd></div>
        <div><dt>Click rate</dt><dd><b>Link clicks &divide; impressions</b>Whether the ad made people want to see the product page.</dd></div>
        <div><dt>Cost per purchase</dt><dd><b>Spend &divide; purchases Meta attributes to the ad</b>The number that pays the bills, and the noisiest one. The readout shows how many purchases it rests on, so a result built on six sales is not read like one built on sixty.</dd></div>
        <div><dt>Verdict</dt><dd><b>Scale, try new hooks or drop</b>One line for each concept, and a brief for the next batch that follows from it.</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- ── PORTFOLIO ── -->
<section class="sec" id="footage" aria-labelledby="footageTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="footageTitle">What the videos look like</h2>
      <p class="sec-sub">Stills from finished product videos in our portfolio, made from product photos with AI video tools and edited by hand. They show the production quality. They are not test results.</p>
    </div>
    <div class="wall rv">
      <a class="wall-tile" href="/product-videos">
        <span class="wall-img"><img src="/videos/products/fig-gelato-launch-poster.webp" alt="Still from a launch ad for a roasted fig gelato" loading="lazy" decoding="async" width="540" height="960"></span>
        <span class="wall-cap"><b>Fig gelato launch</b>Launch ad</span>
      </a>
      <a class="wall-tile" href="/product-videos">
        <span class="wall-img"><img src="/videos/products/smoked-chilli-oil-poster.webp" alt="Still from an ingredient story for a smoked chilli oil" loading="lazy" decoding="async" width="540" height="960"></span>
        <span class="wall-cap"><b>Smoked chilli oil</b>Ingredient story</span>
      </a>
      <a class="wall-tile" href="/product-videos">
        <span class="wall-img"><img src="/videos/products/watch-exploded-view-poster.webp" alt="Still from an exploded view of a watch with spec callouts" loading="lazy" decoding="async" width="540" height="960"></span>
        <span class="wall-cap"><b>Watch exploded view</b>How it works</span>
      </a>
      <a class="wall-tile" href="/product-videos">
        <span class="wall-img"><img src="/videos/products/leash-spiral-poster.webp" alt="Still from a product video of a patterned dog leash" loading="lazy" decoding="async" width="540" height="960"></span>
        <span class="wall-cap"><b>Leash spiral</b>Product shot</span>
      </a>
    </div>
    <p class="wall-more"><a class="txt-link" href="/product-videos">Watch these and the rest of the portfolio</a></p>
  </div>
</section>

<!-- ── ACCESS ── -->
<section class="sec" id="access" aria-labelledby="accessTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="accessTitle">What we need from you</h2>
      <p class="sec-sub">Enough to make the ads and read the numbers. Nothing that lets us spend your money or see your customers.</p>
    </div>
    <div class="access rv">
      <div class="access-card">
        <h3>For a test</h3>
        <ul>
          <li>''' + ic('check-circle') + r'''<div>Partner access to your Meta ad account <span>at advertiser level, or none at all if your media buyer launches the ads</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>Product photos, any footage you have, your logo and brand colours</div></li>
          <li>''' + ic('check-circle') + r'''<div>Ad results for the last three months <span>read access or an export</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>The claims you can prove <span>ingredients, test results, guarantees, review counts</span></div></li>
          <li>''' + ic('check-circle') + r'''<div>One person who approves concepts and claims</div></li>
        </ul>
      </div>
      <div class="access-card is-never">
        <h3>We never ask for</h3>
        <ul>
          <li>''' + ic('x-circle') + r'''<div>Admin control of your Meta business account</div></li>
          <li>''' + ic('x-circle') + r'''<div>Your card or billing details <span>ad spend stays on your account</span></div></li>
          <li>''' + ic('x-circle') + r'''<div>Customer lists or any personal data</div></li>
          <li>''' + ic('x-circle') + r'''<div>The admin login for your store</div></li>
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
      <p class="sec-sub">Nobody can promise that an ad will sell. We promise different ideas, a fair test and an honest reading of it.</p>
    </div>
    <div class="guards rv">
      <div class="guard">''' + ic('prohibit') + r'''<h3>No return promises</h3><p>We will not quote a return on ad spend before the test has run. The readout shows what happened, including the concepts that lost.</p></div>
      <div class="guard">''' + ic('user-circle') + r'''<h3>No invented customers</h3><p>No AI presenter poses as a buyer, and no review or before and after is made up. Claims come from you, with proof.</p></div>
      <div class="guard">''' + ic('check-circle') + r'''<h3>You approve every ad</h3><p>Concepts, scripts and claims are signed off before production, and the finished ads before launch.</p></div>
      <div class="guard">''' + ic('lock-simple') + r'''<h3>Your account stays yours</h3><p>We work as a partner on your ad account. Billing, pixels and customer data stay with you.</p></div>
      <div class="guard">''' + ic('arrows-clockwise') + r'''<h3>No lock-in</h3><p>The pilot is a one-time fee. The monthly plan runs month to month and stops with 30 days&rsquo; notice.</p></div>
      <div class="guard">''' + ic('key') + r'''<h3>Every file is yours</h3><p>The videos, the briefs and the readouts belong to you and can keep running if we stop working together.</p></div>
    </div>
  </div>
</section>

<!-- ── PRICING ── -->
<section class="sec" id="pricing" aria-labelledby="pricingTitle">
  <div class="container">
    <div class="sec-head">
      <h2 class="sec-h2" id="pricingTitle">What it costs</h2>
      <p class="sec-sub">Two prices. Ad spend is separate and goes straight from you to Meta.</p>
    </div>
    <div class="price-grid rv">
      <div class="plan is-main">
        <div class="plan-top">
          <h3 class="plan-name">Monthly testing</h3>
          <span><span class="p-price">$1,997</span><span class="p-unit">a month</span></span>
        </div>
        <p>A new batch every month and a readout on the last one.</p>
        <ul>
          <li>''' + ic('check-circle') + r'''Four new concepts, researched and briefed</li>
          <li>''' + ic('check-circle') + r'''12 new video ads: four concepts with three hooks each</li>
          <li>''' + ic('check-circle') + r'''Four new variations of last month&rsquo;s winner</li>
          <li>''' + ic('check-circle') + r'''Every ad cut for feed, Stories and Reels</li>
          <li>''' + ic('check-circle') + r'''The test set up in your ad account, or handed to your media buyer</li>
          <li>''' + ic('check-circle') + r'''A one-page readout and the next brief</li>
        </ul>
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="pricing">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
      </div>
      <div class="plan-side">
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Pilot</h3>
            <span><span class="p-price">$997</span><span class="p-unit">one time</span></span>
          </div>
          <p>Ten ads delivered within 14 days: five concepts with two hooks each. We set up the test and send a readout once it has run for two weeks. The quickest way to see whether this suits your account.</p>
          <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-ghost" data-loc="pricing-pilot">Start with the pilot</a>
        </div>
        <div class="plan">
          <div class="plan-top">
            <h3 class="plan-name">Ad spend</h3>
          </div>
          <p>Paid by you to Meta, never through us. For a test worth reading we suggest about $100 a day while it runs. With less, we rank concepts on hook rate and click rate and say so in the readout.</p>
        </div>
      </div>
    </div>
    <p class="price-note">Prices are in US dollars. The cost of generating the videos is included. There is no setup fee and no minimum term on the monthly plan.</p>
  </div>
</section>

<!-- ── BREAK-EVEN ── -->
<section class="sec" id="worth" aria-labelledby="worthTitle">
  <div class="container">
    <div class="split-wide">
      <div>
        <h2 class="sec-h2" id="worthTitle">How far would cost per purchase have to fall to cover it?</h2>
        <div class="prose rv">
          <p>We do not forecast results. What you can check is whether the sum makes sense for your account before you spend anything.</p>
          <p>If a winning concept lowers your cost per purchase, you get the same number of sales for less. The saving is your monthly ad spend multiplied by the size of the drop. Move the slider to what you spend on Meta each month.</p>
          <p>If the answer is a large number, this service is too early for you, and the page should say so.</p>
        </div>
      </div>
      <div class="calc rv">
        <div class="calc-row">
          <label for="spendRange"><span>Monthly ad spend on Meta</span><output id="spendOut" for="spendRange">$15,000</output></label>
          <input type="range" id="spendRange" min="2000" max="100000" step="1000" value="15000">
        </div>
        <div class="calc-out" aria-live="polite">
          <span class="calc-big" id="calcBig">13.3%</span>
          <p id="calcText">At that spend, a 13.3% lower cost per purchase covers the monthly fee.</p>
        </div>
        <p class="calc-fine">Monthly fee $1,997. This is arithmetic, not a forecast.</p>
      </div>
    </div>
  </div>
</section>

<!-- ── RULES ── -->
<section class="sec" id="rules" aria-labelledby="rulesTitle">
  <div class="container">
    <div class="split">
      <div class="split-head">
        <h2 class="sec-h2" id="rulesTitle">AI-made ads and the rules</h2>
      </div>
      <div class="prose rv">
        <p>An ad made with AI is still an ad, and the existing rules apply to it. In the United States the <a class="txt-link" href="https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials" target="_blank" rel="noopener noreferrer">FTC&rsquo;s rule on reviews and testimonials</a> has banned fake ones since October 2024, and it names reviews written by AI for people who do not exist.</p>
        <p>In the United Kingdom fake reviews have been banned outright since April 2025, and the <a class="txt-link" href="https://www.asa.org.uk/codes-and-rulings/advertising-codes/non-broadcast-code.html" target="_blank" rel="noopener noreferrer">advertising code</a> requires that an ad does not mislead. In the European Union the transparency rules of the <a class="txt-link" href="https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai" target="_blank" rel="noopener noreferrer">AI Act</a> began to apply in August 2026. They require realistic AI-generated video to be disclosed as such.</p>
        <p>In practice that means product shots and demonstrations are the default. If a presenter appears, they speak as the brand and never as a customer. We do not write reviews, invent results or fake a before and after. Where a platform or a law asks for an AI label, the ad carries one.</p>
        <p>We are not lawyers and this is not legal advice. The final call on any claim is yours.</p>
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
      <a class="rel-card" href="/product-videos">
        <span class="rel-kicker">Product Videos</span>
        <h3>Want the videos without the testing?</h3>
        <p>Single product videos made from your photos: launch ads, ingredient stories, exploded views and product shots. The portfolio has twelve finished examples.</p>
        <span class="rel-go">See the portfolio''' + ic('arrow-right') + r'''</span>
      </a>
      <a class="rel-card" href="/ai-visibility">
        <span class="rel-kicker">AI Visibility</span>
        <h3>Run a local firm instead?</h3>
        <p>Find out whether ChatGPT, Gemini and Perplexity name your firm, and fix what decides it.</p>
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
        <p class="sec-sub">Every figure and rule on this page, with where it came from. Checked on {{TODAY_LONG}}.</p>
      </div>
      <ol class="sources">
        <li><a href="https://info.ncsolutions.com/hubfs/2023%20Five%20Keys%20to%20Advertising%20Effectiveness/NCS_Five_Keys_to_Advertising_Effectiveness_E-Book_08-23.pdf" target="_blank" rel="noopener noreferrer">NCSolutions, Five Keys to Advertising Effectiveness, 2023 update</a>. Creative 49%, brand 21%, reach 14%, targeting 11% and recency 5% of incremental sales, from nearly 450 US consumer goods campaigns on TV and digital.</li>
        <li><a href="https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/" target="_blank" rel="noopener noreferrer">Meta Engineering, the Andromeda ads retrieval engine</a>. More than a million advertisers made more than 15 million ads with Meta&rsquo;s generative AI tools in a month. Published 2 December 2024.</li>
        <li><a href="https://www.socialmediatoday.com/news/meta-introduces-new-ai-powered-tools-at-ad-week-2026/832288/" target="_blank" rel="noopener noreferrer">Social Media Today, Meta&rsquo;s announcements at Advertising Week 2026</a>. Video generation from static assets in Advantage+ creative is generally available. Published 6 October 2026. This is press coverage and not Meta&rsquo;s own page.</li>
        <li><a href="https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials" target="_blank" rel="noopener noreferrer">US Federal Trade Commission, final rule banning fake reviews and testimonials</a>. Announced August 2024, in force from 21 October 2024.</li>
        <li><a href="https://www.gov.uk/government/publications/fake-reviews-cma208" target="_blank" rel="noopener noreferrer">UK Competition and Markets Authority, guidance on fake reviews</a>. The ban took effect in April 2025.</li>
        <li><a href="https://www.asa.org.uk/codes-and-rulings/advertising-codes/non-broadcast-code.html" target="_blank" rel="noopener noreferrer">UK Advertising Standards Authority, the CAP Code</a>.</li>
        <li><a href="https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai" target="_blank" rel="noopener noreferrer">European Commission, the AI Act</a>. Transparency rules apply from 2 August 2026.</li>
      </ol>
    </div>
  </div>
</section>

<!-- ── FINAL CTA ── -->
<section id="final-cta" aria-labelledby="ctaTitle">
  <div class="container">
    <div class="cta-wrap">
      <h2 id="ctaTitle">Start with ten ads and one honest readout</h2>
      <p>Bring a product link and your last three months of ad results to the call. We will tell you whether a pilot makes sense for your account, and say so if it does not.</p>
      <div class="cta-actions">
        <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="final">Book a call
          ''' + ic('arrow-right') + r'''
        </a>
        <a href="/product-videos" class="btn-ghost">See product videos</a>
      </div>
    </div>
  </div>
</section>
'''

JS = r'''
/* Break-even: the drop in cost per purchase that pays the monthly fee */
(function(){
  const range=document.getElementById('spendRange');
  if(!range) return;
  const out=document.getElementById('spendOut'),big=document.getElementById('calcBig'),text=document.getElementById('calcText');
  const FEE=1997;
  const money=n=>'$'+n.toLocaleString('en-US');
  function update(){
    const v=Number(range.value);
    const pct=FEE/v*100;
    const shown=(pct>=10?Math.round(pct*10)/10:Math.round(pct*100)/100)+'%';
    out.textContent=money(v);
    big.textContent=shown;
    text.textContent=pct>=40
      ?'At that spend the monthly plan is hard to justify. Run the pilot first, or wait until your spend is higher.'
      :'At that spend, a '+shown+' lower cost per purchase covers the monthly fee.';
  }
  range.addEventListener('input',update);
  update();
})();
'''

SERVICE = {
    'name': 'Ad creative testing',
    'serviceType': 'Paid social ad creative production and testing',
    'description': ('Coremagna researches ad concepts for an e-commerce brand, produces a monthly batch of short video ads '
                    'from the brand\'s product photos and footage, sets up a like-for-like test in the brand\'s Meta ad '
                    'account, and reports which concept won on hook rate, click rate and cost per purchase.'),
    'audience': {'@type': 'BusinessAudience', 'name': 'E-commerce and direct-to-consumer brands that advertise on Facebook and Instagram'},
    'offers': [
        offer('Pilot', 997, 'Ten video ads delivered within 14 days, a test set up in the ad account, and a readout after two weeks.'),
        offer('Monthly testing', 1997, 'Four new concepts, 12 new video ads, four variations of the previous winner, test setup and a one-page readout.', 'month'),
    ],
}
VIDEO = {
    'name': 'How monthly ad creative testing works',
    'description': ('An ad that has run too long loses its edge. The video shows four new concepts with three hooks each, '
                    'the two-week readout that ranks them, and the monthly loop of research, production, launch and reading.'),
    'thumbnailUrl': SITE + '/videos/services/ad-creative-testing-poster.jpg',
    'contentUrl': SITE + '/videos/services/ad-creative-testing.mp4',
    'duration': 'PT34S',
}

PAGE = {
    'n': 2,
    'slug': SLUG,
    'title': TITLE,
    'desc': DESC,
    'og_title': 'New ad concepts every month and a read on which one wins',
    'og_desc': 'A monthly batch of video ads from your product photos, tested in your Meta account, with a one-page readout of what won.',
    'og_alt': 'New ad concepts every month and a read on which one wins. Coremagna Ad Creative Testing.',
    'css': CSS,
    'body': BODY,
    'js': JS,
    'icons': ['arrow-right', 'check-circle', 'x-circle', 'prohibit', 'user-circle', 'lock-simple',
              'arrows-clockwise', 'key'],
    'mail_subject': 'Ad creative testing',
    'jsonld': graph(SLUG, 'Ad Creative Testing', TITLE, DESC, SERVICE, VIDEO, 'Ad Creative Testing'),
}
