#!/usr/bin/env python3
"""
Run on your ORIGINAL index.html (the one you pasted to me):
    python patch_portfolio_v2.py
If you already ran the first script, use the backup it made instead:
    python patch_portfolio_v2.py index.backup.html
Output is always written to index.html. Your original is kept safe.
"""
import re, shutil, sys, os

SRC = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(SRC, encoding="utf-8").read()
if SRC == "index.html" and not os.path.exists("index.original.html"):
    shutil.copy(SRC, "index.original.html")
missed = []

def rep(old, new, all_=False):
    global s
    if old not in s: missed.append(old[:70]); return
    s = s.replace(old, new) if all_ else s.replace(old, new, 1)

def rx(pat, new):
    global s
    s, c = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
    if c == 0: missed.append("REGEX " + pat[:60])

# ================= 1. Facts to match your CV and your updates =================
# Waji ended about two weeks ago, so the original "Oct 2025 to Oct 2026" is right and stays.
rep('Records Clerk &amp; Credit Analyst', 'Data Entry Specialist &amp; Credit Analyst')
rep('<li>Use HubSpot CRM and customer data to strengthen client relationships and improve business performance.</li>',
    '<li>Use HubSpot CRM and customer data to strengthen client relationships and improve business performance.</li>'
    '<li>Deployed a Chatly AI agent to handle customer and lead responses, qualification, follow ups and templates.</li>')
rep('<div class="exp-entry"><div class="when">Sep 2026 to Present</div>',
    '<div class="exp-entry"><div class="when">Sep 2024 to Dec 2024</div><div><h3>Student Researcher</h3>'
    '<div class="role-org">Kabarak University</div><ul><li>Researched fiscal policies and their impact on poverty.</li>'
    '<li>Presented findings in group discussions with faculty and students.</li></ul></div></div>\n'
    '    <div class="exp-entry"><div class="when">Sep 2026 to Present</div>')
rep('<div class="edu-card"><h3>Economics and Finance</h3>',
    '<div class="edu-card"><h3>Bachelor\'s Degree, Economics and Finance</h3>'
    '<div class="role-org">Kabarak University · Sep 2021 to Dec 2025</div>')
rep('Demonstrated foundational digital productivity and computer skills.</p></div>',
    'Demonstrated foundational digital productivity and computer skills.</p></div>'
    '<div class="cert"><strong>Strathmore Mathlete Medal</strong><span>Award</span></div>')
rep('where I can combine structured execution with an analytical mindset.</p>',
    'where I can combine structured execution with an analytical mindset. Based in Kenya and available to cover US and UK business hours remotely.</p>')

# ================= 2. Remove Mozzart everywhere =================
rep('<div class="result-card"><div class="result-number">~90%</div><div class="result-label">First contact resolution</div>'
    '<div class="result-note">At Mozzart, across phone, chat and email.</div></div>',
    '<div class="result-card"><div class="result-number">3%</div><div class="result-label">Sales conversion</div>'
    '<div class="result-note">Monthly sales conversion at Vibeora, up from 0.2% at the start.</div></div>')
rep('Calls handled and documented across Airtel and Mozzart.', 'Calls handled and documented at Airtel Kenya.')
rx(r'<div class="case-meta">Airtel Kenya · Mozzart</div>.*?(?=<a class="case-link" href="#customer-operations">)',
   '<div class="case-meta">Airtel Kenya · 2021 to 2024</div><p>Handled around 150 calls a day at Airtel Kenya across complaints, '
   'account activation and order processing, resolving issues diplomatically, running regular account checks and training peers.</p>'
   '<div class="case-results"><div><strong>~150/day</strong><span>Calls</span></div><div><strong>~92%</strong><span>CSAT</span></div></div>')
rep('<li>Handled approximately 150 calls a day at Airtel and Mozzart.</li>', '<li>Handled approximately 150 calls a day at Airtel Kenya.</li>')
rep('<li>Covered complaints, account activation, order processing, and technical support.</li>',
    '<li>Covered complaints, account activation and order processing.</li>')
