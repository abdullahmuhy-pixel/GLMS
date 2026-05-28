using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using System.Text;
using System.Text.Json;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    // Integration Tests: call the actual running API endpoints
    // These verify that HTTP status codes and JSON responses are correct
    public class ContractsApiIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ContractsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetContracts_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");

            // Assert — HTTP 200 OK
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetContracts_ReturnsJsonContentType()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");

            // Assert — response is JSON
            Assert.Equal("application/json",
                response.Content.Headers.ContentType?.MediaType);
        }

        [Fact]
        public async Task GetContracts_ReturnsNotNull()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts");
            var content  = await response.Content.ReadAsStringAsync();

            // Assert — body is not null or empty
            Assert.NotNull(content);
            Assert.NotEmpty(content);
        }

        [Fact]
        public async Task GetContractById_InvalidId_ReturnsNotFound()
        {
            // Act — request a contract that does not exist
            var response = await _client.GetAsync("/api/contracts/99999");

            // Assert — HTTP 404 Not Found
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }

        [Fact]
        public async Task GetActiveContracts_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/contracts/active");

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }
    }
}
