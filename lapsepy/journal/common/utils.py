from datetime import datetime


def format_iso_time(dt: datetime) -> str:
    """
    Takes in a datetime object and returns a str of the iso format Lapse uses.
    :param dt: datetime object to convert.
    :return: Formatted datetime object.
    """
    return dt.isoformat()[:-3] + "Z"
