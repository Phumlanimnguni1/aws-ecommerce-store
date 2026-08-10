def validate_product_data(product_data):
    """
    Validates incoming product payload.
    Returns a list of error strings. If the list is empty, validation passed.
    """
    errors = []
    
    # Check that name exists and is not just empty spaces
    name = product_data.get('name', '')
    if not name or not str(name).strip():
        errors.append("Product name is required.")
        
    # Check that price is a positive number
    price = product_data.get('price', 0)
    if not isinstance(price, (int, float)) or price < 0:
        errors.append("Price must be a positive number.")
        
    # Check that the category is valid
    valid_categories = ['Electronics', 'Sports', 'Home Goods', 'Clothing']
    category = product_data.get('category', '')
    if category not in valid_categories:
        errors.append(f"Category must be one of: {', '.join(valid_categories)}")
        
    return errors