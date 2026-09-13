import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import requests
import feedparser

# ==============================================================================
# APP CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="GovPulse | MICT Intelligence Engine",
    page_icon="🇳🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete 14 Administrative Regions of Namibia
NAMIBIA_REGIONS = [
    "Erongo", "Hardap", "Kavango East", "Kavango West", "Khomas", 
    "Kunene", "Ohangwena", "Omaheke", "Omusati", "Oshana", 
    "Oshikoto", "Otjozondjupa", "Zambezi", "ǁKaras"
]

# Custom High-Professional Styling & Command Center CSS with Header Animation
st.markdown("""
    <style>
    @keyframes fadeInGlow {
        0% { opacity: 0; transform: translateY(-8px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .animated-header {
        animation: fadeInGlow 1.2s ease-out forwards;
        font-size: 2.0rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #00e5ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Command Center Alert Window */
    .command-window {
        background-color: #0d1b2a;
        border: 1px solid #1b4965;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Professional Retouched Color-Coded Alert Cards */
    .alert-card-crit { 
        background: linear-gradient(135deg, #3d1414, #2a0d0d); 
        border-left: 4px solid #ff5252; 
        border-top: 1px solid #ff525233;
        border-right: 1px solid #ff525233;
        border-bottom: 1px solid #ff525233;
        padding: 10px 14px; 
        border-radius: 6px; 
        color: #ff8a80; 
        font-weight: 500; 
        margin-bottom: 8px; 
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .alert-card-pos { 
        background: linear-gradient(135deg, #113523, #0b2217); 
        border-left: 4px solid #2ecc71; 
        border-top: 1px solid #2ecc7133;
        border-right: 1px solid #2ecc7133;
        border-bottom: 1px solid #2ecc7133;
        padding: 10px 14px; 
        border-radius: 6px; 
        color: #a3e4d7; 
        font-weight: 500; 
        margin-bottom: 8px; 
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .alert-card-neut { 
        background: linear-gradient(135deg, #332d12, #221e0b); 
        border-left: 4px solid #f1c40f; 
        border-top: 1px solid #f1c40f33;
        border-right: 1px solid #f1c40f33;
        border-bottom: 1px solid #f1c40f33;
        padding: 10px 14px; 
        border-radius: 6px; 
        color: #f9e79f; 
        font-weight: 500; 
        margin-bottom: 8px; 
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Compact Professional Crawler Control Container */
    .power-btn-container {
        background: #1b263b;
        border: 1px solid #415a77;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="animated-header">🛡️ GovPulse: MICT National Media & Sentiment Engine</div>', unsafe_allow_html=True)

# ==============================================================================
# DATA ENGINE & INITIALIZATION
# ==============================================================================
def real_live_monitor():
    rss_queries = [
        {"type": "Print Media", "query": "Namibia newspaper OR 'The Namibian' OR 'New Era'"},
        {"type": "Online Media", "query": "Namibia digital news OR tech portal"},
        {"type": "Broadcast", "query": "NBC Namibia television OR news broadcast"},
        {"type": "Radio Media", "query": "Namibia radio broadcast OR talk show"},
        {"type": "Social Media", "query": "Namibia trending social media discourse"}
    ]

    latest_entries = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for item in rss_queries:
        media_type = item["type"]
        encoded_q = item["query"].replace(" ", "%20")
        feed_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=NA&ceid=NA:en"

        try:
            # Fetch via requests to handle headers and prevent connection drops
            response = requests.get(feed_url, headers=headers, timeout=5)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries[:2]:
                    title = entry.title
                    source_name = entry.source.title if hasattr(entry, 'source') else f"{media_type} Outlet"
                    link = entry.link

                    text_lower = title.lower()
                    if any(w in text_lower for w in ["fail", "protest", "delay", "outcry", "crisis", "unemployed", "shortage"]):
                        sentiment = "Negative"
                        crisis = "CRITICAL"
                    elif any(w in text_lower for w in ["success", "launch", "praise", "growth", "benefit", "boost"]):
                        sentiment = "Positive"
                        crisis = "NORMAL"
                    else:
                        sentiment = "Neutral"
                        crisis = "NORMAL"

                    latest_entries.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Media Type": media_type,
                        "Source/Outlet": source_name,
                        "Region": random.choice(NAMIBIA_REGIONS),
                        "Excerpt": title,
                        "Sentiment": sentiment,
                        "Crisis Alert": crisis,
                        "Source URL": link
                    })
        except Exception as e:
            print(f"Skipping feed due to error: {e}")

    return latest_entries

@st.cache_data
def generate_initial_intel():
    media_channels = ["Print Media", "Online Media", "Social Media", "Broadcast"]
    logs = [
        {"Date": "2026-10-14", "Media Type": "Print Media", "Source/Outlet": "The Namibian", "Region": "Khomas", "Excerpt": "New digital employment pathways launched at ICT summit promise 5,000 youth jobs.", "Sentiment": "Positive", "Crisis Alert": "NORMAL", "Source URL": "https://www.namibian.com.na"},
        {"Date": "2026-10-15", "Media Type": "Print Media", "Source/Outlet": "New Era", "Region": "Oshana", "Excerpt": "Delays in rural broadband setup spark complaints from local business associations.", "Sentiment": "Negative", "Crisis Alert": "CRITICAL", "Source URL": "https://newera.com.na"},
        {"Date": "2026-10-16", "Media Type": "Print Media", "Source/Outlet": "Namibian Sun", "Region": "Erongo", "Excerpt": "Ministry of ICT outlines core guidelines for the upcoming regional technology hubs.", "Sentiment": "Neutral", "Crisis Alert": "NORMAL", "Source URL": "https://www.namibiansun.com"},
    ]
    phrases = {
        "Positive": ["Successful introduction of digital literacy centers", "Grants ease poverty pressures in rural regions", "Innovators present brilliant application frameworks"],
        "Neutral": ["MICT holds consultative assembly on telecommunications", "Standard review of daily broadcast logs underway", "Media houses submit documentation frameworks"],
        "Negative": ["Protests breakout over persistent lack of employment opportunities", "System failure crashes application portal", "Severe public outcry on institutional service delivery gaps"]
    }
    base_date = datetime(2026, 10, 16)
    for _ in range(40):
        sent = random.choice(["Positive", "Neutral", "Negative"])
        med = random.choice(media_channels)
        date_str = (base_date - timedelta(days=random.randint(0, 4))).strftime("%Y-%m-%d")
        chosen_region = random.choice(NAMIBIA_REGIONS)
        logs.append({
            "Date": date_str, "Media Type": med,
            "Source/Outlet": "National Broadcaster" if med == "Broadcast" else "Digital Feed Source",
            "Region": chosen_region,
            "Excerpt": random.choice(phrases[sent]) + f" inside the {chosen_region} sector.",
            "Sentiment": sent,
            "Crisis Alert": "CRITICAL" if sent == "Negative" and random.random() > 0.3 else "NORMAL",
            "Source URL": "https://www.gov.na"
        })
    return pd.DataFrame(logs)

if 'media_db' not in st.session_state:
    st.session_state.media_db = generate_initial_intel()
if 'sms_logs' not in st.session_state:
    st.session_state.sms_logs = [
        {"id": 1, "text": "⚠️ [CRITICAL ALERT] New Era (Oshana): Delays in rural broadband setup spark complaints...", "type": "Negative", "outlet": "New Era", "region": "Oshana", "excerpt": "Delays in rural broadband setup spark complaints from local business associations.", "date": "2026-10-15", "url": "https://newera.com.na"},
        {"id": 2, "text": "🟢 [POSITIVE PULSE] The Namibian (Khomas): New digital employment pathways launched...", "type": "Positive", "outlet": "The Namibian", "region": "Khomas", "excerpt": "New digital employment pathways launched at ICT summit promise 5,000 youth jobs.", "date": "2026-10-14", "url": "https://www.namibian.com.na"}
    ]
if 'crawler_active' not in st.session_state:
    st.session_state.crawler_active = False
if 'nav_view' not in st.session_state:
    st.session_state.nav_view = "Executive"
if 'selected_alert_detail' not in st.session_state:
    st.session_state.selected_alert_detail = None

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Namibia.svg", width=100)
st.sidebar.markdown("### ⚙️ Operations Control")

st.sidebar.markdown("##### 📡 Live Crawler Engine")

st.sidebar.markdown("""
    <div class="power-btn-container">
        <span style="font-size: 0.95rem; font-weight: 600; color: #00e5ff; display: block; margin-bottom: 4px;">Master Crawler Control</span>
        <span style="font-size: 0.75rem; color: #8d99ae;">Execute live endpoint sweep</span>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("⏻ RUN LIVE CRAWLER PULSE", use_container_width=True):
    st.session_state.crawler_active = True
    with st.spinner("🔴 Initializing secure RSS sweep across live Google News feeds..."):
        time.sleep(0.4)
        live_scraped_items = real_live_monitor()
        
        if live_scraped_items:
            new_rows_df = pd.DataFrame(live_scraped_items)
            st.session_state.media_db = pd.concat([new_rows_df, st.session_state.media_db], ignore_index=True)
            
            for scraped_data in live_scraped_items:
                sent_type = scraped_data["Sentiment"]
                new_id = len(st.session_state.sms_logs) + 1
                if sent_type == "Negative":
                    payload = {
                        "id": new_id,
                        "text": f"🚨 [CRITICAL ALERT] {scraped_data['Source/Outlet']} ({scraped_data['Region']}): '{scraped_data['Excerpt'][:35]}...'",
                        "type": "Negative",
                        "outlet": scraped_data["Source/Outlet"],
                        "region": scraped_data["Region"],
                        "excerpt": scraped_data["Excerpt"],
                        "date": scraped_data["Date"],
                        "url": scraped_data["Source URL"]
                    }
                elif sent_type == "Positive":
                    payload = {
                        "id": new_id,
                        "text": f"🟢 [POSITIVE PULSE] {scraped_data['Source/Outlet']} ({scraped_data['Region']}): '{scraped_data['Excerpt'][:35]}...'",
                        "type": "Positive",
                        "outlet": scraped_data["Source/Outlet"],
                        "region": scraped_data["Region"],
                        "excerpt": scraped_data["Excerpt"],
                        "date": scraped_data["Date"],
                        "url": scraped_data["Source URL"]
                    }
                else:
                    payload = {
                        "id": new_id,
                        "text": f"🟡 [NEUTRAL NOTICE] {scraped_data['Source/Outlet']} ({scraped_data['Region']}): '{scraped_data['Excerpt'][:35]}...'",
                        "type": "Neutral",
                        "outlet": scraped_data["Source/Outlet"],
                        "region": scraped_data["Region"],
                        "excerpt": scraped_data["Excerpt"],
                        "date": scraped_data["Date"],
                        "url": scraped_data["Source URL"]
                    }
                st.session_state.sms_logs.insert(0, payload)
        
        st.session_state.crawler_active = False

with st.sidebar.expander("📥 Manual Intake Form", expanded=False):
    with st.form("manual_form", clear_on_submit=True):
        m_type = st.selectbox("Channel Type", ["Print Media", "Online Media", "Social Media", "Broadcast"])
        m_outlet = st.text_input("Source Outlet Name")
        m_region = st.selectbox("Region", NAMIBIA_REGIONS)
        m_text = st.text_area("Content Excerpt")
        m_url = st.text_input("Source URL (e.g. https://...)")
        m_submit = st.form_submit_button("Analyze & Store", use_container_width=True)
        
        if m_submit and m_text:
            t_low = m_text.lower()
            if any(w in t_low for w in ["fail", "protest", "delay", "outcry", "crisis", "unemployed", "poverty"]):
                s_val = "Negative"
            elif any(w in t_low for w in ["success", "launch", "praise", "growth", "benefit"]):
                s_val = "Positive"
            else:
                s_val = "Neutral"
            c_val = "CRITICAL" if s_val == "Negative" else "NORMAL"
            
            row = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d"), "Media Type": m_type,
                "Source/Outlet": m_outlet if m_outlet else "Manual Agent", "Region": m_region,
                "Excerpt": m_text, "Sentiment": s_val, "Crisis Alert": c_val,
                "Source URL": m_url if m_url else "https://www.gov.na"
            }])
            st.session_state.media_db = pd.concat([row, st.session_state.media_db], ignore_index=True)
            
            new_id = len(st.session_state.sms_logs) + 1
            prefix = "🚨" if s_val == "Negative" else ("🟢" if s_val == "Positive" else "🟡")
            st.session_state.sms_logs.insert(0, {
                "id": new_id,
                "text": f"{prefix} [{s_val.upper()}] Manual Report ({m_region}): '{m_text[:30]}...'",
                "type": s_val,
                "outlet": m_outlet if m_outlet else "Manual Agent",
                "region": m_region,
                "excerpt": m_text,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "url": m_url if m_url else "https://www.gov.na"
            })

