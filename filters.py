import streamlit as st
import pandas as pd

def render_filters(df: pd.DataFrame) -> dict:
    """
    Renders sidebar widgets for filtering the building energy dataset.
    Returns a dictionary containing the selected filter ranges/values.
    """
    st.sidebar.markdown("### 🔍 Filter Building Designs")
    
    # Initialize reset flag in session state if not present
    if "filters_reset" in st.session_state and st.session_state["filters_reset"]:
        st.session_state["filters_reset"] = False
    
    # Expanders for filters to keep the sidebar tidy
    with st.sidebar.expander("📐 Dimensional Features", expanded=True):
        # Relative Compactness (X1)
        x1_min, x1_max = float(df['X1'].min()), float(df['X1'].max())
        x1_val = st.slider(
            "Relative Compactness (X1)",
            min_value=x1_min,
            max_value=x1_max,
            value=(x1_min, x1_max),
            step=0.01,
            help="Relative compactness of the building shape. Higher means more compact (cube-like)."
        )
        
        # Surface Area (X2)
        x2_min, x2_max = float(df['X2'].min()), float(df['X2'].max())
        x2_val = st.slider(
            "Surface Area (X2) [m²]",
            min_value=x2_min,
            max_value=x2_max,
            value=(x2_min, x2_max),
            step=0.5,
            help="Total surface area of the building."
        )
        
        # Wall Area (X3)
        x3_min, x3_max = float(df['X3'].min()), float(df['X3'].max())
        x3_val = st.slider(
            "Wall Area (X3) [m²]",
            min_value=x3_min,
            max_value=x3_max,
            value=(x3_min, x3_max),
            step=0.5,
            help="Total area of the walls."
        )
        
        # Roof Area (X4)
        x4_min, x4_max = float(df['X4'].min()), float(df['X4'].max())
        x4_val = st.slider(
            "Roof Area (X4) [m²]",
            min_value=x4_min,
            max_value=x4_max,
            value=(x4_min, x4_max),
            step=0.5,
            help="Total area of the roof."
        )

        # Overall Height (X5) - unique heights are 3.5, 7.0
        heights = sorted(df['X5'].unique().tolist())
        heights_selected = st.multiselect(
            "Overall Height (X5) [m]",
            options=heights,
            default=heights,
            format_func=lambda h: f"{h}m ({'Short/1-Story' if h==3.5 else 'Tall/2-Story'})"
        )
        
    with st.sidebar.expander("☀️ Orientation & Glazing", expanded=True):
        # Orientation (X6) - 2: North, 3: East, 4: South, 5: West
        orientation_map = {2: "North", 3: "East", 4: "South", 5: "West"}
        orientations = sorted(df['X6'].unique().tolist())
        orientations_selected = st.multiselect(
            "Orientation (X6)",
            options=orientations,
            default=orientations,
            format_func=lambda o: f"{o} ({orientation_map.get(o, 'Unknown')})"
        )
        
        # Glazing Area (X7) - 0.0, 0.1, 0.25, 0.4
        glazing_areas = sorted(df['X7'].unique().tolist())
        glazing_selected = st.multiselect(
            "Glazing Area Ratio (X7)",
            options=glazing_areas,
            default=glazing_areas,
            format_func=lambda g: f"{int(g*100)}%"
        )
        
        # Glazing Area Distribution (X8) - 0: Unused, 1: Uniform, 2: North, 3: East, 4: South, 5: West
        dist_map = {0: "Unused (No Glazing)", 1: "Uniform", 2: "North", 3: "East", 4: "South", 5: "West"}
        distributions = sorted(df['X8'].unique().tolist())
        distributions_selected = st.multiselect(
            "Glazing Distribution (X8)",
            options=distributions,
            default=distributions,
            format_func=lambda d: f"{d} - {dist_map.get(d, 'Unknown')}"
        )
        
    # Reset button
    if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
        st.session_state["filters_reset"] = True
        st.rerun()

    return {
        "X1": x1_val,
        "X2": x2_val,
        "X3": x3_val,
        "X4": x4_val,
        "X5": heights_selected,
        "X6": orientations_selected,
        "X7": glazing_selected,
        "X8": distributions_selected
    }

def apply_filters(df: pd.DataFrame, selected: dict) -> pd.DataFrame:
    """
    Subsets the building dataframe using the selected dictionary filters.
    Returns the filtered DataFrame.
    """
    filtered_df = df.copy()
    
    # Relative Compactness (X1)
    filtered_df = filtered_df[
        (filtered_df['X1'] >= selected['X1'][0]) & 
        (filtered_df['X1'] <= selected['X1'][1])
    ]
    
    # Surface Area (X2)
    filtered_df = filtered_df[
        (filtered_df['X2'] >= selected['X2'][0]) & 
        (filtered_df['X2'] <= selected['X2'][1])
    ]
    
    # Wall Area (X3)
    filtered_df = filtered_df[
        (filtered_df['X3'] >= selected['X3'][0]) & 
        (filtered_df['X3'] <= selected['X3'][1])
    ]
    
    # Roof Area (X4)
    filtered_df = filtered_df[
        (filtered_df['X4'] >= selected['X4'][0]) & 
        (filtered_df['X4'] <= selected['X4'][1])
    ]
    
    # Overall Height (X5)
    if selected['X5']:
        filtered_df = filtered_df[filtered_df['X5'].isin(selected['X5'])]
    else:
        return pd.DataFrame(columns=df.columns)
        
    # Orientation (X6)
    if selected['X6']:
        filtered_df = filtered_df[filtered_df['X6'].isin(selected['X6'])]
    else:
        return pd.DataFrame(columns=df.columns)
        
    # Glazing Area (X7)
    if selected['X7']:
        filtered_df = filtered_df[filtered_df['X7'].isin(selected['X7'])]
    else:
        return pd.DataFrame(columns=df.columns)
        
    # Glazing Distribution (X8)
    if selected['X8']:
        filtered_df = filtered_df[filtered_df['X8'].isin(selected['X8'])]
    else:
        return pd.DataFrame(columns=df.columns)
        
    return filtered_df
