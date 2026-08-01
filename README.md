# 🏥 Hospital Analytics Dashboard | End-to-End Data Analytics Project

## 📌 Project Overview

Healthcare organizations generate thousands of patient records every day. Without proper analysis, it becomes difficult for hospital administrators to monitor patient admissions, doctor performance, billing trends, insurance claims, and departmental efficiency.

This project demonstrates a complete **end-to-end healthcare analytics pipeline** that goes beyond traditional reporting. It extracts hospital data, cleans and transforms it using Python, performs SQL-based business analysis, and visualizes insights through a Streamlit dashboard and Power BI-style reporting.

On top of the analytics layer, the project adds two advanced capabilities:

- A **machine learning model** that predicts whether a patient stay is likely to become a prolonged / high-burden case, giving providers early warning instead of only historical reporting.
- A **local RAG-based AI chatbot** (LangChain + Ollama) that reads directly from the database and answers natural-language analytical questions — letting non-technical stakeholders like hospital managers or clients query the data themselves, without writing SQL or opening Power BI.

The project follows the ETL (Extract → Transform → Load) methodology commonly used in real-world healthcare analytics, extended with an ML and RAG layer on top.

Dataset source: https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset

---

# ▶ Quick Start

### 1) Clone the repo and create a virtual environment

```powershell
git clone https://github.com/saqlain914/Hospital_Analytics
cd Hospital-Analytics
python -m venv test_env
.\test_env\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
cp .env.example .env          # defaults to a local DB, zero setup needed
```

### 3) Run the ETL pipeline

```powershell
python src/main.py            # runs Extract -> Transform -> Load end to end
```

This produces:
- `data/raw/hospital_raw.csv` — extracted data
- `data/cleaned/hospital_cleaned.csv` — cleaned, transformed data
- a local database loaded with the cleaned patient records

### 4) Run the Streamlit dashboard

```powershell
python -m streamlit run app.py
```

### 5) Train the ML prediction model (optional)

```powershell
python src/ml/train.py
python src/ml/predict.py --input data/raw/hospital_raw.csv
```

### 6) Run the AI chatbot (optional)

```powershell
ollama serve
ollama pull llama3.2:latest
```

To use a different model:

```powershell
$env:OLLAMA_MODEL = "llama3.1"
```

The chatbot prefers a local Ollama model and falls back gracefully if no local AI setup is available.

---

## 📥 About the Data Source

`src/extract.py` is wired to pull the real dataset from Kaggle via `kagglehub` using the dataset linked above. To enable the live download:

1. `pip install kagglehub`
2. Get an API token from https://www.kaggle.com/settings → "Create New Token"
3. Place it at `~/.kaggle/kaggle.json` (or set `KAGGLE_USERNAME` / `KAGGLE_KEY`)
4. Run `python src/extract.py`

If Kaggle credentials aren't available, the script falls back to a **local CSV / synthetic dataset with an identical schema** (same columns, same data quality issues — duplicates and missing values included), so the rest of the pipeline (clean → load → SQL analysis → dashboard → ML → chatbot) is fully runnable and testable without needing Kaggle access. Once real credentials are available, re-running `extract.py` flows the real data through the same `transform.py` / `load_sql.py` / `sql/analysis.sql` / ML / chatbot pipeline unchanged.

---

# 🎯 Business Problem

Hospitals often face challenges such as:

- Difficulty tracking patient admissions.
- No centralized reporting system for operational performance.
- Lack of visibility into department-wise revenue and billing trends.
- Difficulty identifying top-performing or underperforming doctors/providers.
- Manual reporting consumes significant time.
- Insurance and billing trends are hard to analyze.
- Decision-making is based on incomplete or delayed information.
- **No early warning system** — long or high-burden patient stays are only discovered after the fact, not predicted in advance.
- **Non-technical stakeholders can't query data directly** — managers and clients depend on an analyst for every question, since reading SQL or building Power BI reports isn't something they can do themselves.

---

# 💡 Proposed Solution

Develop an automated analytics solution that:

- Extracts hospital data from Kaggle or local files.
- Cleans and validates raw data using Python.
- Loads processed data into a relational database.
- Performs SQL-based business analysis.
- Builds a dashboard experience through Streamlit and Power BI-style reporting.
- **Predicts** whether a patient stay is likely to become a prolonged/high-burden case using a trained ML model, so providers can act early rather than react late.
- **Answers natural-language questions** through a local, database-grounded AI chatbot (RAG), so managers or clients can ask things like *"which department had the highest revenue last quarter?"* in plain English and get a real, data-backed answer — no SQL knowledge required.

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data extraction, ETL, ML, chatbot logic |
| Pandas | Data cleaning & transformation |
| KaggleHub API | Dataset download |
| SQLAlchemy | Database interaction |
| SQL | Data storage & business analysis |
| Scikit-learn | Provider/stay-duration prediction model |
| Streamlit | Interactive dashboard web app |
| Power BI | Dashboard & reporting workflows |
| LangChain + Ollama | Local RAG-based AI chatbot |
| Git & GitHub | Version control |

---

# 📂 Project Structure

