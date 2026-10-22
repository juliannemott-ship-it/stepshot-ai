import html, json, os
D="Oct 16, 2026"
CSS="""*{box-sizing:border-box}body{margin:0;font:18px/1.6 system-ui,sans-serif;background:#f7f5f0;color:#2b2d42}
a{color:#3a6ea5}header,footer{background:#fff;padding:14px 20px;border-bottom:1px solid #e6e2d8}footer{border-top:1px solid #e6e2d8;font-size:15px;margin-top:40px}
nav a{margin-right:16px;font-weight:600;text-decoration:none}.logo{font-weight:800;font-size:22px;color:#2b2d42;text-decoration:none;margin-right:24px}
main{max-width:860px;margin:auto;padding:20px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}
.card{background:#fff;border-radius:16px;padding:18px;border:1px solid #e6e2d8}.tag{display:inline-block;padding:2px 10px;border-radius:99px;font-size:14px;font-weight:600}
.ready{background:#d8f3dc;color:#1b4332}.soon{background:#eee;color:#555}.hero{background:#e8f1fb;border-radius:20px;padding:28px;margin-bottom:24px}
.step{background:#fff;border-radius:18px;margin:22px 0;border:1px solid #e6e2d8;overflow:hidden}.sh{display:flex;gap:14px;align-items:center;padding:16px 18px;font-size:21px;font-weight:700}
.num{flex:none;width:46px;height:46px;border-radius:50%;color:#fff;display:grid;place-items:center;font-size:22px}
.mock{margin:0 18px;border:3px dashed #c9c2b3;border-radius:14px;padding:14px;background:#fbfaf7;position:relative}
.mock:before{content:"ILLUSTRATION — not a real screenshot";font-size:12px;letter-spacing:.05em;color:#8a8273;display:block;margin-bottom:8px}
.bar{height:14px;border-radius:7px;background:#e3ded3;margin:6px 0}.btn{display:inline-block;padding:10px 18px;border-radius:12px;color:#fff;font-weight:700;box-shadow:0 0 0 5px #ffd16680}
.input{border:2px solid #b9b2a3;border-radius:12px;padding:10px;background:#fff;color:#777}.hl{outline:5px solid #ffd166;outline-offset:3px}
.see{margin:14px 18px 18px;padding:12px 16px;border-radius:12px;background:#d8f3dc;color:#1b4332}.see b:before{content:"✔ "}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden}td,th{padding:10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top;font-size:16px}
.note{background:#fff4d6;border-radius:12px;padding:12px 16px;font-size:16px}input[type=email]{font-size:18px;padding:12px;border-radius:12px;border:2px solid #b9b2a3;width:100%;max-width:340px}
button{font-size:18px;padding:12px 20px;border-radius:12px;border:0;background:#3a6ea5;color:#fff;font-weight:700;margin-top:8px}
.c0{background:#3a6ea5}.c1{background:#2a9d8f}.c2{background:#e76f51}.c3{background:#8e6bbf}.c4{background:#d4a017}
.sheet{background:#fff;color:#111}.sheet h1{font-size:40px;line-height:1.15;margin:0 0 8px}
.sheet .sh{font-size:24px;line-height:1.3;padding:10px 0;border-bottom:2px solid #111}
.sheet .num{width:44px;height:44px;font-size:22px}
.sheet .grid{grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:16px}
.sheet .card{border:2px solid #111}.sheet .card h2{margin:0 0 6px;font-size:20px}
.sheet .note{background:#fff;color:#111;border:2px solid #111}
@page{size:letter;margin:0.5in}
@media print{
body.sheet{background:#fff;color:#000;font-size:14pt;line-height:1.25}
body.sheet header,body.sheet footer,body.sheet .noprint{display:none!important}
body.sheet main{max-width:none;margin:0;padding:0}
body.sheet h1{font-size:36pt;margin:0 0 8pt}
body.sheet .note{font-size:13pt;padding:7pt 9pt;margin:0 0 10pt}
body.sheet .sh{font-size:20pt;line-height:1.28;padding:6pt 0;gap:10pt;border-bottom:2px solid #000}
body.sheet .num{width:30pt;height:30pt;font-size:16pt}
body.sheet .grid{grid-template-columns:1fr 1fr;gap:12pt;margin-top:12pt}
body.sheet .card{padding:10pt 12pt}
body.sheet .card h2{font-size:16pt;margin:0 0 4pt}
body.sheet .card p{font-size:14.5pt;line-height:1.32;margin:4pt 0 0}
body.sheet a{color:#000;text-decoration:none}
*{print-color-adjust:exact;-webkit-print-color-adjust:exact}
}"""
def page(t,body,depth=0,body_class=""):
    p="../"*depth
    bc=f" class={body_class}" if body_class else ""
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{t} · StepShot AI</title><link rel=stylesheet href="{p}style.css"></head><body{bc}>
<header><a class=logo href="{p}index.html">📸 StepShot AI</a><nav><a href="{p}index.html">Guides</a><a href="{p}checker.html">Should I pay?</a><a href="{p}scores.html">Scoring</a><a href="{p}changes.html">What changed</a><a href="{p}disclosure.html">Disclosure</a></nav></header>
<main>{body}</main><footer>Some links on StepShot AI may become affiliate links; we'll label them. <a href="{p}disclosure.html">Affiliate disclosure</a>. Visuals are illustrations, not real screenshots. Product names belong to their owners; StepShot AI is not affiliated with them.</footer></body></html>"""
NS="Not yet scored — needs a timed hands-on test"
TOOLS={
"chatgpt":dict(src2="https://help.openai.com/en/articles/7232927",n="ChatGPT",src="https://chatgpt.com/pricing",free="Yes. OpenAI's pricing page: \"The free version of ChatGPT is available to everyone\"; paid plans Go, Plus, Pro (plus Business/Enterprise).",fs="Generous free tier",sub="OpenAI Help (help.openai.com/en/articles/7232927): web subscribers cancel via account menu > Settings > Billing > Cancel plan > Cancel; App Store / Google Play subscribers must cancel in that store. Uninstalling the app does NOT cancel. Cancel 24h+ before billing date.",ss="Medium risk: clear cancel steps, but three different billing places and \"uninstall doesn't cancel\" are easy traps"),
"claude":dict(n="Claude",src="https://claude.com/pricing",free="Yes. Anthropic's pricing page lists a Free plan at $0 (chat on web, desktop, mobile). Pro is $20/mo monthly or $17/mo billed annually ($200 up front).",fs="Generous free tier",sub="Official FAQ: cancel in Settings > Billing (web/desktop) or via App Store / Google Play if bought there; cancel 24h+ before renewal; plan drops to Free at period end. Annual billing charges a year up front.",ss="Medium risk: clear cancel path, but annual prepay and app-store purchases add places to forget"),
"gemini":dict(n="Gemini",src="https://gemini.google/subscriptions/",free="Yes. Google's subscriptions page (US) lists a Free plan including the Gemini app. Paid: Google AI Plus, Pro, Ultra (Ultra from $99.99/mo).",fs="Generous free tier",sub="Official page: \"Cancel anytime. No refunds for partial billing periods.\" Paid plans bundle storage and other Google One benefits.",ss="Medium-high risk: bundled benefits blur what the charge is for"),
"copilot":dict(n="Microsoft Copilot",src="https://www.microsoft.com/en-us/copilot/solutions/individuals",free="Yes, a free version exists: Microsoft's page describes paid plans as having \"higher usage than free\" and offers \"Try for free\". Microsoft 365 Personal (with Copilot) is $9.99/mo; Family $12.99/mo. Free-tier limits not verified.",fs="Free tier exists (limits not verified)",sub="Official page: \"Subscription automatically renews unless canceled in Microsoft account.\" A 1-month free trial is offered. Copilot is bundled with Office apps and 1 TB storage.",ss="High risk: free trial that auto-renews, inside a bundle"),
"perplexity":dict(src2="https://www.perplexity.ai/help-center/en/articles/10353002-billing-faq-for-pro-plan-subscribers",n="Perplexity",src="https://www.perplexity.ai/pro",free="Yes. Official page offers \"sign up for free\" and Pro is \"Everything in Free and…\". Pro is $17/mo billed annually; Max $167/mo billed annually. Monthly price not verified.",fs="Free tier exists (limits not verified)",sub="Perplexity Help: profile icon > Account > Subscription > Manage Plan (web). iOS: App Store > profile > Subscriptions > Perplexity > Cancel subscription. Refunds: up to 24h after purchase (monthly), 72h (annual) outside EU/UK.",ss="Medium risk: clear cancel path; short refund windows; app-store billing is separate"),
"canva":dict(src2="https://www.canva.com/help/cancel-canva-plan/",n="Canva AI",src="https://www.canva.com/pricing/",free="Yes. Canva Free is US$0 with \"Up to 20 Standard or Premium AI uses\". Pro US$144/year; Business US$250/year per person. Pro offers a free trial.",fs="Small AI allowance on free",sub="Canva Help: profile menu > Settings > Billing > Cancel plan > Continue cancellation > Cancel subscription. Plans auto-renew. App Store / Google Play / PayPal subscribers cancel there; uninstalling doesn't cancel. You can pause for 3 months instead.",ss="Medium risk: Pro starts with a free trial that auto-renews; clear cancel and pause options"),
"gamma":dict(src2="https://help.gamma.app/en/articles/8568920-how-do-i-manage-or-cancel-my-gamma-subscription",n="Gamma",src="https://gamma.app/pricing",free="Yes. Free plan $0, \"No credit card required\", 400 credits at signup, up to 10 slides per prompt. Plus $9/seat/mo, Pro $18, Ultra $90 (annual prices shown).",fs="Free start, one-time credits",sub="Gamma Help: Settings > Billing > Cancel subscription (bottom of page). Cancel at least 30 days before renewal to avoid the next charge. Free plan needs no card.",ss="Medium risk: no card to start, but the 30-day-before-renewal cancel rule is easy to miss"),
"notion":dict(n="Notion AI",src="https://www.notion.com/pricing",free="Free plan $0 includes only a \"Trial of Notion AI\". Full Notion Agent is listed on Business ($20/member/mo).",fs="AI is trial-only on free",sub="Official FAQ: subscriptions \"automatically renew until you cancel\"; cancel in Settings > Billing > Change plan (desktop). Refund if you downgrade within 3 days (monthly) or 30 days (annual).",ss="Medium risk: clear cancel path and refund window; per-member billing can grow"),
"elevenlabs":dict(n="ElevenLabs",src="https://elevenlabs.io/pricing",free="Yes. Free $0 with 10k credits/month. Starter $6/mo, Creator $22/mo, Pro $99/mo.",fs="Usable free tier",sub="Official FAQ: cancel any time; stays active to end of cycle, then drops to Free and unused paid credits expire. Cheap first-month promos shown, which then renew at full price.",ss="Medium risk: discounted first month, then full price"),
"otter":dict(src2="https://help.otter.ai/hc/en-us/articles/360048593573-Cancel-your-Otter-Pro-subscription",n="Otter",src="https://otter.ai/pricing",free="Yes. Basic is free with 300 monthly transcription minutes and 3 lifetime file imports. Pro $16.99/user/mo monthly.",fs="Usable free tier",sub="Otter Help: sign in as admin > Account Settings (Integrations) > Billing > Cancel Plan. Auto-renews; cancel 24h+ before billing date; non-refundable. App Store / Google Play subscriptions must be cancelled in the store.",ss="Medium risk: clear steps, but no refunds and separate app-store billing"),
}
OTHER=[]
G=lambda title,url,acts,sees,kinds,src,flags=None:(title,acts,sees,kinds,url,src,flags or [])
GUIDES={
"chatgpt":G("Ask ChatGPT your first question","chatgpt.com",["Open chatgpt.com in your browser.","Find the text box. (In supported countries you can try it without an account.)","Type one short question in the text box.","Send it.","Read the answer. Ask a follow-up in the same box."],["The ChatGPT home page with a text box.","A text box ready for typing. If you're asked to log in, accounts are required where you are.","Your question sitting in the box.","Your question moves up; an answer appears below it.","A second answer under your follow-up. Chats are saved only if you log in."],["url","box","typed","sent","answer"],[("OpenAI Help: The ChatGPT home page","https://help.openai.com/en/articles/9125172-the-chatgpt-home-page")],["The exact look of the send control isn't named in the help article; worded as \"Send it.\""]),
"claude":G("Ask Claude your first question","claude.ai",["Open claude.ai in your browser.","Sign up with Google or your email. New accounts verify a phone number by text message.","Click into the chat box.","Type one short request, then click the submit button.","Read the reply. Type your next message to keep going."],["The Claude sign-in page.","The Claude chat screen after sign-up.","A blinking cursor in the box.","Your message at the top; Claude's reply writing out below.","The conversation continuing in one thread."],["url","signin","box","sent","answer"],[("Claude Help: Get started with Claude","https://support.claude.com/en/articles/8114491-get-started-with-claude"),("Claude Help: Verify your phone number","https://support.claude.com/en/articles/8287232-verify-your-phone-number")]),
"gemini":G("Ask Gemini your first question","gemini.google.com",["Go to gemini.google.com on your computer.","(Optional) Click Sign in to save your chats. Some features work without signing in.","Click the text box at the bottom.","Type your question, then click Submit.","Read the answer. For a fresh start, click New chat (top left)."],["The Gemini page.","Your Google profile picture in a corner.","A blinking cursor in the bottom box.","Your question, then Gemini's answer below.","An empty new chat."],["url","signin","box","button:Submit","answer"],[("Gemini Apps Help: Use Gemini Apps","https://support.google.com/gemini/answer/13275745?co=GENIE.Platform%3DDesktop&hl=en")]),
"copilot":G("Ask Copilot your first question","Microsoft Copilot website",["Open Microsoft Copilot in your web browser (or the Copilot app).","(Optional) Sign in with a Microsoft, Apple or Google account.","Click the message box.","Type a clear, specific question and send it.","Not quite right? Follow up and ask it to change the format or go deeper."],["The Copilot chat page.","Your account picture in a corner.","A blinking cursor in the box.","An answer under your question.","A revised answer under your follow-up."],["url","signin","box","sent","answer"],[("Microsoft Support: Get started with Microsoft Copilot","https://support.microsoft.com/en-US/microsoft-copilot/getting-started-with-microsoft-copilot")],["Exact web address not stated on the help page; the address bar picture says \"Microsoft Copilot website\".","Whether you can chat without signing in isn't confirmed on the help page, so sign-in is marked optional."]),
"perplexity":G("Look something up with Perplexity","perplexity.ai",["Open perplexity.ai in your browser.","Click the box where you type a question.","Type your question in plain language.","Send it.","Click a numbered source to check where that part of the answer came from."],["The Perplexity home page.","A blinking cursor in the box.","Your question in the box.","An answer summarizing what it found.","The source web page opening."],["url","box","typed","sent","sources"],[("Perplexity Help: Getting started with Perplexity","https://www.perplexity.ai/help-center/en/articles/10354975-getting-started-with-perplexity")],["The question box's on-screen label isn't named in the help article; described generically."]),
"canva":G("Make a design draft with Canva AI","canva.com",["Open canva.com and sign in or sign up free.","On the homepage, select Canva AI in the side navigation.","Describe the design you have in mind.","Press Enter or select Submit.","Pick a result and select Edit to open it in the editor."],["Your Canva homepage.","The Canva AI prompt screen.","Your description in the prompt box.","Up to eight template results.","Your chosen design open in the editor."],["signin","button:Canva AI","typed","button:Submit","grid"],[("Canva Help: Create your design drafts with Canva AI","https://www.canva.com/help/using-magic-design/")]),
"gamma":G("Make a slide deck from one sentence in Gamma","gamma.app",["Open gamma.app and sign up free (no credit card required).","On your dashboard, click Create New AI. (Newer accounts may see a chat agent first; click Use classic generator.)","Choose Generate, then Presentation.","Type your topic.","Review the outline, then generate the slides."],["Your Gamma dashboard.","The creation options: Generate, Paste, Import.","A topic box for your presentation.","Your topic in the box.","An outline, then finished slides you can click through."],["signin","button:Create New AI","button:Generate","typed","grid"],[("Gamma Help: Create a new presentation","https://help.gamma.app/en/articles/7838093-how-do-i-create-a-new-presentation-document-or-webpage-in-gamma"),("Gamma pricing","https://gamma.app/pricing")],["The \"Presentation\" choice and the final generate button aren't named step-by-step on the help page; worded generically."]),
"notion":G("Ask Notion AI a question","notion.com",["Open notion.com and sign in or sign up.","Open any page.","Click the circular icon with a face in the bottom-right corner.","Ask something short, like \"make me a packing checklist\".","Keep chatting to refine it."],["Your Notion workspace sidebar.","A page open.","The Notion AI chat panel.","Notion AI's answer.","An updated answer."],["signin","answer","button:◉ AI","typed","answer"],[("Notion Help: Everything you can do with Notion AI","https://www.notion.com/help/guides/everything-you-can-do-with-notion-ai"),("Notion pricing (AI is a trial on Free)","https://www.notion.com/pricing")]),
"elevenlabs":G("Turn text into speech with ElevenLabs","elevenlabs.io",["Open elevenlabs.io and sign up free.","Select Text to Speech in the sidebar.","Type or paste a short paragraph into the input box.","Pick a voice from your Voices (bottom left).","Click Generate speech, then play it."],["Your ElevenLabs home screen.","A big text input box.","Your paragraph in the box.","A voice name selected.","An audio player with your clip."],["signin","button:Text to Speech","para","button:Voices ▾","play"],[("ElevenLabs docs: Text to Speech","https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech")]),
"otter":G("Record and transcribe with Otter","otter.ai",["Sign in to otter.ai (Basic is free).","Click Record, next to Import in the upper corner.","Speak into your microphone.","Click Stop in the playback bar.","Open the conversation from My Conversations."],["Your Otter home page.","A new recording titled \"Note\".","Words appearing as you talk.","The recording processing; keep the tab open until it starts.","Your words written out."],["signin","button:● Record","answer","button:■ Stop","answer"],[("Otter Help: Record a conversation","https://help.otter.ai/hc/en-us/articles/360048269733-Record-a-conversation"),("Otter Help: Recording best practices","https://help.otter.ai/hc/en-us/articles/40917035359255-Otter-Recording-Best-Practices-Pause-Resume-and-Upload")]),
}
def mock(kind,c,url):
    if kind=="url": return f'<div class=bar style="width:60%"></div><div class="input hl">🔒 {url}</div>'
    if kind=="signin": return f'<div class=bar style="width:40%"></div><div class=bar style="width:70%"></div><span class="btn {c}">Sign in / Sign up</span>'
    if kind=="box": return f'<div class=bar style="width:50%"></div><br><div class="input hl">Ask anything…</div>'
    if kind=="typed": return f'<div class="input hl">How do I write a polite email to reschedule?</div>'
    if kind=="sent": return f'<div class=input>How do I write a polite email to reschedule? <span class="btn {c}" style="float:right;padding:2px 12px">➤</span></div>'
    if kind=="answer": return '<div class=input style="text-align:right">You</div><div class=bar></div><div class=bar style="width:85%"></div><div class=bar style="width:70%"></div>'
    if kind=="sources": return f'<div class=bar></div><div class=bar style="width:80%"></div><span class="btn {c}">[1] source</span> <span class="btn {c}">[2] source</span>'
    if kind=="grid": return '<div class=grid style="grid-template-columns:repeat(3,1fr);gap:8px">'+''.join('<div class="bar" style="height:60px"></div>' for _ in range(3))+'</div>'
    if kind=="para": return '<div class="input hl">Good morning! Today we are going to learn three easy steps to…</div>'
    if kind=="play": return f'<div class=input><span class="btn {c}" style="padding:2px 12px">▶</span> ━━━━━━━━○──── 0:12</div>'
    if kind.startswith("button:"): return f'<div class=bar style="width:50%"></div><span class="btn {c}">{kind[7:]}</span>'
