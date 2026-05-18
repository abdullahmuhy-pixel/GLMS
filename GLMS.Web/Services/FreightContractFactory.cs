using GLMS.Web.Models;
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
