# app.py - Enhanced Streamlit Web Application
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Open-Source Issue Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.stDataFrame {
    border: 1px solid #e0e0e0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data(ttl=3600)  # Cache the data for 1 hour
def load_data():
    """Loads the issues.csv file from the GitHub repository."""
    csv_url = "https://raw.githubusercontent.com/andyresonner/automated-issue-finder/main/issues.csv"
    try:
        df = pd.read_csv(csv_url)
        # Convert date columns if they exist
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        if 'updated_at' in df.columns:
            df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def check_data_freshness():
    """Check when the data was last updated."""
    try:
        api_url = "https://api.github.com/repos/andyresonner/automated-issue-finder/commits?path=issues.csv&per_page=1"
        response = requests.get(api_url)
        if response.status_code == 200:
            commit_data = response.json()[0]
            last_updated = commit_data['commit']['committer']['date']
            return pd.to_datetime(last_updated)
    except:
        pass
    return None

# --- UI Layout ---
st.title("🚀 Automated Open-Source Issue Finder")
st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h4 style='margin: 0; color: white;'>Find Your Next Open-Source Contribution</h4>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Discover beginner-friendly issues from popular repositories, updated daily to help new contributors get started.</p>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_data()
last_update = check_data_freshness()

if not df.empty:
    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filter Issues")
    
    # Data freshness indicator
    if last_update:
        st.sidebar.success(f"Data last updated: {last_update.strftime('%Y-%m-%d %H:%M UTC')}")
    
    # Repository filter
    all_repos = sorted(df['repository'].unique())
    selected_repos = st.sidebar.multiselect(
        "📚 Select Repositories", 
        all_repos, 
        default=all_repos[:10] if len(all_repos) > 10 else all_repos,
        help="Choose which repositories to display"
    )
    
    # Search filter
    search_term = st.sidebar.text_input(
        "🔎 Search in titles", 
        placeholder="e.g., 'documentation', 'bug fix'",
        help="Search for specific terms in issue titles"
    )
    
    # Language filter (if available)
    if 'language' in df.columns:
        all_languages = sorted(df['language'].dropna().unique())
        if len(all_languages) > 0:
            selected_languages = st.sidebar.multiselect(
                "💻 Programming Languages",
                all_languages,
                default=all_languages,
                help="Filter by programming language"
            )
    
    # Label filter (if available)
    if 'labels' in df.columns:
        # Extract unique labels from comma-separated values
        all_labels = set()
        for labels_str in df['labels'].dropna():
            if isinstance(labels_str, str):
                all_labels.update([label.strip() for label in labels_str.split(',')])
        
        if all_labels:
            selected_labels = st.sidebar.multiselect(
                "🏷️ Issue Labels",
                sorted(all_labels),
                help="Filter by GitHub labels"
            )
    
    # --- Apply Filters ---
    filtered_df = df[df['repository'].isin(selected_repos)]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False)
        ]
    
    if 'language' in df.columns and 'selected_languages' in locals():
        filtered_df = filtered_df[filtered_df['language'].isin(selected_languages)]
    
    if 'labels' in df.columns and 'selected_labels' in locals() and selected_labels:
        mask = filtered_df['labels'].apply(
            lambda x: any(label in str(x) for label in selected_labels) if pd.notna(x) else False
        )
        filtered_df = mask[mask].index
        filtered_df = df.loc[filtered_df]
    
    # --- Analytics Dashboard ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Issues", len(filtered_df), delta=f"of {len(df)} total")
    
    with col2:
        if not filtered_df.empty:
            unique_repos = filtered_df['repository'].nunique()
            st.metric("📚 Repositories", unique_repos)
    
    with col3:
        if 'language' in filtered_df.columns:
            unique_languages = filtered_df['language'].nunique()
            st.metric("💻 Languages", unique_languages)
    
    with col4:
        if 'created_at' in filtered_df.columns:
            recent_issues = filtered_df[
                filtered_df['created_at'] > (datetime.now() - pd.Timedelta(days=7))
            ]
            st.metric("🆕 This Week", len(recent_issues))
    
    # --- Visualizations ---
    if len(filtered_df) > 0:
        st.header("📈 Issue Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Repository Distribution", "Language Breakdown", "Timeline"])
        
        with tab1:
            if len(filtered_df) > 0:
                repo_counts = filtered_df['repository'].value_counts().head(10)
                fig = px.bar(
                    x=repo_counts.values, 
                    y=repo_counts.index,
                    orientation='h',
                    title="Top 10 Repositories by Issue Count",
                    labels={'x': 'Number of Issues', 'y': 'Repository'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if 'language' in filtered_df.columns and not filtered_df['language'].isna().all():
                lang_counts = filtered_df['language'].value_counts().head(8)
                fig = px.pie(
                    values=lang_counts.values,
                    names=lang_counts.index,
                    title="Programming Language Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            if 'created_at' in filtered_df.columns:
                # Group by date and count issues
                daily_counts = filtered_df.groupby(
                    filtered_df['created_at'].dt.date
                ).size().reset_index(name='count')
                
                if len(daily_counts) > 1:
                    fig = px.line(
                        daily_counts,
                        x='created_at',
                        y='count',
                        title="Issue Creation Timeline",
                        labels={'created_at': 'Date', 'count': 'Issues Created'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # --- Display Data ---
    st.header("📋 Latest Beginner-Friendly Issues")
    
    if len(filtered_df) > 0:
        # Sort options
        sort_col1, sort_col2 = st.columns(2)
        
        with sort_col1:
            sort_by = st.selectbox(
                "Sort by:",
                options=['created_at', 'updated_at', 'title', 'repository'] if 'created_at' in filtered_df.columns else ['title', 'repository'],
                index=0
            )
        
        with sort_col2:
            sort_order = st.selectbox("Order:", ["Descending", "Ascending"])
        
        # Apply sorting
        ascending = sort_order == "Ascending"
        if sort_by in filtered_df.columns:
            filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
        
        st.write(f"Displaying **{len(filtered_df)}** of **{len(df)}** issues.")
        
        # Configure columns for better display
        column_config = {
            "url": st.column_config.LinkColumn("Issue URL", display_text="🔗 Open"),
            "title": st.column_config.TextColumn("Title", width="large"),
            "repository": st.column_config.TextColumn("Repository", width="medium"),
        }
        
        if 'created_at' in filtered_df.columns:
            column_config["created_at"] = st.column_config.DatetimeColumn(
                "Created", format="MMM DD, YYYY"
            )
        
        if 'language' in filtered_df.columns:
            column_config["language"] = st.column_config.TextColumn("Language", width="small")
        
        # Display the filtered dataframe
        st.dataframe(
            filtered_df,
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
        
        # Export options
        st.header("📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📊 Download as CSV",
                data=csv,
                file_name=f"issues_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Create a summary report
            summary = f"""
# Issue Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Statistics
- Total Issues: {len(filtered_df)}
- Unique Repositories: {filtered_df['repository'].nunique()}
- Search Term: {search_term if search_term else 'None'}

## Top Repositories
{filtered_df['repository'].value_counts().head(5).to_string()}
            """
            
            st.download_button(
                label="📄 Download Summary",
                data=summary,
                file_name=f"issue_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    else:
        st.info("No issues match your current filters. Try adjusting your search criteria.")
        
        # Suggestions
        st.subheader("💡 Suggestions")
        st.write("- Try removing some filters")
        st.write("- Use broader search terms")
        st.write("- Select more repositories")

else:
    st.warning("⚠️ No data available or failed to load. Please check back later.")
    
    # Debug information
    with st.expander("🔍 Debug Information"):
        st.write("If this issue persists, please check:")
        st.write("- GitHub repository accessibility")
        st.write("- CSV file existence and format")
        st.write("- Network connectivity")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Made with ❤️ for the open-source community | Data updates every 24 hours</p>
    <p>Found a bug or have suggestions? <a href='https://github.com/andyresonner/automated-issue-finder' target='_blank'>Contribute on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
