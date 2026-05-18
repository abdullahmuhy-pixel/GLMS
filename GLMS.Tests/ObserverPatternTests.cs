using GLMS.Web.Models;
using GLMS.Web.Services;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;
namespace GLMS.Tests
{
    public class ObserverPatternTests
    {
        private class SpyObserver : IContractObserver
        {
            public bool StatusChangedCalled { get; private set; }
            public bool ExpiryCalled { get; private set; }
            public Contract? LastContract { get; private set; }
            public int LastExpiredId { get; private set; }
            public void OnStatusChanged(Contract c) { StatusChangedCalled = true; LastContract = c; }
            public void OnExpiry(int id) { ExpiryCalled = true; LastExpiredId = id; }
        }

        [Fact]
        public void NotifyStatusChanged_RegisteredObserver_IsNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.NotifyStatusChanged(new Contract { Id = 1, Status = ContractStatus.Expired });
            Assert.True(spy.StatusChangedCalled);
        }

        [Fact]
        public void NotifyExpiry_RegisteredObserver_IsNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.NotifyExpiry(42);
            Assert.True(spy.ExpiryCalled);
            Assert.Equal(42, spy.LastExpiredId);
        }

        [Fact]
        public void DetachedObserver_DoesNotReceiveNotification()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy = new SpyObserver();
            subject.Attach(spy);
            subject.Detach(spy);
            subject.NotifyStatusChanged(new Contract { Id = 5 });
            Assert.False(spy.StatusChangedCalled);
        }

        [Fact]
        public void MultipleObservers_AllNotified()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var spy1 = new SpyObserver(); var spy2 = new SpyObserver();
            subject.Attach(spy1); subject.Attach(spy2);
            subject.NotifyStatusChanged(new Contract { Id = 3 });
            Assert.True(spy1.StatusChangedCalled);
            Assert.True(spy2.StatusChangedCalled);
        }

        [Fact]
        public void NoObservers_NotifyDoesNotThrow()
        {
            var subject = new ContractSubject(NullLogger<ContractSubject>.Instance);
            var ex = Record.Exception(() => subject.NotifyStatusChanged(new Contract { Id = 99 }));
            Assert.Null(ex);
        }
    }
}
