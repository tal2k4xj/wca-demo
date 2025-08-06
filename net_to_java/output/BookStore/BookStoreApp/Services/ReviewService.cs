// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
using BookStoreApp.Models;

namespace BookStoreApp.Services
{
    public class ReviewService
    {
        private readonly BookStoreContext _context;

        public ReviewService(BookStoreContext context)
        {
            _context = context;
        }

        public List<Review> GetReviews()
        {
            return _context.Reviews.ToList();
        }

        public Review GetReviewById(int id)
        {
            return _context.Reviews.FirstOrDefault(r => r.Id == id);
        }

        public void AddReview(Review review)
        {
            _context.Reviews.Add(review);
            _context.SaveChanges();
        }

        public void UpdateReview(Review review)
        {
            _context.Reviews.Update(review);
            _context.SaveChanges();
        }

        public void DeleteReview(int id)
        {
            var review = _context.Reviews.Find(id);
            if (review != null)
            {
                _context.Reviews.Remove(review);
                _context.SaveChanges();
            }
        }
    }
}