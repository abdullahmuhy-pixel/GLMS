# GLMS — Global Logistics Management System
**Student:** Abdullah Muhydeen | **Student Number:** ST10540222  
**Module:** PROG7311 — Enterprise Application Development (EAPD7111/w)  
**Institution:** The Independent Institute of Education (IIE) — Rosebank College  
**Year:** 2026

---

## What This Project Does

GLMS is a web-based contract and service request management system built for TechMove Logistics. It replaces their legacy spreadsheet system with a centralised ASP.NET Core MVC application that handles:

- Client and contract management with status tracking
- Service requests linked to active contracts only
- Automatic USD → ZAR currency conversion via live API
- PDF signed agreement upload and download
- 3 GoF design patterns: Factory Method, Observer, Strategy

---

## Tech Stack

| Technology | Purpose |
|---|---|
| ASP.NET Core 8 MVC | Web application framework |
| Entity Framework Core 8 | ORM — code-first SQL Server |
| SQL Server (LocalDB) | Database |
| xUnit | Unit testing framework |
| Bootstrap 5 | Frontend styling |
| open.er-api.com | Free exchange rate API |

---

## How to Run

### Prerequisites
- Visual Studio 2022 (or VS Code with C# extension)
- .NET 8 SDK
- SQL Server LocalDB (installed with Visual Studio)

### Steps

1. **Clone the repository**
   ```
   git clone https://github.com/YOUR_USERNAME/GLMS.git
   cd GLMS
   ```

2. **Open the solution**
   Open `GLMS.sln` in Visual Studio 2022

3. **Run database migrations**
   In the Package Manager Console (Tools → NuGet → Package Manager Console):
   ```
   Add-Migration InitialCreate
   Update-Database
   ```
   Or run the `DatabaseMigration.sql` script directly in SQL Server Management Studio.

4. **Run the application**
   Press `F5` or click the green play button in Visual Studio.  
   The app opens at `https://localhost:7xxx`

5. **Run the unit tests**
   Open Test Explorer (Test → Test Explorer) and click **Run All Tests**.  
   All 28 tests should show green ✅

---

## Project Structure

```
GLMS/
├── GLMS.Web/                    # Main ASP.NET Core MVC application
│   ├── Controllers/             # HTTP request handlers
│   │   ├── ClientsController.cs
│   │   ├── ContractsController.cs
│   │   └── ServiceRequestsController.cs
│   ├── Data/
│   │   └── ApplicationDbContext.cs   # EF Core database context
│   ├── Models/                  # Database entities
│   │   ├── Client.cs
│   │   ├── Contract.cs
│   │   └── ServiceRequest.cs
│   ├── Services/                # Business logic & design patterns
│   │   ├── ICurrencyService.cs          # Strategy Pattern interface
│   │   ├── ExchangeRateCurrencyService.cs # Strategy: live API
│   │   ├── IContractFactory.cs          # Factory Method interface
│   │   ├── FreightContractFactory.cs    # Factory: freight contracts
│   │   ├── SLAContractFactory.cs        # Factory: SLA contracts
│   │   ├── IContractObserver.cs         # Observer Pattern interface
│   │   ├── ContractSubject.cs           # Observer: subject/publisher
│   │   ├── EmailNotifier.cs             # Observer: email alerts
│   │   ├── AuditLogger.cs               # Observer: audit logging
│   │   └── FileService.cs              # PDF upload/validation
│   ├── Views/                   # Razor views (UI)
│   │   ├── Clients/
│   │   ├── Contracts/
│   │   └── ServiceRequests/
│   ├── wwwroot/uploads/         # Uploaded PDF files stored here
│   ├── appsettings.json         # Connection string & config
│   └── Program.cs               # DI registration & app setup
│
├── GLMS.Tests/                  # xUnit test project
│   ├── Mocks/
│   │   └── MockCurrencyService.cs       # Strategy Pattern mock
│   ├── CurrencyCalculationTests.cs      # 8 tests
│   ├── FileValidationTests.cs           # 10 tests
│   ├── WorkflowLogicTests.cs            # 10 tests
│   └── ObserverPatternTests.cs          # 5 tests
│
└── DatabaseMigration.sql        # Manual SQL setup script
```

---

## Design Patterns Implemented

### 1. Factory Method (Creational)
`IContractFactory` → `FreightContractFactory` / `SLAContractFactory`  
Decouples contract creation logic from the controller. Adding a new contract type requires only one new class.

### 2. Observer (Behavioural)
`IContractObserver` → `EmailNotifier` / `AuditLogger`  
`ContractSubject` notifies all observers when a contract status changes, without knowing what they do.

### 3. Strategy (Behavioural)
`ICurrencyService` → `ExchangeRateCurrencyService` / `MockCurrencyService`  
Swaps live API for a fixed-rate mock in unit tests — no internet required for testing.

---

## Unit Tests (28 total — all should pass green)

| Test Class | Tests | What Is Verified |
|---|---|---|
| CurrencyCalculationTests | 8 | USD→ZAR math, edge cases, zero, negative, rounding |
| FileValidationTests | 10 | .pdf accepted, .exe/.docx/.jpg rejected, null, empty, no extension |
| WorkflowLogicTests | 10 | Contract status rules, factory validation, date edge cases |
| ObserverPatternTests | 5 | Observer attach/detach/notify, multiple observers, no observers |

---

## Connection String

Located in `GLMS.Web/appsettings.json`:
```json
"ConnectionStrings": {
  "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=GLMS_DB;Trusted_Connection=True;"
}
```

---

## References

- Freeman, A. 2022. *Pro ASP.NET Core 7*. New York: Apress.
- Gamma, E. et al. 1994. *Design Patterns*. Boston: Addison-Wesley.
- Martin, R.C. 2017. *Clean Architecture*. Boston: Prentice Hall.
