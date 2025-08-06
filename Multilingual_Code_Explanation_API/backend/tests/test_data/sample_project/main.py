
def calculate_total(items):
    """Calculate total price with tax"""
    TAX_RATE = 0.08
    return sum(item['price'] for item in items) * (1 + TAX_RATE)
