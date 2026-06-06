import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def render_educational_insights(df: pd.DataFrame):
    """
    Renders an interactive educational portal demonstrating the 24 topics
    using NumPy, Pandas, and Data Visualization.
    """
    st.title("🎓 Interactive Data Science Topic Explorer")
    st.write(
        "Explore how core data science concepts in NumPy, Pandas, and Data Visualization "
        "apply directly to our Building Energy Efficiency dataset. Select a category and a topic below to see live code, explanations, and execution results."
    )

    # Topic Categories
    category = st.radio(
        "Select Category",
        options=["NumPy (Numerical Computing)", "Pandas (Data Wrangling)", "Data Visualization Techniques"],
        horizontal=True
    )

    if category == "NumPy (Numerical Computing)":
        render_numpy_topics(df)
    elif category == "Pandas (Data Wrangling)":
        render_pandas_topics(df)
    else:
        render_viz_topics(df)


# ==========================================
# 🔢 NUMPY TOPICS
# ==========================================
def render_numpy_topics(df: pd.DataFrame):
    topic = st.selectbox(
        "Select NumPy Topic",
        options=[
            "1. Array Creation [Lec-3.01]",
            "2. Array vs List Speed Benchmark [Lec-3.02]",
            "3. Basic Vectorized Operations [Lec-3.03]",
            "4. Array Indexing and Slicing [Lec-3.04]",
            "5. Broadcasting and Reshaping [Lec-3.05]",
            "6. Array Manipulation & Stacking [Lec-3.06]"
        ]
    )

    st.markdown("---")

    if "1. Array Creation" in topic:
        st.subheader("NumPy Array Creation")
        st.write(
            "NumPy arrays are homogeneous, multi-dimensional structures. We can create them from scratch using functions "
            "like `np.zeros()`, `np.ones()`, `np.arange()`, or by converting a Pandas DataFrame/Series."
        )
        
        # Interactive UI
        n_elements = st.slider("Select number of elements for np.arange", 5, 20, 10)
        
        code = f"""import numpy as np

# Convert a slice of our building loads (first 5 rows of Heating Load) to a NumPy array
loads_arr = df['Y1'].head(5).to_numpy()

# Create arrays from scratch
zeros_arr = np.zeros(shape=(2, 3))
arange_arr = np.arange({n_elements})
random_arr = np.random.uniform(low=0.62, high=0.98, size=5)
"""
        st.code(code, language="python")
        
        # Live Run
        loads_arr = df['Y1'].head(5).to_numpy()
        zeros_arr = np.zeros(shape=(2, 3))
        arange_arr = np.arange(n_elements)
        random_arr = np.random.uniform(0.62, 0.98, 5)
        
        st.write("**Live Output:**")
        st.write("Converted Y1 loads array:", loads_arr)
        st.write("2x3 Zeros array:\n", zeros_arr)
        st.write(f"np.arange({n_elements}) array:", arange_arr)
        st.write("Random Uniform relative compactness simulation:", random_arr)

    elif "2. Array vs List" in topic:
        st.subheader("Array vs List Performance Benchmark")
        st.write(
            "NumPy arrays are implemented in C and store data in contiguous memory blocks, enabling vectorized calculations. "
            "Python lists store references to objects scattered in memory, requiring loop overhead."
        )
        
        size = st.selectbox("Benchmark size (number of elements)", [100000, 500000, 1000000], index=1)
        
        if st.button("🚀 Run Live Speed Benchmark"):
            # Python List sum
            py_list = list(range(size))
            start_time = time.perf_counter()
            list_sum = sum(py_list)
            end_time = time.perf_counter()
            list_time = (end_time - start_time) * 1000
            
            # NumPy Array sum
            np_arr = np.arange(size)
            start_time = time.perf_counter()
            arr_sum = np.sum(np_arr)
            end_time = time.perf_counter()
            arr_time = (end_time - start_time) * 1000
            
            st.success(f"Benchmark completed for {size:,} elements!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Python List Sum Time", f"{list_time:.2f} ms")
            with col2:
                st.metric("NumPy Array Sum Time", f"{arr_time:.2f} ms", delta=f"{list_time/arr_time:.1f}x Faster!", delta_color="inverse")
                
            # Plot comparison
            fig, ax = plt.subplots(figsize=(6, 3))
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#1E2330')
            bars = ax.bar(['Python List', 'NumPy Array'], [list_time, arr_time], color=['#FF4B4B', '#00D2C4'], width=0.4)
            ax.set_ylabel("Execution Time (ms)", color='white')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('#444444')
            ax.spines['left'].set_color('#444444')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # Annotate
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}ms',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', color='white', weight='bold')
            st.pyplot(fig)

    elif "3. Basic Vectorized Operations" in topic:
        st.subheader("Basic Operations (Vectorized Math)")
        st.write(
            "Vectorization allows operations to be performed element-by-element across arrays without writing slow `for` loops. "
            "For example, we can calculate the total energy load (Heating + Cooling) or the load difference directly."
        )
        
        code = """import numpy as np

# Load Y1 (Heating) and Y2 (Cooling) as NumPy arrays
y1 = df['Y1'].to_numpy()
y2 = df['Y2'].to_numpy()

# Vectorized addition: Total Load
total_load = y1 + y2

# Vectorized difference: Y2 - Y1
load_diff = y2 - y1

# Basic statistical operations
mean_total = np.mean(total_load)
max_diff = np.max(np.abs(load_diff))
"""
        st.code(code, language="python")
        
        # Run live
        y1 = df['Y1'].to_numpy()
        y2 = df['Y2'].to_numpy()
        total_load = y1 + y2
        load_diff = y2 - y1
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Total Load (Y1+Y2)", f"{np.mean(total_load):.2f} kWh/m²")
        col2.metric("Max Load Difference", f"{np.max(np.abs(load_diff)):.2f} kWh/m²")
        col3.metric("Correlation Coefficient (Y1, Y2)", f"{np.corrcoef(y1, y2)[0,1]:.4f}")
        
        st.write("**First 5 rows computed values:**")
        preview_df = pd.DataFrame({
            'Heating Load (Y1)': y1[:5],
            'Cooling Load (Y2)': y2[:5],
            'Vectorized Sum (Total)': total_load[:5],
            'Vectorized Diff (Y2 - Y1)': load_diff[:5]
        })
        st.dataframe(preview_df)

    elif "4. Array Indexing and Slicing" in topic:
        st.subheader("Array Indexing and Slicing")
        st.write(
            "NumPy uses standard slicing `[start:end, step]` syntax. Because arrays are multi-dimensional, "
            "we slice across dimensions using commas: `array[row_slice, col_slice]`."
        )
        
        # Load dataset as 2D numpy array
        building_arr = df.to_numpy()
        
        row_range = st.slider("Select Row Slicing Range", 0, len(df), (0, 5))
        col_index = st.selectbox(
            "Select Column Sliced (Features X1 to Y2)",
            options=list(range(10)),
            format_func=lambda c: f"Column {c} - {df.columns[c]} ({FEATURE_LABELS.get(df.columns[c])})"
        )
        
        code = f"""# Convert entire dataset to 2D numpy array (shape: {building_arr.shape})
arr = df.to_numpy()

# Slice rows {row_range[0]} to {row_range[1]} for column {col_index}
slice_1d = arr[{row_range[0]}:{row_range[1]}, {col_index}]

# Slice a 2D sub-array (first 3 rows, first 4 columns)
sub_2d = arr[0:3, 0:4]
"""
        st.code(code, language="python")
        
        slice_1d = building_arr[row_range[0]:row_range[1], col_index]
        sub_2d = building_arr[0:3, 0:4]
        
        st.write(f"**Live Sliced 1D array (rows {row_range[0]}:{row_range[1]}, col {col_index}):**", slice_1d)
        st.write("**Live 2D sub-array (rows 0:3, cols 0:4):**\n", sub_2d)

    elif "5. Broadcasting and Reshaping" in topic:
        st.subheader("Broadcasting and Reshaping")
        st.write(
            "**Reshaping** changes the structure of an array without changing its data (e.g., flat list to matrix). "
            "**Broadcasting** allows arithmetic operations on arrays of different shapes, projecting the smaller array "
            "across the larger one."
        )
        
        st.markdown("#### Reshaping Demo")
        code_reshape = """# Reshape a 1D vector of 12 load readings into a 3x4 matrix
flat_loads = df['Y1'].head(12).to_numpy()
matrix_loads = flat_loads.reshape(3, 4)
"""
        st.code(code_reshape, language="python")
        flat_loads = df['Y1'].head(12).to_numpy()
        matrix_loads = flat_loads.reshape(3, 4)
        st.write("Flat load vector:", flat_loads)
        st.write("Reshaped 3x4 matrix:\n", matrix_loads)
        
        st.markdown("#### Broadcasting Demo")
        multiplier = st.slider("Scalar value to broadcast", 1.0, 5.0, 1.5, step=0.5)
        code_broadcast = f"""# Multiply a 2x3 matrix of loads by a scalar {multiplier}
# The scalar is 'broadcasted' to match the matrix dimensions.
scaled_matrix = matrix_loads[0:2, 0:3] * {multiplier}
"""
        st.code(code_broadcast, language="python")
        scaled_matrix = matrix_loads[0:2, 0:3] * multiplier
        st.write("Original 2x3 sub-matrix:\n", matrix_loads[0:2, 0:3])
        st.write(f"Scaled by {multiplier} via broadcasting:\n", scaled_matrix)

    elif "6. Array Manipulation" in topic:
        st.subheader("Array Manipulation & Stacking")
        st.write(
            "Array manipulation includes operations such as transposing, concatenating, splitting, and stacking arrays. "
            "Stacking allows us to combine separate feature columns into a new matrix."
        )
        
        code = """import numpy as np

# Select two design columns as separate vectors
compactness = df['X1'].head(5).to_numpy()
surface_area = df['X2'].head(5).to_numpy()

# Stack them horizontally (column-wise)
col_stacked = np.column_stack((compactness, surface_area))

# Stack them vertically (row-wise)
row_stacked = np.vstack((compactness, surface_area))

# Transpose the column stacked array
transposed = col_stacked.T
"""
        st.code(code, language="python")
        
        compactness = df['X1'].head(5).to_numpy()
        surface_area = df['X2'].head(5).to_numpy()
        col_stacked = np.column_stack((compactness, surface_area))
        row_stacked = np.vstack((compactness, surface_area))
        
        st.write("Compactness Vector (X1):", compactness)
        st.write("Surface Area Vector (X2):", surface_area)
        st.write("np.column_stack output:\n", col_stacked)
        st.write("np.vstack output:\n", row_stacked)
        st.write("Transposed vstack output:\n", row_stacked.T)