EMBED=open("beehiiv_embed.txt").read().strip()
SIGNUP='<h2>Get one new guide a week</h2><div class=card>'+EMBED+'<p style="font-size:16px">Form not showing? <a href="https://stepshotai.beehiiv.com/subscribe">Subscribe here</a>.</p></div>'
def printable_box(k):
    return ('<div class=card><h2>Get the printable version</h2>'
        '<p>Big type on one US Letter page: the five steps, the free tier, and how to cancel. Enter your email in the form above.</p>'
        f'<!-- Direct link fallback: <a href="../print/{k}.html">Open the printable cheat sheet</a> -->'
        '<p><span class="tag soon">Bundle of all 10, coming soon</span></p></div>')
def cheat_sheet(k):
    title,steps,sees,kinds,url,src,flags=GUIDES[k]
    T=TOOLS[k]
    rows="".join(f'<div class=sh><span class="num c{i%5}">{i+1}</span>{html.escape(s)}</div>' for i,s in enumerate(steps))
    links=f'<a href="{html.escape(T["src"],quote=True)}">Pricing</a>'
    if "src2" in T: links+=f' · <a href="{html.escape(T["src2"],quote=True)}">Cancel steps</a>'
    return (f'<p class=noprint><a href="../guides/{k}.html">Back to the {html.escape(T["n"])} guide</a></p>'
        f'<h1>{html.escape(T["n"])}</h1>'
        f'<p class=note>StepShot AI · {html.escape(title)} · Last checked {D} · {links}</p>'
        f'{rows}<div class=grid>'
        f'<div class=card><h2>Free tier</h2><p><b>{html.escape(T["fs"])}</b></p><p>{html.escape(T["free"])}</p></div>'
        f'<div class=card><h2>How to cancel</h2><p>{html.escape(T["sub"])}</p></div></div>')
