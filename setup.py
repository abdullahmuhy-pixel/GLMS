import os, subprocess

def make(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  created: {path}")

print("Creating GLMS project files...")

# ── Models ─────────────────────────────────────────────────────────────────────

make("GLMS.Web/Models/Client.cs", """using System.ComponentModel.DataAnnotations;
namespace GLMS.Web.Models
{
    public class Client
    {
        public int Id { get; set; }
        [Required(ErrorMessage = "Name is required")]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;
        [Required(ErrorMessage = "Contact details are required")]
        [StringLength(200)]
        public string ContactDetails { get; set; } = string.Empty;
        [Required(ErrorMessage = "Region is required")]
        [StringLength(100)]
        public string Region { get; set; } = string.Empty;
        public ICollection<Contract> Contracts { get; set; } = new List<Contract>();
    }
}
""")

make("GLMS.Web/Models/Contract.cs", """using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace GLMS.Web.Models
{
    public enum ContractStatus { Draft, Active, Expired, OnHold }
    public class Contract
    {
        public int Id { get; set; }
        [Required] public int ClientId { get; set; }
        [Required][DataType(DataType.Date)] public DateTime StartDate { get; set; }
        [Required][DataType(DataType.Date)] public DateTime EndDate { get; set; }
        [Required] public ContractStatus Status { get; set; } = ContractStatus.Draft;
        [Required(ErrorMessage = "Service level is required")]
        [StringLength(200)] public string ServiceLevel { get; set; } = string.Empty;
        public string? SignedAgreementPath { get; set; }
        public Client? Client { get; set; }
        public ICollection<ServiceRequest> ServiceRequests { get; set; } = new List<ServiceRequest>();
    }
}
""")

make("GLMS.Web/Models/ServiceRequest.cs", """using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace GLMS.Web.Models
{
    public enum ServiceRequestStatus { Pending, InProgress, Completed, Cancelled }
    public class ServiceRequest
    {
        public int Id { get; set; }
        [Required] public int ContractId { get; set; }
        [Required(ErrorMessage = "Description is required")]
        [StringLength(500)] public string Description { get; set; } = string.Empty;
        [Required][Column(TypeName = "decimal(18,2)")]
        [Range(0.01, double.MaxValue, ErrorMessage = "Cost must be greater than zero")]
        public decimal CostUSD { get; set; }
        [Column(TypeName = "decimal(18,2)")] public decimal CostZAR { get; set; }
        public ServiceRequestStatus Status { get; set; } = ServiceRequestStatus.Pending;
        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public Contract? Contract { get; set; }
    }
}
""")

# ── Data ───────────────────────────────────────────────────────────────────────

make("GLMS.Web/Data/ApplicationDbContext.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Models;
namespace GLMS.Web.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options) { }
        public DbSet<Client> Clients { get; set; }
        public DbSet<Contract> Contracts { get; set; }
        public DbSet<ServiceRequest> ServiceRequests { get; set; }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Contract>()
                .HasOne(c => c.Client).WithMany(cl => cl.Contracts)
                .HasForeignKey(c => c.ClientId).OnDelete(DeleteBehavior.Restrict);
            modelBuilder.Entity<ServiceRequest>()
                .HasOne(sr => sr.Contract).WithMany(c => c.ServiceRequests)
                .HasForeignKey(sr => sr.ContractId).OnDelete(DeleteBehavior.Restrict);
            modelBuilder.Entity<Client>().HasData(
                new Client { Id = 1, Name = "Acme Logistics", ContactDetails = "acme@logistics.com", Region = "Johannesburg" },
                new Client { Id = 2, Name = "FastFreight Ltd", ContactDetails = "info@fastfreight.co.za", Region = "Cape Town" }
            );
        }
    }
}
""")

# ── Services ───────────────────────────────────────────────────────────────────

make("GLMS.Web/Services/ICurrencyService.cs", """namespace GLMS.Web.Services
{
    // Strategy Pattern interface
    public interface ICurrencyService
    {
        Task<decimal> ConvertUsdToZarAsync(decimal amountUsd);
    }
}
""")

make("GLMS.Web/Services/ExchangeRateCurrencyService.cs", """using System.Text.Json;
namespace GLMS.Web.Services
{
    public class ExchangeRateCurrencyService : ICurrencyService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<ExchangeRateCurrencyService> _logger;
        public ExchangeRateCurrencyService(HttpClient httpClient,
            ILogger<ExchangeRateCurrencyService> logger)
        { _httpClient = httpClient; _logger = logger; }

        public async Task<decimal> ConvertUsdToZarAsync(decimal amountUsd)
        {
            try
            {
                var response = await _httpClient.GetAsync("https://open.er-api.com/v6/latest/USD");
                response.EnsureSuccessStatusCode();
                var json = await response.Content.ReadAsStringAsync();
                var doc  = JsonDocument.Parse(json);
                var rate = doc.RootElement.GetProperty("rates").GetProperty("ZAR").GetDecimal();
                return Math.Round(amountUsd * rate, 2);
            }
            catch (Exception ex)
            {
                _logger.LogWarning("API unavailable: {msg}. Using fallback rate.", ex.Message);
                return Math.Round(amountUsd * 18.50m, 2);
            }
        }
    }
}
""")

make("GLMS.Web/Services/IContractFactory.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    // Factory Method Pattern interface
    public interface IContractFactory
    {
        Contract CreateContract(string contractType);
        bool ValidateContract(Contract contract);
    }
}
""")

