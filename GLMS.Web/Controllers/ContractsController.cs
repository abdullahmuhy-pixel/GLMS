using Microsoft.AspNetCore.Mvc;
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