def w(path,s): open(path,"w").write(s)
w("style.css",CSS)
os.makedirs("print",exist_ok=True)
cards="".join(f'<a class=card href="guides/{k}.html" style="text-decoration:none;color:inherit"><span class="tag ready">Guide ready</span><h3>{TOOLS[k]["n"]}</h3>{GUIDES[k][0]} · 5 steps</a>' for k in GUIDES)
cards+="".join(f'<div class=card><span class="tag soon">Coming soon</span><h3>{o}</h3>Guide and score card not written yet.</div>' for o in OTHER)
w("index.html",page("Home",f"""<div class=hero><h1>AI tools, one picture at a time.</h1><p>Color-coded, step-by-step guides for visual learners and ADHD brains. One action per step. A <b>“you should see this”</b> check after every step, so you always know you're on track.</p></div>
<h2>Guides</h2><div class=grid>{cards}</div>
{SIGNUP}"""))
for k,(title,steps,sees,kinds,url,src,flags) in GUIDES.items():
    T=TOOLS[k]
    body=f'<p><a href="../tools/{k}.html">{T["n"]} score card →</a></p><h1>{title}</h1><p class=note>⏱ 5 steps · Last checked {D}. Pictures are simplified illustrations; the real screen may look different and changes often.</p>'
    for i,(s,e) in enumerate(zip(steps,sees)):
        c=f"c{i%5}"
        body+=f'<section class=step><div class=sh><span class="num {c}">{i+1}</span>{html.escape(s)}</div><div class=mock>{mock(kinds[i],c,url)}</div><div class=see><b>You should see:</b> {html.escape(e)}</div></section>'
    body+='<div class=card><b>Source for these steps</b> (checked '+D+'):<ul>'+''.join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for n,u in src)+'</ul>'+(('<p class=note>⚠ Not confirmed in official docs, so worded generally:<br>'+'<br>'.join(html.escape(f) for f in flags)+'</p>') if flags else '<p>✔ All steps matched official docs.</p>')+'</div>'
    body+=SIGNUP
    body+=printable_box(k)
    body+='<p>🎉 Done! You got your first result. <a href="../index.html">Pick another guide</a>.</p>'
    w(f"guides/{k}.html",page(title,body,1))
    w(f"print/{k}.html",page(T["n"]+" cheat sheet",cheat_sheet(k),1,"sheet"))
