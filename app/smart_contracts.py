def validate_transaction(sender: str, recipient: str, amount: float) -> bool:
    return all([
        amount > 0,
        sender != recipient,
        len(sender) > 0,
        len(recipient) > 0,
        isinstance(amount, (int, float))
    ])