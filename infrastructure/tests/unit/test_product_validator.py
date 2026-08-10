import unittest
import json
class TestProductValidation(unittest.TestCase):
    def setUp(self):
        """Set up realistic test data."""
        self.valid_products = [
            {
                'name': 'Wireless Headphones',
                'price': 199.99,
                'category': 'Electronics',
                'description': 'High-quality wireless headphones',
                'inventory_count': 50
            },
            {
                'name': 'Running Shoes',
                'price': 129.99,
                'category': 'Sports',
                'description': 'Comfortable running shoes',
                'inventory_count': 25
            }
        ]
        
        self.invalid_products = [
            {
                'name': '',  # Empty name
                'price': 99.99,
                'category': 'Electronics'
            },
            {
                'name': 'Valid Product',
                'price': -50,  # Negative price
                'category': 'Electronics'
            },
            {
                'name': 'Another Product',
                'price': 199.99,
                'category': 'NonexistentCategory'  # Invalid category
            }
        ]

    def test_product_validation_with_valid_data(self):
        """Test validation passes for valid product data."""
        from product_validator import validate_product_data
        
        for product in self.valid_products:
            with self.subTest(product=product['name']):
                errors = validate_product_data(product)
                self.assertEqual(len(errors), 0, 
                    f"Valid product {product['name']} should not have validation errors")

    def test_product_validation_with_invalid_data(self):
        """Test validation catches invalid product data."""
        from product_validator import validate_product_data
        
        for product in self.invalid_products:
            with self.subTest(product=product):
                errors = validate_product_data(product)
                self.assertGreater(len(errors), 0, 
                    f"Invalid product should have validation errors: {product}")