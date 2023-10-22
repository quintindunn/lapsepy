from PIL.Image import Image
from datetime import datetime

from lapsepy.auth.refresher import refresh
from lapsepy.journal.journal import Journal
from lapsepy.journal.common.exceptions import AuthTokenExpired


class Lapse:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token
        self.auth_token: str | None = None
        self.journal = Journal(authorization=self.auth_token)
        self._refresh_auth_token()

    def upload_photo(self, im: Image,
                     develop_in: int,
                     file_uuid: str | None = None,
                     taken_at: datetime | None = None,
                     color_temperature: float = 6000,
                     exposure_value: float = 9,
                     flash: bool = False,
                     timezone: str = "America/New_York"):
        try:
            return self.journal.upload_photo(im=im, develop_in=develop_in, file_uuid=file_uuid, taken_at=taken_at,
                                             color_temperature=color_temperature, exposure_value=exposure_value,
                                             flash=flash,
                                             timezone=timezone)
        except AuthTokenExpired:
            return self.journal.upload_photo(im=im, develop_in=develop_in, file_uuid=file_uuid, taken_at=taken_at,
                                             color_temperature=color_temperature, exposure_value=exposure_value,
                                             flash=flash,
                                             timezone=timezone)

    def get_friends_feed(self, count: int = 10):
        try:
            return self.journal.get_friends_feed(count=count)
        except AuthTokenExpired:
            return self.journal.get_friends_feed(count=count)

    def _refresh_auth_token(self) -> None:
        """
        Refreshes auth token in all subclasses that use the auth token.
        :return: None
        """
        self.auth_token = refresh(self.refresh_token)
        self.journal.refresh_authorization(self.auth_token)
