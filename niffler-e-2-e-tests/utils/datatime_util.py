from datetime import datetime, timedelta


def get_past_date_iso(days_ago: int = 7) -> str:
    """Возвращает дату в прошлом в ISO формате."""
    past_date = datetime.now() - timedelta(days=days_ago)
    return past_date.isoformat() + "Z"

def get_past_date_str(days_ago: int = 1) -> str:
    """Возвращает день месяца в виде строки (для выбора в календаре UI)."""
    past_date = datetime.now() - timedelta(days=days_ago)
    return str(past_date.day)