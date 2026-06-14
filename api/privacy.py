from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get(
    "/privacy",
    response_class=HTMLResponse
)
def privacy_policy():

    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy — MailMind AI</title>
  <link rel="icon" href="/static/favicon.ico" type="image/png">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #0b0f1a;
      color: rgba(255,255,255,0.75);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      line-height: 1.75;
      padding: 64px 24px 100px;
    }

    .container {
      max-width: 720px;
      margin: 0 auto;
    }

    /* ── Header ── */
    .header {
      margin-bottom: 56px;
      padding-bottom: 40px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 36px;
      text-decoration: none;
    }

    .brand-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4facfe;
      box-shadow: 0 0 10px #4facfe;
    }

    .brand-name {
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: #4facfe;
    }

    h1 {
      font-size: 38px;
      font-weight: 700;
      color: #f0f4ff;
      letter-spacing: -1px;
      line-height: 1.2;
      margin-bottom: 14px;
    }

    .meta {
      font-size: 13px;
      color: rgba(255,255,255,0.28);
      letter-spacing: 0.3px;
    }

    .meta span {
      display: inline-block;
      width: 3px;
      height: 3px;
      border-radius: 50%;
      background: rgba(255,255,255,0.2);
      vertical-align: middle;
      margin: 0 10px;
    }

    /* ── Intro card ── */
    .intro-card {
      background: rgba(79,172,254,0.05);
      border: 1px solid rgba(79,172,254,0.14);
      border-radius: 16px;
      padding: 24px 28px;
      margin-bottom: 52px;
      color: rgba(255,255,255,0.55);
      font-size: 14px;
      line-height: 1.7;
    }

    /* ── Sections ── */
    .section {
      margin-bottom: 44px;
    }

    .section-label {
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #4facfe;
      margin-bottom: 10px;
    }

    h2 {
      font-size: 19px;
      font-weight: 600;
      color: #f0f4ff;
      letter-spacing: -0.3px;
      margin-bottom: 14px;
    }

    p {
      color: rgba(255,255,255,0.55);
      font-size: 14px;
    }

    /* ── Item list ── */
    .item-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 4px;
    }

    .item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 10px;
      padding: 12px 16px;
      font-size: 14px;
      color: rgba(255,255,255,0.6);
    }

    .item-icon {
      width: 18px;
      height: 18px;
      flex-shrink: 0;
      margin-top: 1px;
      opacity: 0.5;
    }

    /* ── Highlight pills ── */
    .pill-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 4px;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 100px;
      padding: 6px 14px;
      font-size: 13px;
      color: rgba(255,255,255,0.5);
    }

    .pill-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: #4facfe;
      opacity: 0.7;
      flex-shrink: 0;
    }

    /* ── Guarantee cards ── */
    .guarantee-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 4px;
    }

    @media (max-width: 540px) {
      .guarantee-grid { grid-template-columns: 1fr; }
      h1 { font-size: 28px; }
    }

    .guarantee-card {
      background: rgba(255,255,255,0.025);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 12px;
      padding: 18px 20px;
    }

    .guarantee-title {
      font-size: 13px;
      font-weight: 600;
      color: rgba(255,255,255,0.75);
      margin-bottom: 5px;
    }

    .guarantee-desc {
      font-size: 12px;
      color: rgba(255,255,255,0.32);
      line-height: 1.6;
    }

    .guarantee-icon {
      font-size: 18px;
      margin-bottom: 10px;
      opacity: 0.6;
    }

    /* ── Contact card ── */
    .contact-card {
      background: rgba(255,255,255,0.025);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 14px;
      padding: 22px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }

    .contact-label {
      font-size: 12px;
      color: rgba(255,255,255,0.28);
      margin-bottom: 4px;
    }

    .contact-email {
      font-size: 14px;
      font-weight: 500;
      color: #a8c8fe;
      text-decoration: none;
    }

    .contact-email:hover {
      color: #4facfe;
    }

    .contact-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(79,172,254,0.1);
      border: 1px solid rgba(79,172,254,0.2);
      border-radius: 100px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 500;
      color: #4facfe;
      text-decoration: none;
      white-space: nowrap;
      transition: background 0.15s;
    }

    .contact-btn:hover {
      background: rgba(79,172,254,0.18);
    }

    /* ── Divider ── */
    .divider {
      border: none;
      border-top: 1px solid rgba(255,255,255,0.05);
      margin: 48px 0;
    }

    /* ── Footer ── */
    .footer {
      font-size: 12px;
      color: rgba(255,255,255,0.18);
      text-align: center;
      padding-top: 40px;
      border-top: 1px solid rgba(255,255,255,0.05);
    }
  </style>
