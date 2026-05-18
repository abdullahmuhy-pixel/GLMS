using GLMS.Web.Models;
namespace GLMS.Web.Services
{
    public class AuditLogger : IContractObserver
    {
        private readonly ILogger<AuditLogger> _logger;
        public AuditLogger(ILogger<AuditLogger> logger) { _logger = logger; }
        public void OnStatusChanged(Contract contract) =>
            _logger.LogInformation("[AUDIT] {Time} | Contract #{Id} | Status -> {Status}",
                DateTime.UtcNow, contract.Id, contract.Status);
        public void OnExpiry(int contractId) =>
            _logger.LogWarning("[AUDIT] {Time} | Contract #{Id} | EXPIRED",
                DateTime.UtcNow, contractId);
    }
}
