import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----- Page Config -----
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# ----- Custom CSS Styling -----
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .metric-container {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
    }

    .section-header {
        font-size: 22px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
        color: #2c3e50;
    }

    /* Dark theme specific styles for containers and headers */
    .dark .metric-container {
        background-color: #1e1e1e;
        color: white;
    }

    .dark .section-header {
        color: #ffffff;
    }

    /* Custom styles for multiselect selected tags */
    /* Light theme for multiselect tags */
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #607D8B !important; /* A neutral blue-gray for light theme */
        color: white !important;
        border-radius: 8px !important; /* Slightly rounded corners for tags */
    }

    /* Dark theme for multiselect tags */
    .dark div[data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #90A4AE !important; /* Lighter blue-gray for dark theme */
        color: black !important;
        border-radius: 8px !important;
    }

    /* Hover effect for multiselect tags */
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"]:hover {
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Load Data -----
@st.cache_data
def load_data():
    """
    Loads the superstore dataset, cleans column names,
    converts date columns, and handles missing values.
    """
    df = pd.read_csv("superstore.csv", encoding='ISO-8859-1')
    # Clean column names: strip whitespace, replace spaces with underscores, remove periods
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '', regex=False)
    # Drop problematic column if it exists (observed in some datasets)
    df = df.drop(columns=['è®°å½\x93æ\x95°'], errors='ignore')
    # Convert date columns to datetime objects, coercing errors
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    df['ShipDate'] = pd.to_datetime(df['ShipDate'], errors='coerce')
    # Convert Sales and Profit to numeric, coercing errors
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    # Drop rows with NaN values in critical columns for analysis
    df = df.dropna(subset=['Sales', 'Profit', 'Region', 'Segment', 'Category', 'SubCategory', 'CustomerName'])
    return df

# Load the data
df = load_data()

# ----- Sidebar Filters -----
st.sidebar.header("🔍 Filters")

# Theme selection toggle
selected_theme = st.sidebar.radio("🌗 Theme", options=["Light", "Dark"], index=0)

# Apply dark theme to matplotlib plots only
if selected_theme == "Dark":
    plt.style.use('dark_background')
else:
    plt.style.use('default') # Reset to default for light theme

# Multiselect filters for Region, Category, and Sub-Category
selected_regions = st.sidebar.multiselect(
    "🌍 Region",
    sorted(df['Region'].unique()),
    default=sorted(df['Region'].unique())
)
selected_categories = st.sidebar.multiselect(
    "📦 Category",
    sorted(df['Category'].unique()),
    default=sorted(df['Category'].unique())
)
selected_subcategories = st.sidebar.multiselect(
    "🧷 Sub-Category",
    sorted(df['SubCategory'].unique()),
    default=sorted(df['SubCategory'].unique())
)

# ----- Filtered Data -----
# Apply filters to the DataFrame
df_filtered = df[
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories)) &
    (df['SubCategory'].isin(selected_subcategories))
]

# ----- Title & KPIs -----
st.title("📊 Superstore Business Intelligence Dashboard")

# Display Key Performance Indicators (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-container'><h4>💰 Total Sales</h4><h2>${df_filtered['Sales'].sum():,.2f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-container'><h4>📈 Total Profit</h4><h2>${df_filtered['Profit'].sum():,.2f}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-container'><h4>🧾 Total Orders</h4><h2>{df_filtered['OrderID'].nunique()}</h2></div>", unsafe_allow_html=True)

# ----- Visualization Rows -----
# Row 1: Top 5 Customers by Sales & Segment-wise Sales Share
st.markdown("<div class='section-header'>📦 Sales Performance Analysis</div>", unsafe_allow_html=True)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("##### 🏆 Top 5 Customers by Sales")
    # Group by CustomerName and sum Sales, then get the top 5
    top_customers = df_filtered.groupby('CustomerName')['Sales'].sum().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots(figsize=(10, 6)) # Set figure size for better readability
    sns.barplot(x=top_customers.index, y=top_customers.values, palette='viridis', ax=ax1) # Use seaborn for better aesthetics
    ax1.set_ylabel("Sales ($)", fontsize=12)
    ax1.set_xlabel("Customer Name", fontsize=12)
    ax1.set_title("Top 5 Customers by Sales", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10) # Rotate x-axis labels for readability
    plt.yticks(fontsize=10)
    plt.tight_layout() # Adjust layout to prevent labels overlapping
    st.pyplot(fig1)
    st.caption("This bar chart displays the top 5 customers based on their total sales, highlighting key revenue generators.")

with row1_col2:
    st.markdown("##### 🧊 Segment-wise Sales Share")
    # Group by Segment and sum Sales
    segment_sales = df_filtered.groupby('Segment')['Sales'].sum()
    fig2, ax2 = plt.subplots(figsize=(8, 8)) # Set figure size for better readability
    # Create a pie chart with autopct for percentage display
    ax2.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"), textprops={'fontsize': 10})
    ax2.set_title("Sales by Segment", fontsize=14, fontweight='bold')
    ax2.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig2)
    st.caption("This pie chart illustrates the distribution of total sales across different customer segments (e.g., Consumer, Corporate, Home Office).")

