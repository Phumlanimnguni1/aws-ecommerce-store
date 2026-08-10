import json

def create_response(status_code, body):
    """Base response generator with CORS headers."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body) if body else ""
    }

def create_success_response(body, status_code=200):
    """Helper for successful requests (200 OK or 201 Created)."""
    return create_response(status_code, body)

def create_error_response(status_code, message):
    """Helper for failed requests to format the error message consistently."""
    return create_response(status_code, {'error': message})