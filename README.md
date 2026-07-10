# 🏥 Hospital Analytics Dashboard | End-to-End Data Analytics Project

## 📌 Project Overview

Healthcare organizations generate thousands of patient records every day. Without proper analysis, it becomes difficult for hospital administrators to monitor patient admissions, doctor performance, billing trends, insurance claims, and departmental efficiency.

This project demonstrates a complete **End-to-End Data Analytics Pipeline** that extracts hospital data from Kaggle, cleans and transforms it using Python, stores it in SQL Server, performs analytical queries using SQL, and visualizes key insights using Power BI.

The project follows the ETL (Extract → Transform → Load) methodology commonly used in real-world healthcare analytics.

Dataset source: https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset

---

# ▶ Quick Start

```bash
git clone <this-repo>
cd Hospital-Analytics
pip install -r requirements.txt
cp .env.example .env          # defaults to a local SQLite DB, zero setup needed
python src/main.py            # runs Extract -> Transform -> Load end to end
```

This produces:
- `data/raw/hospital_raw.csv` — extracted data
- `data/cleaned/hospital_cleaned.csv` — cleaned, transformed data
- `data/cleaned/hospital.db` — local SQLite database loaded with the `Patients` table

To switch to a real SQL Server instance, set `DB_ENGINE=sqlserver` and fill in
`DB_SERVER` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` in `.env`.

## 📥 About the data source

`src/extract.py` is wired to pull the real dataset from Kaggle via `kagglehub`
using the dataset above. To enable the live download:

1. `pip install kagglehub`
2. Get an API token from https://www.kaggle.com/settings → "Create New Token"
3. Place it at `~/.kaggle/kaggle.json` (or set `KAGGLE_USERNAME` / `KAGGLE_KEY`)
4. Run `python src/extract.py`

If Kaggle credentials aren't available, the script automatically falls back to
generating a **synthetic dataset with an identical schema** (same columns,
same data quality issues — duplicates and missing values included) so the
rest of the pipeline (clean → load → SQL analysis → Power BI) is fully
runnable and testable without needing Kaggle access. Once you have real
credentials, just re-run `extract.py` and the real data flows through the
same `transform.py` / `load_sql.py` / `sql/analysis.sql` unchanged.

---

# 🎯 Business Problem

Hospitals often face challenges such as:

- Difficulty tracking patient admissions.
- No centralized reporting system.
- Lack of visibility into department-wise revenue.
- Difficulty identifying top-performing doctors.
- Manual reporting consumes significant time.
- Insurance and billing trends are hard to analyze.
- Decision-making is based on incomplete information.

---

# 💡 Proposed Solution

Develop an automated ETL pipeline that:

- Extracts hospital data directly from Kaggle.
- Cleans and validates raw data using Python.
- Loads processed data into Microsoft SQL Server.
- Performs SQL-based business analysis.
- Builds an interactive Power BI dashboard for hospital management.

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data Extraction & ETL |
| Pandas | Data Cleaning & Transformation |
| KaggleHub API | Dataset Download |
| SQL Server | Data Storage |
| SQL | Data Analysis |
| Power BI | Dashboard & Reporting |
| Git & GitHub | Version Control |

---

# 📂 Project Structure

```
Hospital-Analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   └── EDA.ipynb
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load_sql.py
│   └── main.py
│
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
│
├── powerbi/
│   └── HospitalDashboard.pbix
│
├── screenshots/
│
├── README.md
│
└── requirements.txt
```

---

# 🔄 Project Workflow

```
Hospital Dataset (Kaggle)
            │
            ▼
Python Extraction
            │
            ▼
Data Cleaning & Transformation
            │
            ▼
Clean Dataset
            │
            ▼
SQL Server Database
            │
            ▼
SQL Business Analysis
            │
            ▼
Power BI Dashboard
            │
            ▼
Business Insights
```

---

# ⚙ ETL Pipeline

## Step 1 – Extract (`src/extract.py`)

- Download dataset using KaggleHub API
- Store raw CSV files
- Validate downloaded data
- Synthetic fallback generator if Kaggle isn't configured

## Step 2 – Transform (`src/transform.py`)

Cleaning operations include:

- Remove duplicate records
- Handle missing values
- Convert data types
- Standardize date formats
- Create calculated columns
- Validate billing values
- Generate age groups
- Calculate patient stay duration

## Step 3 – Load (`src/load_sql.py`)

- Connect Python with SQL Server (or local SQLite for testing)
- Create Hospital Database
- Load cleaned dataset
- Verify successful insertion

---

# 📊 SQL Analysis (`sql/analysis.sql`)

The project performs business analysis such as:

- Total Patients
- Monthly Admissions
- Department-wise Revenue
- Top Doctors
- Average Billing Amount
- Average Length of Stay
- Insurance Analysis
- Gender Distribution
- Age Group Distribution
- Yearly Patient Trends
- Revenue Ranking
- Window Functions
- Common Table Expressions (CTE)
- Views & Aggregations

---

# 📈 Power BI Dashboard

See `powerbi/README.md` for connection instructions. The dashboard provides interactive insights including:

### Executive Dashboard
- Total Patients, Total Revenue, Average Billing, Average Length of Stay

### Admissions Dashboard
- Monthly Admissions, Department Distribution, Gender Analysis

### Doctor Dashboard
- Top Performing Doctors, Patient Count, Department Performance

### Financial Dashboard
- Revenue Analysis, Insurance Coverage, Billing Trends

---

# 📊 Key Business Insights

The dashboard helps management answer questions such as:

- Which department generates the highest revenue?
- Which doctors treat the most patients?
- Which insurance provider is most commonly used?
- What is the average hospital stay?
- Which months receive the highest patient admissions?
- Which diagnosis occurs most frequently?
- Which age group visits the hospital most often?

---

# ✅ Business Impact

This project enables hospitals to:

- Improve operational efficiency.
- Monitor doctor performance.
- Track revenue trends.
- Analyze patient demographics.
- Support data-driven decision making.
- Reduce manual reporting efforts.
- Improve healthcare planning.

---

# 🏆 Project Achievements

✔ End-to-End ETL Pipeline
✔ Automated Data Extraction
✔ Data Cleaning & Validation
✔ SQL Server Integration
✔ Business Intelligence Dashboard
✔ Healthcare Domain Analytics
✔ Interactive Reporting
✔ GitHub Ready Project

---

# 📚 Skills Demonstrated

- Python Programming
- Pandas
- SQL
- SQL Server
- ETL Pipeline
- Data Cleaning
- Data Validation
- Data Analysis
- Power BI
- Business Intelligence
- Git & GitHub
- Healthcare Analytics

---

# 🚀 Future Enhancements

- Automate daily data refresh
- Integrate with Hospital Information System (HIS)
- Predict patient admissions using Machine Learning
- Forecast revenue trends
- Deploy dashboard to Power BI Service
- Build REST API for live analytics

---

# 👨‍💻 Author

**Saqlain Sheikh**

BCA Student | Aspiring Data Analyst

Skills:
Python • SQL • Power BI • Pandas • SQL Server • ETL • Data Analytics

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
