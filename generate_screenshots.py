import os
import pandas as pd
import matplotlib.pyplot as plt

# Import static plotting functions from charts.py
from charts import (
    plot_correlation_heatmap_matplotlib,
    plot_load_distributions_matplotlib,
    plot_compactness_vs_loads_matplotlib,
    plot_grouped_loads_matplotlib,
    plot_pairplot_matplotlib
)

def main():
    print("[INFO] Initializing Screenshot Generator...")
    
    # Define paths
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(workspace_dir, "screenshots")
    data_file = os.path.join(workspace_dir, "ENB2012_data.xlsx")
    
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        print(f"[INFO] Created screenshots folder at: {screenshots_dir}")
    else:
        print(f"[INFO] Using existing screenshots folder: {screenshots_dir}")
        
    # Load dataset
    if not os.path.exists(data_file):
        print(f"[ERROR] Dataset file not found at {data_file}")
        return
        
    print("[INFO] Loading building energy dataset...")
    df = pd.read_excel(data_file)
    print(f"[SUCCESS] Loaded dataset successfully. Shape: {df.shape}")
    
    # List of figures to generate and save
    print("\n[INFO] Generating and saving static charts...")
    
    # 1. Correlation Heatmap
    print("  -> Generating Correlation Heatmap...")
    fig_corr = plot_correlation_heatmap_matplotlib(df)
    fig_corr.savefig(os.path.join(screenshots_dir, "correlation_heatmap.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_corr)
    
    # 2. Load Distributions Boxplot
    print("  -> Generating Load Distributions Boxplot...")
    fig_dist = plot_load_distributions_matplotlib(df)
    fig_dist.savefig(os.path.join(screenshots_dir, "load_distributions.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_dist)
    
    # 3. Compactness vs Heating Load Scatter
    print("  -> Generating Compactness vs Heating Load Scatter plot...")
    fig_scat_h = plot_compactness_vs_loads_matplotlib(df, load_type="Heating Load")
    fig_scat_h.savefig(os.path.join(screenshots_dir, "compactness_vs_heating.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_scat_h)
    
    # 4. Compactness vs Cooling Load Scatter
    print("  -> Generating Compactness vs Cooling Load Scatter plot...")
    fig_scat_c = plot_compactness_vs_loads_matplotlib(df, load_type="Cooling Load")
    fig_scat_c.savefig(os.path.join(screenshots_dir, "compactness_vs_cooling.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_scat_c)
    
    # 5. Grouped by Height
    print("  -> Generating Grouped by Height Bar chart...")
    fig_group_h = plot_grouped_loads_matplotlib(df, "X5")
    fig_group_h.savefig(os.path.join(screenshots_dir, "grouped_by_height.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_group_h)
    
    # 6. Grouped by Orientation
    print("  -> Generating Grouped by Orientation Bar chart...")
    fig_group_o = plot_grouped_loads_matplotlib(df, "X6")
    fig_group_o.savefig(os.path.join(screenshots_dir, "grouped_by_orientation.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_group_o)
    
    # 7. Grouped by Glazing Ratio
    print("  -> Generating Grouped by Glazing Ratio Bar chart...")
    fig_group_g = plot_grouped_loads_matplotlib(df, "X7")
    fig_group_g.savefig(os.path.join(screenshots_dir, "grouped_by_glazing.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_group_g)
    
    # 8. Grouped by Glazing Distribution
    print("  -> Generating Grouped by Glazing Distribution Bar chart...")
    fig_group_gd = plot_grouped_loads_matplotlib(df, "X8")
    fig_group_gd.savefig(os.path.join(screenshots_dir, "grouped_by_glazing_distribution.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_group_gd)
    
    # 9. Pairplot Grid
    print("  -> Generating Pairplot Grid (this may take a few seconds)...")
    fig_pair = plot_pairplot_matplotlib(df)
    fig_pair.savefig(os.path.join(screenshots_dir, "pairplot.png"), dpi=150, bbox_inches='tight')
    plt.close(fig_pair)
    
    print(f"\n[SUCCESS] All 9 charts have been saved to: {screenshots_dir}\n")

if __name__ == "__main__":
    main()