make("GLMS.Web/Services/FreightContractFactory.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class FreightContractFactory : IContractFactory
    {
        public Contract CreateContract(string contractType) => new Contract
        {
            ServiceLevel = "Standard Freight SLA - 48hr delivery",
            Status = ContractStatus.Draft,
            StartDate = DateTime.Today,
            EndDate = DateTime.Today.AddYears(1)
        };

        public bool ValidateContract(Contract contract)
        {
            if (contract == null) return false;
            if (string.IsNullOrWhiteSpace(contract.ServiceLevel)) return false;
            if (contract.EndDate <= contract.StartDate) return false;
            if (contract.ClientId <= 0) return false;
            return true;
        }
    }
}
""")

make("GLMS.Web/Services/SLAContractFactory.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class SLAContractFactory : IContractFactory
    {
        public Contract CreateContract(string contractType) => new Contract
        {
            ServiceLevel = "Premium SLA - 99.9% uptime guaranteed",
            Status = ContractStatus.Draft,
            StartDate = DateTime.Today,
            EndDate = DateTime.Today.AddYears(2)
        };

        public bool ValidateContract(Contract contract)
        {
            if (contract == null) return false;
            if (string.IsNullOrWhiteSpace(contract.ServiceLevel)) return false;
            if (contract.EndDate <= contract.StartDate) return false;
            if (contract.ClientId <= 0) return false;
            if ((contract.EndDate - contract.StartDate).TotalDays < 180) return false;
            return true;
        }
    }
}
""")

make("GLMS.Web/Services/IContractObserver.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    // Observer Pattern interface
    public interface IContractObserver
    {
        void OnStatusChanged(Contract contract);
        void OnExpiry(int contractId);
    }
}
""")

make("GLMS.Web/Services/ContractSubject.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class ContractSubject
    {
        private readonly List<IContractObserver> _observers = new();
        private readonly ILogger<ContractSubject> _logger;

        public ContractSubject(ILogger<ContractSubject> logger) { _logger = logger; }

        public void Attach(IContractObserver observer)
        { if (!_observers.Contains(observer)) _observers.Add(observer); }

        public void Detach(IContractObserver observer) { _observers.Remove(observer); }

        public void NotifyStatusChanged(Contract contract)
        {
            _logger.LogInformation("Notifying {Count} observers for Contract #{Id}",
                _observers.Count, contract.Id);
            foreach (var obs in _observers) obs.OnStatusChanged(contract);
        }

        public void NotifyExpiry(int contractId)
        {
            foreach (var obs in _observers) obs.OnExpiry(contractId);
        }
    }
}
""")

make("GLMS.Web/Services/EmailNotifier.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class EmailNotifier : IContractObserver
    {
        private readonly ILogger<EmailNotifier> _logger;
        public EmailNotifier(ILogger<EmailNotifier> logger) { _logger = logger; }
        public void OnStatusChanged(Contract contract) =>
            _logger.LogInformation("[EMAIL] Contract #{Id} status changed to {Status}.",
                contract.Id, contract.Status);
        public void OnExpiry(int contractId) =>
            _logger.LogWarning("[EMAIL] URGENT: Contract #{Id} has expired.", contractId);
    }
}
""")

make("GLMS.Web/Services/AuditLogger.cs", """using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class AuditLogger : IContractObserver
    {
        private readonly ILogger<AuditLogger> _logger;
        public AuditLogger(ILogger<AuditLogger> logger) { _logger = logger; }
        public void OnStatusChanged(Contract contract) =>
            _logger.LogInformation("[AUDIT] {Time} | Contract #{Id} | Status -> {Status}",
                DateTime.UtcNow, contract.Id, contract.Status);
        public void OnExpiry(int contractId) =>
            _logger.LogWarning("[AUDIT] {Time} | Contract #{Id} | EXPIRED",
                DateTime.UtcNow, contractId);
    }
}
""")

make("GLMS.Web/Services/FileService.cs", """namespace GLMS.Web.Services
{
    public interface IFileService
    {
        bool IsValidPdf(IFormFile file);
        Task<string> SaveFileAsync(IFormFile file, string uploadFolder);
    }

    public class FileService : IFileService
    {
        private static readonly string[] AllowedExtensions = { ".pdf" };
        private const long MaxFileSizeBytes = 5 * 1024 * 1024;

        public bool IsValidPdf(IFormFile file)
        {
            if (file == null || file.Length == 0) return false;
            var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
            if (!AllowedExtensions.Contains(ext)) return false;
            if (file.Length > MaxFileSizeBytes) return false;
            return true;
        }

        public async Task<string> SaveFileAsync(IFormFile file, string uploadFolder)
        {
            Directory.CreateDirectory(uploadFolder);
            var uniqueName = $"{Guid.NewGuid()}_{Path.GetFileName(file.FileName)}";
            using var stream = new FileStream(Path.Combine(uploadFolder, uniqueName), FileMode.Create);
            await file.CopyToAsync(stream);
            return uniqueName;
        }
    }
}
""")

# ── Controllers ────────────────────────────────────────────────────────────────

make("GLMS.Web/Controllers/HomeController.cs", """using Microsoft.AspNetCore.Mvc;
namespace GLMS.Web.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index() => View();
    }
}
""")

make("GLMS.Web/Controllers/ClientsController.cs", """using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
namespace GLMS.Web.Controllers
{
    public class ClientsController : Controller
    {
        private readonly ApplicationDbContext _context;
        public ClientsController(ApplicationDbContext context) { _context = context; }

        public async Task<IActionResult> Index()
            => View(await _context.Clients.AsNoTracking().ToListAsync());

        public IActionResult Create() => View();

        [HttpPost][ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Name,ContactDetails,Region")] Client client)
        {
            if (ModelState.IsValid)
            { _context.Clients.Add(client); await _context.SaveChangesAsync(); return RedirectToAction(nameof(Index)); }
            return View(client);
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null) return NotFound();
            var client = await _context.Clients.Include(c => c.Contracts)
                .AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);
            if (client == null) return NotFound();
            return View(client);
        }

        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null) return NotFound();
            var client = await _context.Clients.FindAsync(id);
            if (client == null) return NotFound();
            return View(client);
        }

        [HttpPost][ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("Id,Name,ContactDetails,Region")] Client client)
        {
            if (id != client.Id) return NotFound();
            if (ModelState.IsValid)
            { _context.Update(client); await _context.SaveChangesAsync(); return RedirectToAction(nameof(Index)); }
            return View(client);
        }
    }
}
""")

make("GLMS.Web/Controllers/ContractsController.cs", """using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
using GLMS.Web.Services;
namespace GLMS.Web.Controllers
{
    public class ContractsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IFileService _fileService;
        private readonly IWebHostEnvironment _env;
        private readonly ContractSubject _subject;

