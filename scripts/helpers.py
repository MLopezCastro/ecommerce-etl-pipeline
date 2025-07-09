from datetime import datetime

ISO_DATE_FMT = "%Y-%m-%d"

def parse_iso_date(date_str: str):
    """Convierte string a datetime o None si falla."""
    try:
        return datetime.strptime(date_str, ISO_DATE_FMT)  # <-- devuelve datetime, no .date()
    except ValueError:
        return None



