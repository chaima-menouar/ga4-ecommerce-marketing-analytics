"""Local analytics dashboard for exported BigQuery GA4 query results."""
import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="GA4 E-commerce Analytics", page_icon="📊", layout="wide")
st.title("📊 E-Commerce Marketing Performance")
st.caption("Google Merchandise Store · GA4 + BigQuery · Local preview")
st.info("Upload actual BigQuery CSV exports below. No sample or invented KPI values are displayed.")

def load_csv(label, expected):
    uploaded = st.file_uploader(label, type=["csv"], key=label)
    if uploaded is None:
        return None
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        return None
    missing = set(expected) - set(df.columns)
    if missing:
        st.error(f"Missing columns: {', '.join(sorted(missing))}")
        return None
    return df

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Acquisition", "Funnel", "Tracking plan"])
with tab1:
    daily = load_csv("Upload 01_daily_sessions.sql CSV", ["day", "sessions"])
    purchases = load_csv("Upload 02_purchases.sql CSV", ["day", "purchases", "purchase_revenue"])
    if daily is not None:
        daily["day"] = pd.to_datetime(daily["day"], errors="coerce")
        daily["sessions"] = pd.to_numeric(daily["sessions"], errors="coerce").fillna(0)
        st.metric("Sessions", f"{daily['sessions'].sum():,.0f}")
        st.line_chart(daily.set_index("day")["sessions"])
    if purchases is not None:
        purchases["day"] = pd.to_datetime(purchases["day"], errors="coerce")
        for col in ["purchases", "purchase_revenue"]:
            purchases[col] = pd.to_numeric(purchases[col], errors="coerce").fillna(0)
        c1, c2 = st.columns(2)
        c1.metric("Purchase events", f"{purchases['purchases'].sum():,.0f}")
        c2.metric("Purchase revenue (dataset currency)", f"{purchases['purchase_revenue'].sum():,.2f}")
        st.line_chart(purchases.set_index("day")[["purchases"]])
    if daily is not None and purchases is not None and daily["sessions"].sum() > 0:
        st.caption("Purchases / sessions is an event-per-session ratio, NOT a session conversion rate.")
with tab2:
    channels = load_csv("Upload 03_channels.sql CSV", ["first_user_source", "first_user_medium", "sessions", "purchases", "session_purchase_rate"])
    if channels is not None:
        st.warning("Source/medium here is first-user acquisition, not GA4 session default channel grouping.")
        channels["sessions"] = pd.to_numeric(channels["sessions"], errors="coerce").fillna(0)
        st.bar_chart(channels.set_index("first_user_source")["sessions"])
        st.dataframe(channels, use_container_width=True)
with tab3:
    funnel = load_csv("Upload 04_funnel.sql CSV", ["sessions", "sessions_view_item", "sessions_add_to_cart", "sessions_begin_checkout", "sessions_purchase"])
    if funnel is not None and not funnel.empty:
        row = funnel.iloc[0]
        labels = {
            "sessions_view_item": "View item", "sessions_add_to_cart": "Add to cart",
            "sessions_begin_checkout": "Begin checkout", "sessions_purchase": "Purchase"
        }
        values = pd.Series({label: pd.to_numeric(row[col], errors="coerce") for col, label in labels.items()})
        st.bar_chart(values)
        st.caption("These are session-level event-presence counts, not a strictly sequential funnel.")
with tab4:
    st.markdown("""### Tracking events
| Event | Trigger |
|---|---|
| page_view | Page loaded |
| view_item | Product viewed |
| add_to_cart | Product added to cart |
| begin_checkout | Checkout started |
| purchase | Order completed |

**Consent Mode v2:** analytics_storage, ad_storage, ad_user_data, ad_personalization.

**Limitations:** public GA4 data is historical and obfuscated; missing consent-related data cannot be recovered from the export.
""")
st.divider()
st.caption("Educational project · Results require exported BigQuery data · Dashboard is local, not publicly hosted.")
