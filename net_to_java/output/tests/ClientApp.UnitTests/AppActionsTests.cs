// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using Xunit;

namespace eShop.ClientApp.Tests
{
    public class AppActionsTests
    {
        [Fact]
        public void ViewProfileAction_HasExpectedName()
        {
            // Arrange
            var action = AppActions.ViewProfileAction;

            // Act
            var name = action.Name;

            // Assert
            Assert.Equal("View Profile", name);
        }

        [Fact]
        public void ViewProfileAction_HasExpectedDescription()
        {
            // Arrange
            var action = AppActions.ViewProfileAction;

            // Act
            var description = action.Description;

            // Assert
            Assert.Equal("View your user profile", description);
        }

        [Fact]
        public void ViewProfileAction_HasExpectedId()
        {
            // Arrange
            var action = AppActions.ViewProfileAction;

            // Act
            var id = action.Id;

            // Assert
            Assert.Equal("view_profile", id);
        }
    }
}