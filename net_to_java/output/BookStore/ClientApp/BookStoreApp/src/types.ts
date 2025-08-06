// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
export interface Book {
  id: string;
  isbn: string;
  title: string;
  author: string;
  description: string;
  price: number;
  publishDate: Date;
  category: string;
  publisher: string;
  stockQuantity: number;
  averageRating: number;
}