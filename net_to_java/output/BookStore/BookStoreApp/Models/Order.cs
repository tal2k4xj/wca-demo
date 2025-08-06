// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System;
using System.Collections.Generic;

namespace BookStoreApp.Models
{
    public class Order
    {
        public Guid Id { get; set; }
        public Guid CustomerId { get; set; }
        public DateTime OrderDate { get; set; }
        public OrderStatus Status { get; set; }
        public decimal TotalAmount { get; set; }
        public Address ShippingAddress { get; set; }
        public PaymentStatus PaymentStatus { get; set; }
        public List<OrderItem> OrderItems { get; set; }
    }
}