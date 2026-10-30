import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NEXUS | Commerce Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;color:#e8eef9}
.stApp {background:radial-gradient(ellipse at 80% 0%,#192a47 0%,#0a101d 45%,#080d17 100%)}
[data-testid="stSidebar"] {background:#0d1524;border-right:1px solid #24334a}
[data-testid="stSidebar"] * {color:#cbd6e9}
.block-container {padding-top:2rem;max-width:1500px}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.04em!important}
div[data-testid="stMetric"] {background:linear-gradient(135deg,#172338,#111a2a);padding:20px 22px;border:1px solid #2b3b55;border-radius:18px;box-shadow:0 12px 35px #0003}
div[data-testid="stMetricLabel"] {color:#91a3bf}
div[data-testid="stMetricValue"] {color:#f4f7ff;font-family:'Space Grotesk';font-size:2rem}
div[data-testid="stTabs"] button {font-weight:600}
[data-testid="stFileUploader"] {border:1px dashed #415674;border-radius:14px;padding:8px}
[data-testid="stAlert"] {border-radius:12px}
.hero {border:1px solid #304461;border-radius:24px;padding:38px 42px;background:linear-gradient(115deg,#1c3351 0%,#14243a 55%,#111d30 100%);margin-bottom:25px;position:relative}
.eyebrow {color:#67e8d4;font-weight:700;letter-spacing:.18em;font-size:.72rem}
.hero-title {font-family:'Space Grotesk';font-weight:700;font-size:clamp(2rem,4vw,3.4rem);letter-spacing:-.06em;line-height:1.1;margin:12px 0}
.hero-desc {color:#b0c0d6;font-size:1rem;max-width:680px}
.pill {display:inline-block;background:#173e3d;color:#7ff3da;border:1px solid #2c7069;padding:6px 12px;border-radius:99px;font-size:.78rem;font-weight:700;margin-top:14px}
.section {font-family:'Space Grotesk';font-size:1.3rem;font-weight:700;margin:20px 0 12px}
.muted {color:#92a5bf}
.footer {border-top:1px solid #263750;padding-top:20px;margin-top:35px;color:#879ab6;font-size:.82rem}
</style>
""", unsafe_allow_html=True)

def chart_style(fig, height=340):
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans',color='#aabbd2'), margin=dict(l=12,r=12,t=30,b=15),
        xaxis=dict(showgrid=False,zeroline=False),yaxis=dict(gridcolor='#25334a',zeroline=False),
        hoverlabel=dict(bgcolor='#1c2c43',font_color='#ffffff'))
    return fig

def upload(label, cols, key):
    f=st.file_uploader(label,type='csv',key=key)
    if f is None: return None
    try:
        df=pd.read_csv(f)
        missing=set(cols)-set(df.columns)
        if missing:
            st.error('Missing columns: '+', '.join(sorted(missing)));return None
        return df
    except Exception as e:
        st.error(f'Cannot read CSV: {e}');return None

def showcase_data():
    import numpy as np
    rng = np.random.default_rng(2026)
    dates = pd.date_range("2020-11-01", periods=60)
    daily = pd.DataFrame({"day": dates, "sessions": 650 + np.arange(60) * 7 + rng.integers(-100, 100, 60)})
    purchases = pd.DataFrame({"day": dates, "purchases": rng.integers(10, 48, 60), "purchase_revenue": rng.integers(500, 3000, 60)})
    channels = pd.DataFrame({"first_user_source": ["google", "(direct)", "youtube", "newsletter", "referral"], "first_user_medium": ["organic", "(none)", "social", "email", "referral"], "sessions": [18000, 12500, 7200, 4300, 2600], "purchases": [310, 190, 85, 105, 30], "session_purchase_rate": [.017, .015, .012, .024, .011]})
    funnel = pd.DataFrame([{"sessions": 44600, "sessions_view_item": 26000, "sessions_add_to_cart": 9300, "sessions_begin_checkout": 4100, "sessions_purchase": 720}])
    return daily, purchases, channels, funnel

with st.sidebar:
    st.markdown("## ✦ NEXUS")
    st.caption("COMMERCE INTELLIGENCE / 2026")
    st.divider()
    st.markdown("**WORKSPACE**")
    page=st.radio("Navigation",["Overview","Acquisition","Conversion funnel","Tracking & privacy"],label_visibility="collapsed")
    st.divider()
    st.markdown("**DISPLAY MODE**")
    demo_mode=st.toggle("Showcase data (synthetic)",value=False)
    st.divider()
    st.markdown("**DATA CONNECTORS**")
    daily=upload("Sessions CSV",["day","sessions"],"daily")
    purchases=upload("Purchases CSV",["day","purchases","purchase_revenue"],"purchases")
    channels=upload("Channels CSV",["first_user_source","first_user_medium","sessions","purchases","session_purchase_rate"],"channels")
    funnel=upload("Funnel CSV",["sessions","sessions_view_item","sessions_add_to_cart","sessions_begin_checkout","sessions_purchase"],"funnel")
    st.caption("Export the four SQL query results from BigQuery, then upload them here.")
    st.divider()
    st.caption("GA4 · BIGQUERY · LOOKER STUDIO")

if demo_mode:
    daily, purchases, channels, funnel = showcase_data()
    st.warning("DEMO MODE — All figures are synthetic illustrations, NOT actual GA4 results. Turn off demo mode to use BigQuery CSV exports.")

st.markdown("""<div class="hero"><div class="eyebrow">✦ MARKETING ANALYTICS PLATFORM</div>
<div class="hero-title">Your commerce.<br>In sharper focus.</div>
<div class="hero-desc">Explore acquisition, purchase behavior and conversion performance through a modern analytics workspace powered by GA4 exports.</div>
<span class="pill">● DATA-DRIVEN WORKSPACE</span></div>""",unsafe_allow_html=True)

if page=="Overview":
    st.markdown('<div class="section">Executive overview</div>',unsafe_allow_html=True)
    total_sessions=total_purchases=revenue=None
    if daily is not None:
        daily['day']=pd.to_datetime(daily['day'],errors='coerce')
        daily['sessions']=pd.to_numeric(daily['sessions'],errors='coerce').fillna(0)
        total_sessions=int(daily.sessions.sum())
    if purchases is not None:
        purchases['day']=pd.to_datetime(purchases['day'],errors='coerce')
        for c in ['purchases','purchase_revenue']:
            purchases[c]=pd.to_numeric(purchases[c],errors='coerce').fillna(0)
        total_purchases=int(purchases.purchases.sum())
        revenue=float(purchases.purchase_revenue.sum())
    a,b,c=st.columns(3)
    a.metric("Total sessions",f"{total_sessions:,}" if total_sessions is not None else "—")
    b.metric("Purchase events",f"{total_purchases:,}" if total_purchases is not None else "—")
    c.metric("Recorded revenue",f"{revenue:,.2f}" if revenue is not None else "—")
    st.markdown('<div class="section">Performance over time</div>',unsafe_allow_html=True)
    if daily is not None and not daily.empty:
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=daily.day,y=daily.sessions,mode='lines',line=dict(color='#60e5ce',width=3),fill='tozeroy',fillcolor='rgba(96,229,206,.09)',name='Sessions'))
        st.plotly_chart(chart_style(fig),use_container_width=True)
    else:
        st.info("Upload the sessions CSV from BigQuery to unlock your performance timeline.")
    if purchases is not None and not purchases.empty:
        fig=go.Figure(go.Bar(x=purchases.day,y=purchases.purchases,marker_color='#8b9cf8',name='Purchases'))
        st.plotly_chart(chart_style(fig,300),use_container_width=True)
elif page=="Acquisition":
    st.markdown('<div class="section">Acquisition intelligence</div>',unsafe_allow_html=True)
    st.caption("Source/medium reflects first-user attribution, not GA4 session default channel grouping.")
    if channels is not None and not channels.empty:
        for c in ['sessions','purchases','session_purchase_rate']:
            channels[c]=pd.to_numeric(channels[c],errors='coerce').fillna(0)
        top=channels.sort_values('sessions',ascending=False).head(12)
        fig=go.Figure(go.Bar(x=top.sessions,y=top.first_user_source.fillna('(not set)'),orientation='h',marker_color='#60e5ce'))
        fig.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(chart_style(fig,440),use_container_width=True)
        st.dataframe(channels,use_container_width=True,hide_index=True)
    else: st.info("Upload the channels CSV to explore acquisition sources.")
elif page=="Conversion funnel":
    st.markdown('<div class="section">Conversion journey</div>',unsafe_allow_html=True)
    if funnel is not None and not funnel.empty:
        row=funnel.iloc[0]
        cols=['sessions_view_item','sessions_add_to_cart','sessions_begin_checkout','sessions_purchase']
        labels=['Product viewed','Added to cart','Checkout started','Purchased']
        values=[pd.to_numeric(row[c],errors='coerce') for c in cols]
        fig=go.Figure(go.Bar(x=values,y=labels,orientation='h',marker=dict(color=['#60e5ce','#72c7e5','#869ef5','#ac86ff'])))
        fig.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(chart_style(fig,400),use_container_width=True)
        st.warning("These counts indicate event presence within sessions, not a strict sequential funnel.")
    else: st.info("Upload the funnel CSV to visualize conversion stages.")
else:
    st.markdown('<div class="section">Measurement framework</div>',unsafe_allow_html=True)
    st.markdown("""| GA4 event | Business purpose | Key parameters |
|---|---|---|
| `page_view` | Page engagement | page_location, page_title |
| `view_item` | Product discovery | items, currency, value |
| `add_to_cart` | Purchase intent | items, currency, value |
| `begin_checkout` | Checkout initiation | items, currency, value |
| `purchase` | Transaction | transaction_id, items, value |
""")
    st.markdown("#### Consent Mode v2")
    st.info("Track analytics_storage, ad_storage, ad_user_data and ad_personalization according to user consent and applicable law.")
    st.markdown("#### Data quality")
    st.caption("The public GA4 sample is historical and obfuscated. Consent-related gaps and modelled conversions cannot be recovered from the export.")

st.markdown('<div class="footer">NEXUS / E-COMMERCE ANALYTICS · TDIA3 WEBMARKETING & CRM · No fabricated metrics: figures appear only after uploading query results.</div>',unsafe_allow_html=True)
