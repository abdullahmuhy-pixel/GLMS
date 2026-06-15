using Microsoft.AspNetCore.Mvc;
using GLMS.API.Models;
using GLMS.API.Services;

namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/auth")]
    public class AuthController : ControllerBase
    {
        private readonly IJwtService _jwtService;

        public AuthController(IJwtService jwtService)
        {
            _jwtService = jwtService;
        }

        // POST /api/auth/login
        // Returns a JWT token if credentials are valid
        [HttpPost("login")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public IActionResult Login([FromBody] LoginRequest request)
        {
            if (!_jwtService.ValidateCredentials(request.Username, request.Password))
                return Unauthorized(new { message = "Invalid username or password." });

            var role  = request.Username.ToLower() == "admin" ? "Admin" : "Manager";
            var token = _jwtService.GenerateToken(request.Username, role);

            return Ok(new LoginResponse
            {
                Token    = token,
                Username = request.Username,
                Expiry   = DateTime.UtcNow.AddHours(8)
            });
        }

        // GET /api/auth/test
        // Verifies that a token is valid (for testing)
        [HttpGet("test")]
        [Microsoft.AspNetCore.Authorization.Authorize]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status401Unauthorized)]
        public IActionResult TestAuth()
        {
            var username = User.Identity?.Name;
            return Ok(new { message = $"Authenticated as {username}", success = true });
        }
    }
}