rep('<li>Maintained accurate CRM records.</li>', '<li>Ran regular account checks to keep customer contact records current.</li>')
rep('<li>Escalated complex cases through to resolution.</li>',
    '<li>Resolved complaints diplomatically, offering compensation to retain customers where appropriate.</li>')
rep('<div class="study-stat"><strong>~90%</strong><span>FCR</span></div>',
    '<div class="study-stat"><strong>3+ years</strong><span>At Airtel</span></div>')
rx(r'<div class="exp-entry"><div class="when">Jan 2025 to Dec 2025</div><div><h3>Customer Service Specialist</h3>.*?Issue Resolution</span></div></div></div>\s*', '')
rx(r'<div class="role-case reverse">\s*<div class="role-case-copy">\s*<div class="study-kicker">Mozzart.*?No real customer records are shown\.</p>\s*</div>\s*</div>', '')
rep('The work moved between billing, network complaints, account requests, activations, and cases that needed escalation.',
    'The work moved between customer complaints, account activations, order processing, and cases where compensation was the right way to keep a customer.')
rep('<span>Issue <b>Billing discrepancy</b></span>', '<span>Issue <b>Customer complaint</b></span>')

# ================= 3. Real figures only: CSAT and calls at Airtel =================
rx(r'<div class="service-dashboard">.*?(?=<div class="workflow"><span>Identify issue)',
   '<div class="service-dashboard"><div class="big-metric"><strong>~150</strong><span>Calls handled a day</span></div>'
   '<div class="big-metric"><strong>~92%</strong><span>Customer satisfaction</span><div class="meter"><i style="width:92%"></i></div></div></div>'
   '<div class="hcap" style="margin-top:9px">Figures from my own work records at Airtel Kenya.</div>')

# ================= 4. Vibeora: real conversion figures =================
def crow(label, val, w):
    return (f'<div class="hrow vrow"><span>{label}</span><div class="htrack"><i style="width:{w}%"></i></div><b>{val}</b></div>')
rep('<span>From served clients</span></div></div><div class="growth-note">',
    '<span>From served clients</span></div><div class="sales-box"><small>Monthly sales conversion</small>'
    + crow("Start", "0.2%", 6.7) + crow("Now", "3%", 100) + '</div></div><div class="growth-note">')

# ================= 5. Flamingo: plain process, no invented numbers =================
def steps(items):
    return '<div class="steps">' + ''.join(f'<div class="step"><b>{i}</b><span>{t}</span></div>' for i, t in enumerate(items, 1)) + '</div>'
rx(r'<h4>Reporting trend \(illustrative\)</h4><div class="mini-bars">.*?</div>',
   '<h4>From data to decision</h4>' + steps(["Track costs and project spend", "Analyse budget variances",
        "Prepare the management report", "Leadership uses it to decide"]))
rep('<span>3 items need follow up</span>', '<span>Follow ups tracked</span>')
rep('<strong>09:30</strong><span>Finance review</span>', '<strong>Meetings</strong><span>Finance review</span>')
rep('<strong>4 / 6</strong><span>Items closed</span>', '<strong>Tracked</strong><span>Until closed</span>')

# ================= 6. Credit analyst: real workflow, honest role split =================
rx(r'<div class="finance-dashboard">.*?(?=<div class="workflow"><span>Financial review)',
   '<div class="credit-table" style="background:#fff;border:1px solid #D8E0DB">'
   '<div class="credit-row head"><span>Review step</span><span>Done by</span><span>Outcome</span></div>'
   '<div class="credit-row"><span>Client documentation</span><span>Analyst</span><b>Reviewed</b></div>'
   '<div class="credit-row"><span>Risk control checklist</span><span>Analyst</span><b>Applied</b></div>'
   '<div class="credit-row"><span>Repayment capacity</span><span>Analyst</span><b>Assessed</b></div>'
   '<div class="credit-row"><span>Portfolio activity</span><span>Analyst</span><b>Monitored</b></div>'
   '<div class="credit-row"><span>Early default signs</span><span>Analyst</span><b>Flagged</b></div>'
   '<div class="credit-row"><span>Credit decision</span><span>Senior analyst</span><b>Final approval</b></div></div>')
