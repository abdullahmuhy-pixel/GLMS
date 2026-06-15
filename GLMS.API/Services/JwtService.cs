using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;

namespace GLMS.API.Services
{
    public class JwtService : IJwtService
    {
        private readonly IConfiguration _config;

        // Demo users — in production these would come from a database
        private readonly Dictionary<string, (string Password, string Role)> _users = new()
        {
            { "admin",   ("Admin@123", "Admin") },
            { "manager", ("Manager@123", "Manager") },
        };

        public JwtService(IConfiguration config)
        {
            _config = config;
        }

        public bool ValidateCredentials(string username, string password)
        {
            return _users.TryGetValue(username.ToLower(), out var user)
                && user.Password == password;
        }

        public string GenerateToken(string username, string role)
        {
            var key     = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
            var creds   = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var expiry  = DateTime.UtcNow.AddHours(8);

            var claims = new[]
            {
                new Claim(ClaimTypes.Name,  username),
                new Claim(ClaimTypes.Role,  role),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            };

            var token = new JwtSecurityToken(
                issuer:   _config["Jwt:Issuer"],
                audience: _config["Jwt:Audience"],
                claims:   claims,
                expires:  expiry,
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
