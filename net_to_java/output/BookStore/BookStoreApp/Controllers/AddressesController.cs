using System.Web.Http;

namespace BookStoreApp.Controllers
{
    [RoutePrefix("api/addresses")]
    public class AddressesController : ApiController
    {
        // GET: api/addresses
        public IHttpActionResult Get()
        {
            // Implement logic to retrieve addresses from the database
            return Ok(addresses);
        }

        // GET: api/addresses/5
        public IHttpActionResult Get(int id)
        {