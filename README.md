
# 📊 Superstore Business Intelligence Dashboard 

An interactive dashboard built with **Streamlit** for visualizing and analyzing **sales, profit**, and **segment-wise performance** using the **Global Superstore Dataset**.

---

## 🎯 Task Objective

> **Interactive Business Dashboard in Streamlit**

- Clean and prepare the dataset.
- Build an interactive Streamlit dashboard.
- Include filters for Region, Category, and Sub-Category.
- Display key performance indicators (KPIs) and insights using visual charts.

---

## 📁 Dataset Used

**Name**: `superstore.csv`  
**Source**: Global Superstore Dataset

### 🔎 Key Fields:
- **Sales Metrics**: `Sales`, `Profit`, `Quantity`
- **Dates**: `OrderDate`, `ShipDate`
- **Geography**: `Region`, `Country`, `State`, `City`
- **Product Info**: `Category`, `Sub-Category`, `ProductName`
- **Customer Info**: `CustomerName`, `Segment`

---

## 🧹 Data Preparation

Data cleaning steps performed in `app.py`:
- Renamed columns for uniformity (replaced spaces, removed special characters).
- Converted date columns to datetime format.
- Converted `Sales` and `Profit` to numeric.
- Dropped rows with missing values in critical fields.
- Removed non-standard or corrupted columns.

---

## ✨ Dashboard Features

### 🔧 Interactive Filters
- Region 🌍
- Category 📦
- Sub-Category 🧷

### 💡 KPI Metrics
- 💰 **Total Sales**
- 📈 **Total Profit**
- 🧾 **Total Orders**

### 📊 Visual Charts
- 🏆 **Top 5 Customers by Sales** – Bar chart
- 🧊 **Sales by Segment** – Pie chart
- 📅 **Monthly Sales & Profit Trends** – Line chart
- 💡 **Profit vs Sales by Category** – Scatter plot
- 📍 **Sales by Region** – Bar chart
- 🏷️ **Sales by Category** – Bar chart
- 📈 **Top 10 Profitable Sub-Categories** – Bar chart

### 🔁 Other Functionalities
- 📁 Download filtered dataset as CSV
- 🔍 View raw data in an expandable table
- 🌗 Switch between **Light** and **Dark** themes
- ✅ Fully responsive layout with custom CSS styling

---

## 🚀 Getting Started

### 🛠 Requirements

- Python 3.7+
- pip package manager

### 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Shilpachhatani/Interactive-Business-Dashboard-in-Streamlit.git
cd Interactive-Business-Dashboard-in-Streamlit

# 2. Create virtual environment (optional but recommended)
python -m venv venv
# Activate (Windows)
.\venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install streamlit pandas matplotlib seaborn
```

### ▶️ Running the Dashboard

Make sure `superstore.csv` is placed in the project root folder. Then run:

```bash
streamlit run app.py
```

---

## 📈 Key Insights Uncovered

- **Top Customers**: Visualize the highest contributors to revenue.
- **Segment Analysis**: Understand which customer segments are most profitable.
- **Geographical Trends**: Analyze regional performance and market penetration.
- **Category Insights**: Spot high-performing and low-performing product categories.
- **Temporal Trends**: Identify monthly patterns in sales and profit.

---

## 🧠 Skills Demonstrated

- ✅ Business Intelligence (BI) Dashboarding
- ✅ Data Storytelling through Visualization
- ✅ Interactivity with Streamlit Components
- ✅ Visual KPI Representation and Analysis

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo and clone
git checkout -b feature/YourFeatureName
git commit -m "Add feature"
git push origin feature/YourFeatureName
```

Open a pull request for review.

---

## 📬 Contact

- **GitHub**: `Shilpachhatani`
- **Email**: shilpachhatani669@gmail.com

> _Designed with ❤️ — Interactive BI Dashboard | Streamlit | Global Superstore Dataset_
