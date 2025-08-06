// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System;

namespace BookStoreApp.Models
{
    public class Book
    {
        public Guid Id { get; set; }
        public string ISBN { get; set; }
        public string Title { get; set; }
        public string Author { get; set; }
        public string Description { get; set; }
        public decimal Price { get; set; }
        public DateTime PublishDate { get; set; }
        public string Category { get; set; }
        public string Publisher { get; set; }
        public int StockQuantity { get; set; }
        public decimal AverageRating { get; set; }
    }
}