</head>
<body>
  <div class="container">

    <!-- Header -->
    <div class="header">
      <div class="brand">
        <span class="brand-dot"></span>
        <span class="brand-name">MailMind AI</span>
      </div>
      <h1>Privacy Policy</h1>
      <p class="meta">
        Last updated: June 2026
        <span></span>
        Effective immediately
      </p>
    </div>

    <!-- Intro -->
    <div class="intro-card">
      MailMind AI is an email productivity assistant that connects to your Gmail
      account to generate summaries, extract tasks, detect calendar events, and
      deliver AI-powered digests — all through Telegram. This policy explains
      exactly what data we access, how we use it, and what we never do with it.
    </div>

    <!-- Data We Access -->
    <div class="section">
      <p class="section-label">01</p>
      <h2>Data We Access</h2>
      <div class="item-list">
        <div class="item">
          <svg class="item-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <rect x="2" y="4" width="16" height="13" rx="2"/><polyline points="2,7 10,12 18,7"/>
          </svg>
          Gmail message metadata and email content required for analysis
        </div>
        <div class="item">
          <svg class="item-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <rect x="3" y="2" width="14" height="17" rx="2"/><line x1="7" y1="7" x2="13" y2="7"/><line x1="7" y1="11" x2="13" y2="11"/><line x1="7" y1="15" x2="10" y2="15"/>
          </svg>
          Google Calendar events — only if you enable calendar features
        </div>
        <div class="item">
          <svg class="item-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <circle cx="10" cy="10" r="8"/><polyline points="7,10 9,12 13,8"/>
          </svg>
          Google Tasks — only if you enable task features
        </div>
      </div>
    </div>

    <!-- How We Use Data -->
    <div class="section">
      <p class="section-label">02</p>
      <h2>How We Use Your Data</h2>
      <p style="margin-bottom: 16px;">
        Your data is used exclusively to power the features you have enabled.
        Nothing more.
      </p>
      <div class="pill-grid">
        <div class="pill"><span class="pill-dot"></span>Email summaries</div>
        <div class="pill"><span class="pill-dot"></span>AI digests</div>
        <div class="pill"><span class="pill-dot"></span>Task extraction</div>
        <div class="pill"><span class="pill-dot"></span>Calendar event detection</div>
        <div class="pill"><span class="pill-dot"></span>Reminder notifications</div>
        <div class="pill"><span class="pill-dot"></span>Priority classification</div>
      </div>
    </div>

    <!-- Guarantees -->
    <div class="section">
      <p class="section-label">03</p>
      <h2>Our Guarantees</h2>
      <div class="guarantee-grid">
        <div class="guarantee-card">
          <div class="guarantee-icon">◈</div>
          <div class="guarantee-title">No data selling</div>
          <div class="guarantee-desc">We never sell, rent, or trade your personal data with any third party.</div>
        </div>
        <div class="guarantee-card">
          <div class="guarantee-icon">◉</div>
          <div class="guarantee-title">Secure storage</div>
          <div class="guarantee-desc">All user data is stored securely and used only to deliver MailMind AI services.</div>
        </div>
        <div class="guarantee-card">
          <div class="guarantee-icon">⊘</div>
          <div class="guarantee-title">No third-party sharing</div>
          <div class="guarantee-desc">Your emails and account data are never shared with advertisers or partners.</div>
        </div>
        <div class="guarantee-card">
          <div class="guarantee-icon">✓</div>
          <div class="guarantee-title">Your control</div>
          <div class="guarantee-desc">Disconnect your account at any time and request complete removal of your data.</div>
        </div>
      </div>
    </div>

    <hr class="divider">

    <!-- Contact -->
    <div class="section">
      <p class="section-label">04</p>
      <h2>Contact & Privacy Requests</h2>
      <p style="margin-bottom: 20px;">
        For privacy questions, data removal requests, or any concerns about
        how your information is handled, reach out directly.
      </p>
      <div class="contact-card">
        <div>
          <p class="contact-label">Privacy contact</p>
          <a class="contact-email" href="mailto:valtryfreefire@gmail.com">
            valtryfreefire@gmail.com
          </a>
        </div>
        <a class="contact-btn" href="mailto:valtryfreefire@gmail.com">
          ⟡ Send message
        </a>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      &copy; 2026 MailMind AI &nbsp;·&nbsp; All rights reserved &nbsp;·&nbsp;
      Your data, your control.
    </div>

  </div>
</body>
</html>"""