// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
export interface Sort {
  field: string;
  order: SortOrder;
}

export enum SortOrder {
  Ascending = 'Ascending',
  Descending = 'Descending',
}