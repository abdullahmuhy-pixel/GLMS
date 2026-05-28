using GLMS.Web.Models;
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
