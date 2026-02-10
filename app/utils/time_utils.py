from datetime import datetime, timedelta

def now_timestamp():
    return datetime.utcnow()

def days_ago(days: int):
    return datetime.utcnow() - timedelta(days=days)