        public ContractsController(ApplicationDbContext context, IFileService fileService,
            IWebHostEnvironment env, ContractSubject subject)
        { _context = context; _fileService = fileService; _env = env; _subject = subject; }

        public async Task<IActionResult> Index(DateTime? startDate, DateTime? endDate, ContractStatus? status)
        {
            var query = _context.Contracts.Include(c => c.Client).AsNoTracking().AsQueryable();
            if (startDate.HasValue) query = query.Where(c => c.StartDate >= startDate.Value);
            if (endDate.HasValue)   query = query.Where(c => c.EndDate   <= endDate.Value);
            if (status.HasValue)    query = query.Where(c => c.Status    == status.Value);
            ViewBag.StartDate = startDate?.ToString("yyyy-MM-dd");
            ViewBag.EndDate   = endDate?.ToString("yyyy-MM-dd");
            ViewBag.Status    = status;
            return View(await query.ToListAsync());
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null) return NotFound();
            var contract = await _context.Contracts.Include(c => c.Client)
                .Include(c => c.ServiceRequests).AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);
            if (contract == null) return NotFound();
            return View(contract);
        }

        public IActionResult Create()
        { ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name"); return View(); }

        [HttpPost][ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(
            [Bind("ClientId,StartDate,EndDate,Status,ServiceLevel")] Contract contract,
            IFormFile? signedAgreement)
        {
            if (ModelState.IsValid)
            {
                if (signedAgreement != null)
                {
                    if (!_fileService.IsValidPdf(signedAgreement))
                    { ModelState.AddModelError("", "Only PDF files are allowed (max 5MB).");
                      ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name");
                      return View(contract); }
                    var folder = Path.Combine(_env.WebRootPath, "uploads");
                    contract.SignedAgreementPath = await _fileService.SaveFileAsync(signedAgreement, folder);
                }
                _context.Contracts.Add(contract);
                await _context.SaveChangesAsync();
                _subject.NotifyStatusChanged(contract);
                return RedirectToAction(nameof(Index));
            }
            ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name", contract.ClientId);
            return View(contract);
        }

        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null) return NotFound();
            var contract = await _context.Contracts.FindAsync(id);
            if (contract == null) return NotFound();
            ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name", contract.ClientId);
            return View(contract);
        }

        [HttpPost][ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id,
            [Bind("Id,ClientId,StartDate,EndDate,Status,ServiceLevel,SignedAgreementPath")] Contract contract,
            IFormFile? signedAgreement)
        {
            if (id != contract.Id) return NotFound();
            if (ModelState.IsValid)
            {
                if (signedAgreement != null)
                {
                    if (!_fileService.IsValidPdf(signedAgreement))
                    { ModelState.AddModelError("", "Only PDF files are allowed.");
                      ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name", contract.ClientId);
                      return View(contract); }
                    var folder = Path.Combine(_env.WebRootPath, "uploads");
                    contract.SignedAgreementPath = await _fileService.SaveFileAsync(signedAgreement, folder);
                }
                _context.Update(contract);
                await _context.SaveChangesAsync();
                _subject.NotifyStatusChanged(contract);
                return RedirectToAction(nameof(Index));
            }
            ViewBag.Clients = new SelectList(_context.Clients, "Id", "Name", contract.ClientId);
            return View(contract);
        }

        public async Task<IActionResult> Download(int? id)
        {
            if (id == null) return NotFound();
            var contract = await _context.Contracts.FindAsync(id);
            if (contract == null || string.IsNullOrEmpty(contract.SignedAgreementPath)) return NotFound();
            var filePath = Path.Combine(_env.WebRootPath, "uploads", contract.SignedAgreementPath);
            if (!System.IO.File.Exists(filePath)) return NotFound();
            var bytes = await System.IO.File.ReadAllBytesAsync(filePath);
            return File(bytes, "application/pdf", contract.SignedAgreementPath);
        }
    }
}
""")

make("GLMS.Web/Controllers/ServiceRequestsController.cs", """using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
using GLMS.Web.Services;
namespace GLMS.Web.Controllers
{
    public class ServiceRequestsController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ICurrencyService _currencyService;

        public ServiceRequestsController(ApplicationDbContext context, ICurrencyService currencyService)
        { _context = context; _currencyService = currencyService; }

        public async Task<IActionResult> Index()
        {
            var requests = await _context.ServiceRequests
                .Include(sr => sr.Contract).ThenInclude(c => c!.Client)
                .AsNoTracking().ToListAsync();
            return View(requests);
        }

        public async Task<IActionResult> Create()
        {
            var active = await _context.Contracts.Include(c => c.Client)
                .Where(c => c.Status == ContractStatus.Active).AsNoTracking().ToListAsync();
            ViewBag.Contracts = new SelectList(
                active.Select(c => new { c.Id,
                    Display = $"{c.Client!.Name} - {c.ServiceLevel} (ends {c.EndDate:dd MMM yyyy})" }),
                "Id", "Display");
            return View();
        }

