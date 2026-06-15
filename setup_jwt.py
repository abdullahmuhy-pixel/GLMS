import os, subprocess

def make(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  created: {path}")

print("Adding JWT Authentication to GLMS.API...")

# ── Auth Models ───────────────────────────────────────────────────────────────

make("GLMS.API/Models/LoginRequest.cs", """namespace GLMS.API.Models
{
    public class LoginRequest
    {
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }
}
""")

make("GLMS.API/Models/LoginResponse.cs", """namespace GLMS.API.Models
{
    public class LoginResponse
    {
        public string Token { get; set; } = string.Empty;
        public string Username { get; set; } = string.Empty;
        public DateTime Expiry { get; set; }
    }
}
""")

# ── JWT Service ───────────────────────────────────────────────────────────────

make("GLMS.API/Services/IJwtService.cs", """namespace GLMS.API.Services
{
    public interface IJwtService
    {
        string GenerateToken(string username, string role);
        bool ValidateCredentials(string username, string password);
    }
}
""")

make("GLMS.API/Services/JwtService.cs", """using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

namespace GLMS.API.Services
{
    public class JwtService : IJwtService
    {
        private readonly IConfiguration _config;

        // Demo users — in production these would come from a database
        private readonly Dictionary<string, (string Password, string Role)> _users = new()
        {
            { "admin",   ("Admin@123", "Admin") },
            { "manager", ("Manager@123", "Manager") },
        };

        public JwtService(IConfiguration config)
        {
            _config = config;
        }

        public bool ValidateCredentials(string username, string password)
        {
            return _users.TryGetValue(username.ToLower(), out var user)
                && user.Password == password;
        }

        public string GenerateToken(string username, string role)
        {
            var key     = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
            var creds   = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var expiry  = DateTime.UtcNow.AddHours(8);

            var claims = new[]
            {
                new Claim(ClaimTypes.Name,  username),
                new Claim(ClaimTypes.Role,  role),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            };

            var token = new JwtSecurityToken(
                issuer:   _config["Jwt:Issuer"],
                audience: _config["Jwt:Audience"],
                claims:   claims,
                expires:  expiry,
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
""")

# ── Auth Controller ───────────────────────────────────────────────────────────

make("GLMS.API/Controllers/AuthController.cs", """using Microsoft.AspNetCore.Mvc;
using GLMS.API.Models;
using GLMS.API.Services;

namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/auth")]
    public class AuthController : ControllerBase
    {
        private readonly IJwtService _jwtService;

        public AuthController(IJwtService jwtService)
        {
            _jwtService = jwtService;
        }

        // POST /api/auth/login
        // Returns a JWT token if credentials are valid
        [HttpPost("login")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public IActionResult Login([FromBody] LoginRequest request)
        {
            if (!_jwtService.ValidateCredentials(request.Username, request.Password))
                return Unauthorized(new { message = "Invalid username or password." });

            var role  = request.Username.ToLower() == "admin" ? "Admin" : "Manager";
            var token = _jwtService.GenerateToken(request.Username, role);

            return Ok(new LoginResponse
            {
                Token    = token,
                Username = request.Username,
                Expiry   = DateTime.UtcNow.AddHours(8)
            });
        }

        // GET /api/auth/test
        // Verifies that a token is valid (for testing)
        [HttpGet("test")]
        [Microsoft.AspNetCore.Authorization.Authorize]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public IActionResult TestAuth()
        {
            var username = User.Identity?.Name;
            return Ok(new { message = $"Authenticated as {username}", success = true });
        }
    }
}
""")

# ── Updated ContractsApiController with [Authorize] ──────────────────────────

make("GLMS.API/Controllers/ContractsApiController.cs", """using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;

namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/contracts")]
    [Authorize] // JWT required for all contract endpoints
    public class ContractsApiController : ControllerBase
    {
        private readonly IContractRepository _repo;

        public ContractsApiController(IContractRepository repo)
        {
            _repo = repo;
        }

        // GET /api/contracts
        [HttpGet]
        [AllowAnonymous] // Allow unauthenticated read for demo
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
        [AllowAnonymous]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var contract = await _repo.GetByIdAsync(id);
            if (contract == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(contract);
        }

        // POST /api/contracts — requires JWT token
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public async Task<IActionResult> Create([FromBody] Contract contract)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);
            var created = await _repo.CreateAsync(contract);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }

        // PATCH /api/contracts/5/status — requires JWT token
        [HttpPatch("{id}/status")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] ContractStatus status)
        {
            var updated = await _repo.UpdateStatusAsync(id, status);
            if (updated == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(updated);
        }

        // GET /api/contracts/active
        [HttpGet("active")]
        [AllowAnonymous]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetActive()
        {
            var contracts = await _repo.GetActiveContractsAsync();
            return Ok(contracts);
        }
    }
}
""")

# ── Updated ServiceRequestsApiController with [Authorize] ────────────────────

make("GLMS.API/Controllers/ServiceRequestsApiController.cs", """using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;

namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/servicerequests")]
    [Authorize]
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

        [HttpGet]
        [AllowAnonymous]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll()
            => Ok(await _repo.GetAllAsync());

        [HttpGet("{id}")]
        [AllowAnonymous]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var sr = await _repo.GetByIdAsync(id);
            if (sr == null) return NotFound(new { message = $"ServiceRequest {id} not found." });
            return Ok(sr);
        }

        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public async Task<IActionResult> Create([FromBody] ServiceRequest sr)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);

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

# ── Updated Program.cs with JWT ───────────────────────────────────────────────

make("GLMS.API/Program.cs", """using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;
using GLMS.Web.Data;
using GLMS.API.Repositories;
using GLMS.API.Services;

var builder = WebApplication.CreateBuilder(args);

// ── Services ──────────────────────────────────────────────────────────────────
builder.Services.AddControllers()
    .AddJsonOptions(opts =>
        opts.JsonSerializerOptions.ReferenceHandler =
            System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles);

// EF Core
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// Repository Pattern
builder.Services.AddScoped<IContractRepository, ContractRepository>();
builder.Services.AddScoped<IServiceRequestRepository, ServiceRequestRepository>();
builder.Services.AddScoped<IClientRepository, ClientRepository>();

// JWT Service
builder.Services.AddScoped<IJwtService, JwtService>();

// ── JWT Authentication ────────────────────────────────────────────────────────
var jwtKey = builder.Configuration["Jwt:Key"]!;
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer           = true,
            ValidateAudience         = true,
            ValidateLifetime         = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer              = builder.Configuration["Jwt:Issuer"],
            ValidAudience            = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey         = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtKey))
        };
    });

