import json

# Complete API Gateway event structure for product API
api_gateway_event = {
    'httpMethod': 'GET',
    'path': '/products/prod_123',
    'pathParameters': {
        'id': 'prod_123'
    },
    'queryStringParameters': {
        'category': 'Electronics',
        'limit': '10'
    },
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token123',
        'User-Agent': 'Mozilla/5.0...'
    },
    'body': None,
    'isBase64Encoded': False,
    'requestContext': {
        'requestId': 'test-request-id',
        'stage': 'dev',
        'httpMethod': 'GET'
    }
}

class APIGatewayEventFactory:
    """Factory for creating API Gateway events for testing."""
    
    @staticmethod
    def create_get_product_event(product_id, query_params=None):
        """Create event for GET /products/{id} requests."""
        return {
            'httpMethod': 'GET',
            'path': f'/products/{product_id}',
            'pathParameters': {'id': product_id},
            'queryStringParameters': query_params,
            'headers': {'Content-Type': 'application/json'},
            'body': None,
            'isBase64Encoded': False
        }
    
    @staticmethod
    def create_post_product_event(product_data):
        """Create event for POST /products requests."""
        return {
            'httpMethod': 'POST',
            'path': '/products',
            'pathParameters': None,
            'queryStringParameters': None,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(product_data),
            'isBase64Encoded': False
        }
    
    @staticmethod
    def create_query_products_event(category=None, limit=None):
        """Create event for GET /products with query parameters."""
        query_params = {}
        if category:
            query_params['category'] = category
        if limit:
            query_params['limit'] = str(limit)
            
        return {
            'httpMethod': 'GET',
            'path': '/products',
            'pathParameters': None,
            'queryStringParameters': query_params if query_params else None,
            'headers': {'Content-Type': 'application/json'},
            'body': None,
            'isBase64Encoded': False
        }