# ==============================================================================
# COMMAND CENTER: TELECOMMUNICATION BROADCAST WINDOW WITH DEDUPLICATED METRICS
# ==============================================================================
current_data = st.session_state.media_db
total_items = len(current_data)

unique_crit_df = current_data[current_data["Crisis Alert"] == "CRITICAL"].drop_duplicates(subset=["Excerpt"])
crit_items = len(unique_crit_df)
alertness_pct = int((crit_items / total_items) * 100) if total_items > 0 else 0

st.markdown("""
    <div class="command-window">
        <h4 style='color: #00e5ff; margin-top: 0;'>🚨 Live Command Telecommunication Broadcast & Alert Window</h4>
        <p style='color: #8d99ae; font-size: 0.85rem; margin-bottom: 8px;'>Inspect live incoming signals and pulse feeds instantly using the action buttons below.</p>
    </div>
""", unsafe_allow_html=True)

col_m1, col_m2 = st.columns([1, 3])
with col_m1:
    st.metric(label="National Threat Con", value=f"{alertness_pct}%", delta=f"{crit_items} Unique Critical Risks" if crit_items > 0 else "Stable")
with col_m2:
    st.progress(alertness_pct / 100.0, text=f"System Alertness Index Level: {alertness_pct}% Risk Factor")