        [HttpPost][ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("ContractId,Description,CostUSD")] ServiceRequest sr)
        {
            var contract = await _context.Contracts.FindAsync(sr.ContractId);
            if (contract == null)
                ModelState.AddModelError("", "Selected contract does not exist.");
            else if (contract.Status == ContractStatus.Expired)
                ModelState.AddModelError("ContractId", "Cannot create a request for an Expired contract.");
            else if (contract.Status == ContractStatus.OnHold)
                ModelState.AddModelError("ContractId", "Cannot create a request for an On Hold contract.");

            if (ModelState.IsValid)
            {
                sr.CostZAR   = await _currencyService.ConvertUsdToZarAsync(sr.CostUSD);
                sr.CreatedAt = DateTime.Now;
                _context.ServiceRequests.Add(sr);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            var active = await _context.Contracts.Include(c => c.Client)
                .Where(c => c.Status == ContractStatus.Active).AsNoTracking().ToListAsync();
            ViewBag.Contracts = new SelectList(
                active.Select(c => new { c.Id, Display = $"{c.Client!.Name} - {c.ServiceLevel}" }),
                "Id", "Display", sr.ContractId);
            return View(sr);
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null) return NotFound();
            var sr = await _context.ServiceRequests
                .Include(s => s.Contract).ThenInclude(c => c!.Client)
                .AsNoTracking().FirstOrDefaultAsync(s => s.Id == id);
            if (sr == null) return NotFound();
            return View(sr);
        }

        [HttpGet]
        public async Task<IActionResult> GetZarRate(decimal usd)
        {
            if (usd <= 0) return BadRequest();
            var zar = await _currencyService.ConvertUsdToZarAsync(usd);
            return Json(new { usd, zar });
        }
    }
}
""")

# ── Program.cs ─────────────────────────────────────────────────────────────────

make("GLMS.Web/Program.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Strategy Pattern
builder.Services.AddHttpClient<ICurrencyService, ExchangeRateCurrencyService>();
// Factory Method Pattern
builder.Services.AddScoped<IContractFactory, FreightContractFactory>();
// Observer Pattern
builder.Services.AddScoped<ContractSubject>();
builder.Services.AddScoped<IContractObserver, EmailNotifier>();
builder.Services.AddScoped<IContractObserver, AuditLogger>();
// File Service
builder.Services.AddScoped<IFileService, FileService>();

var app = builder.Build();
if (!app.Environment.IsDevelopment()) { app.UseExceptionHandler("/Home/Error"); app.UseHsts(); }
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();
app.MapControllerRoute(name: "default", pattern: "{controller=Home}/{action=Index}/{id?}");
app.Run();
public partial class Program { }
""")

make("GLMS.Web/appsettings.json", """{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\\\mssqllocaldb;Database=GLMS_DB;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
""")

make("GLMS.Web/GLMS.Web.csproj", """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
  </ItemGroup>
</Project>
""")

# ── Views ──────────────────────────────────────────────────────────────────────

make("GLMS.Web/Views/_ViewImports.cshtml", """@using GLMS.Web
@using GLMS.Web.Models
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
""")

make("GLMS.Web/Views/_ViewStart.cshtml", """@{
    Layout = "_Layout";
}
""")

make("GLMS.Web/Views/Shared/_Layout.cshtml", """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - GLMS</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" />
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #0D47A1 !important; }
        .navbar-brand, .nav-link { color: white !important; }
        .nav-link:hover { color: #90CAF9 !important; }
        .card { border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">GLMS</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" asp-controller="Clients" asp-action="Index">Clients</a></li>
                    <li class="nav-item"><a class="nav-link" asp-controller="Contracts" asp-action="Index">Contracts</a></li>
                    <li class="nav-item"><a class="nav-link" asp-controller="ServiceRequests" asp-action="Index">Service Requests</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">@RenderBody()</div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
""")

make("GLMS.Web/Views/Shared/_ValidationScriptsPartial.cshtml",
"""<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.21.0/jquery.validate.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validation-unobtrusive/4.0.0/jquery.validate.unobtrusive.min.js"></script>
""")

make("GLMS.Web/Views/Home/Index.cshtml", """@{ ViewData["Title"] = "Dashboard"; }
<div class="row mb-4">
    <div class="col">
        <h2 class="text-primary fw-bold">Global Logistics Management System</h2>
        <p class="text-muted">TechMove Logistics - Contract and Service Request Platform</p>
    </div>
</div>
<div class="row g-4">
    <div class="col-md-4">
        <div class="card p-4 text-center h-100">
            <h5 class="mt-2">Clients</h5>
            <p class="text-muted small">Manage client profiles</p>
            <a asp-controller="Clients" asp-action="Index" class="btn btn-primary mt-auto">View Clients</a>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card p-4 text-center h-100">
            <h5 class="mt-2">Contracts</h5>
            <p class="text-muted small">Manage freight and SLA contracts</p>
            <a asp-controller="Contracts" asp-action="Index" class="btn btn-primary mt-auto">View Contracts</a>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card p-4 text-center h-100">
            <h5 class="mt-2">Service Requests</h5>
            <p class="text-muted small">Raise requests with USD to ZAR conversion</p>
            <a asp-controller="ServiceRequests" asp-action="Index" class="btn btn-primary mt-auto">View Requests</a>
        </div>
    </div>
</div>
""")

make("GLMS.Web/Views/Clients/Index.cshtml", """@model IEnumerable<Client>
@{ ViewData["Title"] = "Clients"; }
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-primary">Clients</h3>
    <a asp-action="Create" class="btn btn-success">+ New Client</a>
</div>
<div class="card">
    <table class="table table-hover mb-0">
        <thead class="table-dark">
            <tr><th>Name</th><th>Contact</th><th>Region</th><th>Actions</th></tr>
        </thead>
        <tbody>
            @foreach (var c in Model)
            {
                <tr>
                    <td class="fw-bold">@c.Name</td>
                    <td>@c.ContactDetails</td>
                    <td>@c.Region</td>
                    <td>
                        <a asp-action="Details" asp-route-id="@c.Id" class="btn btn-sm btn-outline-info">Details</a>
                        <a asp-action="Edit" asp-route-id="@c.Id" class="btn btn-sm btn-outline-secondary">Edit</a>
                    </td>
                </tr>
            }
        </tbody>
    </table>
</div>
""")

make("GLMS.Web/Views/Clients/Create.cshtml", """@model Client
@{ ViewData["Title"] = "New Client"; }
<h3 class="text-primary mb-4">New Client</h3>
<div class="card p-4" style="max-width:500px;">
    <form asp-action="Create" method="post">
        <div asp-validation-summary="All" class="alert alert-danger"></div>
        <div class="mb-3">
            <label asp-for="Name" class="form-label">Company Name</label>
            <input asp-for="Name" class="form-control" />
            <span asp-validation-for="Name" class="text-danger small"></span>
        </div>
        <div class="mb-3">
            <label asp-for="ContactDetails" class="form-label">Contact Details</label>
            <input asp-for="ContactDetails" class="form-control" />
        </div>
        <div class="mb-3">
            <label asp-for="Region" class="form-label">Region</label>
            <input asp-for="Region" class="form-control" />
        </div>
        <div class="d-flex gap-2">
            <button type="submit" class="btn btn-success">Save</button>
            <a asp-action="Index" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
@section Scripts { @{await Html.RenderPartialAsync("_ValidationScriptsPartial");} }
""")

