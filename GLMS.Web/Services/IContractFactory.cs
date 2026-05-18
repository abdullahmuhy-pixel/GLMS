using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    // Factory Method Pattern interface
    public interface IContractFactory
    {
        Contract CreateContract(string contractType);
        bool ValidateContract(Contract contract);
    }
}
