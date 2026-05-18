using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    // Observer Pattern interface
    public interface IContractObserver
    {
        void OnStatusChanged(Contract contract);
        void OnExpiry(int contractId);
    }
}
