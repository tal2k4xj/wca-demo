// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using BookStoreApp.Models;

namespace BookStoreApp.Services
{
    public class AddressService
    {
        private readonly BookStoreContext _context;

        public AddressService(BookStoreContext context)
        {
            _context = context;
        }

        public List<Address> GetAddresses()
        {
            return _context.Addresses.ToList();
        }

        public Address GetAddressById(int id)
        {
            return _context.Addresses.FirstOrDefault(a => a.Id == id);
        }

        public void AddAddress(Address address)
        {
            _context.Addresses.Add(address);
            _context.SaveChanges();
        }

        public void UpdateAddress(Address address)
        {
            _context.Addresses.Update(address);
            _context.SaveChanges();
        }

        public void DeleteAddress(int id)
        {
            var address = _context.Addresses.Find(id);
            if (address != null)
            {
                _context.Addresses.Remove(address);
                _context.SaveChanges();
            }
        }
    }
}