rep('CREDIT ANALYSIS · ILLUSTRATIVE DATA', 'CREDIT REVIEW WORKFLOW · PORTFOLIO DEMONSTRATION')
rx(r'<div class="credit-summary">.*?(?=<div class="credit-footer">)',
   '<div class="credit-table" style="margin-top:12px">'
   '<div class="credit-row head"><span>Information reviewed</span><span>Done by</span><span>Status</span></div>'
   '<div class="credit-row"><span>Financial records</span><span>Analyst</span><b>Reviewed</b></div>'
   '<div class="credit-row"><span>Repayment history</span><span>Analyst</span><b>Reviewed</b></div>'
   '<div class="credit-row"><span>Existing obligations</span><span>Analyst</span><b>Reviewed</b></div>'
   '<div class="credit-row"><span>Collateral and terms</span><span>Analyst</span><b>Reviewed</b></div>'
   '<div class="credit-row"><span>Approval decision</span><span>Senior analyst</span><b>Final say</b></div></div>')
rep('CREDIT REVIEW · SAMPLE WORKSPACE', 'CREDIT REVIEW · SUPPORT ROLE')
rep('<b>ILLUSTRATIVE DATA</b>', '<b>REVIEW STEPS</b>')
rep('Illustrative portfolio data only. No real borrower information is shown.',
    'Portfolio demonstration of the review steps. No real borrower information is shown.')

# ================= 7. Product analytics: definitions, not made-up data =================
def krow(q, k, m):
    return f'<div class="kpirow"><span>{q}</span><b>{k}</b><span>{m}</span></div>'
rx(r'<div class="chart">.*?<div class="chart-caption">[^<]*</div></div>',
   '<div class="chart"><div class="mock-label">Business question → KPI → how it is measured</div><div class="kpimap">'
   '<div class="kpirow head"><span>Question</span><span>KPI</span><span>Measured as</span></div>'
   + krow("Are new players coming back?", "Retention rate", "Players active on day N ÷ players who started")
   + krow("How big is the daily community?", "DAU", "Unique players active in one day")
   + krow("Are we losing players?", "Churn rate", "Players lost in a period ÷ players at the start")
   + krow("Are players buying?", "Conversion rate", "Players who purchase ÷ all players")
   + '</div><div class="chart-caption">Business question → KPI → finding → recommendation</div></div>')
rep('A product dashboard that looks at the player journey', 'How each KPI maps to the player journey')
def stage(n, name, kpi, q):
    return f'<div class="jstage"><small>{n} · {name}</small><strong>{kpi}</strong><span>{q}</span></div>'
rx(r'<div class="product-screen">.*?analysis workflow\.</p>\s*</div>',
   '<div class="product-screen"><div class="ps-top"><span>LEGENDS OF AETHER</span><span>PLAYER JOURNEY · KPI MAP</span><b>● PORTFOLIO DEMO</b></div>'
   '<div class="journey">'
   + stage("01", "Come back", "Retention rate", "Do new players return after their first session?")
   + stage("02", "Stay active", "DAU", "How many players are active each day?")
   + stage("03", "Spend", "Conversion rate", "What share of players complete a purchase?")
   + stage("04", "Leave", "Churn rate", "How many players are we losing over a period?")
   + '</div><div class="ps-footer"><span>Method</span><strong>Question</strong><span>→</span><strong>KPI</strong>'
     '<span>→</span><strong>Finding</strong><span>→</span><strong>Recommendation</strong></div>'
   '<p class="mock-disclaimer">Portfolio demonstration of how each KPI maps to a stage of the player journey. No player data is shown.</p></div>')

# ================= 8. Executive mockups: no made-up counts =================
rep('<h4>Inbox triage</h4>', '<h4>Inbox triage · 80 to 100 a day</h4>')
rep('<span>Urgent</span><span class="status">3</span>', '<span>Urgent</span><span class="status">REPLY</span>')
rep('<span>Follow up</span><span class="status">7</span>', '<span>Follow up</span><span class="status">TRACK</span>')
rep('<span>Done</span><span class="status">18</span>', '<span>Done</span><span class="status">FILED</span>')
rep('<small>In progress · 70%</small>', '<small>In progress</small>')
rep('<div class="mini-progress"><i style="width:70%"></i></div>', '')

