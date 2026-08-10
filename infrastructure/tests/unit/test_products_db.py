import unittest
import boto3
import os
from decimal import Decimal
from moto import mock_dynamodb
from unittest.mock import patch, MagicMock

# Set dummy environment variables so boto3 doesn't complain during tests
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@mock_dynamodb
class TestProductDatabase(unittest.TestCase):
    def setUp(self):
        """Set up mock DynamoDB table for testing."""
        # Create mock DynamoDB resource
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create mock table with same structure as production
        self.table = self.dynamodb.create_table(
            TableName='Products',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Populate with test data
        self.seed_test_data()
    
    def seed_test_data(self):
        """Add sample products for testing (using Decimal for prices)."""
        test_products = [
            {
                'id': 'prod_001',
                'name': 'Wireless Headphones',
                'price': Decimal('199.99'),
                'category': 'Electronics',
                'inventory_count': 50
            },
            {
                'id': 'prod_002',
                'name': 'Running Shoes',
                'price': Decimal('129.99'),
                'category': 'Sports',
                'inventory_count': 25
            }
        ]
        
        for product in test_products:
            self.table.put_item(Item=product)
    
    def test_get_product_from_mock_table(self):
        """Test product retrieval from mocked DynamoDB."""
        from products_db import get_product
        
        # Test existing product
        product = get_product('prod_001')
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], 'Wireless Headphones')
        
        # Test non-existent product
        product = get_product('nonexistent')
        self.assertIsNone(product)
    
    def test_create_product_in_mock_table(self):
        """Test product creation in mocked DynamoDB."""
        from products_db import insert_product, get_product
        
        new_product = {
            'name': 'Gaming Mouse',
            'price': Decimal('79.99'),  # Fixed float to Decimal here!
            'category': 'Electronics'
        }
        
        created_product = insert_product(new_product)
        
        # Verify product was created with generated ID
        self.assertIn('product_id', created_product)
        self.assertEqual(created_product['name'], 'Gaming Mouse')
        
        # Verify product exists in table using the generated product_id
        retrieved = get_product(created_product['product_id'])
        self.assertEqual(retrieved['name'], 'Gaming Mouse')


class TestDatabaseErrorHandling(unittest.TestCase):
    
    @patch('products_db.table')
    def test_dynamodb_connection_error(self, mock_table):
        """Test handling of DynamoDB connection failures."""
        # Force the table operation to raise a connection/client error
        mock_table.get_item.side_effect = Exception("Unable to connect to DynamoDB")
        
        from products_db import get_product
        
        with self.assertRaises(Exception) as context:
            get_product('prod_123')
        
        self.assertIn("Unable to connect", str(context.exception))
    
    @mock_dynamodb
    def test_item_not_found_handling(self):
        """Test graceful handling of missing items."""
        # Set up empty table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        dynamodb.create_table(
            TableName='Products',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        from products_db import get_product
        
        # Test that missing item returns None instead of raising exception
        result = get_product('nonexistent_product')
        self.assertIsNone(result)