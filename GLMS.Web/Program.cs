using Microsoft.EntityFrameworkCore;
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
