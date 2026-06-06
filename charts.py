import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Readability mapping for features and loads
FEATURE_LABELS = {
    'X1': 'Relative Compactness',
    'X2': 'Surface Area (m²)',
    'X3': 'Wall Area (m²)',
    'X4': 'Roof Area (m²)',
    'X5': 'Overall Height (m)',
    'X6': 'Orientation',
    'X7': 'Glazing Area Ratio',
    'X8': 'Glazing Area Distribution',
    'Y1': 'Heating Load (kWh/m²)',
    'Y2': 'Cooling Load (kWh/m²)'
}

ORIENTATION_NAMES = {2: "North", 3: "East", 4: "South", 5: "West"}
DISTRIBUTION_NAMES = {0: "Unused", 1: "Uniform", 2: "North", 3: "East", 4: "South", 5: "West"}

# ==========================================
# 📊 INTERACTIVE PLOTLY CHARTS (Streamlit)
# ==========================================

def plot_load_distributions_plotly(df: pd.DataFrame) -> go.Figure:
    """
    Plots the distributions of Heating Load (Y1) and Cooling Load (Y2) using Plotly Box Plots.
    """
    melted = df.melt(
        id_vars=['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8'], 
        value_vars=['Y1', 'Y2'], 
        var_name='Load Type', 
        value_name='Load Value'
    )
    melted['Load Type'] = melted['Load Type'].map({'Y1': 'Heating Load (Y1)', 'Y2': 'Cooling Load (Y2)'})
    
    fig = px.box(
        melted,
        x='Load Type',
        y='Load Value',
        color='Load Type',
        color_discrete_map={'Heating Load (Y1)': '#FF4B4B', 'Cooling Load (Y2)': '#1C83E1'},
        points="all",
        title="Distribution of Heating vs Cooling Loads",
        labels={'Load Value': 'Load (kWh/m²)', 'Load Type': 'Load Type'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(showgrid=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14), tickfont=dict(size=12)),
        title_font=dict(size=16),
        showlegend=False
    )
    return fig


def plot_compactness_vs_loads_plotly(df: pd.DataFrame, load_type='Heating Load') -> go.Figure:
    """
    Plots Relative Compactness (X1) vs Heating/Cooling Load with color mapping for Overall Height (X5).
    """
    y_col = 'Y1' if load_type == 'Heating Load' else 'Y2'
    df_copy = df.copy()
    df_copy['Height'] = df_copy['X5'].map({3.5: '3.5m (Short / 1-Story)', 7.0: '7.0m (Tall / 2-Story)'})
    
    fig = px.scatter(
        df_copy,
        x='X1',
        y=y_col,
        color='Height',
        color_discrete_map={'3.5m (Short / 1-Story)': '#00D2C4', '7.0m (Tall / 2-Story)': '#AB47BC'},
        size=y_col,
        hover_data=['X2', 'X3', 'X4', 'X7', 'X8'],
        title=f"Relative Compactness vs {load_type}",
        labels={'X1': 'Relative Compactness (X1)', y_col: f'{load_type} (kWh/m²)'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14)),
        title_font=dict(size=16)
    )
    return fig


