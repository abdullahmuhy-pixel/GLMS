using Microsoft.AspNetCore.Mvc;
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
