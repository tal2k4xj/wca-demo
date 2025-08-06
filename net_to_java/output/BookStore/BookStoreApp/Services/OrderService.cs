// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using BookStoreApp.Models;

namespace BookStoreApp.Services
{
    public class OrderService
    {
        private readonly BookStoreContext _context;

        public OrderService(BookStoreContext context)
        {
            _context = context;
        }

        public List<Order> GetOrders()
        {
            return _context.Orders.ToList();
        }

        public Order GetOrderByCustomerId(int customerId)
        {
            return _context.Orders.FirstOrDefault(o => o.CustomerId == customerId);
        }

        public void AddOrder(Order order)
        {
            _context.Orders.Add(order);
            _context.SaveChanges();
        }

        public void UpdateOrder(Order order)
        {
            _context.Orders.Update(order);
            _context.SaveChanges();
        }

        public void DeleteOrder(int id)
        {
            var order = _context.Orders.Find(id);
            if (order != null)
            {
                _context.Orders.Remove(order);
                _context.SaveChanges();
            }
        }
    }
}