// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using BookStoreApp.Models;

namespace BookStoreApp.Services
{
    public class OrderItemService
    {
        private readonly BookStoreContext _context;

        public OrderItemService(BookStoreContext context)
        {
            _context = context;
        }

        public List<OrderItem> GetOrderItems()
        {
            return _context.OrderItems.ToList();
        }

        public OrderItem GetOrderItemById(int id)
        {
            return _context.OrderItems.FirstOrDefault(oi => oi.Id == id);
        }

        public void AddOrderItem(OrderItem orderItem)
        {
            _context.OrderItems.Add(orderItem);
            _context.SaveChanges();
        }

        public void UpdateOrderItem(OrderItem orderItem)
        {
            _context.OrderItems.Update(orderItem);
            _context.SaveChanges();
        }

        public void DeleteOrderItem(int id)
        {
            var orderItem = _context.OrderItems.Find(id);
            if (orderItem != null)
            {
                _context.OrderItems.Remove(orderItem);
                _context.SaveChanges();
            }
        }
    }
}