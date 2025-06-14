# app.py - The Streamlit Web Application

import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Open-Source Issue Finder",
    page_icon="🚀",
    layout="wide",
)

# --- Data Loading ---
@st.cache_data(ttl=3600) # Cache the data for 1 hour
def load_data():
    """Loads the issues.csv file from the GitHub repository."""
    csv_url = "https://raw.githubusercontent.com/andyresonner/automated-issue-finder/main/issues.csv"
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- UI Layout ---
st.title("🚀 Automated Open-Source Issue Finder")
st.write("""
This app displays a daily-updated list of beginner-friendly issues from popular open-source projects.
It's designed to help new contributors find their first project. The data is refreshed every 24 hours.
""")

df = load_data()

if not df.empty:
    # --- Interactive Filters ---
    st.sidebar.header("Filter Issues")
    
    # Filter by repository
    all_repos = df['repository'].unique()
    selected_repos = st.sidebar.multiselect("Select Repositories", all_repos, default=all_repos)
    
    # Filter by text search in title
    search_term = st.sidebar.text_input("Search in issue titles")

    # Apply filters
    filtered_df = df[df['repository'].isin(selected_repos)]
    if search_term:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]

    # --- Display Data ---
    st.header("Latest Beginner-Friendly Issues")
    st.write(f"Displaying {len(filtered_df)} of {len(df)} issues.")
    
    # Display the filtered dataframe with clickable URLs
    st.dataframe(
        filtered_df,
        column_config={
            "url": st.column_config.LinkColumn("Issue URL", display_text="🔗 Link")
        },
        use_container_width=True
    )

else:
    st.warning("No data available or failed to load. Please check back later.")