for k,T in TOOLS.items():
    CX=f" Cancel steps: <a href='{T['src2']}'>{T['src2']}</a>." if 'src2' in T else ''
    w(f"tools/{k}.html",page(T["n"]+" score card",f"""<h1>{T['n']} — ADHD-friendly score card</h1><p class=note>Last checked {D}. Source: <a href="{T['src']}">{T['src']}</a>.{CX} <a href="../scores.html">How we score</a>.</p>
<table><tr><th>Measure</th><th>Score</th><th>How it was decided</th></tr>
<tr><td>Clutter</td><td>{NS}</td><td>Needs a timed hands-on review of the first screen.</td></tr>
<tr><td>Steps to first result</td><td>{NS}</td><td>Our guide uses 5 steps, but that is our teaching pace, not a measured count.</td></tr>
<tr><td>Free tier</td><td>{T['fs']}</td><td>{html.escape(T['free'])}</td></tr>
<tr><td>Easy to forget subscription</td><td>{T['ss']}</td><td>{html.escape(T['sub'])}</td></tr></table>
<p><a href="../guides/{k}.html">Read the guide →</a></p>""",1))
w("scores.html",page("Scoring",f"""<h1>How we score</h1><table><tr><th>Measure</th><th>What we check</th></tr>
<tr><td>Clutter</td><td>Count of buttons, banners and pop-ups on the first screen after sign-in (hands-on, fresh account).</td></tr>
<tr><td>Steps to first result</td><td>Clicks/inputs from landing page to first useful answer, timed, fresh account.</td></tr>
<tr><td>Free tier</td><td>Only what the official pricing page says. No guessing.</td></tr>
<tr><td>Easy to forget subscription</td><td>Annual prepay, bundles, app-store billing, and whether official help shows a clear cancel path.</td></tr></table>
<p class=note>If we haven't tested something, we say “not yet scored” instead of guessing. Each card links its source and last-checked date.</p>"""))
w("changes.html",page("What changed",f"""<h1>What changed</h1><p>Before/after picture cards when an AI tool moves a button or changes a plan.</p><div class=card><span class="tag soon">Coming soon</span><p>No entries yet. Tracking starts with ChatGPT, Claude and Gemini. Baseline: {D}.</p></div>"""))
w("disclosure.html",page("Affiliate disclosure","""<h1>Affiliate disclosure</h1><p>StepShot AI may earn a commission when you sign up for a tool through some of our links, at no extra cost to you. Affiliate links will always be labeled. Commissions never change our scores, and we may write guides for tools that pay us nothing.</p><p class=note>Right now this site has no affiliate links.</p>"""))
# "Should I pay?" — verdicts use only TOOLS fields already on the score cards:
#   fs (exact free-tier label), the ss prefix (High / Medium-high / Medium risk),
#   and whether free+sub+ss already mention annual billing or an unverified monthly price.
# No prices are added. User answers are how often, what for, and whether they need paid features.
FREE_CONTINUES={
"Generous free tier","Usable free tier","Free tier exists (limits not verified)","Small AI allowance on free",
}
FREE_RUNS_OUT={"Free start, one-time credits","AI is trial-only on free"}
TITLES={"free":"Free is enough","monthly":"Pay monthly","skip":"Skip it"}
OFTEN_PHRASE={"rare":"rarely (once in a while)","weekly":"a few times a week","daily":"most days"}
PURPOSE_PHRASE={"try":"just trying it","personal":"personal tasks","work":"work or school you depend on"}
def risk_band(ss):
    if ss.startswith("High risk"): return "high"
    if ss.startswith("Medium-high risk"): return "medium-high"
    if ss.startswith("Medium risk"): return "medium"
    raise SystemExit("checker: unknown subscription risk: "+ss)
