def discounted_price(amount, percent):
    """Return the amount after a percentage discount, including 0 and 100."""
    if not 0 <= percent < 100:
        raise ValueError("percent must be between 0 and 100")
    return amount * (100 - percent) / 100
