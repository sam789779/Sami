import streamlit as st
import pandas as pd
import numpy as np

# Import our custom modules
from filters import render_filters, apply_filters
from charts import (
    plot_load_distributions_plotly,
    plot_compactness_vs_loads_plotly,
    plot_grouped_loads_plotly,
    plot_correlation_heatmap_matplotlib,
    plot_pairplot_matplotlib,
    FEATURE_LABELS
)
from educational_insights import render_educational_insights

# ==========================================
# 🎨 PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Building Energy Efficiency Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Dark slate main app background */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Premium glassmorphic metric card styling */
    div[data-testid="metric-container"] {
        background-color: #1A1F2C;
        border: 1px solid #2A3142;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #00D2C4;
    }
    
    /* Metric label and value colors */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8A99AD !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Styled sidebar background and details */
    section[data-testid="stSidebar"] {
        background-color: #121620 !important;
        border-right: 1px solid #1E2433;
    }
    
    /* Headers typography */
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        letter-spacing: -0.5px;
    }
    
    /* Custom divider line */
    .custom-hr {
        height: 2px;
        background: linear-gradient(90deg, #FF4B4B, #00D2C4);
        margin: 20px 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 💾 DATA LOADING (Cached)
# ==========================================
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Loads the ENB2012 Excel file and returns a Pandas DataFrame."""
    try:
        # Load from local Excel file
        df = pd.read_excel(file_path)
        # Verify columns are correct
        expected_cols = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'Y1', 'Y2']
        # If headers are missing or renamed, let's reset them
        if not all(col in df.columns for col in expected_cols):
            df.columns = expected_cols
        return df
    except Exception as e:
        st.error(f"Error loading Excel data file: {e}")
        return pd.DataFrame()


# Load data
DATA_FILE = "ENB2012_data.xlsx"
df_raw = load_data(DATA_FILE)

# Main Application Frame
if df_raw.empty:
    st.error("Could not load building energy data. Please verify the Excel file is present.")
else:
    # Navigation Router
    st.sidebar.image("https://img.icons8.com/nolan/96/structural.png", width=64)
    st.sidebar.title("Building Analytics")
    
    nav_selection = st.sidebar.radio(
        "Navigate",
        options=["🏠 Overview & Dashboard", "📊 Advanced Analytics", "🎓 Educational Topic Explorer"]
    )
    
    st.sidebar.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
    
    # 🏠 OVERVIEW & DASHBOARD
    if nav_selection == "🏠 Overview & Dashboard":
        # Render sidebar filters and apply them
        filters_dict = render_filters(df_raw)
        df_filtered = apply_filters(df_raw, filters_dict)
        
        # Main header
        st.title("🏢 Building Energy Efficiency Dashboard")
        st.markdown(
            "An interactive analytics dashboard for exploring how architectural design choices "
            "(dimensions, glazing, and orientation) affect building Heating and Cooling energy loads."
        )
        st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
        
        if df_filtered.empty:
            st.warning("⚠️ No buildings match the selected filters. Please expand your filter ranges in the sidebar.")
        else:
            # 📊 KPI Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Selected Buildings", f"{len(df_filtered)}")
            
            avg_heating = df_filtered['Y1'].mean()
            col2.metric("Avg Heating Load", f"{avg_heating:.2f} kWh/m²")
            
            avg_cooling = df_filtered['Y2'].mean()
            col3.metric("Avg Cooling Load", f"{avg_cooling:.2f} kWh/m²")
            
            # Combine loads for total efficiency metric
            avg_total = (df_filtered['Y1'] + df_filtered['Y2']).mean()
            col4.metric("Avg Total Load", f"{avg_total:.2f} kWh/m²")
            
            st.write("")
            st.write("")
            
            # Layout Grid for Charts
            chart_col1, chart_col2 = st.columns([1.1, 0.9])
            
            with chart_col1:
                st.markdown("### 📊 Distribution of Energy Loads")
                st.markdown("A box plot displaying the quartile distribution and individual data points for Heating (Y1) and Cooling (Y2) loads.")
                fig_dist = plot_load_distributions_plotly(df_filtered)
                st.plotly_chart(fig_dist, use_container_width=True, key="overview_dist")
                
            with chart_col2:
                st.markdown("### 🌡️ Building Variable Correlation Matrix")
                st.markdown("A static correlation heatmap showing linear associations between the 8 design features (X1-X8) and 2 load outputs (Y1-Y2).")
                # Correlation Heatmap (using matplotlib)
                fig_corr = plot_correlation_heatmap_matplotlib(df_filtered)
                st.pyplot(fig_corr)
                
            st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
            
            # Data preview & download
            with st.expander("📄 View & Download Filtered Data"):
                st.dataframe(df_filtered)
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv,
                    file_name="filtered_building_data.csv",
                    mime="text/csv"
                )

    # 📊 ADVANCED ANALYTICS
    elif nav_selection == "📊 Advanced Analytics":
        # Render sidebar filters and apply them
        filters_dict = render_filters(df_raw)
        df_filtered = apply_filters(df_raw, filters_dict)
        
        st.title("📊 Detailed Design Variable Analysis")
        st.write("Drill down into structural feature relationships and compare averages across design categories.")
        st.markdown("<div class='custom-hr'></div>", unsafe_allow_html=True)
        
        if df_filtered.empty:
            st.warning("⚠️ No buildings match the selected filters. Please expand your filter ranges in the sidebar.")
        else:
            tab1, tab2, tab3 = st.tabs(["🎯 Compactness vs Loads", "📐 Grouped Category Comparisons", "🔗 Pairwise Relationships"])
            
            with tab1:
                st.subheader("Relative Compactness vs Heating and Cooling Loads")
                st.write(
                    "Relative Compactness represents how compact a shape is (higher value means cube-like, "
                    "lower value means spread-out, flat, or elongated). Observe how it relates to energy loads "
                    "colored by building height (Short 3.5m vs Tall 7.0m)."
                )
                
                scatter_col1, scatter_col2 = st.columns(2)
                with scatter_col1:
                    fig_scat_h = plot_compactness_vs_loads_plotly(df_filtered, load_type="Heating Load")
                    st.plotly_chart(fig_scat_h, use_container_width=True, key="adv_scat_h")
                with scatter_col2:
                    fig_scat_c = plot_compactness_vs_loads_plotly(df_filtered, load_type="Cooling Load")
                    st.plotly_chart(fig_scat_c, use_container_width=True, key="adv_scat_c")
                    
            with tab2:
                st.subheader("Average Loads Grouped by Design Categories")
                st.write(
                    "Select a categorical feature to compare the average Heating and Cooling loads across groups."
                )
                
                group_opt = st.selectbox(
                    "Select Grouping Categorical Variable",
                    options=["X5 (Overall Height)", "X6 (Orientation)", "X7 (Glazing Area Ratio)", "X8 (Glazing Area Distribution)"],
                    index=0
                )
                group_col = group_opt.split(" ")[0]
                
                fig_group = plot_grouped_loads_plotly(df_filtered, group_col)
                st.plotly_chart(fig_group, use_container_width=True, key="adv_group")
                
            with tab3:
                st.subheader("Multivariate Pairplot Grid")
                st.write(
                    "This pairplot visualizes pairwise joint distributions and individual density estimations (KDE) "
                    "for key features: Relative Compactness (X1), Surface Area (X2), Height (X5), Heating Load (Y1), and Cooling Load (Y2)."
                )
                # Show pairplot (Seaborn grid)
                with st.spinner("Generating pairplot grid..."):
                    fig_pair = plot_pairplot_matplotlib(df_filtered)
                    st.pyplot(fig_pair)

    # 🎓 EDUCATIONAL TOPIC EXPLORER
    else:
        # Render the educational insights (passes the raw dataframe so that notebook code examples run on full clean data)
        render_educational_insights(df_raw)
        
    # Footer
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("---")
    st.sidebar.caption("⚡ Crafted with Streamlit & Antigravity")
    st.sidebar.caption("Dataset source: UCI Machine Learning Repository (ENB2012)")