def band_label(band):
    return {"high":"High risk","medium-high":"Medium-high risk","medium":"Medium risk"}[band]
def pay_caveat(T):
    blob=" ".join((T["free"],T["sub"],T["ss"])).lower()
    if "monthly price not verified" in blob:
        return "The pricing note already on this site says the monthly price is not verified. Check the official pricing page before you pay. This page does not add a price."
    if "annually" in blob or "annual" in blob or "/year" in blob:
        return "Notes already on this site mention annual billing. If you pay, choose a monthly plan when the official pricing page offers one. This page does not add a price."
    return "This page does not add a price. Read the cancel steps below before you subscribe."
def decide(often,purpose,premium,T):
    fs,name=T["fs"],T["n"]
    if fs in FREE_CONTINUES: runs_out=False
    elif fs in FREE_RUNS_OUT: runs_out=True
    else: raise SystemExit("checker: unknown free-tier label: "+fs)
    band=risk_band(T["ss"])
    elevated=band in ("high","medium-high")
    light=often=="rare" or purpose=="try"
    use=f"You said you would use {name} {OFTEN_PHRASE[often]}, for {PURPOSE_PHRASE[purpose]}."
    caveat=""
    if light and premium=="yes":
        code="skip"
        if purpose=="try" and often!="rare":
            why="paying just to try a tool is how a subscription gets forgotten"
        elif often=="rare" and purpose!="try":
            why="paying for a rare visit is how a subscription gets forgotten"
        else:
            why="paying for a rare visit or a first try is how a subscription gets forgotten"
        reason=use+f" Skip it: {why}. The free-tier note on this site is “{fs}”."
    elif light and premium=="unsure" and elevated:
        code="skip"
        reason=use+f" Skip it: you are not sure you need paid features, and the subscription note on this site starts with “{band_label(band)}”. The free-tier note is “{fs}”."
    elif (not light) and premium=="no" and runs_out:
        code="skip"
        reason=use+f" Skip it: you do not need paid features, and the free-tier note on this site is “{fs}”, so the free plan will not keep covering regular use."
    elif (not light) and premium=="yes":
        code="monthly"
        caveat=pay_caveat(T)
        reason=use+f" Pay monthly: you said you need the paid features. The free-tier note on this site is “{fs}”."
    elif premium in ("no","unsure"):
        code="free"
        if runs_out:
            extra=f"The free-tier note on this site is “{fs}”, so use the free start and stop when it ends."
        else:
            extra=f"The free-tier note on this site is “{fs}”."
        if premium=="unsure":
            extra+=" You are not sure you need paid features, so stay on free."
        else:
            extra+=" You said the free plan covers what you need."
        reason=use+" "+extra+" Free is enough."
    else:
        raise SystemExit("checker: unhandled answers for "+name)
    if elevated and band_label(band) not in reason:
        reason+=f" The subscription note on this site starts with “{band_label(band)}”, so read it before you start a trial or enter a card."
    if "$" in reason or "$" in caveat:
        raise SystemExit("checker: price leaked into verdict for "+name)
    return {"v":code,"title":TITLES[code],"reason":reason,"caveat":caveat}
