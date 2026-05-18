using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class EmailNotifier : IContractObserver
    {
        private readonly ILogger<EmailNotifier> _logger;
        public EmailNotifier(ILogger<EmailNotifier> logger) { _logger = logger; }
        public void OnStatusChanged(Contract contract) =>
            _logger.LogInformation("[EMAIL] Contract #{Id} status changed to {Status}.",
                contract.Id, contract.Status);
        public void OnExpiry(int contractId) =>
            _logger.LogWarning("[EMAIL] URGENT: Contract #{Id} has expired.", contractId);
    }
}
