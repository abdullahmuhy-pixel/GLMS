using Microsoft.EntityFrameworkCore;
using GLMS.Web.Data;
using GLMS.Web.Models;
namespace GLMS.API.Repositories
{
    public class ClientRepository : IClientRepository
    {
        private readonly ApplicationDbContext _context;
        public ClientRepository(ApplicationDbContext context) { _context = context; }

        public async Task<IEnumerable<Client>> GetAllAsync()
            => await _context.Clients.AsNoTracking().ToListAsync();

        public async Task<Client?> GetByIdAsync(int id)
            => await _context.Clients.AsNoTracking().FirstOrDefaultAsync(c => c.Id == id);

        public async Task<Client> CreateAsync(Client client)
        {
            _context.Clients.Add(client);
            await _context.SaveChangesAsync();
            return client;
        }
    }
}
