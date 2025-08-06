// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
export interface Customer {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  address: Address;
  phoneNumber: string;
  registrationDate: Date;
  isActive: boolean;
}

export interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
}