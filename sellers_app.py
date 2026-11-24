"""
Run with:
    pip install streamlit pandas plotly openpyxl
    streamlit run sellers_app.py
(sellers.xlsx must be in the same folder as this file)
"""

# pandas reads the Excel file, plotly draws the charts, streamlit builds the page
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Page title in the browser tab and a wide layout
st.set_page_config(page_title="Sellers dashboard", layout="wide")

# One color per region, so each region looks the same on every chart
COLORS = {"NORTE": "#2a78d6", "SUR": "#eb6834", "ESTE": "#1baf7a", "OESTE": "#6250d6"}


# Read the Excel file once and keep it in memory (cache) so the app stays fast
@st.cache_data
def load_data():
    df = pd.read_excel(Path(__file__).parent / "sellers.xlsx")  # the file next to this script
    df["SELLER"] = df["NAME"] + " " + df["LASTNAME"]  # full name, used in the charts and the seller list
    return df


data = load_data()
regions = list(data["REGION"].unique())  # the four regions in the file

# Sidebar: region filter
# The multiselect starts with every region selected
if "regions" not in st.session_state:
    st.session_state["regions"] = regions


def select_all():
    # Runs when the button is clicked: selects every region again
    st.session_state["regions"] = regions


with st.sidebar:
    st.header("Filters")
    chosen = st.multiselect("Region", regions, key="regions")
    st.button("Select all regions", on_click=select_all)

# Keep only the rows of the chosen regions; stop if none is chosen
df = data[data["REGION"].isin(chosen)]
if df.empty:
    st.warning("Choose at least one region in the sidebar.")
    st.stop()

# Title and summary numbers
st.title("Sellers dashboard")
st.write(f"Showing {len(df)} of {len(data)} sellers.")

# Three numbers side by side that change with the region filter
c1, c2, c3 = st.columns(3)
c1.metric("Sellers", len(df), border=True)
c2.metric("Units sold", f"{df['SOLD UNITS'].sum():,}", border=True)
c3.metric("Total sales", f"{df['TOTAL SALES'].sum():,}", border=True)

# Table
with st.container(border=True):
    st.subheader("Sellers table")
    # Show the filtered table; SALES AVERAGE is shown as a percentage
    st.dataframe(df.drop(columns="SELLER"), hide_index=True,
                 column_config={"SALES AVERAGE": st.column_config.NumberColumn(format="percent")})
    # Button to download the filtered table as a CSV file
    st.download_button("Download table (CSV)", df.drop(columns="SELLER").to_csv(index=False).encode("utf-8-sig"),
                       file_name="sellers.csv", mime="text/csv")

# Charts
with st.container(border=True):
    st.subheader("Charts by seller")
    # One tab per measure; each tab has a bar chart of every seller, highest first, colored by region
    tabs = st.tabs(["Units sold", "Total sales", "Sales average"])
    for tab, column in zip(tabs, ["SOLD UNITS", "TOTAL SALES", "SALES AVERAGE"]):
        with tab:
            fig = px.bar(df, x=column, y="SELLER", color="REGION", orientation="h", color_discrete_map=COLORS,
                         height=20 * len(df) + 150)
            fig.update_yaxes(categoryorder="total ascending", title=None)  # biggest bar on top
            if column == "SALES AVERAGE":
                fig.update_xaxes(tickformat=".0%")  # show the axis as percentages
            st.plotly_chart(fig)
    st.caption("SALES AVERAGE in the file is each seller's share of their region's total sales "
               "(the sellers of each region add up to 100%).")

# One Seller
with st.container(border=True):
    st.subheader("Seller details")
    # List of sellers in the chosen regions, in alphabetical order
    name = st.selectbox("Choose a seller", sorted(df["SELLER"]))
    seller = df[df["SELLER"] == name].iloc[0]  # the row of that seller

    st.write(f"**Region:** {seller['REGION']}, **ID:** {seller['ID']}")
    # The seller's numbers in four boxes
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Income", f"{seller['INCOME']:,}", border=True)
    m2.metric("Units sold", f"{seller['SOLD UNITS']:,}", border=True)
    m3.metric("Total sales", f"{seller['TOTAL SALES']:,}", border=True)
    m4.metric("Sales average", f"{seller['SALES AVERAGE']:.1%}", border=True)
