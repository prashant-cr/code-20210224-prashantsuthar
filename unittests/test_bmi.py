import unittest


from functionality.bmi_data import get_bmi, get_category, get_result_according_data


class TestBMI(unittest.TestCase):

    def test_bmi_method_positive_case(self):
        height = 165
        weight = 70
        test_result = 25.71
        result = get_bmi(height, weight)
        self.assertEqual(test_result, result)

    def test_bmi_method_negative_case(self):
        height = 0
        weight = 0
        test_result = 0
        result = get_bmi(height, weight)
        self.assertEqual(test_result, result)

    def test_bmi_category(self):
        test_bmi = 33
        test_category = "Moderately obese"
        result = get_category(test_bmi)
        self.assertEqual(test_category, result['Category'])

    def test_get_result(self):
        payload = [
            {"Gender": "Male", "HeightCm": 171, "WeightKg": 96}
        ]
        result = get_result_according_data(payload)
        test_result = [{'Gender': 'Male', 'HeightCm': 171, 'WeightKg': 96, 'bmi': 32.83,
                        'Category': 'Moderately obese', 'HealthRisk': 'Medium risk'}]
        self.assertEqual(test_result, result[0])
