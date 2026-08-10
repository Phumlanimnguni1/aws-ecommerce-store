import unittest
import json
from unittest.mock import patch, MagicMock

class TestCreateProduct(unittest.TestCase):
    
    @patch('products_db.insert_product')
    def test_create_product_success(self, mock_insert_product):
        """Test successful product creation."""
        # Arrange
        new_product_data = {
            'name': 'Gaming Mouse',
            'price': 79.99,
            'category': 'Electronics'
        }
        
        mock_insert_product.return_value = {
            'product_id': 'prod_456',
            **new_product_data
        }
        
        create_event = {
            'httpMethod': 'POST',
            'body': json.dumps(new_product_data)
        }
        
        # Act
        from insert_product import handler
        response = handler(create_event, None)
        
        # Assert
        self.assertEqual(response['statusCode'], 201)
        
        body = json.loads(response['body'])
        self.assertEqual(body['name'], 'Gaming Mouse')
        self.assertIn('product_id', body)

class TestCreateProductErrorHandling(unittest.TestCase):
    
    @patch('products_db.insert_product')
    def test_create_product_validation_error(self, mock_insert_product):
        """Test product creation with invalid data."""
        # Arrange
        invalid_product = {
            'name': '',  # Empty name should fail validation
            'price': -10,  # Negative price should fail
            'category': 'InvalidCategory'
        }
        
        create_event = {
            'httpMethod': 'POST',
            'body': json.dumps(invalid_product)
        }
        
        # Act
        from insert_product import handler
        response = handler(create_event, None)
        
        # Assert
        self.assertEqual(response['statusCode'], 400)
        
        body = json.loads(response['body'])
        self.assertIn('validation_errors', body)
        
        # Verify database was not called with invalid data
        mock_insert_product.assert_not_called()