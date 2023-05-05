def price(query, sat_per_token=1):
    """Calculate the price of a query in satoshis based on the query's length."""
    return len(query) * sat_per_token