CHECK_QUESTIONS=[
{"id":"often","prompt":"How often would you use {tool}?","options":[
    {"id":"rare","label":"Rarely — once in a while"},
    {"id":"weekly","label":"A few times a week"},
    {"id":"daily","label":"Most days"}]},
{"id":"purpose","prompt":"What would you use {tool} for?","options":[
    {"id":"try","label":"Just to try it"},
    {"id":"personal","label":"Personal tasks"},
    {"id":"work","label":"Work or school I depend on"}]},
{"id":"premium","prompt":"Do you need the paid features?","options":[
    {"id":"no","label":"No — the free plan covers what I need"},
    {"id":"unsure","label":"Not sure"},
    {"id":"yes","label":"Yes — I need the paid features"}]},
]
CHECK_RULES=[
{"title":"Free is enough","text":"You did not say you need paid features for ongoing use, or you are not sure. The free-tier label still fits, including a free start you stop when it ends."},
{"title":"Pay monthly","text":"You would use it a few times a week or most days, for personal tasks or for work or school, and you said you need the paid features. If the stored notes mention annual billing or an unverified monthly price, the page repeats that. No price is added."},
{"title":"Skip it","text":"You want paid features for a rare try. Or you are not sure, your use is light, and the subscription note is high or medium-high risk. Or you would use it regularly, the free-tier label says it runs out, and you do not want to pay."},
]
if len(TOOLS)!=10: raise SystemExit("checker: expected 10 tools")
checker_tools=[]
answers={}
for tid,T in TOOLS.items():
    if not tid.isalpha(): raise SystemExit("checker: bad id "+tid)
    for url in (T["src"],T.get("src2","")):
        if url and not url.startswith("https://"): raise SystemExit("checker: bad url "+url)
    risk_band(T["ss"])
    checker_tools.append({"id":tid,"n":T["n"],"fs":T["fs"],"ss":T["ss"],"sub":T["sub"],"src":T["src"],"src2":T.get("src2") or ""})
    for q1 in CHECK_QUESTIONS[0]["options"]:
        for q2 in CHECK_QUESTIONS[1]["options"]:
            for q3 in CHECK_QUESTIONS[2]["options"]:
                answers[f"{tid}|{q1['id']}|{q2['id']}|{q3['id']}"]=decide(q1["id"],q2["id"],q3["id"],T)
