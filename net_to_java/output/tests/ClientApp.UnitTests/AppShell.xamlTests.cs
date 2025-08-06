// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using eShop.ClientApp.Services;
using eShop.ClientApp.Views;
using Moq;
using Xunit;

namespace eShop.ClientApp.Tests
{
    public class AppShellTests
    {
        private readonly Mock<INavigationService> _navigationServiceMock = new();
        private readonly AppShell _appShell;

        public AppShellTests()
        {
            _appShell = new AppShell(_navigationServiceMock.Object);
        }

        [Fact]
        public void OnHandlerChanged_WhenHandlerIsNotNull_ShouldInitializeNavigationService()
        {
            // Arrange
            var handlerMock = new Mock<IHandler>();
            _appShell.Handler = handlerMock.Object;

            // Act
            _appShell.OnHandlerChanged();

            // Assert
            _navigationServiceMock.Verify(ns => ns.InitializeAsync(), Times.Once);
        }

        [Fact]
        public void OnHandlerChanged_WhenHandlerIsNull_ShouldNotInitializeNavigationService()
        {
            // Arrange
            _appShell.Handler = null;

            // Act
            _appShell.OnHandlerChanged();

            // Assert
            _navigationServiceMock.Verify(ns => ns.InitializeAsync(), Times.Never);
        }

        [Fact]
        public void InitializeRouting_ShouldRegisterAllRoutes()
        {
            // Act
            AppShell.InitializeRouting();

            // Assert
            Assert.Equal(typeof(LoginView), Routing.GetRoute("Login").TargetType);
            Assert.Equal(typeof(FiltersView), Routing.GetRoute("Filter").TargetType);
            Assert.Equal(typeof(CatalogItemView), Routing.GetRoute("ViewCatalogItem").TargetType);
            Assert.Equal(typeof(BasketView), Routing.GetRoute("Basket").TargetType);
            Assert.Equal(typeof(SettingsView), Routing.GetRoute("Settings").TargetType);
            Assert.Equal(typeof(OrderDetailView), Routing.GetRoute("OrderDetail").TargetType);
            Assert.Equal(typeof(CheckoutView), Routing.GetRoute("Checkout").TargetType);
        }
    }
}