st.markdown("<hr style='border: 0.5px solid #1b4965; margin: 10px 0;'>", unsafe_allow_html=True)

# Retouched Expert Colored Alert Cards paired with Inspect Action Buttons
for alert_item in st.session_state.sms_logs[:4]:
    l_type = alert_item.get("type", "Neutral")
    l_outlet = alert_item.get("outlet", "Media Feed")
    l_region = alert_item.get("region", "National")
    l_excerpt = alert_item.get("excerpt", alert_item.get("text", ""))
    l_id = alert_item.get('id', random.randint(1,99999))
    
    col_card, col_btn = st.columns([5, 1])
    with col_card:
        if l_type == "Negative":
            st.markdown(f'<div class="alert-card-crit">🚨 <b>[CRITICAL ALERT] {l_outlet}</b> ({l_region}) — "{l_excerpt[:75]}..."</div>', unsafe_allow_html=True)
        elif l_type == "Positive":
            st.markdown(f'<div class="alert-card-pos">🟢 <b>[POSITIVE PULSE] {l_outlet}</b> ({l_region}) — "{l_excerpt[:75]}..."</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-card-neut">🟡 <b>[NEUTRAL NOTICE] {l_outlet}</b> ({l_region}) — "{l_excerpt[:75]}..."</div>', unsafe_allow_html=True)
            
    with col_btn:
        if st.button("Inspect 🔍", key=f"inspect_alert_{l_id}", use_container_width=True):
            st.session_state.selected_alert_detail = alert_item
            st.rerun()

