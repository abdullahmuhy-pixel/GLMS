using GLMS.Web.Models;
using GLMS.Web.Services;
using Xunit;
namespace GLMS.Tests
{
    public class WorkflowLogicTests
    {
        private bool CanCreate(ContractStatus s)
            => s != ContractStatus.Expired && s != ContractStatus.OnHold;

        [Fact] public void ActiveContract_CanCreate() => Assert.True(CanCreate(ContractStatus.Active));
        [Fact] public void DraftContract_CanCreate() => Assert.True(CanCreate(ContractStatus.Draft));
        [Fact] public void ExpiredContract_CannotCreate() => Assert.False(CanCreate(ContractStatus.Expired));
        [Fact] public void OnHoldContract_CannotCreate() => Assert.False(CanCreate(ContractStatus.OnHold));

        [Fact]
        public void AllStatuses_CorrectResults()
        {
            Assert.True(CanCreate(ContractStatus.Active));
            Assert.True(CanCreate(ContractStatus.Draft));
            Assert.False(CanCreate(ContractStatus.Expired));
            Assert.False(CanCreate(ContractStatus.OnHold));
        }

        [Fact]
        public void FreightFactory_ValidContract_Passes()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "Freight SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddYears(1) };
            Assert.True(f.ValidateContract(c));
        }

        [Fact] public void FreightFactory_NullContract_Fails()
        { Assert.False(new FreightContractFactory().ValidateContract(null!)); }

        [Fact]
        public void FreightFactory_EndBeforeStart_Fails()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddDays(-1) };
            Assert.False(f.ValidateContract(c));
        }

        [Fact]
        public void SLAFactory_ShortDuration_Fails()
        {
            var f = new SLAContractFactory();
            var c = new Contract { ClientId = 1, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddDays(30) };
            Assert.False(f.ValidateContract(c));
        }

        [Fact]
        public void FreightFactory_MissingClientId_Fails()
        {
            var f = new FreightContractFactory();
            var c = new Contract { ClientId = 0, ServiceLevel = "SLA",
                StartDate = DateTime.Today, EndDate = DateTime.Today.AddYears(1) };
            Assert.False(f.ValidateContract(c));
        }
    }
}
