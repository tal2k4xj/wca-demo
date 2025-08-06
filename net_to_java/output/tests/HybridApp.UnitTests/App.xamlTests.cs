// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using Xunit;

namespace eShop.HybridApp.Tests
{
    public class AppTests
    {
        [Fact]
        public void CreateWindow_HappyPath_ReturnsWindow()
        {
            // Arrange
            var app = new App();

            // Act
            var window = app.CreateWindow(null);

            // Assert
            Assert.NotNull(window);
        }

        [Fact]
        public void CreateWindow_NullActivationState_ReturnsWindow()
        {
            // Arrange
            var app = new App();

            // Act
            var window = app.CreateWindow(null);

            // Assert
            Assert.NotNull(window);
        }

        [Fact]
        public void CreateWindow_ActivationState_ReturnsWindow()
        {
            // Arrange
            var app = new App();
            var activationState = new ActivationState();

            // Act
            var window = app.CreateWindow(activationState);

            // Assert
            Assert.NotNull(window);
        }
    }
}