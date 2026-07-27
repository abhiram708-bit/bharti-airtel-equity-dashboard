import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import io
import base64
from datetime import datetime

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Bharti Airtel Equity Reserach & Financial Intelligence Dashboard 2026",
    page_icon="📶",
    layout="wide"
)

# ── STYLING ──────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp { background-color: #f4f6f9; }

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    background-color: #f4f6f9;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #dde1e7;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 6px;
    padding: 14px 18px;
}

[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #111827 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

button[data-baseweb="tab"] {
    font-size: 13px;
    font-weight: 500;
    color: #6b7280 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #e40000 !important;
    border-bottom: 2px solid #e40000 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #dde1e7;
    border-radius: 6px;
    overflow: hidden;
}

div[data-testid="stAlert"] {
    background-color: #ffffff !important;
    border: 1px solid #dde1e7 !important;
    border-radius: 6px !important;
    color: #374151 !important;
}

h1 { font-size: 22px !important; font-weight: 600 !important; color: #111827 !important; }
h2 { font-size: 17px !important; font-weight: 600 !important; color: #111827 !important; }
h3 { font-size: 15px !important; font-weight: 500 !important; color: #374151 !important; }

/* ── custom components ── */

.page-header {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-left: 4px solid #e40000;
    border-radius: 6px;
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.page-header .company-name {
    font-size: 20px;
    font-weight: 600;
    color: #111827;
    margin: 0;
}

.page-header .company-meta {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 2px;
}

.page-header .price-block {
    text-align: right;
}

.page-header .price-main {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: #111827;
}

.page-header .price-chg-pos {
    font-size: 13px;
    color: #16a34a;
    font-weight: 500;
}

.page-header .price-chg-neg {
    font-size: 13px;
    color: #dc2626;
    font-weight: 500;
}

.price-meta-row {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 2px;
}

.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 6px;
    margin-bottom: 14px;
    margin-top: 4px;
}

.info-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 6px;
    padding: 16px 18px;
    height: 100%;
}

.info-card .card-title {
    font-size: 11px;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
    border-bottom: 1px solid #f3f4f6;
    padding-bottom: 8px;
}

.info-card ul {
    margin: 0; padding: 0; list-style: none;
}

.info-card li {
    font-size: 13px;
    color: #374151;
    padding: 5px 0;
    border-bottom: 1px solid #f3f4f6;
    display: flex;
    justify-content: space-between;
}

.info-card li:last-child { border-bottom: none; }

.info-card li .val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    color: #111827;
}

.ratio-grid {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 20px;
}

.ratio-item {
    display: inline-block;
    width: 155px;
    border: 1px solid #e5e7eb;
    border-radius: 5px;
    padding: 10px 14px;
    margin: 5px;
    background: #fafafa;
    vertical-align: top;
}

.ratio-item .ri-label {
    font-size: 10px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 4px;
}

.ratio-item .ri-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 600;
    color: #111827;
}

.tailwind-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 3px solid #16a34a;
    border-radius: 6px;
    padding: 16px 20px;
}

