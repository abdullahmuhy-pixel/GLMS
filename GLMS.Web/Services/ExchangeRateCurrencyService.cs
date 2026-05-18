using System.Text.Json;
namespace GLMS.Web.Services
{
    public class ExchangeRateCurrencyService : ICurrencyService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<ExchangeRateCurrencyService> _logger;
        public ExchangeRateCurrencyService(HttpClient httpClient,
            ILogger<ExchangeRateCurrencyService> logger)
        { _httpClient = httpClient; _logger = logger; }

        public async Task<decimal> ConvertUsdToZarAsync(decimal amountUsd)
        {
            try
            {
                var response = await _httpClient.GetAsync("https://open.er-api.com/v6/latest/USD");
                response.EnsureSuccessStatusCode();
                var json = await response.Content.ReadAsStringAsync();
                var doc  = JsonDocument.Parse(json);
                var rate = doc.RootElement.GetProperty("rates").GetProperty("ZAR").GetDecimal();
                return Math.Round(amountUsd * rate, 2);
            }
            catch (Exception ex)
            {
                _logger.LogWarning("API unavailable: {msg}. Using fallback rate.", ex.Message);
                return Math.Round(amountUsd * 18.50m, 2);
            }
        }
    }
}