# ==========================================
# 🐼 PANDAS TOPICS
# ==========================================
def render_pandas_topics(df: pd.DataFrame):
    topic = st.selectbox(
        "Select Pandas Topic",
        options=[
            "1. Dictionary to DataFrame & Series/DataFrame Overview [Lec-3.09 to 3.11]",
            "2. File I/O (CSV, Excel, JSON) [Lec-3.12]",
            "3. Subsetting Dataframes [Lec-3.13]",
            "4. Modifying Dataframes (Adding Columns) [Lec-3.14 & 3.15]",
            "5. Handling Missing Data [Lec-3.16]",
            "6. Aggregating and Grouping Data [Lec-3.17]",
            "7. Concatenating & Joining [Lec-3.18]",
            "8. Reshaping (pivot_table, melt, crosstab) [Lec-3.19]",
            "9. Working with Time Series Data [Lec-3.20]"
        ]
    )

    st.markdown("---")

    if "1. Dictionary to DataFrame" in topic:
        st.subheader("Dictionary to DataFrame & Series/DataFrame Overview")
        st.write(
            "A Pandas DataFrame is a table of 2D data, while a Series is a single column of 1D data. "
            "We can easily build a DataFrame from a Python dictionary."
        )
        
        code = """import pandas as pd

# Creating a dataframe of structural materials from a dictionary
materials_dict = {
    'Material': ['Concrete', 'Brick', 'Glass', 'Steel'],
    'U-Value (W/m²K)': [1.6, 2.1, 5.7, 0.5],
    'Cost Index': [1, 2, 4, 5],
    'Eco-Friendly': [False, True, True, False]
}

materials_df = pd.DataFrame(materials_dict)

# Overview properties
types = df.dtypes
series_x1 = df['X1']  # This is a Series
"""
        st.code(code, language="python")
        
        materials_dict = {
            'Material': ['Concrete', 'Brick', 'Glass', 'Steel'],
            'U-Value (W/m²K)': [1.6, 2.1, 5.7, 0.5],
            'Cost Index': [1, 2, 4, 5],
            'Eco-Friendly': [False, True, True, False]
        }
        materials_df = pd.DataFrame(materials_dict)
        
        st.write("**DataFrame created from Dictionary:**")
        st.dataframe(materials_df)
        
        st.write("**Overview of our Building dataset data types:**")
        st.write(df.dtypes)

    elif "2. File I/O" in topic:
        st.subheader("I/O with CSV, EXCEL, and JSON Files")
        st.write(
            "Pandas provides powerful I/O methods to read and write common tabular formats: "
            "`read_csv()`, `read_excel()`, `read_json()`, and their matching `to_...()` write methods."
        )
        
        code = """import pandas as pd

# Reading our excel dataset
# df = pd.read_excel('ENB2012_data.xlsx')

# Exporting a subset to CSV format
df.head(10).to_csv('building_preview.csv', index=False)

# Exporting a subset to JSON format
df.head(5).to_json('building_preview.json', orient='records')

# Reading back the CSV file
# loaded_df = pd.read_csv('building_preview.csv')
"""
        st.code(code, language="python")
        
        # Write files for demonstration
        df.head(5).to_csv('building_preview.csv', index=False)
        df.head(5).to_json('building_preview.json', orient='records')
        
        st.write("**JSON Export Preview:**")
        with open('building_preview.json', 'r') as f:
            st.code(f.read(), language="json")

    elif "3. Subsetting Dataframes" in topic:
        st.subheader("Subsetting Dataframes")
        st.write(
            "Subsetting filters a DataFrame's rows and columns. This can be done via boolean indexing, "
            "logical operations (`&`, `|`, `~`), and the `.loc` (label-based) and `.iloc` (positional) selectors."
        )
        
        height_filter = st.selectbox("Filter by Height", [3.5, 7.0])
        compactness_val = st.slider("Min Relative Compactness", 0.62, 0.98, 0.75)
        
        code = f"""# Filter buildings where Height (X5) is {height_filter} and Compactness (X1) >= {compactness_val}
# And select only specific columns: Compactness, Height, Heating Load
subset_df = df.loc[
    (df['X5'] == {height_filter}) & (df['X1'] >= {compactness_val}),
    ['X1', 'X5', 'Y1', 'Y2']
]
"""
        st.code(code, language="python")
        
        subset_df = df.loc[
            (df['X5'] == height_filter) & (df['X1'] >= compactness_val),
            ['X1', 'X5', 'Y1', 'Y2']
        ]
        
        st.write(f"**Filter matches:** {len(subset_df)} buildings out of {len(df)}")
        st.dataframe(subset_df)

    elif "4. Modifying Dataframes" in topic:
        st.subheader("Modifying Dataframes (Adding Columns & Assignments)")
        st.write(
            "DataFrames are modified by assigning new columns or modifying existing columns. "
            "We can use vectorized formulas, map mappings, or define classification conditions."
        )
        
        code = """# 1. Add Total Load (Y1 + Y2)
df['Total_Load'] = df['Y1'] + df['Y2']

# 2. Add an efficiency class column based on Total Load
# Total Load < 30: High Efficiency, 30-60: Medium, > 60: Low
def classify_efficiency(load):
    if load < 30:
        return 'High Efficiency'
    elif load < 60:
        return 'Medium Efficiency'
    else:
        return 'Low Efficiency'

df['Efficiency_Class'] = df['Total_Load'].apply(classify_efficiency)
"""
        st.code(code, language="python")
        
        # Run live on copy
        df_mod = df.copy()
        df_mod['Total_Load'] = df_mod['Y1'] + df_mod['Y2']
        df_mod['Efficiency_Class'] = df_mod['Total_Load'].apply(
            lambda x: 'High Efficiency' if x < 30 else ('Medium Efficiency' if x < 60 else 'Low Efficiency')
        )
        
        st.write("**Modified DataFrame (first 5 rows with new columns):**")
        st.dataframe(df_mod[['X1', 'X5', 'Y1', 'Y2', 'Total_Load', 'Efficiency_Class']].head(5))
        
        st.write("**Count of buildings by Efficiency Class:**")
        st.write(df_mod['Efficiency_Class'].value_counts())

    elif "5. Handling Missing Data" in topic:
        st.subheader("Handling Missing Data")
        st.write(
            "Missing values (represented as NaN or None) can disrupt modeling and calculations. "
            "We can identify nulls using `.isnull().sum()`, drop them with `.dropna()`, or impute them using `.fillna()`."
        )
        
        st.markdown("#### Simulating Missing Data")
        code = """# Create a copy and insert random NaN values into Heating Load (Y1)
df_nan = df.copy()
np.random.seed(42)
nan_mask = np.random.rand(len(df_nan)) < 0.05 # 5% missing
df_nan.loc[nan_mask, 'Y1'] = np.nan

# 1. Check for missing values
missing_counts = df_nan.isnull().sum()

# 2. Fix the missing values by imputing with the column mean
mean_y1 = df_nan['Y1'].mean()
df_nan['Y1_Imputed'] = df_nan['Y1'].fillna(mean_y1)
"""
        st.code(code, language="python")
        
        df_nan = df.copy()
        np.random.seed(42)
        nan_mask = np.random.rand(len(df_nan)) < 0.05
        df_nan.loc[nan_mask, 'Y1'] = np.nan
        
        st.write("**Null counts in simulated missing dataset:**")
        st.write(df_nan.isnull().sum().to_frame("Missing Count").T)
        
        mean_y1 = df_nan['Y1'].mean()
        df_nan['Y1_Imputed'] = df_nan['Y1'].fillna(mean_y1)
        
        st.success(f"Imputed missing Heating Load values using the column mean value: **{mean_y1:.2f}**")
        st.write("Sample rows where data was missing and is now imputed:")
        st.dataframe(df_nan.loc[nan_mask, ['X1', 'Y1', 'Y1_Imputed']].head(5))

    elif "6. Aggregating and Grouping Data" in topic:
        st.subheader("Aggregating and Grouping Data")
        st.write(
            "Grouping splits the dataset by categories, allowing aggregate metrics (like `.mean()`, "
            "`.sum()`, `.count()`, or `.agg()`) to be calculated for each group."
        )
        
        group_select = st.selectbox("Group By Feature", ["X5 (Height)", "X6 (Orientation)", "X7 (Glazing Area)"])
        group_col = group_select.split(" ")[0]
        
        code = f"""# Group by {group_col} and calculate mean and standard deviation of Y1 (Heating) and Y2 (Cooling)
grouped_df = df.groupby('{group_col}')[['Y1', 'Y2']].agg(['mean', 'std', 'count'])
"""
        st.code(code, language="python")
        
        grouped_df = df.groupby(group_col)[['Y1', 'Y2']].agg(['mean', 'std', 'count'])
        st.write("**Aggregation Result Table:**")
        st.dataframe(grouped_df)

    elif "7. Concatenating & Joining" in topic:
        st.subheader("Appending, Concatenating, Merging, and Joining")
        st.write(
            "These functions combine multiple DataFrames. `concat()` appends rows or columns, while "
            "`merge()` joins datasets using key values (like SQL JOIN)."
        )
        
        code = """import pandas as pd

# 1. Concatenate: split our buildings in two halves and merge them back vertically
half1 = df.iloc[:10]
half2 = df.iloc[10:20]
concat_rows = pd.concat([half1, half2], axis=0)

# 2. Merge: Join our building dataset with metadata on orientation
orientation_metadata = pd.DataFrame({
    'Orientation_ID': [2, 3, 4, 5],
    'Direction_Name': ['North', 'East', 'South', 'West'],
    'Solar_Gain_Multiplier': [0.8, 1.1, 1.4, 1.1]
})

merged_df = pd.merge(
    df.head(5), 
    orientation_metadata, 
    left_on='X6', 
    right_on='Orientation_ID', 
    how='inner'
)
"""
        st.code(code, language="python")
        
        orientation_metadata = pd.DataFrame({
            'Orientation_ID': [2, 3, 4, 5],
            'Direction_Name': ['North', 'East', 'South', 'West'],
            'Solar_Gain_Multiplier': [0.8, 1.1, 1.4, 1.1]
        })
        merged_df = pd.merge(
            df.head(5), 
            orientation_metadata, 
            left_on='X6', 
            right_on='Orientation_ID', 
            how='inner'
        )
        
        st.write("**Merge Join output (X6 mapped to metadata details):**")
        st.dataframe(merged_df[['X1', 'X6', 'Direction_Name', 'Solar_Gain_Multiplier', 'Y1']])

    elif "8. Reshaping" in topic:
        st.subheader("Reshaping using pivot, melt, and crosstab")
        st.write(
            "Reshaping reshapes tables. `pivot_table` aggregates data into a grid, `melt` unpivots "
            "a table from wide to long format, and `crosstab` calculates frequency tables."
        )
        
        reshape_type = st.radio("Reshape Mode", ["Pivot Table", "Melt", "Crosstab"])
        
        if reshape_type == "Pivot Table":
            code = """# Pivot Table: Calculate average heating load (Y1) for combinations of Height (X5) and Orientation (X6)
pivot = df.pivot_table(values='Y1', index='X5', columns='X6', aggfunc='mean')
"""
            st.code(code, language="python")
            pivot = df.pivot_table(values='Y1', index='X5', columns='X6', aggfunc='mean')
            st.dataframe(pivot)
            
        elif reshape_type == "Melt":
            code = """# Melt: Flatten Y1 and Y2 into a single 'Load Type' and 'Load Value' column
melted = df[['X1', 'X5', 'Y1', 'Y2']].head(5).melt(
    id_vars=['X1', 'X5'], 
    value_vars=['Y1', 'Y2'],
    var_name='Load_Type', 
    value_name='Load_Value'
)
"""
            st.code(code, language="python")
            melted = df[['X1', 'X5', 'Y1', 'Y2']].head(3).melt(
                id_vars=['X1', 'X5'], 
                value_vars=['Y1', 'Y2'],
                var_name='Load_Type', 
                value_name='Load_Value'
            )
            st.dataframe(melted)
            
        else:
            code = """# Crosstab: Show number of buildings for combinations of Glazing Area (X7) and Orientation (X6)
ct = pd.crosstab(df['X7'], df['X6'])
"""
            st.code(code, language="python")
            ct = pd.crosstab(df['X7'], df['X6'])
            st.dataframe(ct)

    elif "9. Working with Time Series Data" in topic:
        st.subheader("Working with Time Series Data")
        st.write(
            "While our building energy dataset is static, energy readings in the real world are time series. "
            "Pandas handles this with datetime indices, resampling (`.resample()`), and rolling window calculations."
        )
        
        code = """import pandas as pd
import numpy as np

# Let's generate synthetic hourly energy readings for 1 week (168 hours)
dates = pd.date_range(start='2026-06-01', periods=168, freq='h')
hourly_data = pd.DataFrame({
    'Heating_Usage': np.random.normal(loc=15.0, scale=3.0, size=168),
    'Cooling_Usage': np.random.normal(loc=20.0, scale=4.0, size=168)
}, index=dates)

# Resample from hourly to daily averages
daily_avg = hourly_data.resample('D').mean()

# Calculate 24-hour rolling average
hourly_data['Heating_24h_Rolling'] = hourly_data['Heating_Usage'].rolling(window=24).mean()
"""
        st.code(code, language="python")
        
        dates = pd.date_range(start='2026-06-01', periods=168, freq='h')
        hourly_data = pd.DataFrame({
            'Heating_Usage': np.random.normal(loc=15.0, scale=3.0, size=168),
            'Cooling_Usage': np.random.normal(loc=20.0, scale=4.0, size=168)
        }, index=dates)
        daily_avg = hourly_data.resample('D').mean()
        hourly_data['Heating_24h_Rolling'] = hourly_data['Heating_Usage'].rolling(window=24).mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Resampled Daily Average (first 5 days):**")
            st.dataframe(daily_avg.head(5))
        with col2:
            st.write("**Hourly with 24h Rolling Average:**")
            st.dataframe(hourly_data[['Heating_Usage', 'Heating_24h_Rolling']].iloc[22:28])


