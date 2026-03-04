# heatmap_streamlit_countrynames.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Political Violence Heatmap 2025",
    layout="wide",
    page_icon="🌎"
)

st.title("🌎 Political Violence Heatmap – 2025")
st.markdown("""
This interactive heatmap shows political violence events around the world for 2025.
Hover over a country to see details, including its category, number of events, rank, and % of world events.
""")

# ---- LOAD DATA ----
df = pd.read_csv("pv_2025_categorized.csv")

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
    "Eswatini": "Swaziland"  # older name often recognized
    # You can add more if needed
}

df["PLOTLY_NAME"] = df["COUNTRY"].apply(
    lambda x: name_map[x] if x in name_map else x
)

# ---- ADD RANK & WORLD % ----
df['% of world total'] = df['EVENTS'] / df['EVENTS'].sum() * 100
df['Rank'] = df['EVENTS'].rank(ascending=False, method='min').astype(int)

# ---- COLOR SCALE ----
color_map = {
    'Very Low': '#2ecc71',
    'Low': '#f1c40f',
    'Moderate': '#e67e22',
    'High': '#e74c3c',
    'Extreme': '#c0392b'
}

# ---- PLOTLY FIGURE ----
fig = px.choropleth(
    df,
    locations="PLOTLY_NAME",
    locationmode="country names",
    color="CATEGORY",
    hover_name="COUNTRY",
    hover_data={
        "CATEGORY": True,
        "EVENTS": True,
        "Rank": True,
        "% of world total": ':.2f'
    },
    color_discrete_map=color_map,
    template=None  # remove plotly_dark
)

# Layout tweaks for light/modern look
fig.update_layout(
    title_text="Political Violence Events by Country – 2025",
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="grey",  # subtle coastline
        showland=True,
        showocean=True,
        landcolor="#f0f0f0",  # light grey/white for land
        oceancolor="#6aa6d6",  # soft Earth-blue for oceans
        projection_type='natural earth'
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    legend_title_text='Category',
    paper_bgcolor="white",           # page background
    plot_bgcolor="#6aa6d6"             # plot background
)

# ---- STREAMLIT DISPLAY ----
st.plotly_chart(fig, width='stretch')

# ---- OPTIONAL DATA TABLE ----
with st.expander("Underlying data"):
    st.dataframe(df.sort_values(by="EVENTS", ascending=False))