# Modal / Inspection Panel if an alert is clicked
if st.session_state.selected_alert_detail:
    det = st.session_state.selected_alert_detail
    st.markdown("---")
    st.info(f"🔍 **Live Broadcast Record Inspection (ID: {det.get('id', 'N/A')})**")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(f"**Source Outlet:** {det.get('outlet', 'N/A')}")
        st.markdown(f"**Region:** {det.get('region', 'N/A')}")
        st.markdown(f"**Classification:** {det.get('type', 'N/A').upper()}")
    with col_d2:
        st.markdown(f"**Ingestion Date:** {det.get('date', 'N/A')}")
        st.markdown(f"**Source Portal:** [Open Link]({det.get('url', 'https://www.gov.na')})")
        
    st.markdown(f"> **Full Excerpt / Details:**\n> *\"{det.get('excerpt', 'No detailed text available.')}\"*")
    
    if st.button("❌ Close Inspection View"):
        st.session_state.selected_alert_detail = None
        st.rerun()

# ==============================================================================
# CLICKABLE SHAPED NAVIGATION MODULES
# ==============================================================================
st.markdown("### 🎛️ Intelligence Control Modules")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊\n\nExecutive\nDashboard", use_container_width=True):
        st.session_state.nav_view = "Executive"
with col2:
    if st.button("📰\n\nMulti-Media\nChannels", use_container_width=True):
        st.session_state.nav_view = "Channels"
