import json
import uuid
import products_db
from response_utils import create_success_response, create_error_response

def handler(event, context):
    body = event.get('body') or ''
    try:
        # Parse JSON body
        item = json.loads(body)
        
        # Prevent clients from specifying their own ID
        if 'id' in item:
            return create_error_response(400, 'Product id is not allowed')
        
        # Generate unique ID
        product_id = str(uuid.uuid4())
        item['id'] = product_id
        
        # Extract user Amazon Resource Name (ARN) from request context
        user_arn = event.get('requestContext', {}).get('identity', {}).get('userArn', 'unknown')
        
        # Store in DynamoDB
        inserted = products_db.insert_product(item, user_arn)
        
        # Return created product
        return create_success_response(201, inserted)
    except ValueError as e:
        return create_error_response(409, str(e))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(500, f'Internal server error - {str(e)}')