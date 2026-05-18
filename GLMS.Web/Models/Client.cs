using System.ComponentModel.DataAnnotations;
namespace GLMS.Web.Models
{
    public class Client
    {
        public int Id { get; set; }
        [Required(ErrorMessage = "Name is required")]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;
        [Required(ErrorMessage = "Contact details are required")]
        [StringLength(200)]
        public string ContactDetails { get; set; } = string.Empty;
        [Required(ErrorMessage = "Region is required")]
        [StringLength(100)]
        public string Region { get; set; } = string.Empty;
        public ICollection<Contract> Contracts { get; set; } = new List<Contract>();
    }
}
