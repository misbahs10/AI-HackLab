"""
Food Delivery Analytics Challenge - Streamlit Dashboard (Bonus Feature)
Author: Misbah Sajjad

Run with:  streamlit run app.py
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================
# CUSTOM STYLING
# ==============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(160deg, #FDF6EC 0%, #FBEFE3 40%, #F3E8FA 100%);
    }

    /* Hero header */
    .hero {
        background: linear-gradient(120deg, #FF5F6D 0%, #FF9A44 35%, #FFC93C 70%, #6DD5FA 100%);
        padding: 2.3rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 28px rgba(255, 111, 97, 0.30);
    }
    .hero h1 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .hero p {
        color: rgba(255,255,255,0.95);
        font-size: 1.08rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-weight: 500;
    }

    /* KPI cards - each gets its own gradient via nth-child */
    .kpi-card {
        border-radius: 18px;
        padding: 1.3rem 1rem;
        text-align: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.10);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        color: white;
    }
    .kpi-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 26px rgba(0,0,0,0.18);
    }
    .kpi-1 { background: linear-gradient(135deg, #FF6B6B, #FF8E53); }
    .kpi-2 { background: linear-gradient(135deg, #4E65FF, #92EFFD); }
    .kpi-3 { background: linear-gradient(135deg, #43CBFF, #9708CC); }
    .kpi-4 { background: linear-gradient(135deg, #38EF7D, #11998E); }
    .kpi-5 { background: linear-gradient(135deg, #F857A6, #FF5858); }

    .kpi-icon { font-size: 1.7rem; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.15)); }
    .kpi-value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.65rem;
        font-weight: 800;
        margin: 0.25rem 0;
        text-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .kpi-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
        opacity: 0.95;
    }

    /* Section headers */
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.35rem;
        background: linear-gradient(90deg, #FF6B6B, #6D5BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0.6rem;
        margin-bottom: 0.9rem;
        display: inline-block;
    }

    /* Insight cards - alternating colorful left borders */
    .insight-card {
        background: white;
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.07);
        font-size: 0.98rem;
        color: #333;
    }
    .insight-card:nth-of-type(5n+1) { border-left: 6px solid #FF6B6B; }
    .insight-card:nth-of-type(5n+2) { border-left: 6px solid #4E65FF; }
    .insight-card:nth-of-type(5n+3) { border-left: 6px solid #11998E; }
    .insight-card:nth-of-type(5n+4) { border-left: 6px solid #F857A6; }
    .insight-card:nth-of-type(5n+5) { border-left: 6px solid #FFA940; }

    /* Answer box */
    .answer-box {
        background: linear-gradient(135deg, #FFEAA7, #FFB88C);
        border-radius: 16px;
        padding: 1.1rem 1.4rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: #6B3E00;
        box-shadow: 0 4px 14px rgba(255, 184, 140, 0.35);
    }

    /* AI explanation box */
    .ai-box {
        background: linear-gradient(135deg, #A8FF78, #78FFD6);
        border-radius: 16px;
        padding: 1.3rem 1.5rem;
        color: #0B3D2E;
        font-size: 1rem;
        line-height: 1.65;
        font-weight: 500;
        box-shadow: 0 4px 14px rgba(120, 255, 214, 0.35);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 700;
        border-radius: 10px 10px 0 0 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #FF6B6B, #FFA940) !important;
        color: white !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #6D5BFF, #FF6B6B) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(109, 91, 255, 0.35);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2b2d42 0%, #3d2c5e 100%);
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] hr {
        color: #eaeaf0 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #2b2d42 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-radius: 8px;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] li * {
        color: #2b2d42 !important;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQ = ["#FF6B6B", "#FFA940", "#FFD93D", "#38EF7D", "#4E65FF", "#9708CC", "#F857A6", "#43CBFF"]

# ==============================================================
# LOAD & CLEAN DATA
# ==============================================================
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("food_delivery_dataset.csv")

    df["Delivery_person_Age"] = df["Delivery_person_Age"].fillna(
        df["Delivery_person_Age"].median()
    ).astype(int)
    df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].fillna(
        df["Delivery_person_Ratings"].median()
    )
    df["Time_Orderd"] = df["Time_Orderd"].fillna("Unknown")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y", errors="coerce")

    text_cols = ["Weather_conditions", "Road_traffic_density", "Type_of_order",
                 "Type_of_vehicle", "Festival", "City", "delivery_speed"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    df = df.drop_duplicates()
    df = df[(df["Time_taken (min)"] > 0) & (df["distance_km"] > 0)]
    return df


df = load_and_clean_data()

# ==============================================================
# SIDEBAR FILTERS
# ==============================================================
st.sidebar.markdown("## 🍔 Delivery Analytics")
st.sidebar.markdown("### 🔍 Filters")

city_options = ["All"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("City", city_options)

weather_options = ["All"] + sorted(df["Weather_conditions"].unique().tolist())
selected_weather = st.sidebar.selectbox("Weather", weather_options)

traffic_options = ["All"] + sorted(df["Road_traffic_density"].unique().tolist())
selected_traffic = st.sidebar.selectbox("Traffic Density", traffic_options)

vehicle_options = ["All"] + sorted(df["Type_of_vehicle"].unique().tolist())
selected_vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_options)

festival_options = ["All"] + sorted(df["Festival"].unique().tolist())
selected_festival = st.sidebar.selectbox("Festival", festival_options)

filtered = df.copy()
if selected_city != "All":
    filtered = filtered[filtered["City"] == selected_city]
if selected_weather != "All":
    filtered = filtered[filtered["Weather_conditions"] == selected_weather]
if selected_traffic != "All":
    filtered = filtered[filtered["Road_traffic_density"] == selected_traffic]
if selected_vehicle != "All":
    filtered = filtered[filtered["Type_of_vehicle"] == selected_vehicle]
if selected_festival != "All":
    filtered = filtered[filtered["Festival"] == selected_festival]

st.sidebar.markdown("---")
st.sidebar.markdown(f"📦 **{len(filtered):,}** deliveries match your filters")
st.sidebar.markdown("---")
st.sidebar.caption("Hackathon Task A · AI & Data Science")

# ==============================================================
# HERO HEADER
# ==============================================================
st.markdown("""
<div class="hero">
    <h1>🍔 Food Delivery Analytics Dashboard</h1>
    <p>Turning raw delivery data into business decisions — Python, Pandas & AI</p>
