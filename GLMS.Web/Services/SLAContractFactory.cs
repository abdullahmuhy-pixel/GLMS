using GLMS.Web.Models;
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
