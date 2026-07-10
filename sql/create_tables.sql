-- create_tables.sql
-- Creates the HospitalDB database and the Patients table schema.
-- Note: when using load_sql.py, pandas.to_sql() auto-creates the table for you.
-- This script is provided for manual setup / documentation of the schema.

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'HospitalDB')
BEGIN
    CREATE DATABASE HospitalDB;
END
GO

USE HospitalDB;
GO

IF OBJECT_ID('dbo.Patients', 'U') IS NOT NULL
    DROP TABLE dbo.Patients;
GO

CREATE TABLE dbo.Patients (
    PatientID            INT             PRIMARY KEY,
    Name                  NVARCHAR(150)   NOT NULL,
    Age                   INT             NOT NULL,
    Gender                NVARCHAR(20),
    BloodType             NVARCHAR(5),
    MedicalCondition      NVARCHAR(100),
    DateOfAdmission       DATE            NOT NULL,
    Doctor                NVARCHAR(150)   NOT NULL,
    Hospital              NVARCHAR(150)   NOT NULL,
    Department             NVARCHAR(100),
    InsuranceProvider     NVARCHAR(100),
    BillingAmount         DECIMAL(12,2)   NOT NULL,
    RoomNumber            INT,
    AdmissionType         NVARCHAR(50),
    DischargeDate          DATE,
    Medication             NVARCHAR(100),
    TestResults            NVARCHAR(50),
    AgeGroup                NVARCHAR(50),
    LengthOfStay           INT,
    AdmissionYear           INT,
    AdmissionMonth           INT,
    AdmissionMonthName       NVARCHAR(20)
);
GO

CREATE INDEX IX_Patients_Department ON dbo.Patients(Department);
CREATE INDEX IX_Patients_Doctor ON dbo.Patients(Doctor);
CREATE INDEX IX_Patients_DateOfAdmission ON dbo.Patients(DateOfAdmission);
GO
