import streamlit as st
import base64, os

from prediction_helper import predict

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lauki Finance · Credit Risk Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load hero image as base64 ────────────────────────────────────────────────
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Place hero_image.png in the same folder as main.py
_img_candidates = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero_image.png"),
]
HERO_B64 = None
for _p in _img_candidates:
    if os.path.exists(_p):
        HERO_B64 = img_to_b64(_p)
        break

HERO_HTML = (
    f'<img src="data:image/png;base64,{HERO_B64}" class="hero-img" alt="Credit analysis">'
    if HERO_B64 else
    '<div class="hero-img" style="background:linear-gradient(135deg,#1c2923,#0e1512);height:340px"></div>'
)

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:         #0e1512;
    --bg-mid:     #121a17;
    --bg-card:    #161f1b;
    --bg-light:   #1c2923;
    --gold:       #c9a84c;
    --gold-light: #e2c47a;
    --gold-pale:  #f5e6c2;
    --green:      #3ddc97;
    --green-dim:  #2ab87c;
    --red:        #e05c5c;
    --amber:      #e6a23c;
    --text-main:  #e8ede9;
    --text-muted: #7a9486;
    --border:     rgba(61,220,151,0.13);
    --border-gold:rgba(201,168,76,0.18);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text-main) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 100% 0%,   rgba(61,220,151,0.05) 0%, transparent 55%),
        radial-gradient(ellipse 70% 45% at 0%   100%, rgba(201,168,76,0.06) 0%, transparent 60%),
        linear-gradient(160deg, #0e1512 0%, #08100d 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1300px; }

/* ── Top bar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 0 1.3rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0;
}
.topbar-logo { display: flex; align-items: center; gap: 0.75rem; }
.logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
    border-radius: 9px; display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem; font-weight: 700; color: #0e1512;
    box-shadow: 0 0 18px rgba(201,168,76,0.35);
}
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; font-weight: 700; color: var(--gold-light);
}
.brand-tag {
    font-size: 0.68rem; color: var(--text-muted);
    letter-spacing: 0.12em; text-transform: uppercase; margin-top: -3px;
}
.topbar-badge {
    font-size: 0.71rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--green); border: 1px solid rgba(61,220,151,0.25);
    padding: 0.28rem 0.85rem; border-radius: 20px;
    background: rgba(61,220,151,0.06);
}

/* ── Hero image banner ── */
.hero-banner {
    position: relative; width: 100%; overflow: hidden;
    border-radius: 0 0 24px 24px;
    margin-bottom: 2.8rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.hero-img {
    width: 100%; height: 340px;
    object-fit: cover; object-position: center 40%;
    display: block;
    filter: brightness(0.42) saturate(0.65);
}
.hero-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(
        to bottom,
        rgba(14,21,18,0.05) 0%,
        rgba(14,21,18,0.25) 40%,
        rgba(14,21,18,0.93) 100%
    );
    display: flex; flex-direction: column;
    align-items: center; justify-content: flex-end;
    padding: 2.5rem 2rem;
    text-align: center;
}
.hero-eyebrow {
    font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--green); margin-bottom: 0.65rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.hero-eyebrow::before, .hero-eyebrow::after {
    content:''; flex: 0 0 36px; height:1px; background: rgba(61,220,151,0.35);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem); font-weight: 700; line-height: 1.2;
    background: linear-gradient(135deg, #ffffff 30%, var(--gold-pale) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.7rem;
}
.hero-sub {
    font-size: 0.9rem; color: #a0b8a8; max-width: 520px; line-height: 1.65; margin-bottom: 1.3rem;
}
.stat-row { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; }
.stat-chip {
    background: rgba(255,255,255,0.06); backdrop-filter: blur(8px);
    border: 1px solid rgba(61,220,151,0.18);
    border-radius: 10px; padding: 0.5rem 1rem; text-align: center;
}
.stat-chip .num { font-family:'DM Mono',monospace; font-size:1rem; color:var(--gold-light); font-weight:500; }
.stat-chip .lbl { font-size:0.63rem; color:#7a9486; text-transform:uppercase; letter-spacing:0.1em; }

/* ── Section label ── */
.section-label {
    font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--green); margin-bottom: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.section-label::after { content:''; flex:1; height:1px; background: var(--border); }

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 1.4rem 1.5rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.02);
    transition: border-color 0.3s;
}
.card:hover { border-color: rgba(61,220,151,0.28); }
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem; color: var(--gold-light);
    margin-bottom: 0.9rem; padding-bottom: 0.7rem;
    border-bottom: 1px solid var(--border);
}

