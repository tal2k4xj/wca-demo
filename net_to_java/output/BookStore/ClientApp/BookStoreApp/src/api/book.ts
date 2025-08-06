// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
import axios from 'axios';

const API_URL = 'https://example.com/api/books';

export const getBookDetails = async (bookId: string) => {
  const response = await axios.get(`${API_URL}/${bookId}`);
  return response.data;
};