</div>
""", unsafe_allow_html=True)

if len(filtered) == 0:
    st.warning("No data matches the selected filters. Please widen your filter selection.")
    st.stop()

# ==============================================================
# KPI METRICS
# ==============================================================
avg_speed = (filtered["distance_km"] / (filtered["Time_taken (min)"] / 60)).mean()

kpis = [
    ("📦", f"{len(filtered):,}", "Total Deliveries", "kpi-1"),
    ("⏱️", f"{filtered['Time_taken (min)'].mean():.1f} min", "Avg Delivery Time", "kpi-2"),
    ("📏", f"{filtered['distance_km'].mean():.1f} km", "Avg Distance", "kpi-3"),
    ("🚴", f"{avg_speed:.1f} km/h", "Avg Speed", "kpi-4"),
    ("⭐", f"{filtered['Delivery_person_Ratings'].mean():.2f}", "Avg Rating", "kpi-5"),
]

cols = st.columns(len(kpis))
for col, (icon, value, label, css_class) in zip(cols, kpis):
    col.markdown(f"""
    <div class="kpi-card {css_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ==============================================================
# COMPETITION QUESTIONS
# ==============================================================
st.markdown('<div class="section-title">📋 Competition Questions</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚦 Q1 — Traffic Impact", "📏 Q2 — Distance Impact", "🌦️ Q3 — Combined Conditions"])

with tab1:
    traffic_avg = filtered.groupby("Road_traffic_density")["Time_taken (min)"].mean().sort_values(ascending=False)
    st.markdown(f"""<div class="answer-box">🏆 Highest average delivery time: <b>{traffic_avg.index[0]}</b>
    traffic ({traffic_avg.iloc[0]:.2f} min)</div>""", unsafe_allow_html=True)
    st.write("")
    order = [c for c in ["Low", "Medium", "High", "Jam"] if c in traffic_avg.index]
    plot_df = traffic_avg.reindex(order).reset_index()
    fig = px.bar(plot_df, x="Road_traffic_density", y="Time_taken (min)",
                 color="Road_traffic_density",
                 color_discrete_sequence=["#38EF7D", "#FFD93D", "#FFA940", "#FF6B6B"],
                 text_auto=".1f", template=PLOTLY_TEMPLATE)
    fig.update_layout(showlegend=False, title="Average Delivery Time by Traffic Density",
                       xaxis_title="Traffic Density", yaxis_title="Minutes", height=420)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    correlation = filtered["distance_km"].corr(filtered["Time_taken (min)"])
    st.markdown(f"""<div class="answer-box">📊 Correlation between distance and delivery time:
    <b>{correlation:.3f}</b></div>""", unsafe_allow_html=True)
    st.write("")
    sample = filtered.sample(n=min(2500, len(filtered)), random_state=42)
    fig = px.scatter(sample, x="distance_km", y="Time_taken (min)",
                      color="Road_traffic_density", opacity=0.55,
                      color_discrete_sequence=COLOR_SEQ, template=PLOTLY_TEMPLATE)
    fig.update_layout(title="Delivery Distance vs Delivery Time",
                       xaxis_title="Distance (km)", yaxis_title="Time Taken (minutes)", height=450)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    combo = (filtered.groupby(["Weather_conditions", "Road_traffic_density"])["Time_taken (min)"]
             .mean().sort_values(ascending=False))
    st.markdown(f"""<div class="answer-box">⚠️ Worst combination: <b>{combo.index[0][0]}</b> weather +
    <b>{combo.index[0][1]}</b> traffic ({combo.iloc[0]:.2f} min)</div>""", unsafe_allow_html=True)
    st.write("")
    heat_data = filtered.pivot_table(values="Time_taken (min)", index="Weather_conditions",
                                      columns="Road_traffic_density", aggfunc="mean")
    order = [c for c in ["Low", "Medium", "High", "Jam"] if c in heat_data.columns]
    heat_data = heat_data[order] if order else heat_data
    fig = px.imshow(heat_data, text_auto=".1f", color_continuous_scale="Sunsetdark",
                     template=PLOTLY_TEMPLATE, aspect="auto")
    fig.update_layout(title="Avg Delivery Time (min): Weather × Traffic", height=430)
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ==============================================================
# EXTRA ANALYSIS
# ==============================================================
st.markdown('<div class="section-title">📊 Extra Analysis</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    city_avg = filtered.groupby("City")["Time_taken (min)"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(city_avg, x="City", y="Time_taken (min)", color="City",
                 color_discrete_sequence=COLOR_SEQ, text_auto=".1f", template=PLOTLY_TEMPLATE)
    fig.update_layout(showlegend=False, title="Avg Delivery Time by City", height=380)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fest_avg = filtered.groupby("Festival")["Time_taken (min)"].mean().reset_index()
    fig = px.bar(fest_avg, x="Festival", y="Time_taken (min)", color="Festival",
                 color_discrete_sequence=["#4E65FF", "#F857A6"], text_auto=".1f", template=PLOTLY_TEMPLATE)
    fig.update_layout(showlegend=False, title="Festival vs Normal Days", height=380)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    vehicle_avg = filtered.groupby("Type_of_vehicle")["Time_taken (min)"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(vehicle_avg, x="Type_of_vehicle", y="Time_taken (min)", color="Type_of_vehicle",
                 color_discrete_sequence=COLOR_SEQ, text_auto=".1f", template=PLOTLY_TEMPLATE)
    fig.update_layout(showlegend=False, title="Avg Delivery Time by Vehicle Type", height=380)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    multi_avg = filtered.groupby("multiple_deliveries")["Time_taken (min)"].mean().sort_index().reset_index()
    fig = px.line(multi_avg, x="multiple_deliveries", y="Time_taken (min)", markers=True,
                  template=PLOTLY_TEMPLATE, color_discrete_sequence=["#FF6B35"])
    fig.update_layout(title="Delivery Time vs Number of Multiple Deliveries", height=380)
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ==============================================================
# BUSINESS INSIGHTS
# ==============================================================
st.markdown('<div class="section-title">💡 Business Insights</div>', unsafe_allow_html=True)

traffic_avg_full = filtered.groupby("Road_traffic_density")["Time_taken (min)"].mean()
festival_avg_full = filtered.groupby("Festival")["Time_taken (min)"].mean()
city_avg_full = filtered.groupby("City")["Time_taken (min)"].mean()

insight_points = []
if "Jam" in traffic_avg_full.index and "Low" in traffic_avg_full.index:
    diff = traffic_avg_full["Jam"] - traffic_avg_full["Low"]
    insight_points.append(f"🚦 Traffic jams add <b>~{diff:.1f} extra minutes</b> per delivery vs. low-traffic conditions.")
if "Yes" in festival_avg_full.index and "No" in festival_avg_full.index:
    insight_points.append(
        f"🎉 Festival deliveries take <b>{festival_avg_full['Yes']:.1f} min</b> on average vs. "
        f"<b>{festival_avg_full['No']:.1f} min</b> on normal days.")
insight_points.append(
    f"📏 Distance and delivery time have a correlation of "
    f"<b>{filtered['distance_km'].corr(filtered['Time_taken (min)']):.2f}</b> in the current filtered data.")
if len(city_avg_full) > 1:
    insight_points.append(
        f"🏙️ <b>{city_avg_full.idxmax()}</b> has the slowest average delivery time "
        f"({city_avg_full.max():.1f} min), while <b>{city_avg_full.idxmin()}</b> is fastest "
        f"({city_avg_full.min():.1f} min).")

for point in insight_points:
    st.markdown(f'<div class="insight-card">{point}</div>', unsafe_allow_html=True)

st.write("")

# ==============================================================
# AI-POWERED EXPLANATION (Groq)
# ==============================================================
st.markdown('<div class="section-title">🤖 AI-Powered Business Explanation</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 1])
with col_a:
    api_key_input = st.text_input("Groq API Key", type="password",
                                   value=os.environ.get("GROQ_API_KEY", ""),
                                   placeholder="Paste your Groq API key here (not stored)")
with col_b:
    st.write("")
    st.write("")
    generate = st.button("✨ Generate Explanation", use_container_width=True)

if generate:
    if not api_key_input:
        st.error("Please enter a Groq API key first.")
    else:
        with st.spinner("Asking the AI to explain the findings..."):
            from groq import Groq
            client = Groq(api_key=api_key_input)

            summary_for_ai = f"""
            Total deliveries: {len(filtered)}
            Average delivery time: {filtered['Time_taken (min)'].mean():.2f} minutes
            Average distance: {filtered['distance_km'].mean():.2f} km
            Traffic with highest avg time: {traffic_avg_full.idxmax()} ({traffic_avg_full.max():.2f} min)
            """
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are a business analyst. Explain data findings "
                                                   "in simple, clear language for a food-delivery company's management."},
                    {"role": "user", "content": f"Here are the calculated results:\n{summary_for_ai}\n"
                                                 f"Write a short (5-6 sentence) business explanation."}
                ],
            )
            st.markdown(f'<div class="ai-box">{response.choices[0].message.content}</div>',
                        unsafe_allow_html=True)

st.write("")
st.markdown("---")
st.caption("Built with Python, Pandas, Plotly, Streamlit & Groq AI — Hackathon Task A · Food Delivery Analytics Challenge")