def plot_grouped_loads_plotly(df: pd.DataFrame, group_col: str) -> go.Figure:
    """
    Plots the average Heating and Cooling loads grouped by a categorical/discrete column.
    """
    group_labels = {
        'X5': 'Overall Height (X5)',
        'X6': 'Orientation (X6)',
        'X7': 'Glazing Area Ratio (X7)',
        'X8': 'Glazing Distribution (X8)'
    }
    
    grouped = df.groupby(group_col)[['Y1', 'Y2']].mean().reset_index()
    
    # Map orientation or height for readability
    if group_col == 'X6':
        grouped['Display'] = grouped['X6'].map(ORIENTATION_NAMES)
    elif group_col == 'X5':
        grouped['Display'] = grouped['X5'].map({3.5: '3.5m (Short)', 7.0: '7.0m (Tall)'})
    elif group_col == 'X7':
        grouped['Display'] = grouped['X7'].map(lambda x: f"{int(x*100)}% Glazing")
    elif group_col == 'X8':
        grouped['Display'] = grouped['X8'].map(DISTRIBUTION_NAMES)
    else:
        grouped['Display'] = grouped[group_col].astype(str)
        
    melted = grouped.melt(
        id_vars=['Display'], 
        value_vars=['Y1', 'Y2'], 
        var_name='Load Type', 
        value_name='Average Load'
    )
    melted['Load Type'] = melted['Load Type'].map({'Y1': 'Heating Load', 'Y2': 'Cooling Load'})
    
    fig = px.bar(
        melted,
        x='Display',
        y='Average Load',
        color='Load Type',
        barmode='group',
        color_discrete_map={'Heating Load': '#FF6B6B', 'Cooling Load': '#4D96FF'},
        title=f"Average Loads by {group_labels.get(group_col, group_col)}",
        labels={'Display': group_labels.get(group_col, group_col), 'Average Load': 'Average Load (kWh/m²)'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#E0E0E0',
        xaxis=dict(showgrid=False, title_font=dict(size=14)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(size=14)),
        title_font=dict(size=16)
    )
    return fig


# ==========================================
# 🖼️ STATIC MATPLOTLIB/SEABORN CHARTS (Screenshots)
# ==========================================

def setup_matplotlib_dark_theme(fig, ax):
    """
    Applies a premium dark theme styling to Matplotlib figures.
    """
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#1E2330')
    ax.tick_params(colors='#E0E0E0', which='both', labelsize=10)
    ax.xaxis.label.set_color('#E0E0E0')
    ax.yaxis.label.set_color('#E0E0E0')
    ax.title.set_color('white')
    ax.spines['bottom'].set_color('#444444')
    ax.spines['left'].set_color('#444444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(color='#333333', linestyle='--', linewidth=0.5, alpha=0.7)


def plot_correlation_heatmap_matplotlib(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a beautiful correlation matrix heatmap.
    """
    df_renamed = df.rename(columns=FEATURE_LABELS)
    corr = df_renamed.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    setup_matplotlib_dark_theme(fig, ax)
    
    # We want a diverging palette
    sns.heatmap(
        corr,
        annot=True,
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        fmt=".2f",
        linewidths=.5,
        ax=ax,
        cbar_kws={"shrink": .8},
        annot_kws={"size": 9, "weight": "bold"}
    )
    
    # Customize heatmap text colors for readability
    for text in ax.texts:
        text.set_color('#FFFFFF')
        
    ax.set_title("Feature & Output Correlation Matrix", fontsize=14, pad=20, weight="bold")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    return fig


def plot_load_distributions_matplotlib(df: pd.DataFrame) -> plt.Figure:
    """
    Generates boxplots of heating and cooling loads side by side.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    setup_matplotlib_dark_theme(fig, ax)
    
    # Melt dataframe
    melted = df.melt(value_vars=['Y1', 'Y2'], var_name='Load Type', value_name='Load Value')
    melted['Load Type'] = melted['Load Type'].map({'Y1': 'Heating Load (Y1)', 'Y2': 'Cooling Load (Y2)'})
    
    sns.boxplot(
        data=melted,
        x='Load Type',
        y='Load Value',
        ax=ax,
        palette={'Heating Load (Y1)': '#FF4B4B', 'Cooling Load (Y2)': '#1C83E1'},
        width=0.5,
        linewidth=1.5
    )
    
    # Add jittered points
    sns.stripplot(
        data=melted,
        x='Load Type',
        y='Load Value',
        ax=ax,
        color='white',
        size=3,
        alpha=0.3,
        jitter=0.2
    )
    
    ax.set_title("Distribution of Heating and Cooling Loads", fontsize=14, pad=15, weight="bold")
    ax.set_xlabel("Load Type", fontsize=11)
    ax.set_ylabel("Load Value (kWh/m²)", fontsize=11)
    plt.tight_layout()
    return fig


def plot_compactness_vs_loads_matplotlib(df: pd.DataFrame, load_type='Heating Load') -> plt.Figure:
    """
    Generates a scatter plot of Compactness vs Loads colored by building height.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    setup_matplotlib_dark_theme(fig, ax)
    
    y_col = 'Y1' if load_type == 'Heating Load' else 'Y2'
    df_copy = df.copy()
    df_copy['Height'] = df_copy['X5'].map({3.5: '3.5m (Short)', 7.0: '7.0m (Tall)'})
    
    sns.scatterplot(
        data=df_copy,
        x='X1',
        y=y_col,
        hue='Height',
        palette={'3.5m (Short)': '#00D2C4', '7.0m (Tall)': '#AB47BC'},
        size=y_col,
        sizes=(20, 200),
        alpha=0.8,
        ax=ax
    )
    
    # Customise legend
    legend = ax.legend(frameon=True, facecolor='#1E2330', edgecolor='#444444')
    for text in legend.get_texts():
        text.set_color('#E0E0E0')
        
    ax.set_title(f"Relative Compactness vs {load_type} (by Height)", fontsize=14, pad=15, weight="bold")
    ax.set_xlabel("Relative Compactness (X1)", fontsize=11)
    ax.set_ylabel(f"{load_type} (kWh/m²)", fontsize=11)
    plt.tight_layout()
    return fig


def plot_grouped_loads_matplotlib(df: pd.DataFrame, group_col: str) -> plt.Figure:
    """
    Generates a grouped bar chart of average loads.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    setup_matplotlib_dark_theme(fig, ax)
    
    group_labels = {
        'X5': 'Overall Height (X5)',
        'X6': 'Orientation (X6)',
        'X7': 'Glazing Area Ratio (X7)',
        'X8': 'Glazing Distribution (X8)'
    }
    
    grouped = df.groupby(group_col)[['Y1', 'Y2']].mean().reset_index()
    
    if group_col == 'X6':
        grouped['Display'] = grouped['X6'].map(ORIENTATION_NAMES)
    elif group_col == 'X5':
        grouped['Display'] = grouped['X5'].map({3.5: '3.5m (Short)', 7.0: '7.0m (Tall)'})
    elif group_col == 'X7':
        grouped['Display'] = grouped['X7'].map(lambda x: f"{int(x*100)}% Glazing")
    elif group_col == 'X8':
        grouped['Display'] = grouped['X8'].map(DISTRIBUTION_NAMES)
    else:
        grouped['Display'] = grouped[group_col].astype(str)
        
    melted = grouped.melt(
        id_vars=['Display'], 
        value_vars=['Y1', 'Y2'], 
        var_name='Load Type', 
        value_name='Average Load'
    )
    melted['Load Type'] = melted['Load Type'].map({'Y1': 'Heating Load', 'Y2': 'Cooling Load'})
    
    sns.barplot(
        data=melted,
        x='Display',
        y='Average Load',
        hue='Load Type',
        palette={'Heating Load': '#FF6B6B', 'Cooling Load': '#4D96FF'},
        ax=ax
    )
    
    legend = ax.legend(frameon=True, facecolor='#1E2330', edgecolor='#444444')
    for text in legend.get_texts():
        text.set_color('#E0E0E0')
        
    ax.set_title(f"Average Loads by {group_labels.get(group_col, group_col)}", fontsize=14, pad=15, weight="bold")
    ax.set_xlabel(group_labels.get(group_col, group_col), fontsize=11)
    ax.set_ylabel("Average Load (kWh/m²)", fontsize=11)
    plt.tight_layout()
    return fig


def plot_pairplot_matplotlib(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a pairplot showing key relationships between compactness, area, and loads.
    Returns the PairGrid object.
    """
    # Select a subset of variables for a clean pairplot
    subset_df = df[['X1', 'X2', 'X5', 'Y1', 'Y2']].copy()
    subset_df = subset_df.rename(columns={
        'X1': 'Compactness',
        'X2': 'Surface Area',
        'X5': 'Height',
        'Y1': 'Heating Load',
        'Y2': 'Cooling Load'
    })
    subset_df['Height'] = subset_df['Height'].map({3.5: 'Short', 7.0: 'Tall'})
    
    # Set dark theme style for pairplot
    plt.rcParams.update({
        'figure.facecolor': '#0E1117',
        'axes.facecolor': '#1E2330',
        'text.color': 'white',
        'axes.labelcolor': '#E0E0E0',
        'xtick.color': '#E0E0E0',
        'ytick.color': '#E0E0E0',
        'grid.color': '#333333'
    })
    
    g = sns.pairplot(
        subset_df,
        hue='Height',
        palette={'Short': '#00D2C4', 'Tall': '#AB47BC'},
        diag_kind='kde',
        markers=['o', 's']
    )
    
    # Adjust layout
    g.fig.suptitle("Pairwise Relationships of Key Variables", y=1.02, color='white', fontsize=16, weight="bold")
    
    return g.fig