make("GLMS.Web/Views/Clients/Details.cshtml", """@model Client
@{ ViewData["Title"] = "Client Details"; }
<div class="d-flex justify-content-between mb-3">
    <h3 class="text-primary">@Model.Name</h3>
    <a asp-action="Index" class="btn btn-secondary">Back</a>
</div>
<div class="card p-4" style="max-width:500px;">
    <dl class="row">
        <dt class="col-sm-4">Name</dt><dd class="col-sm-8">@Model.Name</dd>
        <dt class="col-sm-4">Contact</dt><dd class="col-sm-8">@Model.ContactDetails</dd>
        <dt class="col-sm-4">Region</dt><dd class="col-sm-8">@Model.Region</dd>
        <dt class="col-sm-4">Contracts</dt><dd class="col-sm-8">@Model.Contracts.Count</dd>
    </dl>
    <a asp-action="Edit" asp-route-id="@Model.Id" class="btn btn-outline-secondary btn-sm">Edit</a>
</div>
""")

make("GLMS.Web/Views/Clients/Edit.cshtml", """@model Client
@{ ViewData["Title"] = "Edit Client"; }
<h3 class="text-primary mb-4">Edit Client</h3>
<div class="card p-4" style="max-width:500px;">
    <form asp-action="Edit" method="post">
        <input type="hidden" asp-for="Id" />
        <div asp-validation-summary="All" class="alert alert-danger"></div>
        <div class="mb-3">
            <label asp-for="Name" class="form-label">Company Name</label>
            <input asp-for="Name" class="form-control" />
        </div>
        <div class="mb-3">
            <label asp-for="ContactDetails" class="form-label">Contact Details</label>
            <input asp-for="ContactDetails" class="form-control" />
        </div>
        <div class="mb-3">
            <label asp-for="Region" class="form-label">Region</label>
            <input asp-for="Region" class="form-control" />
        </div>
        <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">Update</button>
            <a asp-action="Index" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
""")

make("GLMS.Web/Views/Contracts/Index.cshtml", """@model IEnumerable<Contract>
@{ ViewData["Title"] = "Contracts"; }
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-primary">Contracts</h3>
    <a asp-action="Create" class="btn btn-success">+ New Contract</a>
</div>
<div class="card p-3 mb-4">
    <form method="get" asp-action="Index" class="row g-2 align-items-end">
        <div class="col-md-3">
            <label class="form-label small">Start Date (from)</label>
            <input type="date" name="startDate" class="form-control" value="@ViewBag.StartDate" />
        </div>
        <div class="col-md-3">
            <label class="form-label small">End Date (to)</label>
            <input type="date" name="endDate" class="form-control" value="@ViewBag.EndDate" />
        </div>
        <div class="col-md-3">
            <label class="form-label small">Status</label>
            <select name="status" class="form-select">
                <option value="">All</option>
                @foreach (ContractStatus s in Enum.GetValues(typeof(ContractStatus)))
                { <option value="@s" selected="@(ViewBag.Status?.ToString()==s.ToString())">@s</option> }
            </select>
        </div>
        <div class="col-md-3"><button type="submit" class="btn btn-primary w-100">Filter</button></div>
    </form>
</div>
<div class="card">
    <table class="table table-hover mb-0">
        <thead class="table-dark">
            <tr><th>Client</th><th>Service Level</th><th>Start</th><th>End</th><th>Status</th><th>PDF</th><th>Actions</th></tr>
        </thead>
        <tbody>
            @foreach (var c in Model)
            {
                <tr>
                    <td>@c.Client?.Name</td>
                    <td>@c.ServiceLevel</td>
                    <td>@c.StartDate.ToString("dd MMM yyyy")</td>
                    <td>@c.EndDate.ToString("dd MMM yyyy")</td>
                    <td>
                        @{ var badge = c.Status switch { ContractStatus.Active => "bg-success", ContractStatus.Expired => "bg-danger", ContractStatus.OnHold => "bg-warning text-dark", _ => "bg-secondary" }; }
                        <span class="badge @badge">@c.Status</span>
                    </td>
                    <td>
                        @if (!string.IsNullOrEmpty(c.SignedAgreementPath))
                        { <a asp-action="Download" asp-route-id="@c.Id" class="btn btn-sm btn-outline-primary">Download</a> }
                        else { <span class="text-muted small">None</span> }
                    </td>
                    <td>
                        <a asp-action="Details" asp-route-id="@c.Id" class="btn btn-sm btn-outline-info">Details</a>
                        <a asp-action="Edit" asp-route-id="@c.Id" class="btn btn-sm btn-outline-secondary">Edit</a>
                    </td>
                </tr>
            }
            @if (!Model.Any()) { <tr><td colspan="7" class="text-center text-muted py-3">No contracts found.</td></tr> }
        </tbody>
    </table>
</div>
""")

make("GLMS.Web/Views/Contracts/Create.cshtml", """@model Contract
@{ ViewData["Title"] = "Create Contract"; }
<h3 class="text-primary mb-4">Create New Contract</h3>
<div class="card p-4" style="max-width:640px;">
    <form asp-action="Create" method="post" enctype="multipart/form-data">
        <div asp-validation-summary="ModelOnly" class="alert alert-danger"></div>
        <div class="mb-3">
            <label asp-for="ClientId" class="form-label">Client</label>
            <select asp-for="ClientId" class="form-select" asp-items="ViewBag.Clients">
                <option value="">-- Select Client --</option>
            </select>
        </div>
        <div class="row">
            <div class="col mb-3">
                <label asp-for="StartDate" class="form-label">Start Date</label>
                <input asp-for="StartDate" class="form-control" type="date" />
            </div>
            <div class="col mb-3">
                <label asp-for="EndDate" class="form-label">End Date</label>
                <input asp-for="EndDate" class="form-control" type="date" />
            </div>
        </div>
        <div class="mb-3">
            <label asp-for="Status" class="form-label">Status</label>
            <select asp-for="Status" class="form-select" asp-items="Html.GetEnumSelectList<ContractStatus>()"></select>
        </div>
        <div class="mb-3">
            <label asp-for="ServiceLevel" class="form-label">Service Level</label>
            <input asp-for="ServiceLevel" class="form-control" placeholder="e.g. Standard Freight SLA" />
        </div>
        <div class="mb-3">
            <label class="form-label">Signed Agreement (PDF only, max 5MB)</label>
            <input type="file" name="signedAgreement" class="form-control" accept=".pdf" />
        </div>
        <div class="d-flex gap-2">
            <button type="submit" class="btn btn-success">Save Contract</button>
            <a asp-action="Index" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
@section Scripts { @{await Html.RenderPartialAsync("_ValidationScriptsPartial");} }
""")

make("GLMS.Web/Views/Contracts/Details.cshtml", """@model Contract
@{ ViewData["Title"] = "Contract Details"; }
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-primary">Contract Details</h3>
    <a asp-action="Index" class="btn btn-secondary">Back</a>
</div>
<div class="card p-4">
    <dl class="row">
        <dt class="col-sm-3">Client</dt><dd class="col-sm-9">@Model.Client?.Name</dd>
        <dt class="col-sm-3">Service Level</dt><dd class="col-sm-9">@Model.ServiceLevel</dd>
        <dt class="col-sm-3">Start Date</dt><dd class="col-sm-9">@Model.StartDate.ToString("dd MMM yyyy")</dd>
        <dt class="col-sm-3">End Date</dt><dd class="col-sm-9">@Model.EndDate.ToString("dd MMM yyyy")</dd>
        <dt class="col-sm-3">Status</dt>
        <dd class="col-sm-9">
            @{ var badge = Model.Status switch { ContractStatus.Active => "bg-success", ContractStatus.Expired => "bg-danger", ContractStatus.OnHold => "bg-warning text-dark", _ => "bg-secondary" }; }
            <span class="badge @badge">@Model.Status</span>
        </dd>
        <dt class="col-sm-3">Signed PDF</dt>
        <dd class="col-sm-9">
            @if (!string.IsNullOrEmpty(Model.SignedAgreementPath))
            { <a asp-action="Download" asp-route-id="@Model.Id" class="btn btn-sm btn-outline-primary">Download PDF</a> }
            else { <span class="text-muted">Not uploaded</span> }
        </dd>
    </dl>
</div>
""")

make("GLMS.Web/Views/Contracts/Edit.cshtml", """@model Contract
@{ ViewData["Title"] = "Edit Contract"; }
<h3 class="text-primary mb-4">Edit Contract</h3>
<div class="card p-4" style="max-width:640px;">
    <form asp-action="Edit" method="post" enctype="multipart/form-data">
        <div asp-validation-summary="ModelOnly" class="alert alert-danger"></div>
        <input type="hidden" asp-for="Id" />
        <input type="hidden" asp-for="SignedAgreementPath" />
        <div class="mb-3">
            <label asp-for="ClientId" class="form-label">Client</label>
            <select asp-for="ClientId" class="form-select" asp-items="ViewBag.Clients"></select>
        </div>
        <div class="row">
            <div class="col mb-3">
                <label asp-for="StartDate" class="form-label">Start Date</label>
                <input asp-for="StartDate" class="form-control" type="date" />
            </div>
            <div class="col mb-3">
                <label asp-for="EndDate" class="form-label">End Date</label>
                <input asp-for="EndDate" class="form-control" type="date" />
            </div>
        </div>
        <div class="mb-3">
            <label asp-for="Status" class="form-label">Status</label>
            <select asp-for="Status" class="form-select" asp-items="Html.GetEnumSelectList<ContractStatus>()"></select>
        </div>
        <div class="mb-3">
            <label asp-for="ServiceLevel" class="form-label">Service Level</label>
            <input asp-for="ServiceLevel" class="form-control" />
        </div>
        <div class="mb-3">
            <label class="form-label">Replace PDF (optional)</label>
            @if (!string.IsNullOrEmpty(Model.SignedAgreementPath))
            { <div class="alert alert-info py-1 small mb-1">Current: @Model.SignedAgreementPath</div> }
            <input type="file" name="signedAgreement" class="form-control" accept=".pdf" />
        </div>
        <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">Update</button>
            <a asp-action="Index" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
""")

make("GLMS.Web/Views/ServiceRequests/Index.cshtml", """@model IEnumerable<ServiceRequest>
@{ ViewData["Title"] = "Service Requests"; }
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-primary">Service Requests</h3>
    <a asp-action="Create" class="btn btn-success">+ New Request</a>
</div>
<div class="card">
    <table class="table table-hover mb-0">
        <thead class="table-dark">
            <tr><th>Contract / Client</th><th>Description</th><th>USD</th><th>ZAR</th><th>Status</th><th>Created</th><th></th></tr>
        </thead>
        <tbody>
            @foreach (var sr in Model)
            {
                <tr>
                    <td><div>@sr.Contract?.Client?.Name</div><small class="text-muted">@sr.Contract?.ServiceLevel</small></td>
                    <td>@sr.Description</td>
                    <td>$@sr.CostUSD.ToString("N2")</td>
                    <td class="text-success fw-bold">R@sr.CostZAR.ToString("N2")</td>
                    <td><span class="badge bg-warning text-dark">@sr.Status</span></td>
                    <td>@sr.CreatedAt.ToString("dd MMM yyyy")</td>
                    <td><a asp-action="Details" asp-route-id="@sr.Id" class="btn btn-sm btn-outline-info">Details</a></td>
                </tr>
            }
            @if (!Model.Any()) { <tr><td colspan="7" class="text-center text-muted py-3">No requests yet.</td></tr> }
        </tbody>
    </table>
</div>
""")