EXPECT={
("chatgpt","rare","try","no"):"free",
("chatgpt","rare","try","yes"):"skip",
("chatgpt","daily","work","yes"):"monthly",
("chatgpt","daily","work","no"):"free",
("chatgpt","weekly","personal","unsure"):"free",
("copilot","rare","try","unsure"):"skip",
("copilot","rare","try","no"):"free",
("copilot","daily","work","yes"):"monthly",
("gemini","weekly","try","unsure"):"skip",
("notion","weekly","personal","no"):"skip",
("notion","rare","try","no"):"free",
("notion","daily","work","yes"):"monthly",
("gamma","daily","personal","no"):"skip",
("canva","daily","work","unsure"):"free",
("canva","daily","work","yes"):"monthly",
("elevenlabs","weekly","work","yes"):"monthly",
("otter","rare","personal","yes"):"skip",
("perplexity","daily","work","yes"):"monthly",
("claude","daily","try","yes"):"skip",
("claude","weekly","work","no"):"free",
}
for key,want in EXPECT.items():
    got=answers["|".join(key)]
    if got["v"]!=want: raise SystemExit(f"checker expect {key} {want} got {got['v']}: {got['reason']}")
if "not verified" not in answers["perplexity|daily|work|yes"]["caveat"]: raise SystemExit("checker: perplexity caveat")
if "annual" not in answers["canva|daily|work|yes"]["caveat"].lower(): raise SystemExit("checker: canva caveat")
if "annual" not in answers["claude|weekly|personal|yes"]["caveat"].lower(): raise SystemExit("checker: claude caveat")
plain=answers["chatgpt|daily|work|yes"]["caveat"].lower()
if "annual" in plain or "not verified" in plain or "does not add a price" not in plain: raise SystemExit("checker: chatgpt caveat")
if answers["chatgpt|rare|try|no"]["caveat"]!="": raise SystemExit("checker: free caveat")
if "High risk" not in answers["copilot|rare|try|no"]["reason"]: raise SystemExit("checker: copilot risk sentence")
if "Medium-high risk" not in answers["gemini|daily|work|no"]["reason"]: raise SystemExit("checker: gemini risk sentence")
seen={}
for key,row in answers.items():
    tid,rest=key.split("|",1)
    T=TOOLS[tid]
    if T["fs"] not in row["reason"] or T["n"] not in row["reason"]: raise SystemExit("checker: reason missing fact "+key)
    if "$" in row["reason"] or "$" in row["title"] or "$" in row["caveat"]: raise SystemExit("checker: price in "+key)
    if row["title"]!=TITLES[row["v"]]: raise SystemExit("checker: bad title "+key)
    if row["v"]=="monthly" and not row["caveat"]: raise SystemExit("checker: monthly without caveat "+key)
    if row["v"]!="monthly" and row["caveat"]: raise SystemExit("checker: caveat on "+key)
    seen.setdefault(tid,set()).add(row["v"])
for tid,vs in seen.items():
    if vs!={"free","monthly","skip"}: raise SystemExit(f"checker: {tid} missing a verdict {vs}")
