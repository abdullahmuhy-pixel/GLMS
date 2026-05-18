using Microsoft.AspNetCore.Mvc;
namespace GLMS.Web.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index() => View();
    }
}