# ==========================================
# 📊 VISUALIZATION TOPICS
# ==========================================
def render_viz_topics(df: pd.DataFrame):
    topic = st.selectbox(
        "Select Data Visualization Topic",
        options=[
            "1. Distribution Analysis (Histograms & Box Plots) [Lec-3.21]",
            "2. Correlation & Heatmaps [Lec-3.22]",
            "3. Scatter Plots & Trend Lines [Lec-3.23]",
            "4. Bar Charts & Grouped Aggregations [Lec-3.24]",
            "5. Multivariate Grid Visualizations (Pairplot) [Lec-3.25]"
        ]
    )

    st.markdown("---")

    if "1. Distribution Analysis" in topic:
        st.subheader("Distribution Analysis (Boxplots & Histograms)")
        st.write(
            "Analyzing distributions reveals range, skewness, outliers, and density peaks. "
            "Box plots show quartiles and outliers, while histograms show frequency density."
        )
        
        # Display Plotly chart
        fig = plot_load_distributions_plotly_local(df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Matplotlib/Seaborn Code Code Snippet")
        st.code("""import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 6))
# Create long-format dataframe for boxplot
melted = df.melt(value_vars=['Y1', 'Y2'], var_name='Load Type', value_name='Load Value')
sns.boxplot(data=melted, x='Load Type', y='Load Value', ax=ax, palette='Set2')
plt.show()""", language="python")

    elif "2. Correlation & Heatmaps" in topic:
        st.subheader("Correlation Heatmaps")
        st.write(
            "Heatmaps display correlation coefficients between all pairs of numeric variables. "
            "This is crucial for identifying which building features (e.g. roof area, height) are most related to energy consumption."
        )
        
        # Display matplotlib correlation plot
        from .charts import plot_correlation_heatmap_matplotlib
        fig = plot_correlation_heatmap_matplotlib(df)
        st.pyplot(fig)
        
        st.markdown("#### Code Code Snippet")
        st.code("""import seaborn as sns
import matplotlib.pyplot as plt

corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix")
plt.show()""", language="python")

    elif "3. Scatter Plots" in topic:
        st.subheader("Scatter Plots & Multi-dimensional Analysis")
        st.write(
            "Scatter plots display relationships between two continuous variables (e.g. Compactness vs heating load). "
            "Adding size and color variables lets us analyze four dimensions simultaneously."
        )
        
        from .charts import plot_compactness_vs_loads_plotly
        load_type = st.radio("Select Load Variable", ["Heating Load", "Cooling Load"])
        fig = plot_compactness_vs_loads_plotly(df, load_type)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Plotly Express Code Snippet")
        st.code(f"""import plotly.express as px

fig = px.scatter(
    df,
    x='X1',
    y='{"Y1" if load_type == "Heating Load" else "Y2"}',
    color='X5',  # Colored by Height
    size='{"Y1" if load_type == "Heating Load" else "Y2"}',
    title="Relative Compactness vs {load_type}"
)
fig.show()""", language="python")

    elif "4. Bar Charts" in topic:
        st.subheader("Bar Charts & Grouped Comparisons")
        st.write(
            "Bar charts excel at comparing categorical or grouped averages. Grouped columns allow us "
            "to contrast Heating and Cooling loads across Orientations, Heights, and Glazing specifications."
        )
        
        from .charts import plot_grouped_loads_plotly
        group_col = st.selectbox("Group By Variable", ["X5", "X6", "X7", "X8"], format_func=lambda x: f"{x} - {FEATURE_LABELS.get(x)}")
        fig = plot_grouped_loads_plotly(df, group_col)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Grouped Aggregation & Plotly Bar Chart Code")
        st.code(f"""import pandas as pd
import plotly.express as px

# Group and calculate mean
grouped = df.groupby('{group_col}')[['Y1', 'Y2']].mean().reset_index()
melted = grouped.melt(id_vars='{group_col}', value_vars=['Y1', 'Y2'])

fig = px.bar(
    melted,
    x='{group_col}',
    y='value',
    color='variable',
    barmode='group'
)
fig.show()""", language="python")

    elif "5. Multivariate Grid Visualizations" in topic:
        st.subheader("Multivariate Grid Visualizations (Pairplot)")
        st.write(
            "A pairplot (or scatterplot matrix) creates a grid of pairwise relationships across all "
            "variables in a dataset, showing bivariate distributions on the grid and univariate distributions on the diagonal."
        )
        
        from .charts import plot_pairplot_matplotlib
        # Show pairplot directly
        fig = plot_pairplot_matplotlib(df)
        st.pyplot(fig)
        
        st.markdown("#### Seaborn Code Snippet")
        st.code("""import seaborn as sns
import matplotlib.pyplot as plt

# Creates a pairwise grid of scatter plots & density plots
sns.pairplot(df[['X1', 'X2', 'X5', 'Y1', 'Y2']], hue='X5')
plt.show()""", language="python")


# Helper for local Plotly box plot to avoid circular imports
def plot_load_distributions_plotly_local(df: pd.DataFrame) -> go.Figure:
    melted = df.melt(value_vars=['Y1', 'Y2'], var_name='Load Type', value_name='Load Value')
    melted['Load Type'] = melted['Load Type'].map({'Y1': 'Heating Load', 'Y2': 'Cooling Load'})
    fig = px.box(
        melted,
        x='Load Type',
        y='Load Value',
        color='Load Type',
        color_discrete_map={'Heating Load': '#FF4B4B', 'Cooling Load': '#1C83E1'},
        points="all",
        title="Heating vs Cooling Load Box Plot",
        labels={'Load Value': 'Load Value (kWh/m²)', 'Load Type': 'Load Type'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig
