import os, subprocess

def make(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  created: {path}")

print("Creating Part 3 files...")

# ── GLMS.API Project ──────────────────────────────────────────────────────────

make("GLMS.API/GLMS.API.csproj", """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../GLMS.Web/GLMS.Web.csproj" />
  </ItemGroup>
</Project>
""")

make("GLMS.API/appsettings.json", """{
  "ConnectionStrings": {
    "DefaultConnection": "Server=sql-server-db,1433;Database=GLMS_DB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;"
  },
  "Jwt": {
    "Key": "GLMSTechMoveSecretKey2026SuperSecure!",
    "Issuer": "GLMS.API",
    "Audience": "GLMS.Web"
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

make("GLMS.API/appsettings.Development.json", """{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\\\mssqllocaldb;Database=GLMS_DB;Trusted_Connection=True;MultipleActiveResultSets=true"
  }
}
""")

# ── Repositories ──────────────────────────────────────────────────────────────

make("GLMS.API/Repositories/IContractRepository.cs", """using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    // Repository Pattern: abstracts database access from controllers
    public interface IContractRepository
    {
        Task<IEnumerable<Contract>> GetAllAsync(DateTime? startDate, DateTime? endDate, ContractStatus? status);
        Task<Contract?> GetByIdAsync(int id);
        Task<Contract> CreateAsync(Contract contract);
        Task<Contract?> UpdateStatusAsync(int id, ContractStatus status);
        Task<IEnumerable<Contract>> GetActiveContractsAsync();
    }
}
""")

make("GLMS.API/Repositories/ContractRepository.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public class ContractRepository : IContractRepository
    {
        private readonly ApplicationDbContext _context;

        public ContractRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Contract>> GetAllAsync(
            DateTime? startDate, DateTime? endDate, ContractStatus? status)
        {
            var query = _context.Contracts
                .Include(c => c.Client)
                .AsNoTracking()
                .AsQueryable();

            if (startDate.HasValue) query = query.Where(c => c.StartDate >= startDate.Value);
            if (endDate.HasValue)   query = query.Where(c => c.EndDate   <= endDate.Value);
            if (status.HasValue)    query = query.Where(c => c.Status    == status.Value);

            return await query.ToListAsync();
        }

        public async Task<Contract?> GetByIdAsync(int id)
        {
            return await _context.Contracts
                .Include(c => c.Client)
                .Include(c => c.ServiceRequests)
                .AsNoTracking()
                .FirstOrDefaultAsync(c => c.Id == id);
        }

        public async Task<Contract> CreateAsync(Contract contract)
        {
            _context.Contracts.Add(contract);
            await _context.SaveChangesAsync();
            return contract;
        }

        public async Task<Contract?> UpdateStatusAsync(int id, ContractStatus status)
        {
            var contract = await _context.Contracts.FindAsync(id);
            if (contract == null) return null;
            contract.Status = status;
            await _context.SaveChangesAsync();
            return contract;
        }

        public async Task<IEnumerable<Contract>> GetActiveContractsAsync()
        {
            return await _context.Contracts
                .Include(c => c.Client)
                .Where(c => c.Status == ContractStatus.Active)
                .AsNoTracking()
                .ToListAsync();
        }
    }
}
""")

make("GLMS.API/Repositories/IServiceRequestRepository.cs", """using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public interface IServiceRequestRepository
    {
        Task<IEnumerable<ServiceRequest>> GetAllAsync();
        Task<ServiceRequest?> GetByIdAsync(int id);
        Task<ServiceRequest> CreateAsync(ServiceRequest serviceRequest);
    }
}
""")

make("GLMS.API/Repositories/ServiceRequestRepository.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public class ServiceRequestRepository : IServiceRequestRepository
    {
        private readonly ApplicationDbContext _context;

        public ServiceRequestRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<ServiceRequest>> GetAllAsync()
        {
            return await _context.ServiceRequests
                .Include(sr => sr.Contract)
                    .ThenInclude(c => c!.Client)
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<ServiceRequest?> GetByIdAsync(int id)
        {
            return await _context.ServiceRequests
                .Include(sr => sr.Contract)
                    .ThenInclude(c => c!.Client)
                .AsNoTracking()
                .FirstOrDefaultAsync(sr => sr.Id == id);
        }

        public async Task<ServiceRequest> CreateAsync(ServiceRequest serviceRequest)
        {
            _context.ServiceRequests.Add(serviceRequest);
            await _context.SaveChangesAsync();
            return serviceRequest;
        }
    }
}
""")

make("GLMS.API/Repositories/IClientRepository.cs", """using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public interface IClientRepository
    {
        Task<IEnumerable<Client>> GetAllAsync();
        Task<Client?> GetByIdAsync(int id);
        Task<Client> CreateAsync(Client client);
    }
}
""")

make("GLMS.API/Repositories/ClientRepository.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public class ClientRepository : IClientRepository
    {
        private readonly ApplicationDbContext _context;
        public ClientRepository(ApplicationDbContext context) { _context = context; }

        public async Task<IEnumerable<Client>> GetAllAsync()
            => await _context.Clients.AsNoTracking().ToListAsync();

        public async Task<Client?> GetByIdAsync(int id)
            => await _context.Clients.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);

        public async Task<Client> CreateAsync(Client client)
        {
            _context.Clients.Add(client);
            await _context.SaveChangesAsync();
            return client;
        }
    }
}
""")

# ── API Controllers ───────────────────────────────────────────────────────────

make("GLMS.API/Controllers/ContractsApiController.cs", """using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;
namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/contracts")]
    public class ContractsApiController : ControllerBase
    {
        private readonly IContractRepository _repo;

        public ContractsApiController(IContractRepository repo)
        {
            _repo = repo;
        }

        // GET /api/contracts — with optional filtering
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll(
            [FromQuery] DateTime? startDate,
            [FromQuery] DateTime? endDate,
            [FromQuery] ContractStatus? status)
        {
            var contracts = await _repo.GetAllAsync(startDate, endDate, status);
            return Ok(contracts);
        }

        // GET /api/contracts/5
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var contract = await _repo.GetByIdAsync(id);
            if (contract == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(contract);
        }

        // POST /api/contracts — create new contract
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Create([FromBody] Contract contract)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);
            var created = await _repo.CreateAsync(contract);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }

        // PATCH /api/contracts/5/status — approve or decline
        [HttpPatch("{id}/status")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] ContractStatus status)
        {
            var updated = await _repo.UpdateStatusAsync(id, status);
            if (updated == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(updated);
        }

        // GET /api/contracts/active — only active contracts
        [HttpGet("active")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetActive()
        {
            var contracts = await _repo.GetActiveContractsAsync();
            return Ok(contracts);
        }
    }
}
""")

make("GLMS.API/Controllers/ServiceRequestsApiController.cs", """using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;
namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/servicerequests")]
    public class ServiceRequestsApiController : ControllerBase
    {
        private readonly IServiceRequestRepository _repo;
        private readonly IContractRepository _contractRepo;

        public ServiceRequestsApiController(
            IServiceRequestRepository repo,
            IContractRepository contractRepo)
        {
            _repo = repo;
            _contractRepo = contractRepo;
        }

        // GET /api/servicerequests
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll()
        {
            var requests = await _repo.GetAllAsync();
            return Ok(requests);
        }

        // GET /api/servicerequests/5
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var sr = await _repo.GetByIdAsync(id);
            if (sr == null) return NotFound(new { message = $"ServiceRequest {id} not found." });
            return Ok(sr);
        }

        // POST /api/servicerequests — with workflow validation
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Create([FromBody] ServiceRequest sr)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);

            // Workflow rule: block Expired or OnHold contracts
            var contract = await _contractRepo.GetByIdAsync(sr.ContractId);
            if (contract == null)
                return BadRequest(new { message = "Contract not found." });
            if (contract.Status == ContractStatus.Expired)
                return BadRequest(new { message = "Cannot create a request for an Expired contract." });
            if (contract.Status == ContractStatus.OnHold)
                return BadRequest(new { message = "Cannot create a request for an On Hold contract." });

            sr.CreatedAt = DateTime.Now;
            var created = await _repo.CreateAsync(sr);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
    }
}
""")

make("GLMS.API/Controllers/ClientsApiController.cs", """using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;
namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/clients")]
    public class ClientsApiController : ControllerBase
    {
        private readonly IClientRepository _repo;
        public ClientsApiController(IClientRepository repo) { _repo = repo; }

        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll()
            => Ok(await _repo.GetAllAsync());

        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var client = await _repo.GetByIdAsync(id);
            if (client == null) return NotFound(new { message = $"Client {id} not found." });
            return Ok(client);
        }

        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Create([FromBody] Client client)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);
            var created = await _repo.CreateAsync(client);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
    }
}
""")

# ── API Program.cs ────────────────────────────────────────────────────────────

make("GLMS.API/Program.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.API.Repositories;

var builder = WebApplication.CreateBuilder(args);

// ── Services ──────────────────────────────────────────────────────────────────
builder.Services.AddControllers()
    .AddJsonOptions(opts =>
        opts.JsonSerializerOptions.ReferenceHandler =
            System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles);

// EF Core — connects to SQL Server
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// Repository Pattern — decouples controllers from database
builder.Services.AddScoped<IContractRepository, ContractRepository>();
builder.Services.AddScoped<IServiceRequestRepository, ServiceRequestRepository>();
builder.Services.AddScoped<IClientRepository, ClientRepository>();

// Swagger / OpenAPI — self-documenting API
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "GLMS Web API",
        Version = "v1",
        Description = "Global Logistics Management System — TechMove Logistics API"
    });
});

// CORS — allow MVC frontend to call the API
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
        policy.WithOrigins("http://localhost:5000", "http://glms-frontend-web")
              .AllowAnyHeader()
              .AllowAnyMethod());
});

var app = builder.Build();

// ── Middleware ────────────────────────────────────────────────────────────────
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "GLMS API v1");
    c.RoutePrefix = "swagger";
});

app.UseCors("AllowFrontend");
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();

public partial class Program { }
""")

# ── Refactored MVC Services ───────────────────────────────────────────────────

make("GLMS.Web/Services/IGlmsApiService.cs", """namespace GLMS.Web.Services
{
    // Interface for all HttpClient calls to the GLMS Web API
    // This replaces direct database access in the MVC controllers
    public interface IGlmsApiService
    {
        Task<string> GetAsync(string endpoint);
        Task<string> PostAsync(string endpoint, object data);
        Task<string> PatchAsync(string endpoint, object data);
    }
}
""")

make("GLMS.Web/Services/GlmsApiService.cs", """using System.Text;
using System.Text.Json;
namespace GLMS.Web.Services
{
    // Concrete implementation — wraps HttpClient calls to the Web API
    public class GlmsApiService : IGlmsApiService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<GlmsApiService> _logger;

        public GlmsApiService(HttpClient httpClient, ILogger<GlmsApiService> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
        }

        public async Task<string> GetAsync(string endpoint)
        {
            try
            {
                var response = await _httpClient.GetAsync(endpoint);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError("API GET failed for {endpoint}: {msg}", endpoint, ex.Message);
                return "[]";
            }
        }

