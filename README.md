Political Violence Heatmap – 2025

This project visualizes political violence events around the world for the year 2025 in an interactive, colorful heatmap.

Hover over a country to see:

Category of political violence (Very Low → Extreme)

Number of events

Rank among all countries

Percentage of world total events

Built with Python, Pandas, Plotly, and Streamlit.

🗂 Project Structure
pv_heatmap/
├─ heatmap_streamlit.py       # Main Streamlit app
├─ pv_2025_categorized.csv    # Processed dataset for 2025
├─ README.md                  # This file
└─ requirements.txt           # Required Python libraries
⚡ Getting Started

Clone the repository:

git clone https://github.com/YOUR_USERNAME/pv_heatmap.git
cd pv_heatmap

Create a virtual environment (recommended):

python -m venv .venv

Activate the environment:

Windows:

.venv\Scripts\activate

Mac/Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the app:

streamlit run heatmap_streamlit.py
📊 Dataset

The dataset pv_2025_categorized.csv contains:

Column	Description
COUNTRY	Name of the country
YEAR	Year (2025)
EVENTS	Number of political violence events
CATEGORY	Violence category (Very Low → Extreme)
ISO3	ISO-3 country code
Rank	Rank based on EVENTS
% of world total	Percentage of world events
🎨 Features

Interactive hover info for each country

Color-coded categories for easy visualization

Land and ocean colors adjusted for a clean, modern look

Optional table to explore underlying data

🛠 Technologies

Python 3.x

Pandas

Plotly

Streamlit

⚠ Notes

The project runs locally via Streamlit.

Make sure the CSV is in the same directory as heatmap_streamlit.py.
