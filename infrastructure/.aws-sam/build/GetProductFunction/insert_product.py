import json
import products_db
from response_utils import create_response
from product_validator import validate_product_data

def handler(event, context):
    # 1. Parse the incoming JSON body
    body_str = event.get('body')
    if not body_str:
        body_str = '{}'
        
    product_data = json.loads(body_str)
        
    # 2. Validate the data
    validation_errors = validate_product_data(product_data)
    if validation_errors:
        # Return 400 immediately if data is bad
        return create_response(400, {'validation_errors': validation_errors})
        
    # 3. Insert into the database
    result = products_db.insert_product(product_data)
    
    # 4. Success! (201 Created)
    return create_response(201, result)