        public async Task<string> PostAsync(string endpoint, object data)
        {
            var json    = JsonSerializer.Serialize(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync(endpoint, content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> PatchAsync(string endpoint, object data)
        {
            var json    = JsonSerializer.Serialize(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await _httpClient.PatchAsync(endpoint, content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}
""")

# ── Updated MVC Program.cs ─────────────────────────────────────────────────────

make("GLMS.Web/Program.cs", """using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();

// EF Core — still needed for file uploads and direct operations
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// Strategy Pattern — currency conversion
builder.Services.AddHttpClient<ICurrencyService, ExchangeRateCurrencyService>();

// Factory Method Pattern
builder.Services.AddScoped<IContractFactory, FreightContractFactory>();

// Observer Pattern
builder.Services.AddScoped<ContractSubject>();
builder.Services.AddScoped<IContractObserver, EmailNotifier>();
builder.Services.AddScoped<IContractObserver, AuditLogger>();

// File Service
builder.Services.AddScoped<IFileService, FileService>();

// API Service — HttpClient that calls GLMS.API (Part 3 decoupling)
builder.Services.AddHttpClient<IGlmsApiService, GlmsApiService>(client =>
{
    client.BaseAddress = new Uri(
        builder.Configuration["ApiSettings:BaseUrl"] ?? "http://glms-backend-api:5001/");
});

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
  "ApiSettings": {
    "BaseUrl": "http://glms-backend-api:5001/"
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

# ── Integration Tests ─────────────────────────────────────────────────────────

make("GLMS.Tests/IntegrationTests/ContractsApiIntegrationTests.cs", """using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using System.Text;
using System.Text.Json;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    // Integration Tests: call the actual running API endpoints
    // These verify that HTTP status codes and JSON responses are correct
    public class ContractsApiIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ContractsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetContracts_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");

            // Assert — HTTP 200 OK
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetContracts_ReturnsJsonContentType()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");

            // Assert — response is JSON
            Assert.Equal("application/json",
                response.Content.Headers.ContentType?.MediaType);
        }

        [Fact]
        public async Task GetContracts_ReturnsNotNull()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");
            var content  = await response.Content.ReadAsStringAsync();

            // Assert — body is not null or empty
            Assert.NotNull(content);
            Assert.NotEmpty(content);
        }

        [Fact]
        public async Task GetContractById_InvalidId_ReturnsNotFound()
        {
            // Act — request a contract that does not exist
            var response = await _client.GetAsync("/api/contracts/99999");

            // Assert — HTTP 404 Not Found
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }

        [Fact]
        public async Task GetActiveContracts_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts/active");

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }
    }
}
""")

make("GLMS.Tests/IntegrationTests/ServiceRequestsApiIntegrationTests.cs", """using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    public class ServiceRequestsApiIntegrationTests
        : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ServiceRequestsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetServiceRequests_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests");

            // Assert — HTTP 200 OK
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetServiceRequests_ReturnsJsonArray()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests");
            var content  = await response.Content.ReadAsStringAsync();

            // Assert — returns a JSON array (not null)
            Assert.NotNull(content);
            Assert.True(content.StartsWith("[") || content.StartsWith("{"));
        }

        [Fact]
        public async Task GetServiceRequestById_InvalidId_ReturnsNotFound()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests/99999");

            // Assert
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }
    }
}
""")

make("GLMS.Tests/IntegrationTests/ClientsApiIntegrationTests.cs", """using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    public class ClientsApiIntegrationTests
        : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ClientsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetClients_ReturnsSuccessStatusCode()
        {
            var response = await _client.GetAsync("/api/clients");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetClients_ReturnsNotNull()
        {
            var response = await _client.GetAsync("/api/clients");
            var content  = await response.Content.ReadAsStringAsync();
            Assert.NotNull(content);
            Assert.NotEmpty(content);
        }

        [Fact]
        public async Task GetClientById_InvalidId_ReturnsNotFound()
        {
            var response = await _client.GetAsync("/api/clients/99999");
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }
    }
}
""")

# Update GLMS.Tests.csproj to include integration test packages
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
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../GLMS.Web/GLMS.Web.csproj" />
    <ProjectReference Include="../GLMS.API/GLMS.API.csproj" />
  </ItemGroup>
</Project>
""")

# ── Dockerfiles ───────────────────────────────────────────────────────────────

make("GLMS.API/Dockerfile", """# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project files
COPY GLMS.Web/GLMS.Web.csproj GLMS.Web/
COPY GLMS.API/GLMS.API.csproj GLMS.API/
RUN dotnet restore GLMS.API/GLMS.API.csproj

# Copy source files
COPY GLMS.Web/ GLMS.Web/
COPY GLMS.API/ GLMS.API/

# Build and publish
WORKDIR /src/GLMS.API
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 5001
ENV ASPNETCORE_URLS=http://+:5001
ENTRYPOINT ["dotnet", "GLMS.API.dll"]
""")

make("GLMS.Web/Dockerfile", """# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project files
COPY GLMS.Web/GLMS.Web.csproj GLMS.Web/
RUN dotnet restore GLMS.Web/GLMS.Web.csproj

# Copy all source files
COPY GLMS.Web/ GLMS.Web/

# Build and publish
WORKDIR /src/GLMS.Web
RUN dotnet publish -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "GLMS.Web.dll"]
""")

# ── Docker Compose ────────────────────────────────────────────────────────────

make("docker-compose.yml", """version: '3.9'

services:

  # Container 1: SQL Server Database
  sql-server-db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: sql-server-db
    environment:
      SA_PASSWORD: "YourStrong@Passw0rd"
      ACCEPT_EULA: "Y"
      MSSQL_PID: "Developer"
    ports:
      - "1433:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql
    networks:
      - glms-network
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -Q 'SELECT 1'"]
      interval: 15s
      timeout: 10s
      retries: 5

  # Container 2: GLMS Web API (Backend)
  glms-backend-api:
    build:
      context: .
      dockerfile: GLMS.API/Dockerfile
    container_name: glms-backend-api
    ports:
      - "5001:5001"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__DefaultConnection=Server=sql-server-db,1433;Database=GLMS_DB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;
    depends_on:
      sql-server-db:
        condition: service_healthy
    networks:
      - glms-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5001/swagger || exit 1"]
      interval: 20s
      timeout: 10s
      retries: 3

  # Container 3: GLMS MVC Frontend (Web App)
  glms-frontend-web:
    build:
      context: .
      dockerfile: GLMS.Web/Dockerfile
    container_name: glms-frontend-web
    ports:
      - "5000:5000"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__DefaultConnection=Server=sql-server-db,1433;Database=GLMS_DB;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;
      - ApiSettings__BaseUrl=http://glms-backend-api:5001/
    depends_on:
      - glms-backend-api
    networks:
      - glms-network

volumes:
  sqlserver_data:

networks:
  glms-network:
    driver: bridge
""")

# ── Updated Solution File ─────────────────────────────────────────────────────

make("GLMS.sln", """
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59

Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "GLMS.Web", "GLMS.Web\\GLMS.Web.csproj", "{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "GLMS.API", "GLMS.API\\GLMS.API.csproj", "{C3D4E5F6-A7B8-9012-CDEF-123456789012}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "GLMS.Tests", "GLMS.Tests\\GLMS.Tests.csproj", "{B2C3D4E5-F6A7-8901-BCDE-F12345678901}"
EndProject

Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|Any CPU = Debug|Any CPU
        Release|Any CPU = Release|Any CPU
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}.Release|Any CPU.Build.0 = Release|Any CPU
        {C3D4E5F6-A7B8-9012-CDEF-123456789012}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {C3D4E5F6-A7B8-9012-CDEF-123456789012}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {C3D4E5F6-A7B8-9012-CDEF-123456789012}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {C3D4E5F6-A7B8-9012-CDEF-123456789012}.Release|Any CPU.Build.0 = Release|Any CPU
        {B2C3D4E5-F6A7-8901-BCDE-F12345678901}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
        {B2C3D4E5-F6A7-8901-BCDE-F12345678901}.Debug|Any CPU.Build.0 = Debug|Any CPU
        {B2C3D4E5-F6A7-8901-BCDE-F12345678901}.Release|Any CPU.ActiveCfg = Release|Any CPU
        {B2C3D4E5-F6A7-8901-BCDE-F12345678901}.Release|Any CPU.Build.0 = Release|Any CPU
    EndGlobalSection
EndGlobal
""")

# ── Git push ──────────────────────────────────────────────────────────────────
print("\nAll Part 3 files created! Pushing to GitHub...")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m",
    "Add Part 3 - Web API, Repository Pattern, Docker, Integration Tests"], check=True)
subprocess.run(["git", "push"], check=True)
print("\nDone! Part 3 code is now on GitHub.")
