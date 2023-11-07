"""
Author: Quintin Dunn
Date: 10/22/23
"""
from PIL.Image import Image
from datetime import datetime

from lapsepy.auth.refresher import refresh
from lapsepy.journal.journal import Journal
from lapsepy.journal.common.exceptions import AuthTokenExpired
from lapsepy.journal.structures import Profile, DarkRoomMedia, ReviewMediaPartition

import logging

logger = logging.getLogger("lapsepy.lapse.lapse.py")


class Lapse:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token
        self.auth_token: str | None = None
        self.journal = Journal(authorization=self.auth_token)
        self._refresh_auth_token()

    def _refresh_auth_token(self) -> None:
        """
        Refreshes auth token in all subclasses that use the auth token.
        :return: None
        """
        logger.debug("Refreshing lapse authentication token.")
        self.auth_token = refresh(self.refresh_token)
        self.journal.refresh_authorization(self.auth_token)

    def upload_photo(self, im: Image,
                     develop_in: int,
                     file_uuid: str | None = None,
                     taken_at: datetime | None = None,
                     color_temperature: float = 6000,
                     exposure_value: float = 9,
                     flash: bool = False,
                     timezone: str = "America/New_York") -> DarkRoomMedia:
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

    def query_darkroom(self) -> list[DarkRoomMedia]:
        """
        Queries your darkroom and returns the media inside it.
        :return:
        """
        return self.journal.query_darkroom()

    def review_snaps(self, archived: list["ReviewMediaPartition"] | None = None,
                     deleted: list["ReviewMediaPartition"] | None = None,
                     shared: list["ReviewMediaPartition"] | None = None):
        """
        Reviews snaps from the darkroom
        :param archived: List of ReviewMediaPartitions for Snaps to archive.
        :param deleted: List of ReviewMediaPartitions for Snaps to delete.
        :param shared: List of ReviewMediaPartitions for Snaps to share.
        :return:
        """
        return self.journal.review_snaps(archived=archived, deleted=deleted, shared=shared)

    def upload_instant(self, im: Image, user: str | Profile, file_uuid: str | None = None, im_id: str | None = None,
                       caption: str | None = None, time_limit: int = 10):
        """
        Uploads an instant to Lapse server and sends it to a profile.
        :param im: Pillow Image object of the image.
        :param user: ID / Object of user to send it to.
        :param file_uuid: UUID of the file, leave this to None unless you know what you're doing
        :param im_id: UUID of the instant, leave this to None unless you know what you're doing
        :param caption: Caption of the instant
        :param time_limit: How long they can view the instant for
        :return:
        """

        if isinstance(user, Profile):
            user = user.user_id

        return self.journal.upload_instant(im=im, user_id=user, file_uuid=file_uuid, im_id=im_id, caption=caption,
                                           time_limit=time_limit)

    def create_status_update(self, text: str, msg_id: str | None = None):
        """
        Creates a status update on your Journal
        :param text: Msg of the text to send
        :param msg_id: Leave None if you don't know what you're doing. FORMAT: STATUS_UPDATE:<(str(uuid.uuid4))>
        :return:
        """
        return self.journal.create_status_update(text=text, msg_id=msg_id)

    def remove_status_update(self, msg_id: str, removed_at: datetime | None = None):
        """
        Removes a status update
        :param msg_id: ID of the status update
        :param removed_at: datetime object of when it was removed
        :return:
        """
        return self.journal.remove_status_update(msg_id=msg_id, removed_at=removed_at)

    def send_kudos(self, user: str | Profile):
        """
        Sends kudos (vibes) to a user.
        :param user: ID / Object of user to send it to.
        :return:
        """
        if isinstance(user, Profile):
            user = user.user_id

        self.journal.send_kudos(user)

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

    def get_profile_by_id(self, user_id: str, album_limit: int = 6, friends_limit: int = 10) -> Profile:
        """
        Get a Profile object
        :param user_id: ID the user of the profile you want to query.
        :param album_limit: Max amount of albums to get.
        :param friends_limit: Max amount of friends to get.
        :return:
        """
        return self.journal.get_profile_by_id(user_id=user_id, album_limit=album_limit, friends_limit=friends_limit)

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

    def update_emojis(self, emojis: list[str]):
        """
        Updates your Lapse emojis
        :param emojis: List of emojis to put as your lapse emojis
        :return: None
        """
        return self.journal.modify_emojis(emojis=emojis)

    def update_dob(self, dob: str | datetime):
        """
        Updates your Lapse date of birth
        :param dob: date of birth in yyyy-mm-dd format
        :return: None
        """
        return self.journal.modify_dob(dob=dob)

    def add_reaction(self, msg_id: str, reaction: str):
        """
        Adds a reaction to a message
        :param msg_id: ID of msg to send reaction to.
        :param reaction: Reaction to send.
        :return:
        """
        return self.journal.add_reaction(msg_id=msg_id, reaction=reaction)

    def remove_reaction(self, msg_id: str, reaction: str):
        """
        removes a reaction from a message
        :param msg_id: ID of msg to remove reaction from.
        :param reaction: Reaction to remove.
        :return:
        """
        return self.journal.remove_reaction(msg_id=msg_id, reaction=reaction)

    def send_comment(self, msg_id: str, text: str, comment_id: str | None = None):
        """
        Adds a comment to a post
        :param comment_id: id of the comment, leave as None unless you know what you're doing
        :param msg_id: id of the message
        :param text: text to send in the comment
        :return:
        """
        return self.journal.create_comment(msg_id=msg_id, text=text, comment_id=comment_id)

    def delete_comment(self, msg_id: str, comment_id: str):
        """
        Deletes a comment from a lapsepy post
        :param msg_id: ID of the post
        :param comment_id: ID of the comment
        :return:
        """
        return self.journal.delete_comment(msg_id=msg_id, comment_id=comment_id)
