// Assisted by watsonx Code Assistant 
// watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.
export interface Filter {
  field: string;
  operator: FilterOperator;
  value: any;
}

export enum FilterOperator {
  Equal = 'Equal',
  GreaterThan = 'GreaterThan',
  LessThan = 'LessThan',
  Contains = 'Contains',
}