```
Hospital-Analytics/
│
├── app.py
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
│   ├── main.py
│   ├── ml/
│   │   ├── train.py
│   │   └── predict.py
│   └── rag/
│       └── chatbot.py
│
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
│
├── powerbi/
│   └── README.md
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
Hospital Dataset (Kaggle or local CSV)
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
Database / SQL Analysis
            │
            ▼
Streamlit Dashboard + Power BI Insights
            │
            ▼
      ┌─────┴─────┐
      ▼           ▼
ML Prediction   RAG Chatbot
(high-burden    (natural-language
 stay risk)      DB querying)
      │           │
      └─────┬─────┘
            ▼
Business Insights for Managers & Clients
```

---

# ⚙ ETL Pipeline

## Step 1 – Extract (`src/extract.py`)

- Download dataset using KaggleHub API
- Store raw CSV files
- Validate downloaded data
- Local/synthetic fallback if Kaggle isn't configured

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

- Connect Python with the database backend
- Create or populate hospital analytics tables
- Verify successful insertion of cleaned data

---

# 🤖 Machine Learning Layer (`src/ml/`)

- **Goal:** predict whether a patient stay is likely to become a **prolonged / high-burden case**, using features derived from the cleaned dataset (admission details, billing, diagnosis, demographics, etc.).
- **Who uses it:** care coordinators and hospital administrators, to flag at-risk stays early instead of discovering cost/resource overruns after discharge.
- `train.py` — trains and saves the model.
- `predict.py` — runs predictions on new/incoming patient data from the command line.

---

# 💬 RAG AI Chatbot (`src/rag/chatbot.py`)

- Built with **LangChain + Ollama**, running fully **locally** — no data leaves the environment.
- Retrieves relevant data directly from the hospital database and grounds its answers in that data (Retrieval-Augmented Generation), rather than relying on the model's own memory — reducing hallucinated answers.
- Lets **non-technical users** (hospital managers, clients) ask analytical questions in plain English, such as:
  - "Which department generated the most revenue this year?"
  - "Who are the top 5 doctors by patient count?"
  - "What's the average length of stay for patients over 60?"
- Falls back gracefully if no local Ollama setup is available, so the rest of the project remains usable without it.

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

# 📈 Dashboard & Reporting

See `powerbi/README.md` for Power BI connection instructions. The Streamlit app and Power BI-style dashboard provide interactive insights including:

### Executive Dashboard
- Total Patients, Total Revenue, Average Billing, Average Length of Stay

### Admissions Dashboard
- Monthly Admissions, Department Distribution, Gender Analysis

### Doctor Dashboard
- Top Performing Doctors, Patient Count, Department Performance

### Financial Dashboard
- Revenue Analysis, Insurance Coverage, Billing Trends

### Predictive & Conversational Layer
- High-burden stay risk predictions (ML)
- Ask-a-question chatbot for non-technical stakeholders (RAG)

---

# 📊 Key Business Insights

The full solution helps management answer questions such as:

- Which department generates the highest revenue?
- Which doctors treat the most patients?
- Which insurance provider is most commonly used?
- What is the average hospital stay?
- Which months receive the highest patient admissions?
- Which diagnosis occurs most frequently?
- Which age group visits the hospital most often?
- Which current or upcoming patient stays are at risk of becoming prolonged/high-burden cases?
- Can a manager or client ask these questions directly, in plain English, without needing an analyst or SQL knowledge?

---

# ✅ Business Impact

This project enables hospitals to:

- Improve operational efficiency.
- Monitor doctor performance.
- Track revenue trends.
- Analyze patient demographics.
- Support data-driven decision making.
- Reduce manual reporting effort.
- Improve healthcare planning.
- **Act proactively** on high-burden patient stays instead of reacting after the fact.
- **Reduce dependency on analysts** by letting non-technical managers and clients self-serve answers via the chatbot.

---

# 🏆 Project Achievements

✔ End-to-End ETL Pipeline
✔ Automated Data Extraction
✔ Data Cleaning & Validation
✔ SQL-Based Analytics Workflow
✔ Interactive Streamlit Dashboard
✔ Power BI Reporting Integration
✔ Machine Learning Prediction Model
✔ Local RAG-Based AI Chatbot
✔ Healthcare Domain Analytics
✔ GitHub Ready Project

---

# 📚 Skills Demonstrated

- Python Programming
- Pandas
- SQL
- ETL Pipeline
- Data Cleaning & Validation
- Data Analysis
- Streamlit
- Power BI
- Business Intelligence
- Scikit-learn / Machine Learning
- LangChain & Retrieval-Augmented Generation (RAG)
- Local LLMs (Ollama)
- Git & GitHub
- Healthcare Analytics

---

# 🚀 Future Enhancements

- Automate daily data refresh
- Integrate with Hospital Information System (HIS)
- Expand ML predictions (readmission risk, resource forecasting)
- Forecast revenue trends
- Deploy dashboard to Power BI Service
- Deploy the chatbot with a web-based UI for non-technical end users
- Build a REST API for live analytics and chatbot access

---

# 👨‍💻 Author

**Saqlain Sheikh**

BCA Student | Aspiring Data Analyst

Skills:
Python • SQL • Power BI • Pandas • Streamlit • Scikit-learn • LangChain • Ollama • ETL • Data Analytics

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!