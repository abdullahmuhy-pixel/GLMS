using Microsoft.EntityFrameworkCore;
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
