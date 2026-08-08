import json

def handler(event, context):
    return {
        "statusCode": 501, 
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"error": "NotImplementedError"})
    }