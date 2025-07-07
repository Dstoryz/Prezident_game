export interface GameParameters {
  interest_rate: number;
  tax_rate: number;
  government_spending: number;
  customs_duty: number;
  social_transfers: number;
}

export interface EconomicIndicators {
  gdp_growth: number;
  inflation: number;
  unemployment: number;
  investments: number;
  president_rating: number;
  public_mood: number;
  export_volume: number;
  import_volume: number;
  // Новые поля:
  money_supply: number;
  gold_reserves: number;
  reserve_ratio: number;
  refinance_rate: number;
  printing_press_active: boolean;
  population: number;
}

export interface GameEvent {
  event_type: string;
  title: string;
  description: string;
  gdp_impact: number;
  inflation_impact: number;
  unemployment_impact: number;
  rating_impact: number;
}

export interface BudgetData {
  tax_revenue: number;
  customs_revenue: number;
  total_revenue: number;
  education_spending: number;
  healthcare_spending: number;
  defense_spending: number;
  infrastructure_spending: number;
  social_spending: number;
  total_spending: number;
  budget_balance: number;
  accumulated_reserves: number;
  // Новое поле:
  social_transfers: number;
}

export interface GameSession {
  id: number;
  current_turn: number;
  current_year: number;
  current_quarter: number;
  elections_passed: number;
  is_active: boolean;
  parameters: GameParameters;
  current_indicators: EconomicIndicators | null;
  current_events: GameEvent[];
  current_budget?: BudgetData | null;
}

export interface GameState {
  game: GameSession | null;
  loading: boolean;
  error: string | null;
}

export interface NextTurnRequest {
  interest_rate?: number;
  tax_rate?: number;
  government_spending?: number;
  customs_duty?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  game?: T;
  new_indicators?: EconomicIndicators;
  events?: GameEvent[];
  game_over?: boolean;
  game_over_reason?: string;
} 