with col3:
    if st.button("📈\n\nDaily Trend\nAnalysis", use_container_width=True):
        st.session_state.nav_view = "Trends"
with col4:
    if st.button("🚨\n\nCrisis &\nRisks", use_container_width=True):
        st.session_state.nav_view = "Crisis"
with col5:
    if st.button("🥧\n\nSentiment\nBreakdown", use_container_width=True):
        st.session_state.nav_view = "Sentiment"

st.markdown("---")

# ==============================================================================
# VIEW ROUTING & RENDER LOGIC
# ==============================================================================
if st.session_state.nav_view == "Executive":
    st.subheader("📊 Analysis Summary")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📁\n\nTotal Media Items\n" + str(len(current_data)), use_container_width=True):
            st.session_state.nav_view = "Exec_Total"
            st.rerun()
    with c2:
        pos_count = len(current_data[current_data['Sentiment'] == 'Positive'])
        if st.button("📈\n\nPositive Coverage\n" + str(pos_count), use_container_width=True):
            st.session_state.nav_view = "Exec_Positive"
            st.rerun()
    with c3:
        if st.button("⚡\n\nCritical Alerts\n" + str(crit_items), use_container_width=True):
            st.session_state.nav_view = "Exec_Critical"
            st.rerun()
    with c4:
        reg_count = current_data["Region"].nunique()
        if st.button("📍\n\nActive Regions\n" + str(reg_count), use_container_width=True):
            st.session_state.nav_view = "Exec_Regions"
            st.rerun()
            
    st.markdown("---")
    fig_reg = px.bar(current_data.groupby("Region")["Sentiment"].count().reset_index(), x="Region", y="Sentiment", title="Media Volume by Region", template="plotly_dark")
    st.plotly_chart(fig_reg, use_container_width=True)

elif st.session_state.nav_view == "Exec_Total":
    st.subheader("📚 Analysis Detail: All Total Media Items")
    if st.button("⬅️ Back to Analysis Summary"):
        st.session_state.nav_view = "Executive"
        st.rerun()
    st.dataframe(
        current_data[["Date", "Media Type", "Source/Outlet", "Region", "Excerpt", "Sentiment", "Source URL"]],
        column_config={
            "Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")
        },
        use_container_width=True
    )

elif st.session_state.nav_view == "Exec_Positive":
    st.subheader("🟢 Analysis Detail: Positive Coverage Stream")
    if st.button("⬅️ Back to Analysis Summary"):
        st.session_state.nav_view = "Executive"
        st.rerun()
    pos_df = current_data[current_data["Sentiment"] == "Positive"]
    st.dataframe(
        pos_df[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
        column_config={
            "Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")
        },
        use_container_width=True
    )

elif st.session_state.nav_view == "Exec_Critical":
    st.subheader("🚨 Analysis Detail: Unique Critical Alerts Stream")
    if st.button("⬅️ Back to Analysis Summary"):
        st.session_state.nav_view = "Executive"
        st.rerun()
    st.dataframe(
        unique_crit_df[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
        column_config={
            "Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")
        },
        use_container_width=True
    )

