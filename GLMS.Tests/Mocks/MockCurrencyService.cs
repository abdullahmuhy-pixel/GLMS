using GLMS.Web.Services;
namespace GLMS.Tests.Mocks
{
    public class MockCurrencyService : ICurrencyService
    {
        private readonly decimal _fixedRate;
        public MockCurrencyService(decimal fixedRate = 18.50m) { _fixedRate = fixedRate; }
        public Task<decimal> ConvertUsdToZarAsync(decimal amountUsd)
            => Task.FromResult(Math.Round(amountUsd * _fixedRate, 2));
    }
}
