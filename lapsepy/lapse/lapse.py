"""
Author: Quintin Dunn
Date: 10/22/23
"""
from PIL.Image import Image
from datetime import datetime

from lapsepy.auth.refresher import refresh
from lapsepy.journal.journal import Journal
from lapsepy.journal.common.exceptions import AuthTokenExpired

import logging

logger = logging.getLogger("lapsepy.lapse.lapse.py")


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
        """
        Upload an image to your Lapse darkroom
        :param im: Pillow object of the Image.
        :param develop_in: How many seconds until the Image should develop.
        :param file_uuid: UUID of the image for backend storage, leave at None unless you know what you're doing.
        :param taken_at: Datetime object of when the image was taken, can be left None to be set automatically to now.
        :param color_temperature: Backend number of the color temperature, most likely from when Lapse applies a filter
        to the image, most likely doesn't change anything. Leaving at 6000 however could help Lapse add bot detection.
        :param exposure_value: Backend number of the exposure value, most likely from when the image is taken,
         most likely doesn't change anything. Leaving at 9 however could help Lapse add bot detection.
        :param flash: Backend boolean of if the image was taken with flash, most likely won't change anything. Leaving
        as False **could** help Lapse with bot detection, though it's a boolean so won't narrow it down for them too
        much
        :param timezone: Timezone that lapse thinks you're using.
        :return: None
        """
        try:
            return self.journal.upload_photo(im=im, develop_in=develop_in, file_uuid=file_uuid, taken_at=taken_at,
                                             color_temperature=color_temperature, exposure_value=exposure_value,
                                             flash=flash,
                                             timezone=timezone)
        except AuthTokenExpired:
            logger.debug("Authentication token expired.")
            return self.journal.upload_photo(im=im, develop_in=develop_in, file_uuid=file_uuid, taken_at=taken_at,
                                             color_temperature=color_temperature, exposure_value=exposure_value,
                                             flash=flash,
                                             timezone=timezone)

    def get_friends_feed(self, count: int = 10):
        """
        Gets your friend upload feed.
        :param count: How many collection to grab.
        :return: A list of profiles
        """
        try:
            return self.journal.get_friends_feed(count=count)
        except AuthTokenExpired:
            logger.debug("Authentication token expired.")
            return self.journal.get_friends_feed(count=count)

    def _refresh_auth_token(self) -> None:
        """
        Refreshes auth token in all subclasses that use the auth token.
        :return: None
        """
        logger.debug("Refreshing lapse authentication token.")
        self.auth_token = refresh(self.refresh_token)
        self.journal.refresh_authorization(self.auth_token)

    def upload_instant(self, im: Image, user_id: str, file_uuid: str | None = None, im_id: str | None = None,
                       caption: str | None = None, time_limit: int = 10):
        """
        Uploads an instant to Lapse server and sends it to a profile.
        :param im: Pillow Image object of the image.
        :param user_id: ID of user to send it to.
        :param file_uuid: UUID of the file, leave this to None unless you know what you're doing
        :param im_id: UUID of the instant, leave this to None unless you know what you're doing
        :param caption: Caption of the instant
        :param time_limit: How long they can view the instant for
        :return:
        """
        return self.journal.upload_instant(im=im, user_id=user_id, file_uuid=file_uuid, im_id=im_id, caption=caption,
                                           time_limit=time_limit)

    def update_bio(self, bio: str):
        """
        Updates your Lapse bio
        :param bio: String of what your new bio should be.
        :return: None
        """
        return self.journal.modify_bio(bio=bio)

    def update_display_name(self, display_name: str):
        """
        Updates your Lapse display name
        :param display_name: String of what your new display name should be.
        :return: None
        """
        return self.journal.modify_display_name(display_name=display_name)

    def update_username(self, username: str):
        """
        Updates your Lapse username
        :param username: String of what your new display name should be.
        :return: None
        """
        return self.journal.modify_username(username=username)
