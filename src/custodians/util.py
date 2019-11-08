from datetime import datetime, timezone

def age_in_days(reference_date, now=None):
    if not now:
        now = datetime.now(timezone.utc)
    return (now - reference_date).days

def flatten_dict(dictionary):
    return ', '.join("{!s}={!r}".format(key, val) for (key, val) in dictionary.items())
