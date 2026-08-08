#!/bin/bash

# Your deployed API URL
API_URL="https://ovu9gpy0o8.execute-api.us-east-1.amazonaws.com/prod"

echo "========================================="
echo "   Running Serverless API Tests          "
echo "========================================="

echo -e "\n# Test 1: List all products (GET /products)"
curl -s "$API_URL/products"

echo -e "\n\n# Test 2: Get specific product (GET /products/{id})"
# Note: Using prod_123 because it exists in your mock data
curl -s "$API_URL/products/prod_123"

echo -e "\n\n# Test 3: Filter by category (GET /products?category=...)"
curl -s "$API_URL/products?category=Electronics"

echo -e "\n\n# Test 4: CORS preflight (OPTIONS /products)"
# Using -i to show the HTTP headers returned by the preflight request
curl -i -X OPTIONS "$API_URL/products"

echo -e "\n\n# Test 5: Create product (POST /products)"
# Expected output: 501 NotImplementedError (based on your placeholder Lambda)
curl -s -X POST "$API_URL/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Product", "price": 99.99}'

echo -e "\n\n# Test 6: Update product (PUT /products/{id})"
# Expected output: 501 NotImplementedError (based on your placeholder Lambda)
curl -s -X PUT "$API_URL/products/prod_123" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Product", "price": 149.99}'

echo -e "\n\n========================================="
echo "           All 6 Tests Completed         "
echo "========================================="