/* ── Inputs ── */
div[data-baseweb="input"] input,
div[data-baseweb="select"] div {
    background: var(--bg-light) !important;
    border: 1px solid rgba(61,220,151,0.18) !important;
    border-radius: 8px !important;
    color: var(--text-main) !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="input"] input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px rgba(61,220,151,0.1) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important; letter-spacing: 0.06em !important;
    text-transform: uppercase !important; font-weight: 500 !important;
}
[data-baseweb="select"] * { color: var(--text-main) !important; }
[data-baseweb="menu"] * { background: var(--bg-light) !important; }

/* ── Ratio box ── */
.ratio-box {
    background: linear-gradient(135deg, rgba(61,220,151,0.06), rgba(201,168,76,0.04));
    border: 1px solid var(--border); border-radius: 10px;
    padding: 0.85rem 1rem; text-align: center;
}
.ratio-label { font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); margin-bottom:0.35rem; }
.ratio-value { font-family:'DM Mono',monospace; font-size:1.45rem; font-weight:500; }

/* ── Button ── */
div.stButton > button {
    width: 100%; padding: 0.85rem 2rem;
    background: linear-gradient(135deg, var(--green-dim) 0%, #1d9966 100%) !important;
    color: #071008 !important; font-weight: 700 !important;
    font-size: 0.95rem !important; letter-spacing: 0.06em !important;
    border: none !important; border-radius: 10px !important;
    box-shadow: 0 6px 24px rgba(61,220,151,0.25) !important;
    cursor: pointer !important; transition: all 0.25s !important;
    font-family: 'DM Sans', sans-serif !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(61,220,151,0.4) !important;
}

/* ── Result panel ── */
.result-panel {
    background: linear-gradient(145deg, #111a16 0%, #141f1a 100%);
    border: 1px solid var(--border); border-radius: 20px; padding: 1.8rem;
    box-shadow: 0 0 60px rgba(61,220,151,0.05), inset 0 1px 0 rgba(255,255,255,0.03);
}
.result-header {
    font-family: 'Playfair Display', serif;
    font-size: 1rem; color: var(--gold-light);
    margin-bottom: 1.3rem; padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border);
}
.score-number {
    font-family: 'Playfair Display', serif;
    font-size: 4rem; font-weight: 700; line-height: 1;
    background: linear-gradient(135deg, #fff 0%, var(--gold-pale) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.score-label { font-size:0.68rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--text-muted); margin-top:0.3rem; }
.score-bar-track {
    height: 10px; background: rgba(255,255,255,0.05);
    border-radius: 99px; margin: 1.1rem 0 0.45rem; overflow: hidden;
}
.score-bar-fill { height: 100%; border-radius: 99px; }
.rating-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.38rem 1.05rem; border-radius: 24px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; margin-top: 0.7rem;
}
.rating-poor     { background:rgba(224,92,92,0.14);  color:#e05c5c; border:1px solid rgba(224,92,92,0.3); }
.rating-average  { background:rgba(230,162,60,0.14); color:#e6a23c; border:1px solid rgba(230,162,60,0.3); }
.rating-good     { background:rgba(61,220,151,0.12); color:#3ddc97; border:1px solid rgba(61,220,151,0.3); }
.rating-excellent{ background:rgba(201,168,76,0.14); color:var(--gold-light); border:1px solid var(--border-gold); }

.metric-row {
    display:flex; align-items:center; justify-content:space-between;
    padding:0.65rem 0; border-bottom:1px solid rgba(255,255,255,0.04);
}
.metric-row:last-child { border-bottom: none; }
.metric-key { font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; }
.metric-val { font-family:'DM Mono',monospace; font-size:0.9rem; color:var(--text-main); font-weight:500; }
.risk-pill {
    display:inline-flex; align-items:center; gap:0.4rem;
    font-family:'DM Mono',monospace; font-size:0.9rem; font-weight:600;
    padding:0.38rem 1rem; border-radius:8px;
}
.risk-low  { background:rgba(61,220,151,0.1);  color:#3ddc97; border:1px solid rgba(61,220,151,0.3); }
.risk-med  { background:rgba(230,162,60,0.1);  color:#e6a23c; border:1px solid rgba(230,162,60,0.3); }
.risk-high { background:rgba(224,92,92,0.1);   color:#e05c5c; border:1px solid rgba(224,92,92,0.3); }

.fancy-divider {
    height:1px; margin:1.3rem 0;
    background: linear-gradient(90deg, transparent 0%, var(--border) 30%, var(--border) 70%, transparent 100%);
}
.disclaimer {
    background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05);
    border-radius:9px; padding:0.8rem 1rem; margin-top:1.3rem;
}
.disclaimer p { font-size:0.69rem; color:var(--text-muted); line-height:1.55; margin:0; }

.footer {
    text-align:center; padding:2rem 0 0.5rem;
    border-top:1px solid var(--border); margin-top:3rem;
}
.footer p { font-size:0.7rem; color:var(--text-muted); margin:0; letter-spacing:0.05em; }
</style>
""", unsafe_allow_html=True)

# ── Top Navigation Bar ───────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-logo">
    <div class="logo-icon">LF</div>
    <div>
      <div class="brand-name">Lauki Finance</div>
      <div class="brand-tag">Credit Intelligence Platform</div>
    </div>
  </div>
  <div class="topbar-badge">⬤ &nbsp;Live Model v2.4</div>
</div>
""", unsafe_allow_html=True)

# ── Hero Banner with Image ───────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  {HERO_HTML}
  <div class="hero-overlay">
    <div class="hero-eyebrow">AI-Powered Credit Assessment</div>
    <div class="hero-title">Credit Risk Intelligence Engine</div>
    <p class="hero-sub">
      Institutional-grade credit scoring powered by machine learning.<br>
      Assess borrower risk in real-time with predictive accuracy.
    </p>
    <div class="stat-row">
      <div class="stat-chip"><div class="num">98.2%</div><div class="lbl">Model Accuracy</div></div>
      <div class="stat-chip"><div class="num">300–900</div><div class="lbl">Score Range</div></div>
      <div class="stat-chip"><div class="num">&lt;200ms</div><div class="lbl">Response Time</div></div>
      <div class="stat-chip"><div class="num">4 Tiers</div><div class="lbl">Risk Bands</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Form Layout ──────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:

    # ① Applicant Profile
    st.markdown('<div class="section-label">① Applicant Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">👤 Personal & Financial Details</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input('Age', min_value=18, max_value=100, step=1, value=28)
    with c2:
        income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=10000)
    with c3:
        loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=10000)

    lti = loan_amount / income if income > 0 else 0
    lti_color = "#e05c5c" if lti > 5 else ("#e6a23c" if lti > 3 else "#3ddc97")

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(f"""
        <div class="ratio-box">
          <div class="ratio-label">Loan-to-Income Ratio</div>
          <div class="ratio-value" style="color:{lti_color}">{lti:.2f}×</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=1, step=1, value=36)
    with c6:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1.1rem"></div>', unsafe_allow_html=True)

    # ② Loan Configuration
    st.markdown('<div class="section-label">② Loan Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">📋 Loan Parameters</div>', unsafe_allow_html=True)

    c7, c8 = st.columns(2)
    with c7:
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
    with c8:
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1.1rem"></div>', unsafe_allow_html=True)

    # ③ Credit Behaviour
    st.markdown('<div class="section-label">③ Credit Behaviour</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">📊 Credit & Delinquency Metrics</div>', unsafe_allow_html=True)

    c9, c10 = st.columns(2)
    with c9:
        delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
        credit_utilization_ratio = st.number_input('Credit Utilization (%)', min_value=0, max_value=100, step=1, value=30)
    with c10:
        avg_dpd_per_delinquency = st.number_input('Avg Days Past Due (DPD)', min_value=0, value=20)
        num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1.4rem"></div>', unsafe_allow_html=True)

    calculate = st.button('⚡  Run Credit Assessment', use_container_width=True)


# ── Results ──────────────────────────────────────────────────────────────────
with right_col:
    st.markdown('<div class="section-label">④ Assessment Result</div>', unsafe_allow_html=True)

    if calculate:
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )

        score_pct = ((credit_score - 300) / 600) * 100

        if credit_score < 500:
            bar_colour = "linear-gradient(90deg,#e05c5c,#c94a4a)"
        elif credit_score < 650:
            bar_colour = "linear-gradient(90deg,#e6a23c,#c98a2a)"
        elif credit_score < 750:
            bar_colour = "linear-gradient(90deg,#3ddc97,#2ab87c)"
        else:
            bar_colour = "linear-gradient(90deg,var(--gold),var(--gold-light))"

        rating_class = {'Poor':'rating-poor','Average':'rating-average','Good':'rating-good','Excellent':'rating-excellent'}.get(rating,'rating-average')
        rating_icon  = {'Poor':'⚠️','Average':'📊','Good':'✅','Excellent':'🏆'}.get(rating,'📊')

        if probability < 0.2:
            risk_label, risk_class = "Low Risk", "risk-low"
        elif probability < 0.5:
            risk_label, risk_class = "Medium Risk", "risk-med"
        else:
            risk_label, risk_class = "High Risk", "risk-high"

        st.markdown(f"""
        <div class="result-panel">
          <div class="result-header">📈 Credit Assessment Report</div>

          <div style="text-align:center;padding:0.5rem 0 1rem">
            <div class="score-number">{credit_score}</div>
            <div class="score-label">Credit Score</div>
            <div class="score-bar-track">
              <div class="score-bar-fill" style="width:{score_pct:.1f}%;background:{bar_colour}"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.62rem;color:var(--text-muted);margin-bottom:0.5rem">
              <span>300</span><span>Poor</span><span>Average</span><span>Good</span><span>900</span>
            </div>
            <span class="rating-badge {rating_class}">{rating_icon} {rating}</span>
          </div>

          <div class="fancy-divider"></div>

          <div class="metric-row">
            <span class="metric-key">Default Probability</span>
            <span class="metric-val">{probability:.2%}</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Risk Classification</span>
            <span class="risk-pill {risk_class}">{risk_label}</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Loan-to-Income</span>
            <span class="metric-val">{lti:.2f}×</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Delinquency Ratio</span>
            <span class="metric-val">{delinquency_ratio}%</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Credit Utilization</span>
            <span class="metric-val">{credit_utilization_ratio}%</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Avg DPD</span>
            <span class="metric-val">{avg_dpd_per_delinquency} days</span>
          </div>

          <div class="disclaimer">
            <p>⚠️ This assessment is generated by a machine learning model for informational
            purposes only. Final credit decisions should incorporate additional due diligence
            and comply with applicable lending regulations.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-panel" style="min-height:500px;display:flex;flex-direction:column;
             align-items:center;justify-content:center;text-align:center">
          <div style="font-size:2.8rem;margin-bottom:1rem;opacity:0.25">📊</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.05rem;
               color:var(--text-muted);margin-bottom:0.6rem">
            Awaiting Assessment
          </div>
          <p style="font-size:0.76rem;color:var(--text-muted);max-width:230px;line-height:1.6;margin:0">
            Fill in the applicant details and click
            <strong style="color:var(--green)">Run Credit Assessment</strong>
          </p>
          <div style="margin-top:2rem;display:flex;gap:0.75rem;flex-wrap:wrap;justify-content:center">
            <div class="stat-chip"><div class="num" style="font-size:0.8rem">300–499</div><div class="lbl">Poor</div></div>
            <div class="stat-chip"><div class="num" style="font-size:0.8rem">500–649</div><div class="lbl">Average</div></div>
            <div class="stat-chip"><div class="num" style="font-size:0.8rem">650–749</div><div class="lbl">Good</div></div>
            <div class="stat-chip"><div class="num" style="font-size:0.8rem">750–900</div><div class="lbl">Excellent</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <p>© 2026 Lauki Finance · Credit Intelligence Platform &nbsp;·&nbsp;
     Powered by ML Risk Engine &nbsp;·&nbsp; All assessments are indicative only</p>
</div>
""", unsafe_allow_html=True)