.tailwind-box h4 { font-size: 13px; font-weight: 600; color: #15803d; margin: 0 0 10px 0; }
.tailwind-box li { font-size: 13px; color: #166534; padding: 3px 0; }

.risk-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-left: 3px solid #ea580c;
    border-radius: 6px;
    padding: 16px 20px;
}

.risk-box h4 { font-size: 13px; font-weight: 600; color: #c2410c; margin: 0 0 10px 0; }
.risk-box li { font-size: 13px; color: #9a3412; padding: 3px 0; }

.footer-bar {
    text-align: center;
    font-size: 11px;
    color: #9ca3af;
    padding: 20px 0 8px;
    border-top: 1px solid #e5e7eb;
    margin-top: 10px;
}

/* ── UPGRADE: Premium IB-grade styles ── */

.exec-thesis-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-left: 4px solid #e40000;
    border-radius: 8px;
    padding: 20px 24px;
    color: #1e293b;
    margin-bottom: 16px;
}
.exec-thesis-card h3 { color: #111827 !important; font-size: 14px !important; font-weight: 700 !important; margin-bottom: 14px; letter-spacing: 0.5px; text-transform: uppercase; }
.exec-thesis-card li { font-size: 13px; color: #374151; padding: 5px 0; border-bottom: 1px solid #f3f4f6; line-height: 1.6; }
.exec-thesis-card li:last-child { border-bottom: none; }
.exec-thesis-card li::before { content: "▸ "; color: #e40000; font-size: 11px; }

.score-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 8px;
    padding: 18px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.score-card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #e40000, #f97316);
}
.score-card .sc-label { font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.score-card .sc-value { font-family: 'IBM Plex Mono', monospace; font-size: 32px; font-weight: 700; color: #111827; }
.score-card .sc-sub { font-size: 11px; color: #6b7280; margin-top: 4px; }

.rec-card-buy {
    background: linear-gradient(135deg, #052e16 0%, #14532d 100%);
    border: 1px solid #16a34a;
    border-radius: 8px;
    padding: 20px 24px;
    text-align: center;
}
.rec-card-buy .rec-label { font-size: 11px; font-weight: 600; color: #86efac; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.rec-card-buy .rec-verdict { font-size: 42px; font-weight: 700; color: #4ade80; letter-spacing: 2px; margin: 4px 0; }
.rec-card-buy .rec-conf { font-size: 14px; color: #86efac; font-weight: 500; margin-bottom: 8px; }
.rec-card-buy .rec-rationale { font-size: 12px; color: #a7f3d0; line-height: 1.7; }

.ai-insight-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-left: 3px solid #1d4ed8;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.ai-insight-card .ai-icon { font-size: 14px; margin-right: 6px; }
.ai-insight-card .ai-text { font-size: 13px; color: #1e3a5f; line-height: 1.6; }
.ai-insight-card .ai-tag { font-size: 10px; font-weight: 600; color: #1d4ed8; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 4px; padding: 1px 6px; display: inline-block; margin-bottom: 4px; }

.swot-card-s { background: #f0fdf4; border: 1px solid #86efac; border-top: 3px solid #16a34a; border-radius: 8px; padding: 18px; }
.swot-card-w { background: #fff7ed; border: 1px solid #fed7aa; border-top: 3px solid #ea580c; border-radius: 8px; padding: 18px; }
.swot-card-o { background: #eff6ff; border: 1px solid #bfdbfe; border-top: 3px solid #1d4ed8; border-radius: 8px; padding: 18px; }
.swot-card-t { background: #fef2f2; border: 1px solid #fecaca; border-top: 3px solid #dc2626; border-radius: 8px; padding: 18px; }
.swot-card-s h4, .swot-card-o h4 { font-size: 12px; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
.swot-card-w h4, .swot-card-t h4 { font-size: 12px; font-weight: 700; color: #9a3412; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
.swot-card-o h4 { color: #1e40af; }
.swot-card-t h4 { color: #991b1b; }
.swot-card-s li, .swot-card-o li { font-size: 12px; color: #166534; padding: 3px 0; }
.swot-card-o li { color: #1e40af; }
.swot-card-w li { font-size: 12px; color: #9a3412; padding: 3px 0; }
.swot-card-t li { font-size: 12px; color: #991b1b; padding: 3px 0; }

.action-card-opp { background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 18px; }
.action-card-risk { background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 18px; }
.action-card-mgmt { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 18px; }
.action-card-opp h4 { font-size: 12px; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
.action-card-risk h4 { font-size: 12px; font-weight: 700; color: #991b1b; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
.action-card-mgmt h4 { font-size: 12px; font-weight: 700; color: #1e40af; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
.action-card-opp li { font-size: 12px; color: #166534; padding: 3px 0; }
.action-card-risk li { font-size: 12px; color: #991b1b; padding: 3px 0; }
.action-card-mgmt li { font-size: 12px; color: #1e40af; padding: 3px 0; }

.rank-row { display: flex; align-items: center; padding: 10px 14px; border-bottom: 1px solid #f3f4f6; background: #fff; }
.rank-row:first-child { border-radius: 6px 6px 0 0; }
.rank-row:last-child { border-bottom: none; border-radius: 0 0 6px 6px; }
.rank-badge { width: 28px; height: 28px; border-radius: 50%; background: #e40000; color: white; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-right: 12px; flex-shrink: 0; }
.rank-badge.r2 { background: #6b7280; }
.rank-badge.r3 { background: #9ca3af; }
.rank-company { font-size: 13px; font-weight: 600; color: #111827; flex: 1; }
.rank-val { font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; color: #111827; margin-right: 12px; }
.rank-pct { font-size: 11px; color: #6b7280; }

.kpi-trend-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 6px;
    padding: 14px 16px;
}
.kpi-trend-card .kt-label { font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.7px; }
.kpi-trend-card .kt-value { font-family: 'IBM Plex Mono', monospace; font-size: 20px; font-weight: 700; color: #111827; margin: 4px 0; }
.kpi-trend-card .kt-delta-pos { font-size: 12px; color: #16a34a; font-weight: 500; }
.kpi-trend-card .kt-delta-neg { font-size: 12px; color: #dc2626; font-weight: 500; }

.valuation-card {
    background: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 6px;
    padding: 16px 20px;
    text-align: center;
}
.valuation-card .vc-label { font-size: 11px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.7px; }
.valuation-card .vc-value { font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 700; color: #111827; margin-top: 6px; }
.valuation-card .vc-sub { font-size: 11px; color: #6b7280; margin-top: 4px; }

.conclusion-undervalued { background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a; border-radius: 6px; padding: 16px 20px; }
.conclusion-fair { background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; border-radius: 6px; padding: 16px 20px; }
.conclusion-overvalued { background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; border-radius: 6px; padding: 16px 20px; }

.scenario-bear { background: #fef2f2; }
.scenario-base { background: #f0fdf4; }
.scenario-bull { background: #eff6ff; }

.nav-link { display: block; padding: 8px 14px; font-size: 12px; font-weight: 500; color: #374151; border-radius: 5px; text-decoration: none; margin-bottom: 2px; }
.nav-link:hover { background: #f3f4f6; color: #e40000; }

.sidebar-fact-row { display: flex; justify-content: space-between; font-size: 12px; padding: 5px 0; border-bottom: 1px solid #f3f4f6; }
.sidebar-fact-row .sf-label { color: #9ca3af; }
.sidebar-fact-row .sf-val { font-family: 'IBM Plex Mono', monospace; color: #111827; font-weight: 500; font-size: 11px; }

</style>
""", unsafe_allow_html=True)


# ── SIDEBAR: DARK MODE TOGGLE ────────────────────────────────────────────────

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

# ── SIDEBAR: QUICK NAVIGATION & COMPANY FACTS ────────────────────────────────

st.sidebar.markdown("---")
st.sidebar.markdown('<p style="font-size:11px;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;">⚡ Quick Navigation</p>', unsafe_allow_html=True)
nav_sections = {
    "🏛 Executive Summary": "exec_summary",
    "📈 Stock Performance": "stock_perf",
    "📊 Quarterly Results": "quarterly",
    "🔍 Peer Comparison": "peer_comp",
    "🔮 Forecasting & Valuation": "forecasting",
    "🧠 Strategic Outlook": "strategic",
}
for label, _ in nav_sections.items():
    st.sidebar.markdown(f'<div class="nav-link">{label}</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown('<p style="font-size:11px;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;">🏢 Company Quick Facts</p>', unsafe_allow_html=True)
quick_facts = [
    ("Founded", "1995"),
    ("Headquarters", "New Delhi"),
    ("CEO", "Gopal Vittal"),
    ("Chairman", "Sunil Mittal"),
    ("Employees", "~21,000"),
    ("Countries", "15"),
    ("Listed", "NSE / BSE"),
    ("Index", "Nifty 50"),
    ("Sector", "Telecom"),
    ("FY End", "March"),
]
for label, val in quick_facts:
    st.sidebar.markdown(f'<div class="sidebar-fact-row"><span class="sf-label">{label}</span><span class="sf-val">{val}</span></div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown('<p style="font-size:10px;color:#9ca3af;text-align:center;margin-top:8px;">Bharti Airtel · Equity Research Terminal<br>May 2026 · Not Investment Advice</p>', unsafe_allow_html=True)


if dark_mode:
    st.markdown("""
<style>
.stApp { background-color: #0f1117; color: #f9fafb; }
.main .block-container { background-color: #0f1117; }
section[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3148; }
[data-testid="stMetric"] { background: #1e2130; border: 1px solid #2d3148; }
.page-header { background: #1e2130; border-color: #2d3148; }
</style>
""", unsafe_allow_html=True)


# ── LIVE DATA ─────────────────────────────────────────────────────────────────

ticker = yf.Ticker("BHARTIARTL.NS")

try:
    info = ticker.info
    current_price  = info.get("currentPrice", 1885)
    market_cap     = round(info.get("marketCap", 0) / 10000000, 2)
    pe_ratio       = info.get("trailingPE", 40)
    dividend_yield = info.get("dividendYield", 0.0085)
    fifty_two_high = info.get("fiftyTwoWeekHigh", 2175)
    fifty_two_low  = info.get("fiftyTwoWeekLow", 1740)
    prev_close     = info.get("previousClose", 1904.9)
    open_price     = info.get("open", 1911)
    day_high       = info.get("dayHigh", 1915)
    day_low        = info.get("dayLow", 1880)
except Exception:
    current_price  = 1885
    market_cap     = 1148524
    pe_ratio       = 40.0
    dividend_yield = 0.0085
    fifty_two_high = 2175
    fifty_two_low  = 1740
    prev_close     = 1904.9
    open_price     = 1911
    day_high       = 1915
    day_low        = 1880

price_change     = round(current_price - prev_close, 2)
price_change_pct = round((price_change / prev_close) * 100, 2)
chg_class        = "price-chg-pos" if price_change >= 0 else "price-chg-neg"
chg_arrow        = "▲" if price_change >= 0 else "▼"


# ── HEADER ────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="page-header">
    <div>
        <p class="company-name">Bharti Airtel Limited</p>
        <p class="company-meta">NSE: BHARTIARTL &nbsp;|&nbsp; BSE: 532454 &nbsp;|&nbsp; Telecom – Cellular & Fixed Line &nbsp;|&nbsp; FY 2025-26</p>
    </div>
    <div class="price-block">
        <div class="price-main">₹{current_price:,.2f}</div>
        <div class="{chg_class}">{chg_arrow} ₹{abs(price_change)} ({abs(price_change_pct)}%)</div>
        <div class="price-meta-row">Prev Close ₹{prev_close:,.2f} &nbsp;|&nbsp; Live NSE Price &nbsp;|&nbsp; May 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── INTRADAY SNAPSHOT ─────────────────────────────────────────────────────────

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
m1.metric("Current Price",  f"₹{current_price:,.0f}")
m2.metric("Day Open",       f"₹{open_price:,.0f}")
m3.metric("Day High",       f"₹{day_high:,.0f}")
m4.metric("Day Low",        f"₹{day_low:,.0f}")
m5.metric("52W High",       f"₹{fifty_two_high:,.0f}")
m6.metric("52W Low",        f"₹{fifty_two_low:,.0f}")
m7.metric("Mkt Cap",        f"₹{market_cap:,.0f} Cr")

st.markdown("<br>", unsafe_allow_html=True)


# ── BUSINESS SNAPSHOT ─────────────────────────────────────────────────────────

st.markdown('<p class="section-title">Business Snapshot — FY 2025</p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Revenue",       "₹2,10,973 Cr", "+22% YoY")
k2.metric("EBITDA Margin", "57.8%",         "+500 bps")
k3.metric("Net Profit",    "₹33,823 Cr",    "+18% YoY")
k4.metric("ARPU",          "₹257",          "+15% YoY")
k5.metric("Subscribers",   "666 M+",        "+4% YoY")

st.markdown("<br>", unsafe_allow_html=True)


# ── CASH FLOW STATEMENT ───────────────────────────────────────────────────────

st.markdown('<p class="section-title">Cash Flow Statement — FY 2025</p>', unsafe_allow_html=True)

cf1, cf2, cf3 = st.columns(3)
cf1.metric("CFO (Cash from Operations)", "₹1,04,240 Cr", "+19% YoY")
cf2.metric("Capex",                       "₹63,800 Cr",   "-5% YoY")
cf3.metric("Free Cash Flow (FCF)",        "₹40,440 Cr",   "+68% YoY")

st.markdown("<br>", unsafe_allow_html=True)


# ── PILLAR CARDS ──────────────────────────────────────────────────────────────

st.markdown('<p class="section-title">Operational Overview</p>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown("""
    <div class="info-card">
        <div class="card-title">Revenue & Margins</div>
        <ul>
            <li>Revenue <span class="val">₹2,10,973 Cr</span></li>
            <li>Revenue Growth <span class="val">+22%</span></li>
            <li>EBITDA Margin <span class="val">57.8%</span></li>
            <li>EBIT <span class="val">₹70,146 Cr</span></li>
            <li>Operating Profit <span class="val">₹1,19,674 Cr</span></li>
        </ul>
    </div>""", unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="info-card">
        <div class="card-title">Operational KPIs</div>
        <ul>
            <li>ARPU <span class="val">₹257</span></li>
            <li>OPM <span class="val">56.7%</span></li>
            <li>Data / User <span class="val">31.4 GB</span></li>
            <li>Postpaid Base <span class="val">29 M+</span></li>
            <li>India Subscribers <span class="val">380 M+</span></li>
        </ul>
    </div>""", unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="info-card">
        <div class="card-title">Digital & Adjacencies</div>
        <ul>
            <li>Nxtra Expansion <span class="val">$1 B</span></li>
            <li>Payments Bank <span class="val">120 M users</span></li>
            <li>AI & Cloud DCs <span class="val">Active</span></li>
            <li>Airtel Black <span class="val">Premium</span></li>
            <li>Africa – Airtel Money <span class="val">Scaling</span></li>
        </ul>
    </div>""", unsafe_allow_html=True)

with p4:
    st.markdown("""
    <div class="info-card">
        <div class="card-title">Market Footprint</div>
        <ul>
            <li>Countries <span class="val">15</span></li>
            <li>5G Cities <span class="val">5,000+</span></li>
            <li>Fiber Homes <span class="val">10 M+</span></li>
            <li>Enterprise Clients <span class="val">2,500+</span></li>
            <li>Spectrum <span class="val">Industry #1</span></li>
        </ul>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── FINANCIAL RATIOS ──────────────────────────────────────────────────────────

st.markdown('<p class="section-title">Key Financial Ratios — FY 2025-26</p>', unsafe_allow_html=True)

st.markdown("""
<div class="ratio-grid">
<div class="ratio-item"><div class="ri-label">Stock P/E</div><div class="ri-val">40.0x</div></div>
<div class="ratio-item"><div class="ri-label">P/B Ratio</div><div class="ri-val">7.7x</div></div>
<div class="ratio-item"><div class="ri-label">EV / EBITDA</div><div class="ri-val">14.2x</div></div>
<div class="ratio-item"><div class="ri-label">ROCE</div><div class="ri-val">18.5%</div></div>
<div class="ratio-item"><div class="ri-label">ROE</div><div class="ri-val">21.9%</div></div>
<div class="ratio-item"><div class="ri-label">ROA</div><div class="ri-val">6.88%</div></div>
<div class="ratio-item"><div class="ri-label">OPM</div><div class="ri-val">56.7%</div></div>
<div class="ratio-item"><div class="ri-label">Net Margin</div><div class="ri-val">13.6%</div></div>
<div class="ratio-item"><div class="ri-label">EPS (TTM)</div><div class="ri-val">₹43.8</div></div>
<div class="ratio-item"><div class="ri-label">Book Value</div><div class="ri-val">₹245</div></div>
<div class="ratio-item"><div class="ri-label">Debt / Equity</div><div class="ri-val">1.31</div></div>
<div class="ratio-item"><div class="ri-label">Net Debt/EBITDA</div><div class="ri-val">1.1x</div></div>
<div class="ratio-item"><div class="ri-label">Current Ratio</div><div class="ri-val">0.52</div></div>
<div class="ratio-item"><div class="ri-label">Int. Coverage</div><div class="ri-val">3.25x</div></div>
<div class="ratio-item"><div class="ri-label">Earnings Yield</div><div class="ri-val">5.34%</div></div>
<div class="ratio-item"><div class="ri-label">Dividend Yield</div><div class="ri-val">0.85%</div></div>
<div class="ratio-item"><div class="ri-label">5Y Profit CAGR</div><div class="ri-val">24%</div></div>
<div class="ratio-item"><div class="ri-label">5Y Revenue CAGR</div><div class="ri-val">16%</div></div>
</div>
""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Stock Performance",
    "Quarterly Results",
    "Peer Comparison",
    "Reports & Links",
    "Strategic Outlook"
])

# ── NEW TABS ──────────────────────────────────────────────────────────────────
tab_exec, tab_forecast = st.tabs([
    "🏛 Executive Summary",
    "🔮 Forecasting & Valuation"
])

# shared chart layout (light theme)
CL = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(color="#374151", family="IBM Plex Sans", size=11),
    xaxis=dict(showgrid=False, color="#9ca3af", linecolor="#e5e7eb", tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af", linecolor="#e5e7eb"),
    margin=dict(l=10, r=10, t=36, b=10),
    height=320
)


# ── TAB 1 ──────────────────────────────────────────

with tab1:
    try:
        hist = yf.download("BHARTIARTL.NS", start="2005-01-01", progress=False)
        all_time_high = float(hist["Close"].max())

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            mode="lines", name="Share Price",
            line=dict(color="#e40000", width=1.4),
            fill="tozeroy", fillcolor="rgba(228,0,0,0.05)"
        ))
        fig.update_layout(
            height=420,
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(color="#374151", family="IBM Plex Sans"),
            xaxis=dict(showgrid=False, color="#9ca3af", linecolor="#e5e7eb"),
            yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af",
                       title="Price (₹)", titlefont=dict(color="#9ca3af")),
            margin=dict(l=10, r=10, t=10, b=10),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric("All-Time High", f"₹{all_time_high:,.2f}")
    except Exception:
        pass


# ── TAB 2 ──────────────────────────────────────────

with tab2:
    quarterly_df = pd.DataFrame({
        "Quarter": [
            "Mar-23","Jun-23","Sep-23","Dec-23",
            "Mar-24","Jun-24","Sep-24","Dec-24",
            "Mar-25","Jun-25","Sep-25","Dec-25","Mar-26"
        ],
        "Sales": [
            36009,37440,37044,37900,
            37599,38506,41473,45129,
            47876,49463,52145,53982,55383
        ],
        "Expenses": [
            17312,17842,17530,18085,
            18234,18799,19627,20533,
            20867,21624,22584,23199,23892
        ],
        "Operating Profit": [
            18697,19598,19514,19815,
            19365,19708,21846,24597,
            27009,27839,29561,30783,31492
        ],
        "OPM %": [52,52,53,52,52,51,53,54,56,56,57,57,57],
        "Net Profit": [
            4226,1520,2093,2876,
            2068,4718,4153,16135,
            12476,7422,8651,8503,9247
        ],
        "EPS": [5.39,2.89,2.39,4.34,3.66,7.31,6.31,25.95,19.33,10.43,11.91,11.63,12.02]
    })

    st.markdown('<p class="section-title" style="margin-top:16px">Quarterly Financial Results</p>', unsafe_allow_html=True)
    st.dataframe(quarterly_df, use_container_width=True, hide_index=True)
    st.info("📌 Dec-24 net profit of ₹16,135 Cr includes a one-time exceptional gain from AGR/spectrum dues reassessment by DoT. Adjusted recurring PAT was approximately ₹4,200 Cr.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fs = px.line(quarterly_df, x="Quarter", y="Sales", markers=True,
                     title="Quarterly Sales (₹ Cr)")
        fs.update_traces(line_color="#1d4ed8", marker_color="#1d4ed8", marker_size=5)
        fs.update_layout(**CL)
        st.plotly_chart(fs, use_container_width=True)
    with c2:
        fp = px.line(quarterly_df, x="Quarter", y="Net Profit", markers=True,
                     title="Net Profit (₹ Cr)")
        fp.update_traces(line_color="#16a34a", marker_color="#16a34a", marker_size=5)
        fp.update_layout(**CL)
        st.plotly_chart(fp, use_container_width=True)

    fo = px.bar(quarterly_df, x="Quarter", y="OPM %", title="Operating Margin (%)")
    fo.update_traces(marker_color="#e40000", marker_opacity=0.8)
    opm_layout = {**CL, "height": 280}
    fo.update_layout(**opm_layout)
    st.plotly_chart(fo, use_container_width=True)


# ── TAB 3 ──────────────────────────────────────────

with tab3:
    peer_df = pd.DataFrame({
        "Company":       ["Bharti Airtel","Vodafone Idea","Bharti Hexacom","Tata Communications","Tata Tele. Mah.","MTNL"],
        "CMP (₹)":       [1885.30, 13.62, 1568.90, 1896.30, 42.18, 28.94],
        "P/E":           [40.0, "—", 44.61, 49.08, "—", "—"],
        "ROE %":         [21.86, -12.35, 26.86, 34.01, -66.49, -30.57],
        "ROCE %":        [18.50, -1.60, 21.82, 14.69, 55.65, -2.25],
        "Debt/Equity":   [1.31, "—", 0.86, 3.55, "—", "—"],
        "Mkt Cap (₹ Cr)":[1148524, 147563, 78469, 53987, 8250, 1823],
        "Sales (₹ Cr)":  [210973, 44873, 9354, 24803, 1160, 956]
    })

    st.markdown('<p class="section-title" style="margin-top:16px">Peer Comparison — Telecom Sector</p>', unsafe_allow_html=True)
    st.dataframe(peer_df, use_container_width=True, hide_index=True)
    st.markdown("<br>", unsafe_allow_html=True)

    numeric_peer = peer_df[peer_df["ROE %"].apply(lambda x: isinstance(x, (int, float)))].copy()
    PEER_COLORS = {
        "Bharti Airtel":      "#e40000",
        "Vodafone Idea":      "#d1d5db",
        "Bharti Hexacom":     "#f97316",
        "Tata Communications":"#6b7280",
        "Tata Tele. Mah.":   "#9ca3af",
        "MTNL":               "#e5e7eb"
    }

    c1, c2 = st.columns(2)
    with c1:
        fr = px.bar(numeric_peer, x="Company", y="ROE %",
                    title="ROE Comparison (%)", color="Company",
                    color_discrete_map=PEER_COLORS)
        fr.update_layout(**CL, showlegend=False)
        st.plotly_chart(fr, use_container_width=True)
    with c2:
        fc = px.bar(numeric_peer, x="Company", y="ROCE %",
                    title="ROCE Comparison (%)", color="Company",
                    color_discrete_map=PEER_COLORS)
        fc.update_layout(**CL, showlegend=False)
        st.plotly_chart(fc, use_container_width=True)

    mktcap_df = pd.DataFrame({
        "Company":    ["Bharti Airtel","Bharti Hexacom","Tata Comm","Vi","Tata Tele"],
        "ROE":        [21.86, 26.86, 34.01, -12.35, -66.49],
        "ROCE":       [18.50, 21.82, 14.69, -1.60,   55.65],
        "Market Cap": [1148524, 78469, 53987, 147563,   8250]
    })
    fb = px.scatter(mktcap_df, x="ROE", y="ROCE", size="Market Cap",
                    color="Company", hover_name="Company",
                    title="ROE vs ROCE — Bubble size = Market Cap",
                    size_max=55,
                    color_discrete_map={
                        "Bharti Airtel": "#e40000",
                        "Bharti Hexacom":"#f97316",
                        "Tata Comm":     "#6b7280",
                        "Vi":            "#d1d5db",
                        "Tata Tele":     "#9ca3af"
                    })
    bubble_layout = {**CL, "height": 360}
    bubble_layout["xaxis"] = dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af",
                                  title="ROE (%)", linecolor="#e5e7eb")
    bubble_layout["yaxis"] = dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af",
                                  title="ROCE (%)", linecolor="#e5e7eb")
    fb.update_layout(**bubble_layout,
                     legend=dict(bgcolor="#ffffff", bordercolor="#e5e7eb", borderwidth=1))
    st.plotly_chart(fb, use_container_width=True)


# ── TAB 4 ──────────────────────────────────────────

with tab4:
    st.markdown('<p class="section-title" style="margin-top:16px">Annual Reports & Filings</p>', unsafe_allow_html=True)
    st.link_button("FY 2025 Annual Report — BSE India",    "https://www.bseindia.com/stockinfo/AnnReport.html?scripcode=532454&scode=0")
    st.link_button("FY 2024 Annual Report — BSE India",    "https://www.bseindia.com/stockinfo/AnnReport.html?scripcode=532454&scode=0")
    st.link_button("Screener.in — Bharti Airtel",          "https://www.screener.in/company/BHARTIARTL/consolidated/")
    st.link_button("NSE India — BHARTIARTL",               "https://www.nseindia.com/get-quotes/equity?symbol=BHARTIARTL")
    st.link_button("Airtel Investor Relations",            "https://www.airtel.in/investor-relations")
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("All links direct to official exchange and company filings. For quarterly results visit NSE or BSE.")


# ── TAB 5 ──────────────────────────────────────────

with tab5:
    st.markdown('<p class="section-title" style="margin-top:16px">Strategic Outlook — FY 2026 & Beyond</p>', unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""
        <div class="tailwind-box">
            <h4>Key Tailwinds</h4>
            <ul>
                <li>Postpaid base crossed 29 million</li>
                <li>5G rollout across 5,000+ cities</li>
                <li>Broadband & fiber expansion — 10M homes</li>
                <li>Airtel Money scaling rapidly in Africa</li>
                <li>AI & Cloud data center monetization</li>
                <li>Enterprise & B2B services growing 30%+</li>
                <li>ARPU expected to cross ₹300 by FY27</li>
                <li>Nxtra data center $1B expansion</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="risk-box">
            <h4>Structural Risks</h4>
            <ul>
                <li>Regulatory intervention risk (TRAI)</li>
                <li>High spectrum & network capex cycle</li>
                <li>Competitive pricing pressure from Jio</li>
                <li>High interest cost due to leverage</li>
                <li>Currency risk in African operations</li>
                <li>Promoter holding declined over 3 years</li>
                <li>AGR dues & DoT regulatory overhang</li>
                <li>Capex intensity for 5G monetization</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Analyst Consensus — May 2026</p>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Analyst Rating",      "BUY",          "12 of 15 analysts")
    a2.metric("1Y Target Price",     "₹2,150",       "+14% upside")
    a3.metric("EPS Estimate FY27",   "₹52.0",        "+18% growth")
    a4.metric("Revenue Est. FY27",   "₹2,40,000 Cr", "+14% growth")


# ── SHAREHOLDING ──────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown('<p class="section-title">Shareholding Pattern — March 2026</p>', unsafe_allow_html=True)

shareholding_df = pd.DataFrame({
    "Category": ["Promoters", "FIIs", "DIIs", "Public"],
    "Holding %": [53.11, 20.60, 20.49, 5.80]
})

sh1, sh2 = st.columns([1, 1])

with sh1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=shareholding_df["Category"],
        values=shareholding_df["Holding %"],
        hole=0.45,
        marker=dict(colors=["#e40000", "#1d4ed8", "#16a34a", "#9ca3af"],
                    line=dict(color="#ffffff", width=2)),
        textfont=dict(size=12),
        hovertemplate="%{label}: %{value}%<extra></extra>"
    )])
    fig_pie.update_layout(
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        font=dict(color="#374151", family="IBM Plex Sans"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=260,
        showlegend=True,
        legend=dict(bgcolor="#ffffff", font=dict(color="#374151", size=12)),
        annotations=[dict(text="Equity", x=0.5, y=0.5,
                          font_size=13, font_color="#6b7280", showarrow=False)]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with sh2:
    st.dataframe(shareholding_df, use_container_width=True, hide_index=True)
    st.markdown("""
    <div style="margin-top:14px; padding:12px 16px; background:#f9fafb;
                border:1px solid #e5e7eb; border-radius:5px;
                font-size:13px; color:#6b7280; line-height:1.8;">
        <strong style="color:#374151">Note:</strong> Promoter (Sunil Mittal group) holds a majority stake of 53.11%.<br>
        FII interest remains high at 20.6%, reflecting global investor confidence.<br>
        DII participation at 20.5% indicates strong domestic institutional support.
    </div>""", unsafe_allow_html=True)


# ── PROS & CONS ───────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown('<p class="section-title">Investment Summary</p>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown("""
    <div class="tailwind-box">
        <h4>Pros</h4>
        <ul>
            <li>24% Profit CAGR over last 5 years</li>
            <li>Healthy dividend payout with growing ARPU</li>
            <li>Industry-leading telecom franchise in India</li>
            <li>Strong 5G rollout and spectrum leadership</li>
            <li>Improving cash flows & debt reduction path</li>
            <li>Africa operations profitable and growing</li>
        </ul>
    </div>""", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="risk-box">
        <h4>Cons</h4>
        <ul>
            <li>Trading at 7.7x Book Value (expensive valuation)</li>
            <li>High absolute debt: ₹1,95,412 Cr</li>
            <li>Large ongoing capex requirement (5G)</li>
            <li>Regulatory uncertainty (AGR, TRAI)</li>
            <li>Promoter holding declined over 3 years</li>
            <li>Intense competition from Reliance Jio</li>
        </ul>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── FEATURE BLOCK — EXECUTIVE SUMMARY TAB ─────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

with tab_exec:
    st.markdown('<p class="section-title" style="margin-top:16px">Bharti Airtel — Investment Thesis & Executive Summary</p>', unsafe_allow_html=True)

    # ── A. Investment Thesis ────────────────────────────────────────────────
    st.markdown("""
    <div class="exec-thesis-card">
        <h3>📋 Investment Thesis — FY 2025–26</h3>
        <ul>
            <li><strong>Revenue Growth:</strong> Revenue grew 22% YoY to ₹2,10,973 Cr driven by tariff hikes, postpaid addition, and Africa recovery — a 5Y CAGR of 16% underscores sustainable momentum.</li>
            <li><strong>Profitability Inflection:</strong> EBITDA margin expanded 500 bps to 57.8% as operating leverage kicks in; net profit grew 18% YoY with a 24% 5-year profit CAGR, signalling structural earnings power.</li>
            <li><strong>Cash Flow Strength:</strong> Operating cash flow of ₹1,04,240 Cr and Free Cash Flow of ₹40,440 Cr (+68% YoY) confirms transition from capex-heavy build-out to cash generation phase.</li>
            <li><strong>Subscriber Growth & ARPU:</strong> India base of 380M+ with ARPU rising to ₹257 (+15% YoY). Postpaid base exceeded 29M. ARPU seen crossing ₹300 by FY27, unlocking further revenue upside.</li>
            <li><strong>Competitive Position:</strong> Industry #1 in spectrum holdings and 5G coverage (5,000+ cities). Strong enterprise B2B pipeline, Nxtra data centers, and Airtel Black premium bundle create durable moats.</li>
            <li><strong>Africa & Digital Adjacencies:</strong> 14-country Africa business profitable and growing. Airtel Money at scale, Nxtra $1B data center expansion, and AI/Cloud partnerships diversify revenues beyond core connectivity.</li>
            <li><strong>Long-Term Outlook:</strong> Debt reduction path improving (Net Debt/EBITDA at 1.1x), improving ROE trajectory, and sector-leading spectrum position position Airtel as the premium India telecom franchise through FY28.</li>
        </ul>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Peer Ranking System ─────────────────────────────────────────────────
    st.markdown('<p class="section-title">🏆 Peer Ranking Leaderboard</p>', unsafe_allow_html=True)

    rank_data = {
        "ROE (%)": [("Tata Comm", 34.01, "#1"), ("Bharti Airtel", 21.86, "#2"), ("Bharti Hexacom", 26.86, "#2")],
        "Market Cap (₹ Cr)": [("Bharti Airtel", 1148524, "#1"), ("Vodafone Idea", 147563, "#2"), ("Bharti Hexacom", 78469, "#3")],
        "Revenue (₹ Cr)": [("Bharti Airtel", 210973, "#1"), ("Vodafone Idea", 44873, "#2"), ("Tata Comm", 24803, "#3")],
    }

    r1, r2, r3 = st.columns(3)
    rank_cols = [r1, r2, r3]
    badge_classes = ["", "r2", "r3"]

    for col, (metric, entries) in zip(rank_cols, rank_data.items()):
        with col:
            st.markdown(f'<p style="font-size:12px;font-weight:700;color:#374151;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.6px;">{metric}</p>', unsafe_allow_html=True)
            sorted_entries = sorted(entries, key=lambda x: x[1], reverse=True)
            html_block = '<div style="background:#fff;border:1px solid #dde1e7;border-radius:6px;overflow:hidden;">'
            for i, (company, value, rank) in enumerate(sorted_entries):
                badge_class = badge_classes[min(i, 2)]
                is_airtel = "background:#fff8f8;" if company == "Bharti Airtel" else ""
                val_fmt = f"₹{value:,.0f} Cr" if value > 1000 else f"{value:.2f}%"
                pct = ["Top 25%", "Top 50%", "Top 75%"][min(i, 2)]
                html_block += f'''
                <div class="rank-row" style="{is_airtel}">
                    <div class="rank-badge {badge_class}">{i+1}</div>
                    <div class="rank-company">{company}</div>
                    <div>
                        <div class="rank-val">{val_fmt}</div>
                        <div class="rank-pct">{pct}</div>
                    </div>
                </div>'''
            html_block += '</div>'
            st.markdown(html_block, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SWOT Analysis ───────────────────────────────────────────────────────
    st.markdown('<p class="section-title">⚡ SWOT Analysis</p>', unsafe_allow_html=True)

    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown("""
        <div class="swot-card-s">
            <h4>💪 Strengths</h4>
            <ul>
                <li>India's #1 telecom operator by market cap</li>
                <li>Highest spectrum holdings in the industry</li>
                <li>57.8% EBITDA margin — best-in-class</li>
                <li>5G network in 5,000+ cities — fastest rollout</li>
                <li>Diversified across 15 countries</li>
                <li>Premium ARPU base with growing postpaid</li>
                <li>Strong enterprise & B2B franchise</li>
                <li>Airtel Money / fintech optionality</li>
            </ul>
        </div>
        <br>
        <div class="swot-card-o">
            <h4>🚀 Opportunities</h4>
            <ul>
                <li>ARPU expansion to ₹300+ by FY27</li>
                <li>5G monetization through fixed wireless & cloud</li>
                <li>Nxtra AI/Cloud data center build-out ($1B+)</li>
                <li>Africa growth — Airtel Money at scale</li>
                <li>Enterprise & government digital contracts</li>
                <li>Fiber-to-home penetration still early-stage</li>
                <li>Satellite broadband via OneWeb partnership</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with sw2:
        st.markdown("""
        <div class="swot-card-w">
            <h4>⚠️ Weaknesses</h4>
            <ul>
                <li>High absolute debt: ₹1,95,412 Cr</li>
                <li>P/E of 40x — limited margin of safety</li>
                <li>Ongoing high capex requirements for 5G</li>
                <li>Promoter stake declined over past 3 years</li>
                <li>Current ratio of 0.52 — tight liquidity</li>
                <li>Africa revenue exposed to currency risk</li>
                <li>AGR dues regulatory overhang</li>
            </ul>
        </div>
        <br>
        <div class="swot-card-t">
            <h4>🔴 Threats</h4>
            <ul>
                <li>Reliance Jio aggressive pricing strategy</li>
                <li>TRAI tariff intervention risk</li>
                <li>AGR Supreme Court dues (₹43,000 Cr)</li>
                <li>Spectrum auction costs rising cycle</li>
                <li>Macro slowdown dampening ARPU growth</li>
                <li>Vi revival (if government-backed rescue)</li>
                <li>Currency depreciation in Africa markets</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Management Action Center ─────────────────────────────────────────────
    st.markdown('<p class="section-title">🏛 Management Action Center</p>', unsafe_allow_html=True)

    ma1, ma2, ma3 = st.columns(3)
    with ma1:
        st.markdown("""
        <div class="action-card-opp">
            <h4>🟢 Top 5 Opportunities</h4>
            <ul>
                <li><strong>1.</strong> ARPU expansion via premium bundling</li>
                <li><strong>2.</strong> Data center & AI Cloud monetization</li>
                <li><strong>3.</strong> Enterprise B2B — government contracts</li>
                <li><strong>4.</strong> Africa — Airtel Money profitability</li>
                <li><strong>5.</strong> Fiber deep penetration (10M → 30M homes)</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with ma2:
        st.markdown("""
        <div class="action-card-risk">
            <h4>🔴 Top 5 Risks</h4>
            <ul>
                <li><strong>1.</strong> Regulatory pricing intervention (TRAI)</li>
                <li><strong>2.</strong> AGR dues — ₹43,000 Cr liability</li>
                <li><strong>3.</strong> Jio competition — price war risk</li>
                <li><strong>4.</strong> Africa currency depreciation</li>
                <li><strong>5.</strong> Capex overrun in 5G/fiber build-out</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with ma3:
        st.markdown("""
        <div class="action-card-mgmt">
            <h4>🔵 Top 5 Management Actions</h4>
            <ul>
                <li><strong>1.</strong> Continue ARPU improvement roadmap</li>
                <li><strong>2.</strong> Accelerate debt reduction with FCF</li>
                <li><strong>3.</strong> Expand enterprise revenue mix to 25%</li>
                <li><strong>4.</strong> Accelerate fiber rollout to 30M homes</li>
                <li><strong>5.</strong> Unlock Nxtra data center value via IPO</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI Trend Intelligence ───────────────────────────────────────────────
    st.markdown('<p class="section-title">📈 KPI Trend Intelligence</p>', unsafe_allow_html=True)

    kpi_data = {
        "Revenue": {"value": "₹2,10,973 Cr", "delta": "+22% YoY", "pos": True, "trend": [172000, 178000, 188000, 198000, 210973]},
        "Net Profit": {"value": "₹33,823 Cr", "delta": "+18% YoY", "pos": True, "trend": [20000, 24000, 27000, 28500, 33823]},
        "EBITDA Margin": {"value": "57.8%", "delta": "+500 bps", "pos": True, "trend": [50.0, 52.5, 54.0, 55.5, 57.8]},
        "ROE": {"value": "21.86%", "delta": "+340 bps", "pos": True, "trend": [16.0, 17.5, 19.0, 20.5, 21.86]},
        "ROCE": {"value": "18.5%", "delta": "+220 bps", "pos": True, "trend": [14.5, 15.5, 16.5, 17.5, 18.5]},
        "ARPU": {"value": "₹257", "delta": "+15% YoY", "pos": True, "trend": [178, 193, 208, 226, 257]},
    }

    kpi_cols = st.columns(6)
    for col, (name, data) in zip(kpi_cols, kpi_data.items()):
        with col:
            delta_color = "#16a34a" if data["pos"] else "#dc2626"
            delta_class = "kt-delta-pos" if data["pos"] else "kt-delta-neg"
            st.markdown(f"""
            <div class="kpi-trend-card">
                <div class="kt-label">{name}</div>
                <div class="kt-value">{data['value']}</div>
                <div class="{delta_class}">{data['delta']}</div>
            </div>""", unsafe_allow_html=True)
            fig_spark = go.Figure(go.Scatter(
                y=data["trend"], mode="lines",
                line=dict(color="#e40000" if data["pos"] else "#dc2626", width=1.5),
                fill="tozeroy", fillcolor="rgba(228,0,0,0.07)"
            ))
            fig_spark.update_layout(
                height=60, margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False),
                showlegend=False
            )
            st.plotly_chart(fig_spark, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Export Center ────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">📥 Dashboard Export Center</p>', unsafe_allow_html=True)

    financial_data = pd.DataFrame({
        "Metric": ["Revenue (₹ Cr)", "EBITDA Margin (%)", "Net Profit (₹ Cr)", "ARPU (₹)", "Subscribers (M)", "ROE (%)", "ROCE (%)", "EPS (₹)", "Debt/Equity", "FCF (₹ Cr)"],
        "FY2025": [210973, 57.8, 33823, 257, 666, 21.86, 18.50, 43.8, 1.31, 40440],
    })

    peer_export_df = pd.DataFrame({
        "Company":       ["Bharti Airtel","Vodafone Idea","Bharti Hexacom","Tata Communications","Tata Tele. Mah.","MTNL"],
        "CMP (₹)":       [1885.30, 13.62, 1568.90, 1896.30, 42.18, 28.94],
        "ROE %":         [21.86, -12.35, 26.86, 34.01, -66.49, -30.57],
        "ROCE %":        [18.50, -1.60, 21.82, 14.69, 55.65, -2.25],
        "Mkt Cap (₹ Cr)":[1148524, 147563, 78469, 53987, 8250, 1823],
        "Sales (₹ Cr)":  [210973, 44873, 9354, 24803, 1160, 956]
    })

    def df_to_csv(df):
        return df.to_csv(index=False).encode("utf-8")

    def df_to_excel(dfs_dict):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheet, df in dfs_dict.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        return output.getvalue()

    exp1, exp2, exp3, exp4 = st.columns(4)
    with exp1:
        excel_data = df_to_excel({"Financial Data": financial_data, "Peer Comparison": peer_export_df})
        st.download_button("📊 Download Dashboard (Excel)", excel_data, "Airtel_Dashboard_2026.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with exp2:
        st.download_button("📄 Download Financial Data (CSV)", df_to_csv(financial_data),
                           "Airtel_Financial_Data_FY2025.csv", "text/csv", use_container_width=True)
    with exp3:
        st.download_button("🔍 Download Peer Comparison (CSV)", df_to_csv(peer_export_df),
                           "Airtel_Peer_Comparison.csv", "text/csv", use_container_width=True)
    with exp4:
        # Quarterly results export
        quarterly_export = pd.DataFrame({
            "Quarter": ["Mar-23","Jun-23","Sep-23","Dec-23","Mar-24","Jun-24","Sep-24","Dec-24","Mar-25","Jun-25","Sep-25","Dec-25","Mar-26"],
            "Sales (₹ Cr)": [36009,37440,37044,37900,37599,38506,41473,45129,47876,49463,52145,53982,55383],
            "Net Profit (₹ Cr)": [4226,1520,2093,2876,2068,4718,4153,16135,12476,7422,8651,8503,9247],
            "OPM %": [52,52,53,52,52,51,53,54,56,56,57,57,57],
        })
        st.download_button("📈 Download Quarterly Results (CSV)", df_to_csv(quarterly_export),
                           "Airtel_Quarterly_Results.csv", "text/csv", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── FEATURE BLOCK — FORECASTING & VALUATION TAB ────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

with tab_forecast:
    st.markdown('<p class="section-title" style="margin-top:16px">Interactive Forecasting Model — FY27 & FY28</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0f9ff;border:1px solid #bae6fd;border-left:3px solid #0ea5e9;border-radius:6px;padding:12px 18px;margin-bottom:18px;font-size:13px;color:#0c4a6e;">
    ⚙️ Adjust the sliders below to model Bharti Airtel's financial projections for FY27 and FY28. All figures cascade from FY25 actuals.
    </div>""", unsafe_allow_html=True)

    sl1, sl2 = st.columns(2)
    with sl1:
        rev_growth   = st.slider("📈 Revenue Growth Rate (%)", 5, 30, 14, 1)
        ebitda_margin= st.slider("💰 EBITDA Margin (%)",       40, 70, 60, 1)
    with sl2:
        np_growth    = st.slider("📊 Net Profit Growth (%)",    5, 35, 18, 1)
        arpu_growth  = st.slider("📶 ARPU Growth Rate (%)",     5, 30, 15, 1)

    # Base FY25 actuals
    fy25_rev    = 210973
    fy25_ebitda = fy25_rev * 0.578
    fy25_np     = 33823
    fy25_arpu   = 257
    fy25_eps    = 43.8
    shares      = 5970  # approx shares (millions)

    fy27_rev    = round(fy25_rev    * (1 + rev_growth/100)**2)
    fy28_rev    = round(fy25_rev    * (1 + rev_growth/100)**3)
    fy27_ebitda = round(fy27_rev    * (ebitda_margin/100))
    fy28_ebitda = round(fy28_rev    * (ebitda_margin/100))
    fy27_np     = round(fy25_np     * (1 + np_growth/100)**2)
    fy28_np     = round(fy25_np     * (1 + np_growth/100)**3)
    fy27_eps    = round(fy25_eps    * (1 + np_growth/100)**2, 1)
    fy28_eps    = round(fy25_eps    * (1 + np_growth/100)**3, 1)
    fy27_arpu   = round(fy25_arpu   * (1 + arpu_growth/100)**2)
    fy28_arpu   = round(fy25_arpu   * (1 + arpu_growth/100)**3)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Forecast Output</p>', unsafe_allow_html=True)

    # Summary cards
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("FY27E Revenue",    f"₹{fy27_rev:,.0f} Cr",    f"+{round((fy27_rev/fy25_rev-1)*100, 1)}% vs FY25")
    f2.metric("FY27E EBITDA",     f"₹{fy27_ebitda:,.0f} Cr", f"{ebitda_margin}% margin")
    f3.metric("FY27E Net Profit", f"₹{fy27_np:,.0f} Cr",     f"+{round((fy27_np/fy25_np-1)*100, 1)}% vs FY25")
    f4.metric("FY27E EPS",        f"₹{fy27_eps}",             f"+{round((fy27_eps/fy25_eps-1)*100, 1)}% vs FY25")

    f5, f6, f7, f8 = st.columns(4)
    f5.metric("FY28E Revenue",    f"₹{fy28_rev:,.0f} Cr",    f"+{round((fy28_rev/fy25_rev-1)*100, 1)}% vs FY25")
    f6.metric("FY28E EBITDA",     f"₹{fy28_ebitda:,.0f} Cr", f"{ebitda_margin}% margin")
    f7.metric("FY28E Net Profit", f"₹{fy28_np:,.0f} Cr",     f"+{round((fy28_np/fy25_np-1)*100, 1)}% vs FY25")
    f8.metric("FY28E EPS",        f"₹{fy28_eps}",             f"+{round((fy28_eps/fy25_eps-1)*100, 1)}% vs FY25")

    st.markdown("<br>", unsafe_allow_html=True)

    # Forecast bar charts
    fc1, fc2 = st.columns(2)
    forecast_df = pd.DataFrame({
        "Year":      ["FY25A",      "FY27E",  "FY28E"],
        "Revenue":   [fy25_rev,     fy27_rev, fy28_rev],
        "EBITDA":    [int(fy25_ebitda), fy27_ebitda, fy28_ebitda],
        "Net Profit":[fy25_np,      fy27_np,  fy28_np],
        "EPS":       [fy25_eps,     fy27_eps, fy28_eps],
    })

    with fc1:
        fig_frev = px.bar(forecast_df, x="Year", y="Revenue", title="Revenue Forecast (₹ Cr)",
                          color="Year", color_discrete_sequence=["#9ca3af", "#1d4ed8", "#e40000"],
                          text="Revenue")
        fig_frev.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_frev.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", showlegend=False,
                               font=dict(color="#374151", family="IBM Plex Sans", size=11),
                               height=300, margin=dict(l=10, r=10, t=36, b=10),
                               yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af"),
                               xaxis=dict(showgrid=False, color="#9ca3af"))
        st.plotly_chart(fig_frev, use_container_width=True)

    with fc2:
        fig_fnp = px.bar(forecast_df, x="Year", y="Net Profit", title="Net Profit Forecast (₹ Cr)",
                         color="Year", color_discrete_sequence=["#9ca3af", "#1d4ed8", "#16a34a"],
                         text="Net Profit")
        fig_fnp.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_fnp.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", showlegend=False,
                              font=dict(color="#374151", family="IBM Plex Sans", size=11),
                              height=300, margin=dict(l=10, r=10, t=36, b=10),
                              yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af"),
                              xaxis=dict(showgrid=False, color="#9ca3af"))
        st.plotly_chart(fig_fnp, use_container_width=True)

    # ARPU trend chart
    arpu_df = pd.DataFrame({
        "Year": ["FY23A", "FY24A", "FY25A", "FY27E", "FY28E"],
        "ARPU": [193, 208, 257, fy27_arpu, fy28_arpu]
    })
    fig_arpu = px.line(arpu_df, x="Year", y="ARPU", markers=True,
                       title=f"ARPU Growth Trajectory (₹) — {arpu_growth}% Growth Assumption")
    fig_arpu.update_traces(line_color="#e40000", marker_color="#e40000", marker_size=8, line_width=2)
    fig_arpu.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                           font=dict(color="#374151", family="IBM Plex Sans", size=11),
                           height=260, margin=dict(l=10, r=10, t=36, b=10),
                           yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af"),
                           xaxis=dict(showgrid=False, color="#9ca3af"))
    st.plotly_chart(fig_arpu, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scenario Analysis ───────────────────────────────────────────────────
    st.markdown('<p class="section-title">📊 Scenario Analysis — Bear / Base / Bull</p>', unsafe_allow_html=True)

    scenarios = {
        "🐻 Bear Case":  {"rev_g": 8,  "ebitda_m": 54, "np_g": 10, "pe": 28, "color": "#fef2f2", "border": "#fecaca", "text_color": "#991b1b"},
        "⚖️ Base Case":  {"rev_g": 14, "ebitda_m": 60, "np_g": 18, "pe": 38, "color": "#f0fdf4", "border": "#86efac", "text_color": "#166534"},
        "🐂 Bull Case":  {"rev_g": 22, "ebitda_m": 65, "np_g": 28, "pe": 50, "color": "#eff6ff", "border": "#bfdbfe", "text_color": "#1e40af"},
    }

    sc_rows = []
    for scenario, params in scenarios.items():
        s_rev  = round(fy25_rev * (1 + params["rev_g"]/100)**2)
        s_ebitda = round(s_rev  * (params["ebitda_m"]/100))
        s_np   = round(fy25_np  * (1 + params["np_g"]/100)**2)
        s_eps  = round(fy25_eps * (1 + params["np_g"]/100)**2, 1)
        s_tp   = round(s_eps    * params["pe"])
        sc_rows.append({
            "Scenario": scenario, "Rev Growth": f"{params['rev_g']}%",
            "FY27E Revenue (₹ Cr)": f"{s_rev:,.0f}",
            "FY27E EBITDA (₹ Cr)": f"{s_ebitda:,.0f}",
            "FY27E Net Profit (₹ Cr)": f"{s_np:,.0f}",
            "FY27E EPS (₹)": f"{s_eps}",
            "Target P/E": f"{params['pe']}x",
            "Target Price (₹)": f"₹{s_tp:,.0f}",
        })

    sc_df = pd.DataFrame(sc_rows)
    # Color-code using dataframe styling
    def highlight_scenario(row):
        if "Bear" in row["Scenario"]:
            return ["background-color: #fef2f2; color: #991b1b"] * len(row)
        elif "Bull" in row["Scenario"]:
            return ["background-color: #eff6ff; color: #1e40af"] * len(row)
        else:
            return ["background-color: #f0fdf4; color: #166534"] * len(row)

    styled_sc = sc_df.style.apply(highlight_scenario, axis=1)
    st.dataframe(styled_sc, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Valuation Model ──────────────────────────────────────────────────────
    st.markdown('<p class="section-title">💎 Valuation Model & Intrinsic Value</p>', unsafe_allow_html=True)

    sector_avg_pe  = 38.0
    fair_value_pe  = 36.0
    intrinsic_val  = round(fy25_eps * fair_value_pe)
    upside_pct     = round((intrinsic_val / current_price - 1) * 100, 1)
    analyst_target = 2150
    target_upside  = round((analyst_target / current_price - 1) * 100, 1)

    v1, v2, v3, v4, v5, v6, v7 = st.columns(7)
    for col, label, val, sub in [
        (v1, "Current Price",     f"₹{current_price:,.0f}", "NSE Live"),
        (v2, "Current P/E",       f"{pe_ratio:.1f}x",       "Trailing"),
        (v3, "Sector Avg P/E",    f"{sector_avg_pe}x",      "Indian Telecom"),
        (v4, "Fair Value P/E",    f"{fair_value_pe}x",      "Analyst Consensus"),
        (v5, "Intrinsic Value",   f"₹{intrinsic_val:,.0f}", "P/E Based"),
        (v6, "Expected Upside",   f"{upside_pct}%",         "vs CMP"),
        (v7, "Target Price",      f"₹{analyst_target:,.0f}", "12M Consensus"),
    ]:
        with col:
            st.markdown(f"""
            <div class="valuation-card">
                <div class="vc-label">{label}</div>
                <div class="vc-value">{val}</div>
                <div class="vc-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Valuation conclusion
    if upside_pct >= 15:
        conclusion_class = "conclusion-undervalued"
        verdict = "🟢 UNDERVALUED"
        conclusion_text = f"At CMP of ₹{current_price:,.0f}, Airtel trades at a {((current_price/intrinsic_val-1)*100):.1f}% discount to intrinsic value of ₹{intrinsic_val:,.0f} based on {fair_value_pe}x fair P/E applied to FY25 EPS. The stock offers {upside_pct}% upside to 12M consensus target of ₹{analyst_target:,.0f}."
    elif upside_pct >= 0:
        conclusion_class = "conclusion-fair"
        verdict = "🟡 FAIRLY VALUED"
        conclusion_text = f"At CMP of ₹{current_price:,.0f}, Airtel is trading close to its intrinsic value of ₹{intrinsic_val:,.0f}. Limited near-term upside of {upside_pct}%, but long-term fundamentals remain compelling for patient investors."
    else:
        conclusion_class = "conclusion-overvalued"
        verdict = "🔴 OVERVALUED (NEAR TERM)"
        conclusion_text = f"At CMP of ₹{current_price:,.0f}, Airtel trades at a premium to intrinsic value of ₹{intrinsic_val:,.0f}. The {abs(upside_pct)}% premium to fair value suggests near-term caution, though long-term thesis remains intact."

    st.markdown(f"""
    <div class="{conclusion_class}">
        <div style="font-size:16px;font-weight:700;margin-bottom:8px;">{verdict}</div>
        <div style="font-size:13px;line-height:1.7;">{conclusion_text}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Waterfall — value bridge
    wf_df = pd.DataFrame({
        "Stage": ["FY25 EPS Base", "Revenue Growth", "Margin Expansion", "Multiple Compression", "Target Price FY27E"],
        "Value": [fy25_eps * pe_ratio, (fy27_eps - fy25_eps) * pe_ratio,
                  fy27_ebitda * 0.01,
                  -(fy27_eps * (pe_ratio - fair_value_pe)),
                  fy27_eps * fair_value_pe],
        "Type":  ["Base", "Positive", "Positive", "Negative", "Total"]
    })

    wf_colors = {"Base": "#6b7280", "Positive": "#16a34a", "Negative": "#dc2626", "Total": "#1d4ed8"}
    fig_wf = go.Figure(go.Waterfall(
        name="Value Bridge", orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=wf_df["Stage"],
        y=wf_df["Value"],
        connector={"line": {"color": "#e5e7eb"}},
        decreasing={"marker": {"color": "#dc2626"}},
        increasing={"marker": {"color": "#16a34a"}},
        totals={"marker": {"color": "#1d4ed8"}},
    ))
    fig_wf.update_layout(
        title="Price Value Bridge — FY25 to FY27E Target",
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        font=dict(color="#374151", family="IBM Plex Sans", size=11),
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6", color="#9ca3af", title="₹"),
        xaxis=dict(showgrid=False, color="#374151")
    )
    st.plotly_chart(fig_wf, use_container_width=True)


