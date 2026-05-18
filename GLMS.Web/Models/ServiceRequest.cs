using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace GLMS.Web.Models
{
    public enum ServiceRequestStatus { Pending, InProgress, Completed, Cancelled }
    public class ServiceRequest
    {
        public int Id { get; set; }
        [Required] public int ContractId { get; set; }
        [Required(ErrorMessage = "Description is required")]
        [StringLength(500)] public string Description { get; set; } = string.Empty;
        [Required][Column(TypeName = "decimal(18,2)")]
        [Range(0.01, double.MaxValue, ErrorMessage = "Cost must be greater than zero")]
        public decimal CostUSD { get; set; }
        [Column(TypeName = "decimal(18,2)")] public decimal CostZAR { get; set; }
        public ServiceRequestStatus Status { get; set; } = ServiceRequestStatus.Pending;
        public DateTime CreatedAt { get; set; } = DateTime.Now;
        public Contract? Contract { get; set; }
    }
}
