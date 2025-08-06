// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using eShop.HybridApp;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Maui.Controls.Handlers.Compatibility;
using Microsoft.Maui.Handlers;
using Moq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xunit;

namespace eShop.HybridApp.Tests
{
    public class MauiProgramTests
    {
        [Fact]
        public void CreateMauiApp_HappyPath_ReturnsNotNull()
        {
            // Arrange
            var builder = MauiApp.CreateBuilder();
            builder.Services.AddHttpClient<CatalogService>(o => o.BaseAddress = new Uri("http://localhost:11632/"));
            builder.Services.AddSingleton<WebAppComponents.Services.IProductImageUrlProvider, ProductImageUrlProvider>();

            // Act
            var app = builder.Build();

            // Assert
            Assert.NotNull(app);
        }

        [Fact]
        public void CreateMauiApp_EdgeCase_ReturnsNotNull()
        {
            // Arrange
            var builder = MauiApp.CreateBuilder();
            builder.Services.AddHttpClient<CatalogService>(o => o.BaseAddress = new Uri("http://localhost:11632/"));
            builder.Services.AddSingleton<WebAppComponents.Services.IProductImageUrlProvider, ProductImageUrlProvider>();

            // Act
            var app = builder.Build();

            // Assert
            Assert.NotNull(app);
        }

        [Fact]
        public void CreateMauiApp_ErrorCondition_ThrowsException()
        {
            // Arrange
            var builder = MauiApp.CreateBuilder();
            builder.Services.AddHttpClient<CatalogService>(o => o.BaseAddress = new Uri("http://localhost:11632/"));
            builder.Services.AddSingleton<WebAppComponents.Services.IProductImageUrlProvider, ProductImageUrlProvider>();

            // Act
            var app = builder.Build();

            // Assert
            Assert.Throws<Exception>(() => app.Services.GetRequiredService<CatalogService>());
        }
    }
}