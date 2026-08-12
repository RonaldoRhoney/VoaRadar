export interface BudgetDestination {
  city: string;
  uf: string;
  price: number;
}

export interface BudgetSearchParams {
  budget: number;
  originCity: string;
  month: string;
  flexible: boolean;
}
