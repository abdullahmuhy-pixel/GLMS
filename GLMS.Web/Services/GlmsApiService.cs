using System.Text;
using System.Text.Json;
namespace GLMS.Web.Services
{
    // Concrete implementation — wraps HttpClient calls to the Web API
    public class GlmsApiService : IGlmsApiService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<GlmsApiService> _logger;

        public GlmsApiService(HttpClient httpClient, ILogger<GlmsApiService> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
        }

        public async Task<string> GetAsync(string endpoint)
        {
            try
            {
                var response = await _httpClient.GetAsync(endpoint);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError("API GET failed for {endpoint}: {msg}", endpoint, ex.Message);
                return "[]";
            }
        }

        public async Task<string> PostAsync(string endpoint, object data)
        {
            var json    = JsonSerializer.Serialize(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync(endpoint, content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> PatchAsync(string endpoint, object data)
        {
            var json    = JsonSerializer.Serialize(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await _httpClient.PatchAsync(endpoint, content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}