if len(answers)!=270: raise SystemExit("checker: expected 270 verdicts")
checker_payload=json.dumps({
"checked":D,
"questions":CHECK_QUESTIONS,
"rules":CHECK_RULES,
"tools":checker_tools,
"answers":answers,
},ensure_ascii=False,indent=2).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
CHECKER_JS=r"""(function () {
  var DATA = __DATA__;
  var root = document.getElementById("app");
  var state = { step: 0, tool: "", often: "", purpose: "", premium: "" };

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        n.setAttribute(k, attrs[k]);
      });
    }
    if (text != null && text !== "") n.textContent = text;
    return n;
  }
  function toolById(id) {
    for (var i = 0; i < DATA.tools.length; i++) {
      if (DATA.tools[i].id === id) return DATA.tools[i];
    }
    return null;
  }
  function reset() {
    state.step = 0;
    state.tool = "";
    state.often = "";
    state.purpose = "";
    state.premium = "";
    render();
  }
  function goBack(e) {
    e.preventDefault();
    if (state.step > 0) state.step -= 1;
    render();
  }
  function choiceButton(label, onClick) {
    var b = el("button", { type: "button" }, label);
    b.style.display = "block";
    b.style.width = "100%";
    b.style.textAlign = "left";
    b.addEventListener("click", onClick);
    return b;
  }
  function renderPicker() {
    var hero = el("div", { "class": "hero" });
    hero.appendChild(el("h1", null, "Should I pay?"));
    hero.appendChild(el("p", null, "Pick a tool. Answer 3 questions about how you would use it. Get a plain verdict: free is enough, pay monthly, or skip it."));
    root.appendChild(hero);
    root.appendChild(el("p", { "class": "note" }, "Guidance only. A verdict uses two facts already stored for that tool: the free-tier label and the subscription note. This page does not add prices. Your answers stay in this browser and are not sent anywhere. Tool notes last checked " + DATA.checked + "."));
    root.appendChild(el("h2", null, "Pick a tool"));
    var grid = el("div", { "class": "grid" });
    DATA.tools.forEach(function (t) {
      var card = el("div", { "class": "card" });
      card.appendChild(el("h3", null, t.n));
      card.appendChild(el("span", { "class": "tag soon" }, t.fs));
      var btn = el("button", { type: "button" }, "Check " + t.n);
      btn.addEventListener("click", function () {
        state.tool = t.id;
        state.often = "";
        state.purpose = "";
        state.premium = "";
        state.step = 1;
        render();
      });
      card.appendChild(btn);
      grid.appendChild(card);
    });
    root.appendChild(grid);
    var how = el("div", { "class": "card" });
    how.style.marginTop = "24px";
    how.appendChild(el("h2", null, "How this decides"));
    how.appendChild(el("p", null, "Three answers, then one verdict. Under every verdict: that tool’s subscription risk and cancel steps, copied from the score card."));
    var ul = document.createElement("ul");
    DATA.rules.forEach(function (rule) {
      var li = document.createElement("li");
      li.appendChild(el("b", null, rule.title + " — "));
      li.appendChild(document.createTextNode(rule.text));
      ul.appendChild(li);
    });
    how.appendChild(ul);
    root.appendChild(how);
  }
  function renderQuestion() {
    var t = toolById(state.tool);
    var q = DATA.questions[state.step - 1];
    var back = el("a", { href: "#app" }, "Back");
    back.addEventListener("click", goBack);
    root.appendChild(back);
    var tags = el("p");
    var nameTag = el("span", { "class": "tag ready" }, t.n);
    nameTag.style.marginRight = "8px";
    tags.appendChild(nameTag);
    tags.appendChild(el("span", { "class": "tag soon" }, t.fs));
    root.appendChild(tags);
    var step = el("section", { "class": "step" });
    var sh = el("div", { "class": "sh" });
    sh.appendChild(el("span", { "class": "num c" + ((state.step - 1) % 5) }, String(state.step)));
    var label = el("span", null, q.prompt.split("{tool}").join(t.n));
    label.style.flex = "1";
    sh.appendChild(label);
    step.appendChild(sh);
    root.appendChild(step);
    var card = el("div", { "class": "card" });
    q.options.forEach(function (opt) {
      card.appendChild(choiceButton(opt.label, function () {
        state[q.id] = opt.id;
        state.step += 1;
        render();
      }));
    });
    root.appendChild(card);
    window.scrollTo(0, 0);
  }
  function renderVerdict() {
    var t = toolById(state.tool);
    var key = [state.tool, state.often, state.purpose, state.premium].join("|");
    var row = DATA.answers[key];
    var back = el("a", { href: "#app" }, "Back");
    back.addEventListener("click", goBack);
    root.appendChild(back);
    if (!row) {
      root.appendChild(el("p", { "class": "note" }, "That combination has no stored verdict. Re-run build.py."));
      return;
    }
    root.appendChild(el("p", { "class": "note" }, "Guidance only. This uses the free-tier label and the subscription note already published for " + t.n + ". This page does not add prices. Your answers were not sent anywhere."));
    var hero = el("div", { "class": "hero" });
    hero.appendChild(el("span", { "class": "tag ready" }, "Guidance"));
    hero.appendChild(el("h1", null, row.title));
    hero.appendChild(el("p", null, row.reason));
    if (row.caveat) hero.appendChild(el("p", null, row.caveat));
    root.appendChild(hero);
    var chips = el("p");
    DATA.questions.forEach(function (q) {
      var chosen = "";
      q.options.forEach(function (opt) {
        if (opt.id === state[q.id]) chosen = opt.label;
      });
      var chip = el("span", { "class": "tag soon" }, chosen);
      chip.style.marginRight = "8px";
      chips.appendChild(chip);
    });
    root.appendChild(chips);
    root.appendChild(el("h2", null, "Subscription risk"));
    root.appendChild(el("div", { "class": "note" }, t.ss));
    root.appendChild(el("h2", null, "Cancel steps"));
    root.appendChild(el("div", { "class": "card" }, t.sub));
    var links = el("p");
    links.appendChild(el("a", { href: "tools/" + t.id + ".html" }, t.n + " score card"));
    links.appendChild(document.createTextNode(" · "));
    links.appendChild(el("a", { href: t.src }, "Official pricing page"));
    if (t.src2) {
      links.appendChild(document.createTextNode(" · "));
      links.appendChild(el("a", { href: t.src2 }, "Official cancel page"));
    }
    links.appendChild(document.createTextNode(". Notes last checked " + DATA.checked + "."));
    root.appendChild(links);
    var again = el("button", { type: "button" }, "Check another tool");
    again.addEventListener("click", reset);
    root.appendChild(again);
    window.scrollTo(0, 0);
  }
  function render() {
    root.textContent = "";
    if (state.step <= 0) renderPicker();
    else if (state.step <= DATA.questions.length) renderQuestion();
    else renderVerdict();
  }
  render();
})();
"""
w("checker.html",page("Should I pay?","""<!-- Generated by build.py from TOOLS. Edit build.py and rerun it. -->
<div id=app></div>
<noscript><p class=note>Turn on JavaScript to use the checker. Guidance only: verdicts come from the free-tier label and subscription note already on each score card. This page does not add prices.</p></noscript>
<script>
"""+CHECKER_JS.replace("__DATA__",checker_payload)+"""
</script>""",0))
w("CNAME","stepshotai.com\n")
