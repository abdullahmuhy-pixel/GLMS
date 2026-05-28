using Microsoft.EntityFrameworkCore;
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
