import boto3
import boto3.dynamodb.conditions
from datetime import datetime
from botocore.exceptions import ClientError

table = boto3.resource('dynamodb').Table('Products')

def insert_product(item, user_arn=None):
    """Insert a new product into DynamoDB. Fails if product ID already exists."""
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Add audit fields
    item['created_at'] = timestamp
    item['created_by'] = user_arn
    item['updated_at'] = timestamp
    item['updated_by'] = user_arn
    
    try:
        # Use condition to prevent overwriting existing products
        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(id)'
        )
        return item
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Product with id {item['id']} already exists")
        raise

def get_all_products():
    """Retrieve all products from the table"""
    return table.scan()['Items']

def get_products_by_category(category):
    """Retrieve products filtered by category using GSI"""
    # Use GSI query instead of scan for better performance
    return table.query(
        IndexName='category-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('category').eq(category)
    ).get('Items')

def update_product(product_id, fields, user_arn=None):
    """Update an existing product. Fails if product doesn't exist."""
    
    # Fields are already validated by Pydantic before reaching this function
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    update_expression = """SET category = :category,
        title = :title,
        description = :description,
        price = :price,
        updated_at = :updated_at,
        updated_by = :updated_by"""
    
    expression_attribute_values = {
        ':category': fields['category'],
        ':title': fields['title'],
        ':description': fields['description'],
        ':price': fields['price'],
        ':updated_at': timestamp,
        ':updated_by': user_arn
    }
    
    try:
        # Use condition to ensure product exists before updating
        response = table.update_item(
            Key={'id': product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression='attribute_exists(id)',
            ReturnValues='ALL_NEW'
        )
        return response['Attributes']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Product with id {product_id} does not exist")
        raise

def update_product_with_version(product_id, fields, expected_version, user_arn=None):
    """Update product with optimistic locking using version number"""
    
    timestamp = datetime.utcnow().isoformat() + 'Z'
    new_version = expected_version + 1
    
    update_expression = """SET category = :category,
        title = :title,
        description = :description,
        price = :price,
        updated_at = :updated_at,
        updated_by = :updated_by,
        version = :new_version"""
    
    expression_attribute_values = {
        ':category': fields['category'],
        ':title': fields['title'],
        ':description': fields['description'],
        ':price': fields['price'],
        ':updated_at': timestamp,
        ':updated_by': user_arn,
        ':new_version': new_version,
        ':expected_version': expected_version
    }
    
    try:
        response = table.update_item(
            Key={'id': product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression='attribute_exists(id) AND version = :expected_version',
            ReturnValues='ALL_NEW'
        )
        return response['Attributes']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Product was modified by another user. Please refresh and try again.")
        raise
    
def get_product(product_id):
    """Retrieve a single product by its ID from DynamoDB."""
    response = table.get_item(Key={'id': product_id})
    return response.get('Item')