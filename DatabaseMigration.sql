-- GLMS Database Migration Script
-- Run in SQL Server Management Studio against (localdb)\mssqllocaldb

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'GLMS_DB')
    CREATE DATABASE GLMS_DB;
GO
USE GLMS_DB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Clients')
    CREATE TABLE Clients (
        Id             INT IDENTITY(1,1) PRIMARY KEY,
        Name           NVARCHAR(100) NOT NULL,
        ContactDetails NVARCHAR(200) NOT NULL,
        Region         NVARCHAR(100) NOT NULL
    );
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Contracts')
    CREATE TABLE Contracts (
        Id                  INT IDENTITY(1,1) PRIMARY KEY,
        ClientId            INT           NOT NULL,
        StartDate           DATETIME2     NOT NULL,
        EndDate             DATETIME2     NOT NULL,
        Status              INT           NOT NULL DEFAULT 0,
        ServiceLevel        NVARCHAR(200) NOT NULL,
        SignedAgreementPath NVARCHAR(500) NULL,
        CONSTRAINT FK_Contracts_Clients
            FOREIGN KEY (ClientId) REFERENCES Clients(Id) ON DELETE NO ACTION
    );
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ServiceRequests')
    CREATE TABLE ServiceRequests (
        Id          INT IDENTITY(1,1) PRIMARY KEY,
        ContractId  INT           NOT NULL,
        Description NVARCHAR(500) NOT NULL,
        CostUSD     DECIMAL(18,2) NOT NULL,
        CostZAR     DECIMAL(18,2) NOT NULL DEFAULT 0,
        Status      INT           NOT NULL DEFAULT 0,
        CreatedAt   DATETIME2     NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_ServiceRequests_Contracts
            FOREIGN KEY (ContractId) REFERENCES Contracts(Id) ON DELETE NO ACTION
    );
GO

-- Performance indexes
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Contracts_Status')
    CREATE INDEX IX_Contracts_Status   ON Contracts(Status);
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Contracts_ClientId')
    CREATE INDEX IX_Contracts_ClientId ON Contracts(ClientId);
GO

-- Seed data
IF NOT EXISTS (SELECT * FROM Clients WHERE Id = 1)
    INSERT INTO Clients (Name, ContactDetails, Region) VALUES
    ('Acme Logistics',  'acme@logistics.com',      'Johannesburg'),
    ('FastFreight Ltd', 'info@fastfreight.co.za',  'Cape Town');
GO

PRINT 'GLMS_DB migration completed.';
