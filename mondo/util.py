import typing as t


def payload(values: dict[str, t.Any], errors=[]) -> dict[str, dict[str, t.Any]]:
    """Create a JSON payload wrapped in an envelope"""
    return {"values": values, "errors": errors}
