namespace GLMS.Web.Services
{
    // Strategy Pattern interface
    public interface ICurrencyService
    {
        Task<decimal> ConvertUsdToZarAsync(decimal amountUsd);
    }
}
