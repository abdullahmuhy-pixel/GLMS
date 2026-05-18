using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class ContractSubject
    {
        private readonly List<IContractObserver> _observers = new();
        private readonly ILogger<ContractSubject> _logger;

        public ContractSubject(ILogger<ContractSubject> logger) { _logger = logger; }

        public void Attach(IContractObserver observer)
        { if (!_observers.Contains(observer)) _observers.Add(observer); }

        public void Detach(IContractObserver observer) { _observers.Remove(observer); }

        public void NotifyStatusChanged(Contract contract)
        {
            _logger.LogInformation("Notifying {Count} observers for Contract #{Id}",
                _observers.Count, contract.Id);
            foreach (var obs in _observers) obs.OnStatusChanged(contract);
        }

        public void NotifyExpiry(int contractId)
        {
            foreach (var obs in _observers) obs.OnExpiry(contractId);
        }
    }
}