# Row 2: Monthly Sales & Profit Trend & Profit vs Sales Scatter
st.markdown("<div class='section-header'>📈 Trend & Profitability Insights</div>", unsafe_allow_html=True)
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("##### 📅 Monthly Sales & Profit Trend")
    # Extract Month from OrderDate and convert to string for grouping
    df_filtered['Month'] = df_filtered['OrderDate'].dt.to_period('M').astype(str)
    # Group by Month and sum Sales and Profit
    monthly = df_filtered.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
    fig3, ax3 = plt.subplots(figsize=(12, 6)) # Set figure size
    # Plot Sales and Profit trends
    ax3.plot(monthly['Month'], monthly['Sales'], label="Sales", color="#1F618D", marker='o', linewidth=2)
    ax3.plot(monthly['Month'], monthly['Profit'], label="Profit", color="#117A65", marker='s', linewidth=2)
    plt.xticks(rotation=45, ha='right', fontsize=10) # Rotate x-axis labels
    plt.yticks(fontsize=10)
    ax3.set_title("Monthly Sales & Profit Trend", fontsize=14, fontweight='bold')
    ax3.set_xlabel("Month", fontsize=12)
    ax3.set_ylabel("Amount ($)", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, linestyle='--', alpha=0.6) # Add a grid for better readability
    plt.tight_layout()
    st.pyplot(fig3)
    st.caption("This line chart visualizes the monthly trends for both sales and profit, showing their fluctuations over time.")

with row2_col2:
    st.markdown("##### 💡 Profit vs Sales Scatter")
    fig4, ax4 = plt.subplots(figsize=(10, 6)) # Set figure size
    # Create a scatter plot of Sales vs Profit, colored by Category
    sns.scatterplot(data=df_filtered, x='Sales', y='Profit', hue='Category', palette='Set2', s=100, alpha=0.7, ax=ax4) # Increase marker size
    ax4.set_title("Sales vs Profit by Category", fontsize=14, fontweight='bold')
    ax4.set_xlabel("Sales ($)", fontsize=12)
    ax4.set_ylabel("Profit ($)", fontsize=12)
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.legend(title='Category', fontsize=10, title_fontsize='12')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig4)
    st.caption("This scatter plot shows the relationship between sales and profit for individual orders, categorized by product category.")

# New Row 3: Sales by Region and Sales by Category
st.markdown("<div class='section-header'>🌍 Regional & Categorical Performance</div>", unsafe_allow_html=True)
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown("##### 📍 Sales by Region")
    region_sales = df_filtered.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=region_sales.index, y=region_sales.values, palette='coolwarm', ax=ax5)
    ax5.set_ylabel("Total Sales ($)", fontsize=12)
    ax5.set_xlabel("Region", fontsize=12)
    ax5.set_title("Total Sales by Region", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig5)
    st.caption("This bar chart displays the total sales for each geographical region, allowing for regional performance comparison.")

with row3_col2:
    st.markdown("##### 🏷️ Sales by Category")
    category_sales = df_filtered.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=category_sales.index, y=category_sales.values, palette='magma', ax=ax6)
    ax6.set_ylabel("Total Sales ($)", fontsize=12)
    ax6.set_xlabel("Category", fontsize=12)
    ax6.set_title("Total Sales by Category", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig6)
    st.caption("This bar chart illustrates the total sales contribution from each product category.")

# New Row 4: Profit by Sub-Category
st.markdown("<div class='section-header'>📊 Detailed Profitability Analysis</div>", unsafe_allow_html=True)
row4_col1, row4_col2 = st.columns(2) # Using 2 columns for layout consistency, even if only one chart for now

with row4_col1:
    st.markdown("##### 📈 Profit by Sub-Category")
    subcategory_profit = df_filtered.groupby('SubCategory')['Profit'].sum().sort_values(ascending=False).head(10) # Top 10 for clarity
    fig7, ax7 = plt.subplots(figsize=(12, 7))
    sns.barplot(x=subcategory_profit.index, y=subcategory_profit.values, palette='plasma', ax=ax7)
    ax7.set_ylabel("Total Profit ($)", fontsize=12)
    ax7.set_xlabel("Sub-Category", fontsize=12)
    ax7.set_title("Top 10 Profitable Sub-Categories", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig7)
    st.caption("This bar chart highlights the top 10 sub-categories based on their total profit, identifying the most profitable product lines.")

# ----- Export & Raw Data -----
st.markdown("<div class='section-header'>⬇️ Export & Review Data</div>", unsafe_allow_html=True)

# Download button for filtered data
st.download_button(
    label="Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'), # Encode to utf-8
    file_name="filtered_superstore_data.csv",
    mime="text/csv",
    help="Click to download the currently filtered dataset as a CSV file."
)

# Expandable section to view raw data table
with st.expander("📄 View Raw Data Table"):
    st.dataframe(df_filtered)

# ----- Footer -----
st.markdown("---")
st.caption("🚀 Designed with Streamlit | BI Dashboard | Global Superstore Dataset")