elif st.session_state.nav_view == "Exec_Regions":
    st.subheader("🗺️ Analysis Detail: Currently Scanned Active Regions")
    if st.button("⬅️ Back to Analysis Summary"):
        st.session_state.nav_view = "Executive"
        st.rerun()
    regions_summary = current_data.groupby("Region").agg(
        Total_Items=("Sentiment", "count"),
        Critical_Count=("Crisis Alert", lambda x: (x == "CRITICAL").sum()),
        Positive_Count=("Sentiment", lambda x: (x == "Positive").sum())
    ).reset_index()
    st.dataframe(regions_summary, use_container_width=True)

elif st.session_state.nav_view == "Channels":
    st.subheader("Monitored Multi-Media Stream")
    st.dataframe(current_data[["Date", "Media Type", "Source/Outlet", "Region", "Sentiment"]], use_container_width=True)

elif st.session_state.nav_view == "Trends":
    st.subheader("Daily Ingestion Progression")
    trend_df = current_data.groupby(["Date", "Sentiment"]).size().reset_index(name="Count")
    fig_trend = px.line(trend_df, x="Date", y="Count", color="Sentiment", markers=True, title="Sentiment Shifts Over Time", template="plotly_dark")
    st.plotly_chart(fig_trend, use_container_width=True)

elif st.session_state.nav_view == "Crisis":
    st.subheader("Active Crisis & Risk Table (Live Portal Links)")
    if not unique_crit_df.empty:
        st.dataframe(
            unique_crit_df[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
            column_config={
                "Source URL": st.column_config.LinkColumn(
                    "Portal Action",
                    help="Click to open source portal",
                    display_text="🔗 Open Portal"
                )
            },
            use_container_width=True
        )
    else:
        st.info("No active crisis items flagged in current database stream.")

elif st.session_state.nav_view == "Sentiment":
    st.subheader("Sentiment Classification Distribution")
    
    sent_counts = current_data["Sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Count"]
    
    color_map = {
        "Positive": "#2ecc71",
        "Neutral": "#f1c40f",
        "Negative": "#e74c3c"
    }
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=sent_counts["Sentiment"],
        values=sent_counts["Count"],
        hole=0.6,
        marker=dict(colors=[color_map.get(x, "#3498db") for x in sent_counts["Sentiment"]], line=dict(color="#0d1b2a", width=3)),
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        textfont=dict(size=14, color="#ffffff"),
        pull=[0.06 if x == "Negative" else 0.0 for x in sent_counts["Sentiment"]]
    )])
    
    fig_pie.update_layout(
        title=dict(text="Sentiment Breakdown Matrix", font=dict(size=16, color="#00e5ff")),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text=f"Total<br>{len(current_data)}", x=0.5, y=0.5, font=dict(size=15, color="#ffffff"), showarrow=False)]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Categorized Sentiment Alert Streams")
    
    tab_pos, tab_neut, tab_neg = st.tabs(["🟢 Positive Alerts", "🟡 Neutral Alerts", "🚨 Negative Alerts"])
    
    with tab_pos:
        pos_subset = current_data[current_data["Sentiment"] == "Positive"]
        st.markdown(f"**Total Positive Items:** {len(pos_subset)}")
        st.dataframe(
            pos_subset[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
            column_config={"Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")},
            use_container_width=True
        )
        
    with tab_neut:
        neut_subset = current_data[current_data["Sentiment"] == "Neutral"]
        st.markdown(f"**Total Neutral Items:** {len(neut_subset)}")
        st.dataframe(
            neut_subset[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
            column_config={"Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")},
            use_container_width=True
        )
        
    with tab_neg:
        neg_subset = current_data[current_data["Sentiment"] == "Negative"]
        st.markdown(f"**Total Negative Items:** {len(neg_subset)}")
        st.dataframe(
            neg_subset[["Date", "Source/Outlet", "Region", "Excerpt", "Source URL"]],
            column_config={"Source URL": st.column_config.LinkColumn("Portal Link", display_text="🔗 Open Portal")},
            use_container_width=True
        )