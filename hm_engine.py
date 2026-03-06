# hm_engine.py
import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Political Violence Heatmap",
    layout="wide",
    page_icon="🌎"
)

# ---- STYLING ----
st.markdown("""
<style>
/* ---- APP BACKGROUND ---- */
.stApp {
    background: linear-gradient(135deg, #fdf6f0, #b5f0e0); /* fun soft gradient */
}

/* ---- METRIC CARDS ---- */
div[data-testid="stMetric"] {
    background-color: #1f2937;   /* dark slate */
    color: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
}

/* Metric title (heading above number) */
div[data-testid="stMetric"] p {
    color: #ffffff !important;
    font-weight: bold;
    margin: 0;
}

/* Metric value */
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff; /* bright white */
}

/* ---- PLOTLY CHART CONTAINER ---- */
[data-testid="stPlotlyChart"] {
    background-color: white;  
    border: none;
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background-color: #14b8a6; /* soft teal */
    color: white;
    border-radius: 0;
    padding: 1rem;
}

/* Sidebar headers & labels */
section[data-testid="stSidebar"] label, 
section[data-testid="stSidebar"] .stMarkdown p, 
.stSidebarHeader {
    color: #ffffff !important; /* bright white */
    font-weight: bold;
}

/* Sidebar inputs / selectbox / multiselect / sliders / text inputs */
[data-baseweb="select"], .stSlider, .stTextInput, .stNumberInput {
    border-radius: 10px !important;
    border: none !important;
    background-color: #ffffff !important; /* dark input background */
    color: black !important;
    padding: 6px 8px; /* internal padding */
}

/* ---- SELECT YEAR PADDING ONLY ---- */
/* Remove previous global padding on all filters if any */
/* .stExpanderContent, .stSelectbox, .stMultiSelect, .stSlider { padding: 5px 10px !important; } */

/* Padding scoped only to the "Select Year" input container */
div[data-testid="stForm"] label span:contains("Select Year") {
    display: block;
}

</style>
""", unsafe_allow_html=True)

st.title("🌎 Political Violence Heatmap")
st.divider()
st.markdown("""
This interactive heatmap shows political violence events around the world.
Hover over a country to see details, including its category, number of events, rank, and % of world events.
""")

# ---- LOAD FULL MULTI-YEAR DATASET ----
df = pd.read_csv("pv_global_events.csv")  # generated from Excel

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filters")

# Year slider
st.sidebar.markdown("**Select Year**")
year_filter = st.sidebar.select_slider(
    "Select Year",
    options=sorted(df["YEAR"].unique()),
    value=max(df["YEAR"])
)
df = df[df["YEAR"] == year_filter]

# Optional: Dynamic category based on EVENTS
def categorize(events):
    if events < 100: return "Very Low"
    elif events < 500: return "Low"
    elif events < 1500: return "Moderate"
    elif events < 3000: return "High"
    else: return "Extreme"

df["CATEGORY"] = df["EVENTS"].apply(categorize)

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Violence Category",
    options=df["CATEGORY"].unique(),
    default=df["CATEGORY"].unique()
)
df = df[df["CATEGORY"].isin(category_filter)]

# ---- ADD CONTINENT INFO ----
def country_to_continent(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        code = country.alpha_2
        continent_code = pc.country_alpha2_to_continent_code(code)
        continent_map = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania"
        }
        return continent_map.get(continent_code, "Other")
    except:
        return "Other"

df["CONTINENT"] = df["COUNTRY"].apply(country_to_continent)

# Continent filter
continent_filter = st.sidebar.multiselect(
    "Select Continent",
    options=sorted(df["CONTINENT"].unique()),
    default=sorted(df["CONTINENT"].unique())
)
df = df[df["CONTINENT"].isin(continent_filter)]

# ---- FIX NAMES FOR PLOTLY ----
name_map = {
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People’s Republic of",
    "Russia": "Russian Federation",
    "Iran": "Iran (Islamic Republic of)",
    "Moldova": "Moldova, Republic of",
    "Syria": "Syrian Arab Republic",
    "Laos": "Lao People's Democratic Republic",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Brunei": "Brunei Darussalam",
    "Tanzania": "Tanzania, United Republic of",
    "Eswatini": "Swaziland"
}
df["PLOTLY_NAME"] = df["COUNTRY"].apply(lambda x: name_map.get(x, x))

