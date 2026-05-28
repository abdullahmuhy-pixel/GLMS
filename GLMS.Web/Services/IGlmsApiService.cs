namespace GLMS.Web.Services
{
    // Interface for all HttpClient calls to the GLMS Web API
    // This replaces direct database access in the MVC controllers
    public interface IGlmsApiService
    {
        Task<string> GetAsync(string endpoint);
        Task<string> PostAsync(string endpoint, object data);
        Task<string> PatchAsync(string endpoint, object data);
    }
}
