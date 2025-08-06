// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System;

namespace BookStoreApp.Models
{
    public class Review
    {
        public Guid Id { get; set; }
        public Guid BookId { get; set; }
        public Guid CustomerId { get; set; }
        public int Rating { get; set; }
        public string Comment { get; set; }
        public DateTime ReviewDate { get; set; }
    }
}