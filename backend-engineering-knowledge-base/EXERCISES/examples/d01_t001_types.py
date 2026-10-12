def parse_limit(raw: str, default: int = 20, upper: int = 100) -> int:
    """Convert a query-string limit to an int, or raise ValueError."""
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw, 10)
    except ValueError as exc:
        raise ValueError("limit must be an integer") from exc
    if value < 1 or value > upper:
        raise ValueError(f"limit must be between 1 and {upper}")
    return value


if __name__ == "__main__":
    assert parse_limit("20") == 20
    assert parse_limit("") == 20
    assert parse_limit("100") == 100
    try:
        parse_limit("20abc")
    except ValueError as exc:
        assert str(exc) == "limit must be an integer"
    else:
        raise AssertionError("expected ValueError")
    try:
        parse_limit("0")
    except ValueError:
        pass
    else:
        raise AssertionError("expected range error")
    print("ok", parse_limit("15"))
