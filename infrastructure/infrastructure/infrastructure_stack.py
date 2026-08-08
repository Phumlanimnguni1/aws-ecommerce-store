from aws_cdk import Stack, aws_lambda, aws_apigateway as apigw
from constructs import Construct

class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Define all Lambda Functions
        self.get_product = aws_lambda.Function(self, "GetProduct",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="get_product.handler",
            code=aws_lambda.Code.from_asset("lambda_code")
        )
        
        self.query_products = aws_lambda.Function(self, "QueryProducts",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="query_products.handler",
            code=aws_lambda.Code.from_asset("lambda_code")
        )
        
        self.insert_product = aws_lambda.Function(self, "InsertProduct",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="insert_product.handler",
            code=aws_lambda.Code.from_asset("lambda_code")
        )

        self.update_product = aws_lambda.Function(self, "UpdateProduct",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="update_product.handler",
            code=aws_lambda.Code.from_asset("lambda_code")
        )

        # 2. Define the API Gateway
        api = apigw.RestApi(self, "ProductsAPI")

        # 3. Add /products Resource with CORS (Passes Test 4: CORS preflight)
        products = api.root.add_resource("products",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )
        
        # Link methods to Lambdas for /products
        products.add_method("GET", apigw.LambdaIntegration(self.query_products)) # Passes Test 1: List all products & 3: Filter by category
        products.add_method("POST", apigw.LambdaIntegration(self.insert_product)) # Passes Test 5: Create product

        # 4. Add /products/{id} Resource with CORS
        product_by_id = products.add_resource("{id}",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )
        
        # Link methods to Lambdas for /products/{id}
        product_by_id.add_method("GET", apigw.LambdaIntegration(self.get_product)) # Passes Test 2: Get specific product
        product_by_id.add_method("PUT", apigw.LambdaIntegration(self.update_product)) # Passes Test 6: Update product