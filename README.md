# 🏥 Hospital Analytics Dashboard | End-to-End Data Analytics Project

## 📌 Project Overview

Healthcare organizations generate thousands of patient records every day. Without proper analysis, it becomes difficult for hospital administrators to monitor patient admissions, doctor performance, billing trends, insurance claims, and departmental efficiency.

This project demonstrates a complete end-to-end healthcare analytics pipeline that combines data extraction, cleaning, SQL-based analysis, a Power BI-style reporting workflow, a Streamlit dashboard, machine-learning predictions for provider performance, and a local AI assistant powered by Ollama.

The project follows the ETL (Extract → Transform → Load) methodology commonly used in real-world healthcare analytics.

Dataset source: https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset

---

## 🎯 Business Problem

Hospitals often face challenges such as:

- Difficulty tracking patient admissions
- No centralized reporting system for operational performance
- Lack of visibility into department-wise revenue and billing trends
- Difficulty identifying provider or doctor performance issues
- Manual reporting consumes significant time
- Insurance and billing trends are hard to analyze
- Decision-making is based on incomplete or delayed information

---

## 💡 Proposed Solution

This project develops an automated analytics solution that:

- Extracts hospital data from Kaggle or local files
- Cleans and validates raw data using Python
- Loads processed data into a relational database
- Performs SQL-based business analysis
- Builds a dashboard experience through Streamlit and Power BI-style reporting
- Predicts whether a patient stay is likely to become a prolonged/high-burden case
- Supports natural-language questions through a local AI chatbot

---

## 🧠 Key Insights the Project Helps Reveal

The analytics workflow helps answer questions such as:

- Which departments generate the highest revenue?
- Which doctors or providers see the most patients?
- Which insurance providers are most commonly used?
- What is the average hospital stay duration?
- Which months have the highest admission volume?
- Which medical conditions are most frequent?
- Which age groups or demographics are more represented in the patient data?
- Which cases are likely to become long-stay or high-burden cases?

---

## 🔄 Project Workflow

```text
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
Business Insights + ML Predictions + AI Assistant
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data processing and ETL |
| Pandas | Data cleaning and transformation |
| Scikit-learn | Provider-performance prediction model |
| Streamlit | Interactive dashboard web app |
| SQLAlchemy | Database interaction |
| SQL | Data analysis and reporting |
| Power BI | Dashboard and reporting workflows |
| LangChain + Ollama | Local AI chatbot experience |
| Git & GitHub | Version control |

---

## 📂 Project Structure

```text
Hospital-Analytics/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
│   └── EDA.ipynb
├── powerbi/
│   └── README.md
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
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
└── screenshots/
```

---

## ▶ Quick Start

### 1) Create and activate a virtual environment

```powershell
python -m venv test_env
.\test_env\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run the Streamlit app

```powershell
python -m streamlit run app.py
```

### 4) Train the prediction model (optional)

```powershell
python src/ml/train.py
```

### 5) Run predictions from the command line (optional)

```powershell
python src/ml/predict.py --input data/raw/hospital_raw.csv
```

---

## 🤖 Ollama Setup for the Chatbot

The chatbot prefers a local Ollama model and will fall back gracefully if no local AI setup is available.

Install Ollama and run:

```powershell
ollama serve
ollama pull llama3.2:latest
```

If you want to use a different model, set the environment variable:

```powershell
$env:OLLAMA_MODEL = "llama3.1"
```

---

## 📥 About the Data Source

The project can use the hospital dataset from Kaggle, and it also includes local CSV data under the data folder so the workflow can run without live Kaggle access.

If Kaggle credentials are available, the extraction pipeline can still use them to pull the live dataset.

---

## ⚙ ETL Pipeline

### Step 1 – Extract

- Download dataset using KaggleHub API when available
- Store raw CSV files
- Validate downloaded data
- Use local fallback data if needed

### Step 2 – Transform

Cleaning operations include:

- Remove duplicate records
- Handle missing values
- Convert data types
- Standardize date formats
- Create calculated columns
- Validate billing values
- Generate age groups
- Calculate patient stay duration

### Step 3 – Load

- Connect Python with a database backend
- Create or populate the hospital analytics tables
- Verify successful insertion of cleaned data

---

## 📊 SQL Analysis

The project includes SQL analysis scripts for tasks such as:

- Total patients
- Monthly admissions
- Department-wise revenue
- Top doctors or providers
- Average billing amount
- Average length of stay
- Insurance analysis
- Gender and age distribution
- Revenue ranking and trend analysis

---

## 📈 Dashboard & Business Impact

This project helps hospital management answer important operational questions and supports better decision-making by making the data easier to explore and understand.

It enables hospitals to:

- Improve operational efficiency
- Monitor doctor/provider performance
- Track revenue trends
- Analyze patient demographics
- Support data-driven decision making
- Reduce manual reporting effort
- Improve healthcare planning

---

## ✅ Project Achievements

- End-to-end ETL pipeline
- Automated data extraction and cleaning
- SQL-based analytics workflow
- Interactive Streamlit dashboard experience
- Machine-learning prediction flow
- Local AI chatbot integration
- GitHub-ready project structure

---

## 📚 Dependencies

The main dependencies are listed in requirements.txt and include:

- pandas
- numpy
- scikit-learn
- streamlit
- langchain
- langchain-community
- langchain-experimental
- langchain-openai
- langchain-ollama
- SQLAlchemy
- python-dotenv
- kagglehub

---

## 👨‍💻 Author

Saqlain Sheikh

