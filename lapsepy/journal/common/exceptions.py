def sync_journal_exception_router(error: dict):
    if error.get("message") == "No authentication token provided":
        return AuthTokenError(error.get("message"))
    elif error.get("message") == "JWT string does not consist of exactly 3 parts (header, payload, signature)":
        return AuthTokenError("Authentication token is not properly formatted")
    elif error.get("message").startswith("Token expired at "):
        return AuthTokenError("Authentication token expired.")

    return SyncJournalException(f"Unknown Error: {error.get('message')}")


class SyncJournalException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class AuthTokenError(SyncJournalException):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return self.message
