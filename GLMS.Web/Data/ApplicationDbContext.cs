using Microsoft.EntityFrameworkCore;
using GLMS.Web.Models;
namespace GLMS.Web.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options) { }
        public DbSet<Client> Clients { get; set; }
        public DbSet<Contract> Contracts { get; set; }
        public DbSet<ServiceRequest> ServiceRequests { get; set; }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Contract>()
                .HasOne(c => c.Client).WithMany(cl => cl.Contracts)
                .HasForeignKey(c => c.ClientId).OnDelete(DeleteBehavior.Restrict);
            modelBuilder.Entity<ServiceRequest>()
                .HasOne(sr => sr.Contract).WithMany(c => c.ServiceRequests)
                .HasForeignKey(sr => sr.ContractId).OnDelete(DeleteBehavior.Restrict);
            modelBuilder.Entity<Client>().HasData(
                new Client { Id = 1, Name = "Acme Logistics", ContactDetails = "acme@logistics.com", Region = "Johannesburg" },
                new Client { Id = 2, Name = "FastFreight Ltd", ContactDetails = "info@fastfreight.co.za", Region = "Cape Town" }
            );
        }
    }
}