builder.Services.AddAuthorization();

// ── Swagger with JWT support ──────────────────────────────────────────────────
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title       = "GLMS Web API",
        Version     = "v1",
        Description = "Global Logistics Management System API — TechMove Logistics"
    });

    // Add JWT auth to Swagger UI
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "Enter: Bearer {your token}",
        Name        = "Authorization",
        In          = ParameterLocation.Header,
        Type        = SecuritySchemeType.ApiKey,
        Scheme      = "Bearer"
    });
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id   = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

// CORS
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
app.UseAuthentication(); // JWT authentication middleware
app.UseAuthorization();
app.MapControllers();
app.Run();

public partial class Program { }
""")

# ── Updated csproj with JWT package ──────────────────────────────────────────

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
    <PackageReference Include="Microsoft.IdentityModel.Tokens" Version="7.0.0" />
    <PackageReference Include="System.IdentityModel.Tokens.Jwt" Version="7.0.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../GLMS.Web/GLMS.Web.csproj" />
  </ItemGroup>
</Project>
""")

# ── Git push ──────────────────────────────────────────────────────────────────
print("\nAll JWT files created! Pushing to GitHub...")
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m",
    "Add JWT Authentication - POST /api/auth/login + Bearer token protection"], check=True)
subprocess.run(["git", "push"], check=True)
print("\nDone! JWT authentication is now on GitHub.")
print("\nLogin credentials:")
print("  Username: admin    Password: Admin@123    Role: Admin")
print("  Username: manager  Password: Manager@123  Role: Manager")
