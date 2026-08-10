import unittest
import json
from unittest.mock import patch, MagicMock
from tests.mock_events import APIGatewayEventFactory

class TestGetProduct(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_product = {
            'product_id': 'prod_123',
            'name': 'Wireless Headphones',
            'price': 199.99,
            'category': 'Electronics',
            'inventory_count': 50
        }
        
        self.valid_event = {
            'httpMethod': 'GET',
            'pathParameters': {'id': 'prod_123'},
            'queryStringParameters': None,
            'body': None
        }

    @patch('products_db.get_product')
    def test_get_product_success(self, mock_get_product):
        """Test successful product retrieval."""
        # Arrange
        mock_get_product.return_value = self.sample_product
        
        # Act
        from get_product import handler
        response = handler(self.valid_event, None)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        
        body = json.loads(response['body'])
        self.assertEqual(body['product_id'], 'prod_123')
        self.assertEqual(body['name'], 'Wireless Headphones')
        
        # Verify database was called correctly
        mock_get_product.assert_called_once_with('prod_123')

class TestGetProductErrorHandling(unittest.TestCase):
    
    @patch('products_db.get_product')
    def test_get_product_not_found(self, mock_get_product):
        """Test handling of non-existent product requests."""
        # Arrange
        mock_get_product.return_value = None
        
        event = {
            'httpMethod': 'GET',
            'pathParameters': {'id': 'nonexistent_product'}
        }
        
        # Act
        from get_product import handler
        response = handler(event, None)
        
        # Assert
        self.assertEqual(response['statusCode'], 404)
        
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertIn('Product not found', body['error'])

    def test_missing_path_parameters(self):
        """Test handling of malformed requests."""
        # Arrange
        invalid_event = {
            'httpMethod': 'GET',
            'pathParameters': None  # Missing required parameters
        }
        
        # Act
        from get_product import handler
        response = handler(invalid_event, None)
        
        # Assert
        self.assertEqual(response['statusCode'], 400)
        
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertIn('Product ID is required', body['error'])

class TestProductAPI(unittest.TestCase):
    def test_get_product_with_factory(self):
        """Test using event factory for cleaner test code."""
        event = APIGatewayEventFactory.create_get_product_event('prod_123')
        
        with patch('products_db.get_product') as mock_get:
            mock_get.return_value = {'product_id': 'prod_123', 'name': 'Test Product'}
            
            # Fixed the handler name to match your actual file!
            from get_product import handler
            response = handler(event, None)
            
            self.assertEqual(response['statusCode'], 200)