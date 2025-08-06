// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
import axios from 'axios';

export const getBookDetails = async (id: string) => {
  const response = await axios.get(`/api/books/${id}`);
  return response.data;
};