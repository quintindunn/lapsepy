"""
Author: Quintin Dunn
Date: 10/22/23
"""


class SyncJournalException(Exception):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message


class UserNotFoundException(SyncJournalException):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message


class AuthTokenError(SyncJournalException):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message


class AuthTokenExpired(AuthTokenError):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message




def sync_journal_exception_router(error: dict) -> SyncJournalException:
    """
    Takes in errors from https://sync-service.production.journal-api.lapse.app/graphql API and parses them, raises
    the appropriate error.
    :param error: Error from https://sync-service.production.journal-api.lapse.app/graphql
    :return: Error
    """
    if error.get("message") == "No authentication token provided":
        return AuthTokenError(error.get("message"))
    elif error.get("message") == "JWT string does not consist of exactly 3 parts (header, payload, signature)":
        return AuthTokenError("Authentication token is not properly formatted")
    elif error.get("message").startswith("Token expired at "):
        return AuthTokenExpired("Authentication token expired.")

    return SyncJournalException(f"Unknown Error: {error.get('message')}")
