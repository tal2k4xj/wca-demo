// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using System.Web.Http;

namespace BookStoreApp.Controllers
{
    [RoutePrefix("api/customers")]
    public class CustomersController : ApiController
    {
        // GET: api/customers
        public IHttpActionResult Get()
        {
            // Implement logic to retrieve customers from the database
            return Ok(customers);
        }

        // GET: api/customers/5
        public IHttpActionResult Get(int id)
        {
            // Implement logic to retrieve a specific customer by ID
            return Ok(customer);
        }

        // POST: api/customers
        public IHttpActionResult Post([FromBody] Customer customer)
        {
            // Implement logic to add a new customer to the database
            return CreatedAtRoute("GetCustomer", new { id = customer.Id }, customer);
        }

        // PUT: api/customers/5
        public IHttpActionResult Put(int id, [FromBody] Customer customer)
        {
            // Implement logic to update an existing customer in the database
            return Ok();
        }

        // DELETE: api/customers/5
        public IHttpActionResult Delete(int id)
        {
            // Implement logic to delete a customer from the database
            return Ok();
        }
    }
}