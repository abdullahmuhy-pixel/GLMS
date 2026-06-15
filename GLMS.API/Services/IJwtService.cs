namespace GLMS.API.Services
{
    public interface IJwtService
    {
        string GenerateToken(string username, string role);
        bool ValidateCredentials(string username, string password);
    }
}