# ---- ADD RANK & WORLD % ----
df['% of world total'] = df['EVENTS'] / df['EVENTS'].sum() * 100
df['Rank'] = df['EVENTS'].rank(ascending=False, method='min').astype(int)

# ---- GLOBAL METRICS ----
total_events = int(df["EVENTS"].sum())
countries_affected = df.shape[0]
top_country = df.loc[df["EVENTS"].idxmax(), "COUNTRY"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Events", total_events)
col2.metric("Countries Affected", countries_affected)
col3.metric("Most Affected Country", top_country)

# ---- COLOR SCALE ----
color_map = {
    'Very Low': '#2ecc71',
    'Low': '#f1c40f',
    'Moderate': '#e67e22',
    'High': '#e74c3c',
    'Extreme': '#c0392b'
}
category_order = ["Very Low", "Low", "Moderate", "High", "Extreme"]

# ---- HEATMAP FIGURE ----
fig = px.choropleth(
    df,
    locations="PLOTLY_NAME",
    locationmode="country names",
    color="CATEGORY",
    hover_name="COUNTRY",
    hover_data={
        "PLOTLY_NAME": False,
        "CATEGORY": True,
        "EVENTS": ":,",
        "Rank": True,
        "% of world total": ':.2f'
    },
    color_discrete_map=color_map,
    category_orders={"CATEGORY": category_order},
    template=None
)

fig.update_layout(
    title_text=f"Political Violence Events – {year_filter}",
    title_x=0.5,
    geo=dict(
        showframe=False, showcoastlines=True,
        coastlinecolor="grey", showland=True,
        showocean=True, landcolor="#f0f0f0",
        oceancolor="#6aa6d6", projection_type='natural earth'
    ),
    legend=dict(
        orientation="h", yanchor="bottom", y=0.02,
        xanchor="center", x=0.5
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    legend_title_text='Category',
    paper_bgcolor="white",
    plot_bgcolor="#6aa6d6"
)

st.plotly_chart(fig, use_container_width=True)

# ---- COUNTRY ANALYSIS ----
st.divider()
st.subheader("Country Analysis")

selected_country = st.selectbox(
    "Select a country to inspect",
    sorted(df["COUNTRY"].unique())
)
country_data = df[df["COUNTRY"] == selected_country].iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Events", int(country_data["EVENTS"]))
col2.metric("Global Rank", int(country_data["Rank"]))
col3.metric("% of World Events", f"{country_data['% of world total']:.2f}%")
col4.metric("Category", country_data["CATEGORY"])

# Country vs World
st.subheader("Country vs Global Average")
world_avg = df["EVENTS"].mean()
compare_df = pd.DataFrame({
    "Type": ["Selected Country", "Global Average"],
    "Events": [country_data["EVENTS"], world_avg]
})
fig_compare = px.bar(
    compare_df,
    x="Type", y="Events", text="Events", title=f"{selected_country} vs Global Average",
    color="Type",
    color_discrete_map={
        "Selected Country": "#c0392b",
        "Global Average": "#3498db"
    }
)
fig_compare.update_layout(template="simple_white")
st.plotly_chart(fig_compare, use_container_width=True)

# Top 15 Rank chart
st.subheader("Global Rank Position")
rank_df = df.sort_values("Rank").head(15)
fig_rank = px.bar(
    rank_df, x="COUNTRY", y="EVENTS", title="Top 15 Countries by Events",
    color="EVENTS", color_continuous_scale="Reds"
)
fig_rank.update_layout(template="simple_white")
st.plotly_chart(fig_rank, use_container_width=True)

# Top 10 Countries horizontal bar
st.subheader("Top 10 Countries by Political Violence Events")
top10 = df.sort_values("EVENTS", ascending=False).head(10)
fig_bar = px.bar(
    top10, x="EVENTS", y="COUNTRY", orientation="h", text="EVENTS",
    color="EVENTS", color_continuous_scale="Reds"
)
fig_bar.update_layout(yaxis=dict(autorange="reversed"), template="simple_white")
st.plotly_chart(fig_bar, use_container_width=True)

# Optional Data Table
with st.expander("Underlying data"):
    st.dataframe(df.sort_values(by="EVENTS", ascending=False))