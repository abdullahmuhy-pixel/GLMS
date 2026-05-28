using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;
namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/servicerequests")]
    public class ServiceRequestsApiController : ControllerBase
    {
        private readonly IServiceRequestRepository _repo;
        private readonly IContractRepository _contractRepo;

        public ServiceRequestsApiController(
            IServiceRequestRepository repo,
            IContractRepository contractRepo)
        {
            _repo = repo;
            _contractRepo = contractRepo;
        }

        // GET /api/servicerequests
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll()
        {
            var requests = await _repo.GetAllAsync();
            return Ok(requests);
        }

        // GET /api/servicerequests/5
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var sr = await _repo.GetByIdAsync(id);
            if (sr == null) return NotFound(new { message = $"ServiceRequest {id} not found." });
            return Ok(sr);
        }

        // POST /api/servicerequests — with workflow validation
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Create([FromBody] ServiceRequest sr)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);

            // Workflow rule: block Expired or OnHold contracts
            var contract = await _contractRepo.GetByIdAsync(sr.ContractId);
            if (contract == null)
                return BadRequest(new { message = "Contract not found." });
            if (contract.Status == ContractStatus.Expired)
                return BadRequest(new { message = "Cannot create a request for an Expired contract." });
            if (contract.Status == ContractStatus.OnHold)
                return BadRequest(new { message = "Cannot create a request for an On Hold contract." });

            sr.CreatedAt = DateTime.Now;
            var created = await _repo.CreateAsync(sr);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
    }
}
