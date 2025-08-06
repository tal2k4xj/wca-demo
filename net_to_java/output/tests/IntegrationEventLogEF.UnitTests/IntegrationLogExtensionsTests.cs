// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using eShop.IntegrationEventLogEF;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xunit;

namespace eShop.IntegrationEventLogEF.Tests
{
    public class IntegrationLogExtensionsTests
    {
        [Fact]
        public void UseIntegrationEventLogs_HappyPath_Success()
        {
            // Arrange
            var options = new DbContextOptionsBuilder<IntegrationEventLogContext>()
                .UseInMemoryDatabase(databaseName: "UseIntegrationEventLogs_HappyPath_Success")
                .Options;

            // Act
            var builder = new ModelBuilder();
            builder.UseIntegrationEventLogs();
            var model = builder.Model;

            // Assert
            Assert.NotNull(model);
            Assert.Single(model.GetEntityTypes());
            Assert.Equal("IntegrationEventLog", model.GetEntityTypes().Single().GetTableName());
            Assert.Single(model.GetEntityTypes().Single().GetKeys());
            Assert.Equal("EventId", model.GetEntityTypes().Single().GetKeys().Single().GetName());
        }

        [Fact]
        public void UseIntegrationEventLogs_EdgeCases_Success()
        {
            // Arrange
            var options = new DbContextOptionsBuilder<IntegrationEventLogContext>()
                .UseInMemoryDatabase(databaseName: "UseIntegrationEventLogs_EdgeCases_Success")
                .Options;

            // Act
            var builder = new ModelBuilder();
            builder.UseIntegrationEventLogs();
            var model = builder.Model;

            // Assert
            Assert.NotNull(model);
            Assert.Single(model.GetEntityTypes());
            Assert.Equal("IntegrationEventLog", model.GetEntityTypes().Single().GetTableName());
            Assert.Single(model.GetEntityTypes().Single().GetKeys());
            Assert.Equal("EventId", model.GetEntityTypes().Single().GetKeys().Single().GetName());
        }

        [Fact]
        public void UseIntegrationEventLogs_ErrorConditions_Success()
        {
            // Arrange
            var options = new DbContextOptionsBuilder<IntegrationEventLogContext>()
                .UseInMemoryDatabase(databaseName: "UseIntegrationEventLogs_ErrorConditions_Success")
                .Options;

            // Act
            var builder = new ModelBuilder();
            builder.UseIntegrationEventLogs();
            var model = builder.Model;

            // Assert
            Assert.NotNull(model);
            Assert.Single(model.GetEntityTypes());
            Assert.Equal("IntegrationEventLog", model.GetEntityTypes().Single().GetTableName());
            Assert.Single(model.GetEntityTypes().Single().GetKeys());
            Assert.Equal("EventId", model.GetEntityTypes().Single().GetKeys().Single().GetName());
        }
    }
}