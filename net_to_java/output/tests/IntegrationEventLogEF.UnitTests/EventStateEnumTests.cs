// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System;
using Xunit;

namespace eShop.IntegrationEventLogEF.Tests
{
    public class EventStateEnumTests
    {
        [Fact]
        public void NotPublished_HasExpectedValue()
        {
            // Arrange
            EventStateEnum eventState = EventStateEnum.NotPublished;

            // Act

            // Assert
            Assert.Equal(0, (int)eventState);
        }

        [Fact]
        public void InProgress_HasExpectedValue()
        {
            // Arrange
            EventStateEnum eventState = EventStateEnum.InProgress;

            // Act

            // Assert
            Assert.Equal(1, (int)eventState);
        }

        [Fact]
        public void Published_HasExpectedValue()
        {
            // Arrange
            EventStateEnum eventState = EventStateEnum.Published;

            // Act

            // Assert
            Assert.Equal(2, (int)eventState);
        }

        [Fact]
        public void PublishedFailed_HasExpectedValue()
        {
            // Arrange
            EventStateEnum eventState = EventStateEnum.PublishedFailed;

            // Act

            // Assert
            Assert.Equal(3, (int)eventState);
        }
    }
}