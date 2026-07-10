-- analysis.sql
-- Business analysis queries for the Hospital Analytics project.
-- Written against the schema in create_tables.sql (PatientID, Name, Age, Gender,
-- BloodType, MedicalCondition, DateOfAdmission, Doctor, Hospital, Department,
-- InsuranceProvider, BillingAmount, RoomNumber, AdmissionType, DischargeDate,
-- Medication, TestResults, AgeGroup, LengthOfStay, AdmissionYear, AdmissionMonth,
-- AdmissionMonthName).
-- If you loaded data via load_sql.py (pandas to_sql), table/column names will
-- instead match the cleaned CSV headers exactly (e.g. [Billing Amount]) --
-- adjust bracketed identifiers accordingly.

USE HospitalDB;
GO

-- 1. Total Patients
SELECT COUNT(*) AS TotalPatients
FROM dbo.Patients;

-- 2. Monthly Admissions Trend
SELECT AdmissionYear, AdmissionMonth, AdmissionMonthName, COUNT(*) AS Admissions
FROM dbo.Patients
GROUP BY AdmissionYear, AdmissionMonth, AdmissionMonthName
ORDER BY AdmissionYear, AdmissionMonth;

-- 3. Department-wise Revenue
SELECT Department, SUM(BillingAmount) AS TotalRevenue, COUNT(*) AS PatientCount
FROM dbo.Patients
GROUP BY Department
ORDER BY TotalRevenue DESC;

-- 4. Top 10 Doctors by Patient Count
SELECT TOP 10 Doctor, COUNT(*) AS PatientsHandled, SUM(BillingAmount) AS RevenueGenerated
FROM dbo.Patients
GROUP BY Doctor
ORDER BY PatientsHandled DESC;

-- 5. Average Billing Amount Overall and by Department
SELECT Department, AVG(BillingAmount) AS AvgBilling
FROM dbo.Patients
GROUP BY Department
ORDER BY AvgBilling DESC;

-- 6. Average Length of Stay by Department
SELECT Department, AVG(CAST(LengthOfStay AS FLOAT)) AS AvgLengthOfStay
FROM dbo.Patients
GROUP BY Department
ORDER BY AvgLengthOfStay DESC;

-- 7. Insurance Provider Analysis
SELECT InsuranceProvider, COUNT(*) AS PatientCount, SUM(BillingAmount) AS TotalBilled
FROM dbo.Patients
GROUP BY InsuranceProvider
ORDER BY PatientCount DESC;

-- 8. Gender Distribution
SELECT Gender, COUNT(*) AS PatientCount,
       CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5,2)) AS Percentage
FROM dbo.Patients
GROUP BY Gender;

-- 9. Age Group Distribution
SELECT AgeGroup, COUNT(*) AS PatientCount
FROM dbo.Patients
GROUP BY AgeGroup
ORDER BY PatientCount DESC;

-- 10. Yearly Patient Trends
SELECT AdmissionYear, COUNT(*) AS TotalPatients, SUM(BillingAmount) AS TotalRevenue
FROM dbo.Patients
GROUP BY AdmissionYear
ORDER BY AdmissionYear;

-- 11. Revenue Ranking by Department (Window Function)
SELECT Department,
       SUM(BillingAmount) AS TotalRevenue,
       RANK() OVER (ORDER BY SUM(BillingAmount) DESC) AS RevenueRank
FROM dbo.Patients
GROUP BY Department;

-- 12. Doctor Ranking within each Department (Window Function)
SELECT Department, Doctor, PatientsHandled,
       ROW_NUMBER() OVER (PARTITION BY Department ORDER BY PatientsHandled DESC) AS RankInDept
FROM (
    SELECT Department, Doctor, COUNT(*) AS PatientsHandled
    FROM dbo.Patients
    GROUP BY Department, Doctor
) AS DeptDoctorCounts;

-- 13. CTE: Patients with Above-Average Billing
WITH AvgBilling AS (
    SELECT AVG(BillingAmount) AS OverallAvg FROM dbo.Patients
)
SELECT p.PatientID, p.Name, p.Department, p.BillingAmount
FROM dbo.Patients p
CROSS JOIN AvgBilling a
WHERE p.BillingAmount > a.OverallAvg
ORDER BY p.BillingAmount DESC;

-- 14. CTE: Monthly Revenue Growth (Month-over-Month)
WITH MonthlyRevenue AS (
    SELECT AdmissionYear, AdmissionMonth, SUM(BillingAmount) AS Revenue
    FROM dbo.Patients
    GROUP BY AdmissionYear, AdmissionMonth
)
SELECT AdmissionYear, AdmissionMonth, Revenue,
       LAG(Revenue) OVER (ORDER BY AdmissionYear, AdmissionMonth) AS PrevMonthRevenue,
       Revenue - LAG(Revenue) OVER (ORDER BY AdmissionYear, AdmissionMonth) AS RevenueChange
FROM MonthlyRevenue
ORDER BY AdmissionYear, AdmissionMonth;

-- 15. Most Frequent Medical Conditions
SELECT MedicalCondition, COUNT(*) AS Cases
FROM dbo.Patients
GROUP BY MedicalCondition
ORDER BY Cases DESC;

-- 16. Test Results Breakdown
SELECT TestResults, COUNT(*) AS Count
FROM dbo.Patients
GROUP BY TestResults;

-- 17. View: Executive Summary (reusable for Power BI / reporting)
IF OBJECT_ID('dbo.vw_ExecutiveSummary', 'V') IS NOT NULL
    DROP VIEW dbo.vw_ExecutiveSummary;
GO

CREATE VIEW dbo.vw_ExecutiveSummary AS
SELECT
    COUNT(*)                         AS TotalPatients,
    SUM(BillingAmount)               AS TotalRevenue,
    AVG(BillingAmount)               AS AvgBilling,
    AVG(CAST(LengthOfStay AS FLOAT)) AS AvgLengthOfStay
FROM dbo.Patients;
GO

-- 18. View: Department Performance (reusable for Power BI / reporting)
IF OBJECT_ID('dbo.vw_DepartmentPerformance', 'V') IS NOT NULL
    DROP VIEW dbo.vw_DepartmentPerformance;
GO

CREATE VIEW dbo.vw_DepartmentPerformance AS
SELECT
    Department,
    COUNT(*)                          AS PatientCount,
    SUM(BillingAmount)                AS TotalRevenue,
    AVG(BillingAmount)                AS AvgBilling,
    AVG(CAST(LengthOfStay AS FLOAT))  AS AvgLengthOfStay
FROM dbo.Patients
GROUP BY Department;
GO
