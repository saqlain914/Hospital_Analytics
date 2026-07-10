# Power BI Dashboard

Open Power BI Desktop and connect to the `Patients` table:

- **SQLite (default local setup)**: import `data/cleaned/hospital_cleaned.csv` directly via "Get Data > Text/CSV", or use an ODBC SQLite driver pointing to `data/cleaned/hospital.db`.
- **SQL Server (production setup)**: Get Data > SQL Server > enter your `DB_SERVER` / `DB_NAME` from `.env`.

Suggested pages (matching project spec):
1. **Executive Dashboard** - Total Patients, Total Revenue, Avg Billing, Avg Length of Stay (KPI cards)
2. **Admissions Dashboard** - Monthly Admissions line chart, Department donut, Gender bar
3. **Doctor Dashboard** - Top Doctors bar chart, Patient Count by Doctor, Department slicer
4. **Financial Dashboard** - Revenue by Department, Insurance Coverage breakdown, Billing trend line

Save your .pbix file in this folder as HospitalDashboard.pbix.
