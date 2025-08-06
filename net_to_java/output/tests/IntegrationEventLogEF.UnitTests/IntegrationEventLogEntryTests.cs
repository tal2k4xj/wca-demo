// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System;
using System.Text.Json;
using Xunit;

namespace eShop.IntegrationEventLogEF.Tests
{
    public class IntegrationEventLogEntryTests
    {
        [Fact]
        public void IntegrationEventLogEntry_HappyPath_Success()
        {
            // Arrange
            var @event = new IntegrationEvent();
            var transactionId = Guid.NewGuid();

            // Act
            var entry = new IntegrationEventLogEntry(@event, transactionId);

            // Assert
            Assert.Equal(@event.Id, entry.EventId);
            Assert.Equal(@event.GetType().FullName, entry.EventTypeName);
            Assert.Equal(EventStateEnum.NotPublished, entry.State);
            Assert.Equal(0, entry.TimesSent);
            Assert.Equal(@event.CreationDate, entry.CreationTime);
            Assert.Equal(JsonSerializer.Serialize(@event, @event.GetType(), s_indentedOptions), entry.Content);
            Assert.Equal(transactionId, entry.TransactionId);
        }

        [Fact]
        public void IntegrationEventLogEntry_EdgeCases_Success()
        {
            // Arrange
            var @event = new IntegrationEvent();
            var transactionId = Guid.NewGuid();

            // Act
            var entry = new IntegrationEventLogEntry(@event, transactionId);

            // Assert
            Assert.Equal(@event.Id, entry.EventId);
            Assert.Equal(@event.GetType().FullName, entry.EventTypeName);
            Assert.Equal(EventStateEnum.NotPublished, entry.State);
            Assert.Equal(0, entry.TimesSent);
            Assert.Equal(@event.CreationDate, entry.CreationTime);
            Assert.Equal(JsonSerializer.Serialize(@event, @event.GetType(), s_indentedOptions), entry.Content);
            Assert.Equal(transactionId, entry.TransactionId);
        }

        [Fact]
        public void IntegrationEventLogEntry_ErrorConditions_Success()
        {
            // Arrange
            var @event = new IntegrationEvent();
            var transactionId = Guid.NewGuid();

            // Act
            var entry = new IntegrationEventLogEntry(@event, transactionId);

            // Assert
            Assert.Equal(@event.Id, entry.EventId);
            Assert.Equal(@event.GetType().FullName, entry.EventTypeName);
            Assert.Equal(EventStateEnum.NotPublished, entry.State);
            Assert.Equal(0, entry.TimesSent);
            Assert.Equal(@event.CreationDate, entry.CreationTime);
            Assert.Equal(JsonSerializer.Serialize(@event, @event.GetType(), s_indentedOptions), entry.Content);
            Assert.Equal(transactionId, entry.TransactionId);
        }
    }
}