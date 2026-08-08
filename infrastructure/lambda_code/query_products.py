import json

def handler(event, context):
    return {
        "statusCode": 200, 
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps([{"id": "prod_123", "name": "Wireless Headphones", "price": 199.99}])
    }