# ================= 9. Stale demo dates and broken calendar =================
rep('MONDAY · 31 AUG', 'MONDAY · 9 NOV')
rep('31 Aug', '9 Nov', True)
rep('01 Sep', '10 Nov', True)
rep('<span class="day active">4</span><span class="day">5</span><span class="day event">6</span><span class="day">7</span>'
    '<span class="day active">8</span><span class="day">9</span><span class="day">10</span>',
    '<span class="day active">9</span><span class="day">10</span><span class="day event">11</span><span class="day">12</span>'
    '<span class="day active">13</span><span class="day">14</span><span class="day">15</span>')
rx(r'<div class="cal-grid">.*?</div>',
   '<div class="cal-grid"><span></span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span>'
   '<span>09:00</span><span class="busy">Finance review</span><span></span><span></span><span class="busy">Client call</span>'
   '<span>10:30</span><span></span><span class="busy">Board prep</span><span></span><span></span>'
   '<span>13:00</span><span class="busy">Travel check</span><span></span><span class="busy">Meeting</span><span></span>'
   '<span>15:00</span><span></span><span></span><span></span><span class="busy">Follow ups</span></div>')

# ================= 10. Styles =================
css = """<style id="chart-v7">
.hrow{display:grid;grid-template-columns:70px 1fr 38px;gap:8px;align-items:center;margin-bottom:8px;font:8px 'IBM Plex Mono',monospace;color:#59665F}
.vrow{grid-template-columns:34px 1fr 34px;margin:7px 0 0}
.htrack{position:relative;height:10px;background:#E4EAE6}.htrack i{display:block;height:100%;background:#6C9B89}
.hrow b{color:#24473C;text-align:right}.hcap{font:8px 'IBM Plex Mono',monospace;color:#6C7871;line-height:1.5}
.meter{position:relative;height:6px;background:#E0E8E3;margin-top:10px}.meter i{display:block;height:100%;background:#6C9B89}
.steps{display:grid;gap:6px}.step{display:grid;grid-template-columns:22px 1fr;gap:8px;align-items:center;padding:7px 8px;background:#F1F4F2;font-size:10px;color:#33443C}
.step b{display:grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#1E6355;color:#fff;font:9px 'IBM Plex Mono',monospace}
.kpimap{display:grid}.kpirow{display:grid;grid-template-columns:1.2fr .8fr 1.4fr;gap:8px;padding:8px 4px;border-top:1px solid #E7EBE8;font-size:9px;color:#46534C;align-items:center}
.kpirow.head{border-top:0;font:8px 'IBM Plex Mono',monospace;text-transform:uppercase;color:#737F78}.kpirow b{font:600 10px 'IBM Plex Sans',sans-serif;color:#17332D}
.journey{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:9px}
.jstage{background:#F4F7F4;padding:14px;border-top:3px solid #6C9B89}.jstage small{display:block;font:8px 'IBM Plex Mono',monospace;color:#75827A;text-transform:uppercase}
.jstage strong{display:block;font:600 16px 'Fraunces',serif;color:#17332D;margin:5px 0}.jstage span{display:block;font-size:10px;color:#5E6B63;line-height:1.45}
@media(max-width:820px){.journey{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.journey{grid-template-columns:1fr}.kpirow{grid-template-columns:1fr 1fr}.kpirow span:last-child{grid-column:span 2}}
</style>
"""
rep('</head>', css + '</head>')

open("index.html", "w", encoding="utf-8").write(s)
print("Done. Written to index.html")
print("NOT FOUND (%d):" % len(missed) if missed else "All replacements applied.")
for m in missed: print(" -", m)
left = [w for w in ["Mozzart", "MOZ ", "FCR", "First contact", "Payment query"] if w in s]
print("Leftover Mozzart or FCR text: " + ", ".join(left) if left else "Mozzart fully removed.")
