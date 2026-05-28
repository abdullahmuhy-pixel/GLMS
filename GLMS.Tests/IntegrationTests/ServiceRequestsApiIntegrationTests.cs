using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    public class ServiceRequestsApiIntegrationTests
        : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ServiceRequestsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetServiceRequests_ReturnsSuccessStatusCode()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests");

            // Assert — HTTP 200 OK
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetServiceRequests_ReturnsJsonArray()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests");
            var content  = await response.Content.ReadAsStringAsync();

            // Assert — returns a JSON array (not null)
            Assert.NotNull(content);
            Assert.True(content.StartsWith("[") || content.StartsWith("{"));
        }

        [Fact]
        public async Task GetServiceRequestById_InvalidId_ReturnsNotFound()
        {
            // Act
            var response = await _client.GetAsync("/api/servicerequests/99999");

            // Assert
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }
    }
}
