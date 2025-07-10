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
  // Дополнительные поля из базовой модели
  investments?: number;
  public_mood?: number;
  export_volume?: number;
  import_volume?: number;
  reserve_ratio?: number;
  refinance_rate?: number;
  printing_press_active?: boolean;
}

export interface BudgetData {
  total_revenue: number;
  total_spending: number;
  budget_balance: number;
  accumulated_reserves: number;
  // Новые поля для расширенной модели
  social_transfers?: number;
  external_debt?: number;
  // Дополнительные поля из базовой модели
  tax_revenue?: number;
  customs_revenue?: number;
  education_spending?: number;
  healthcare_spending?: number;
  defense_spending?: number;
  infrastructure_spending?: number;
  social_spending?: number;
}

export interface GameSession {
  id: number;
  user: number;
  current_turn: number;
  current_year: number;
  current_quarter: number;
  elections_passed: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  model_type: string;
  budget: number;
  accumulated_reserves: number;
  // Вложенные объекты
  parameters?: GameParameters;
  current_indicators?: EconomicIndicators;
  current_budget?: BudgetData;
  current_events?: GameEvent[];
  // Новые поля для расширенной модели
  crisis?: CrisisInfo;
  // Альтернативные поля для совместимости
  turn?: number;
  indicators?: EconomicIndicators;
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
  currentEvent?: GameEvent;
  indicators?: EconomicIndicators;
  parameters?: GameParameters;
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
  education_priority?: number;
  healthcare_priority?: number;
  defense_priority?: number;
  infrastructure_priority?: number;
  social_priority?: number;
  social_transfers?: number;
  reserve_ratio?: number;
  refinance_rate?: number;
  printing_press_active?: boolean;
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