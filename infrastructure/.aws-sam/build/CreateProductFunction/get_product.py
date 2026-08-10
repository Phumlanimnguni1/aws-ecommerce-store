import json
import products_db
from response_utils import create_response

def handler(event, context):
    path_parameters = event.get('pathParameters')
    
    # 1. Handle missing path parameters
    if not path_parameters or not path_parameters.get('id'):
        # Matches the expected test capitalization exactly
        return create_response(400, {'error': 'Product ID is required'})
        
    product_id = path_parameters['id']
    
    # 2. Get the product from the database
    product = products_db.get_product(product_id)
    
    # 3. Handle product not found
    if not product:
        return create_response(404, {'error': 'Product not found'})
        
    # 4. Success! (Status code MUST be the first argument)
    return create_response(200, product)