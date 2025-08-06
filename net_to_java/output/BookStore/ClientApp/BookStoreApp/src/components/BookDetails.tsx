// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getBookDetails } from '../api/bookApi';
import { Book } from '../types/book';

const BookDetails = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState<Book | null>(null);

  useEffect(() => {
    const fetchBookDetails = async () => {
      try {
        const response = await getBookDetails(bookId);
        setBook(response.data);
      } catch (error) {
        console.error('Error fetching book details:', error);
      }
    };

    fetchBookDetails();
  }, [bookId]);

  return (
    <div>
      {book ? (
        <div>
          <h2>{book.title}</h2>
          <p>{book.description}</p>
          <p>Author: {book.author}</p>
          <p>Price: ${book.price}</p>
          <p>Category: {book.category}</p>
          <p>Publisher: {book.publisher}</p>
          <p>Stock Quantity: {book.stockQuantity}</p>
          <p>Average Rating: {book.averageRating}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default BookDetails;