using Microsoft.AspNetCore.Mvc.Testing;
using System.Net;
using Xunit;
namespace GLMS.Tests.IntegrationTests
{
    public class ClientsApiIntegrationTests
        : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public ClientsApiIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task GetClients_ReturnsSuccessStatusCode()
        {
            var response = await _client.GetAsync("/api/clients");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GetClients_ReturnsNotNull()
        {
            var response = await _client.GetAsync("/api/clients");
            var content  = await response.Content.ReadAsStringAsync();
            Assert.NotNull(content);
            Assert.NotEmpty(content);
        }

        [Fact]
        public async Task GetClientById_InvalidId_ReturnsNotFound()
        {
            var response = await _client.GetAsync("/api/clients/99999");
            Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        }
    }
}
