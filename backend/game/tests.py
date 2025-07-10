from django.test import TestCase
from .services.enhanced_economic_model import EnhancedEconomicModel, EconomicParameters

# Create your tests here.

class EnhancedEconomicModelIntegrationTest(TestCase):
    def setUp(self):
        self.model = EnhancedEconomicModel()

    def test_new_economic_parameters(self):
        params = EconomicParameters(
            interest_rate=5.0,
            tax_rate=20.0,
            government_spending=25.0,
            customs_duty=5.0,
            education_priority=20.0,
            healthcare_priority=20.0,
            defense_priority=20.0,
            infrastructure_priority=20.0,
            social_priority=20.0,
            # Новые параметры:
            reserve_ratio=0.1,
            refinance_rate=0.05,
            printing_press_active=True,
            social_transfers=200.0,
        )
        indicators = self.model.calculate_indicators(params)
        # Проверяем, что новые параметры присутствуют и имеют ожидаемые типы
        self.assertIn('money_supply', indicators)
        self.assertIn('gold_reserves', indicators)
        self.assertIn('reserve_ratio', indicators)
        self.assertIn('refinance_rate', indicators)
        self.assertIn('printing_press_active', indicators)
        self.assertIn('budget_data', indicators)
        self.assertIn('demographic_data', indicators)
        self.assertIn('social_transfers', indicators['budget_data'])
        self.assertIn('social_transfers_per_capita', indicators['demographic_data'])
        # Проверяем, что денежная масса увеличилась из-за печатного станка
        self.assertGreater(indicators['money_supply'], 1000.0)
        # Проверяем, что соц. трансферты учтены в бюджете
        self.assertEqual(indicators['budget_data']['social_transfers'], 200.0)
        # Проверяем, что соц. трансферты на душу населения > 0
        self.assertGreater(indicators['demographic_data']['social_transfers_per_capita'], 0)
