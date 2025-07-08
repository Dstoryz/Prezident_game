export interface EconomicIndicators {
  gdp_absolute: number;
  gdp_growth: number;
  inflation: number;
  unemployment: number;
  president_rating: number;
  money_supply: number;
  gold_reserves: number;
  // Новые поля для расширенной модели
  industry_output?: number;
  services_output?: number;
  exchange_rate?: number;
  external_debt?: number;
  population?: number;
  interest_rate?: number;
}

export interface BudgetData {
  total_revenue: number;
  total_spending: number;
  budget_balance: number;
  accumulated_reserves: number;
  // Новые поля для расширенной модели
  social_transfers?: number;
  external_debt?: number;
}

export interface GameSession {
  id: number;
  user: number;
  turn: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  model_type: string;
  indicators: EconomicIndicators;
  budget: BudgetData;
  // Новые поля для расширенной модели
  crisis?: CrisisInfo;
}

export interface CrisisInfo {
  type: string;
  description: string;
  effects: Record<string, any>;
  severity: 'low' | 'medium' | 'high' | 'critical';
  duration: number;
}

export interface GameParameters {
  interest_rate: number;
  tax_rate: number;
  government_spending: number;
  customs_duty: number;
  education_priority: number;
  healthcare_priority: number;
  defense_priority: number;
  infrastructure_priority: number;
  social_priority: number;
  social_transfers: number;
  reserve_ratio: number;
  refinance_rate: number;
  printing_press_active: boolean;
}

export interface GameHistoryEntry {
  turn: number;
  indicators: EconomicIndicators;
  budget: BudgetData;
  parameters: GameParameters;
  crisis?: CrisisInfo;
  timestamp: string;
}

export interface GameChartProps {
  gameId: number;
  history?: GameHistoryEntry[];
  modelType?: 'basic' | 'enhanced';
}

export interface GameTipsProps {
  modelType?: 'basic' | 'enhanced';
}

export interface EnhancedGameState {
  game: GameSession;
  history: GameHistoryEntry[];
  available_actions: string[];
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