make("GLMS.Web/Views/ServiceRequests/Create.cshtml", """@model ServiceRequest
@{ ViewData["Title"] = "New Service Request"; }
<h3 class="text-primary mb-4">New Service Request</h3>
<div class="card p-4" style="max-width:580px;">
    <form asp-action="Create" method="post">
        <div asp-validation-summary="ModelOnly" class="alert alert-danger"></div>
        <div class="mb-3">
            <label asp-for="ContractId" class="form-label">Contract (Active only)</label>
            <select asp-for="ContractId" class="form-select" asp-items="ViewBag.Contracts">
                <option value="">-- Select Active Contract --</option>
            </select>
            <span asp-validation-for="ContractId" class="text-danger small"></span>
            <div class="form-text">Expired and On Hold contracts are blocked.</div>
        </div>
        <div class="mb-3">
            <label asp-for="Description" class="form-label">Description</label>
            <textarea asp-for="Description" class="form-control" rows="3"></textarea>
            <span asp-validation-for="Description" class="text-danger small"></span>
        </div>
        <div class="mb-3">
            <label asp-for="CostUSD" class="form-label">Cost (USD)</label>
            <input asp-for="CostUSD" class="form-control" type="number" step="0.01" min="0.01" id="costUsdInput" />
            <span asp-validation-for="CostUSD" class="text-danger small"></span>
        </div>
        <div class="alert alert-success py-2" id="zarPreview" style="display:none;">
            <strong>Estimated ZAR:</strong> <span id="zarAmount" class="fw-bold fs-5">R 0.00</span>
            <small class="text-muted ms-2">(live rate)</small>
        </div>
        <div class="d-flex gap-2 mt-3">
            <button type="submit" class="btn btn-success">Submit Request</button>
            <a asp-action="Index" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}
    <script>
        const input = document.getElementById('costUsdInput');
        const preview = document.getElementById('zarPreview');
        const zarSpan = document.getElementById('zarAmount');
        let timer;
        input.addEventListener('input', function () {
            clearTimeout(timer);
            const usd = parseFloat(this.value);
            if (!usd || usd <= 0) { preview.style.display = 'none'; return; }
            timer = setTimeout(async () => {
                try {
                    const res = await fetch('/ServiceRequests/GetZarRate?usd=' + usd);
                    const data = await res.json();
                    zarSpan.textContent = 'R ' + data.zar.toFixed(2);
                    preview.style.display = 'block';
                } catch { zarSpan.textContent = 'Rate unavailable'; preview.style.display = 'block'; }
            }, 500);
        });
    </script>
}
""")

make("GLMS.Web/Views/ServiceRequests/Details.cshtml", """@model ServiceRequest
@{ ViewData["Title"] = "Request Details"; }
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-primary">Service Request Details</h3>
    <a asp-action="Index" class="btn btn-secondary">Back</a>
</div>
<div class="card p-4" style="max-width:540px;">
    <dl class="row">
        <dt class="col-sm-4">Client</dt><dd class="col-sm-8">@Model.Contract?.Client?.Name</dd>
        <dt class="col-sm-4">Contract</dt><dd class="col-sm-8">@Model.Contract?.ServiceLevel</dd>
        <dt class="col-sm-4">Description</dt><dd class="col-sm-8">@Model.Description</dd>
        <dt class="col-sm-4">Cost (USD)</dt><dd class="col-sm-8">$@Model.CostUSD.ToString("N2")</dd>
        <dt class="col-sm-4">Cost (ZAR)</dt><dd class="col-sm-8 text-success fw-bold fs-5">R@Model.CostZAR.ToString("N2")</dd>
        <dt class="col-sm-4">Status</dt><dd class="col-sm-8"><span class="badge bg-warning text-dark">@Model.Status</span></dd>
        <dt class="col-sm-4">Created</dt><dd class="col-sm-8">@Model.CreatedAt.ToString("dd MMM yyyy HH:mm")</dd>
    </dl>
</div>
""")

# ── Tests ──────────────────────────────────────────────────────────────────────

make("GLMS.Tests/Mocks/MockCurrencyService.cs", """using GLMS.Web.Services;
namespace GLMS.Tests.Mocks
{
    public class MockCurrencyService : ICurrencyService
    {
        private readonly decimal _fixedRate;
        public MockCurrencyService(decimal fixedRate = 18.50m) { _fixedRate = fixedRate; }
        public Task<decimal> ConvertUsdToZarAsync(decimal amountUsd)
            => Task.FromResult(Math.Round(amountUsd * _fixedRate, 2));
    }
}
""")

make("GLMS.Tests/CurrencyCalculationTests.cs", """using GLMS.Tests.Mocks;
using Xunit;
namespace GLMS.Tests
{
    public class CurrencyCalculationTests
    {
        [Fact]
        public async Task ConvertUsdToZar_StandardAmount_ReturnsCorrectResult()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(1850.00m, await s.ConvertUsdToZarAsync(100m)); }

        [Fact]
        public async Task ConvertUsdToZar_OneDollar_ReturnsExactRate()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(18.50m, await s.ConvertUsdToZarAsync(1m)); }

        [Fact]
        public async Task ConvertUsdToZar_ZeroAmount_ReturnsZero()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(0.00m, await s.ConvertUsdToZarAsync(0m)); }

        [Fact]
        public async Task ConvertUsdToZar_NegativeAmount_ReturnsNegativeZar()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(-925.00m, await s.ConvertUsdToZarAsync(-50m)); }

        [Fact]
        public async Task ConvertUsdToZar_LargeAmount_CalculatesCorrectly()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(925000.00m, await s.ConvertUsdToZarAsync(50000m)); }

        [Fact]
        public async Task ConvertUsdToZar_DecimalAmount_RoundsToTwoPlaces()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(22.83m, await s.ConvertUsdToZarAsync(1.234m)); }

        [Fact]
        public async Task ConvertUsdToZar_DifferentRates_ProduceDifferentResults()
        {
            var s1 = new MockCurrencyService(18.00m);
            var s2 = new MockCurrencyService(20.00m);
            Assert.Equal(1800.00m, await s1.ConvertUsdToZarAsync(100m));
            Assert.Equal(2000.00m, await s2.ConvertUsdToZarAsync(100m));
        }

        [Fact]
        public async Task ConvertUsdToZar_ZeroRate_ReturnsZero()
        { var s = new MockCurrencyService(0m); Assert.Equal(0.00m, await s.ConvertUsdToZarAsync(100m)); }
    }
}
""")

