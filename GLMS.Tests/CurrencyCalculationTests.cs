using GLMS.Tests.Mocks;
using Xunit;
namespace GLMS.Tests
{
    public class CurrencyCalculationTests
    {
        [Fact]
        public async Task ConvertUsdToZar_StandardAmount_ReturnsCorrectResult()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(1850.00m, await s.ConvertUsdToZarAsync(100m)); }

        [Fact]
        public async Task ConvertUsdToZar_OneDollar_ReturnsExactRate()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(18.50m, await s.ConvertUsdToZarAsync(1m)); }

        [Fact]
        public async Task ConvertUsdToZar_ZeroAmount_ReturnsZero()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(0.00m, await s.ConvertUsdToZarAsync(0m)); }

        [Fact]
        public async Task ConvertUsdToZar_NegativeAmount_ReturnsNegativeZar()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(-925.00m, await s.ConvertUsdToZarAsync(-50m)); }

        [Fact]
        public async Task ConvertUsdToZar_LargeAmount_CalculatesCorrectly()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(925000.00m, await s.ConvertUsdToZarAsync(50000m)); }

        [Fact]
        public async Task ConvertUsdToZar_DecimalAmount_RoundsToTwoPlaces()
        { var s = new MockCurrencyService(18.50m); Assert.Equal(22.83m, await s.ConvertUsdToZarAsync(1.234m)); }

        [Fact]
        public async Task ConvertUsdToZar_DifferentRates_ProduceDifferentResults()
        {
            var s1 = new MockCurrencyService(18.00m);
            var s2 = new MockCurrencyService(20.00m);
            Assert.Equal(1800.00m, await s1.ConvertUsdToZarAsync(100m));
            Assert.Equal(2000.00m, await s2.ConvertUsdToZarAsync(100m));
        }

        [Fact]
        public async Task ConvertUsdToZar_ZeroRate_ReturnsZero()
        { var s = new MockCurrencyService(0m); Assert.Equal(0.00m, await s.ConvertUsdToZarAsync(100m)); }
    }
}
