// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
export interface Order {
  id: string;
  customerId: string;
  orderDate: Date;
  status: OrderStatus;
  totalAmount: number;
  shippingAddress: Address;
  paymentStatus: PaymentStatus;
  orderItems: OrderItem[];
}

export enum OrderStatus {
  Created = 'Created',
  Processing = 'Processing',
  Shipped = 'Shipped',
  Delivered = 'Delivered',
  Cancelled = 'Cancelled',
}

export enum PaymentStatus {
  Pending = 'Pending',
  Failed = 'Failed',
  Succeeded = 'Succeeded',
}

export interface OrderItem {
  bookId: string;
  quantity: number;
}