make("GLMS.Tests/FileValidationTests.cs", """using GLMS.Web.Services;
using Microsoft.AspNetCore.Http;
using System.Text;
using Xunit;
namespace GLMS.Tests
{
    public class FileValidationTests
    {
        private readonly FileService _fileService = new FileService();

        private IFormFile CreateMockFile(string fileName, string content = "fake content")
        {
            var bytes = Encoding.UTF8.GetBytes(content);
            var stream = new MemoryStream(bytes);
            return new FormFile(stream, 0, bytes.Length, "file", fileName)
            { Headers = new HeaderDictionary(), ContentType = "application/octet-stream" };
        }

        [Fact] public void IsValidPdf_ValidPdfFile_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("contract.pdf"))); }

        [Fact] public void IsValidPdf_ExeFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("malware.exe"))); }

        [Fact] public void IsValidPdf_DocxFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("contract.docx"))); }

        [Fact] public void IsValidPdf_JpgFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("photo.jpg"))); }

        [Fact] public void IsValidPdf_NullFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(null!)); }

        [Fact] public void IsValidPdf_EmptyFile_ReturnsFalse()
        {
            var stream = new MemoryStream(Array.Empty<byte>());
            Assert.False(_fileService.IsValidPdf(new FormFile(stream, 0, 0, "file", "empty.pdf")));
        }

        [Fact] public void IsValidPdf_UpperCasePdf_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("CONTRACT.PDF"))); }

        [Fact] public void IsValidPdf_MixedCasePdf_ReturnsTrue()
        { Assert.True(_fileService.IsValidPdf(CreateMockFile("doc.Pdf"))); }

        [Fact] public void IsValidPdf_TxtFile_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("notes.txt"))); }

        [Fact] public void IsValidPdf_NoExtension_ReturnsFalse()
        { Assert.False(_fileService.IsValidPdf(CreateMockFile("contractfile"))); }
    }
}
""")

make("GLMS.Tests/WorkflowLogicTests.cs", """using GLMS.Web.Models;
using GLMS.Web.Services;
using Xunit;
namespace GLMS.Tests
{
    public class WorkflowLogicTests
    {
        private bool CanCreate(ContractStatus s)
            => s != ContractStatus.Expired && s != ContractStatus.OnHold;

        [Fact] public void ActiveContract_CanCreate() => Assert.True(CanCreate(ContractStatus.Active));
        [Fact] public void DraftContract_CanCreate() => Assert.True(CanCreate(ContractStatus.Draft));
        [Fact] public void ExpiredContract_CannotCreate() => Assert.False(CanCreate(ContractStatus.Expired));
        [Fact] public void OnHoldContract_CannotCreate() => Assert.False(CanCreate(ContractStatus.OnHold));

        [Fact]
        public void AllStatuses_CorrectResults()
        {
            Assert.True(CanCreate(ContractStatus.Active));
            Assert.True(CanCreate(ContractStatus.Draft));
            Assert.False(CanCreate(ContractStatus.Expired));
            Assert.False(CanCreate(ContractStatus.OnHold));
        }

        [Fact]
        public void FreightFactory_ValidContract_Passes()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "Freight SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddYears(1) };
            Assert.True(f.ValidateContract(c));
        }

        [Fact] public void FreightFactory_NullContract_Fails()
        { Assert.False(new FreightContractFactory().ValidateContract(null!)); }

        [Fact]
        public void FreightFactory_EndBeforeStart_Fails()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddDays(-1) };
            Assert.False(f.ValidateContract(c));
        }

        [Fact]
        public void SLAFactory_ShortDuration_Fails()
        {
            var f = new SLAContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddDays(30) };
            Assert.False(f.ValidateContract(c));
        }

        [Fact]
        public void FreightFactory_MissingClientId_Fails()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 0, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddYears(1) };
            Assert.False(f.ValidateContract(c));
        }
    }
}
""")

make("GLMS.Tests/ObserverPatternTests.cs", """using GLMS.Web.Models;
using GLMS.Web.Services;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;
namespace GLMS.Tests
{
    public class ObserverPatternTests
    {
        private class SpyObserver : IContractObserver
        {
            public bool StatusChangedCalled { get; private set; }
            public bool ExpiryCalled { get; private set; }
            public Contract? LastContract { get; private set; }
            public int LastExpiredId { get; private set; }
            public void OnStatusChanged(Contract c) { StatusChangedCalled = true; LastContract = c; }
            public void OnExpiry(int id) { ExpiryCalled = true; LastExpiredId = id; }
        }

        [Fact]
        public void NotifyStatusChanged_RegisteredObserver_IsNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.NotifyStatusChanged(new Contract { Id = 1, Status = ContractStatus.Expired });
            Assert.True(spy.StatusChangedCalled);
        }

        [Fact]
        public void NotifyExpiry_RegisteredObserver_IsNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.NotifyExpiry(42);
            Assert.True(spy.ExpiryCalled);
            Assert.Equal(42, spy.LastExpiredId);
        }

        [Fact]
        public void DetachedObserver_DoesNotReceiveNotification()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.Detach(spy);
            subject.NotifyStatusChanged(new Contract { Id = 5 });
            Assert.False(spy.StatusChangedCalled);
        }

        [Fact]
        public void MultipleObservers_AllNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy1 = new SpyObserver(); var spy2 = new SpyObserver();
            subject.Attach(spy1); subject.Attach(spy2);
            subject.NotifyStatusChanged(new Contract { Id = 3 });
            Assert.True(spy1.StatusChangedCalled);
            Assert.True(spy2.StatusChangedCalled);
        }

        [Fact]
        public void NoObservers_NotifyDoesNotThrow()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var ex = Record.Exception(() => subject.NotifyStatusChanged(new Contract { Id = 99 }));
            Assert.Null(ex);
        }
    }
}
""")

make("GLMS.Tests/GLMS.Tests.csproj", """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4" />
    <PackageReference Include="Microsoft.AspNetCore.Http" Version="2.2.2" />
    <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="8.0.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../GLMS.Web/GLMS.Web.csproj" />
  </ItemGroup>
</Project>
""")

# ── Git push ───────────────────────────────────────────────────────────────────
print("\nAll files created! Pushing to GitHub...")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Add complete GLMS project - EAPD7111/w POE Part 2"], check=True)
subprocess.run(["git", "push"], check=True)
print("\nDone! All files are now on GitHub.")
