using Microsoft.AspNetCore.Mvc;
using GLMS.Web.Models;
using GLMS.API.Repositories;
namespace GLMS.API.Controllers
{
    [ApiController]
    [Route("api/contracts")]
    public class ContractsApiController : ControllerBase
    {
        private readonly IContractRepository _repo;

        public ContractsApiController(IContractRepository repo)
        {
            _repo = repo;
        }

        // GET /api/contracts — with optional filtering
        [HttpGet]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll(
            [FromQuery] DateTime? startDate,
            [FromQuery] DateTime? endDate,
            [FromQuery] ContractStatus? status)
        {
            var contracts = await _repo.GetAllAsync(startDate, endDate, status);
            return Ok(contracts);
        }

        // GET /api/contracts/5
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> GetById(int id)
        {
            var contract = await _repo.GetByIdAsync(id);
            if (contract == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(contract);
        }

        // POST /api/contracts — create new contract
        [HttpPost]
        [ProducesResponseType(StatusCodes.Status201Created)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public async Task<IActionResult> Create([FromBody] Contract contract)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);
            var created = await _repo.CreateAsync(contract);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }

        // PATCH /api/contracts/5/status — approve or decline
        [HttpPatch("{id}/status")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] ContractStatus status)
        {
            var updated = await _repo.UpdateStatusAsync(id, status);
            if (updated == null) return NotFound(new { message = $"Contract {id} not found." });
            return Ok(updated);
        }

        // GET /api/contracts/active — only active contracts
        [HttpGet("active")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IActionResult> GetActive()
        {
            var contracts = await _repo.GetActiveContractsAsync();
            return Ok(contracts);
        }
    }
}
