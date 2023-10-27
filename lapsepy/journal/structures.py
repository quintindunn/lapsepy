"""
Author: Quintin Dunn
Date: 10/22/23
"""

import io
import logging
import requests

from datetime import datetime
from PIL import Image

logger = logging.getLogger("lapsepy.journal.structures.py")


def _dt_from_iso(dt_str: str):
    return datetime.fromisoformat(dt_str)


class Profile:
    def __init__(self, user_id: str, username: str, display_name: str, profile_photo_name: str, bio: str | None,
                 emojis: list[str], is_friends: bool, blocked_me: bool, kudos: int, tags: list[dict],
                 is_blocked: bool = False, friends: list["Profile"] = None):
        if friends is None:
            friends = []

        self.bio: str = bio
        self.blocked_me: bool = blocked_me
        self.user_display_name: str = display_name
        self.emojis: list[str] = emojis
        self.is_friends: bool = is_friends
        self.kudos = kudos
        self.profile_photo_name: str = profile_photo_name
        self.tags = tags
        self.user_id: str = user_id
        self.username: str = username
        self.media: list[Snap] = []
        self.is_blocked = is_blocked

        self.friends: list["Profile"] = friends

        self.profile_picture: Image.Image | None = None

    @staticmethod
    def from_dict(profile_data: dict) -> "Profile":
        """
        Generates a Profile object from a dictionary with the necessary profile data
        :param profile_data: Dictionary containing the necessary data.
        :return: Profile object prefilled with the data.
        """
        logger.debug("Creating new Profile object from dictionary.")

        pd = profile_data
        return Profile(
            bio=pd.get('bio'),
            blocked_me=pd.get('blockedMe'),
            display_name=pd.get('displayName'),
            emojis=pd.get("emojis", {}).get("emojis"),
            is_friends=pd.get("friendStatus") == "FRIENDS",
            kudos=pd.get("kudos", {}).get("totalCount", -1),
            profile_photo_name=pd.get('profilePhotoName'),
            tags=pd.get("tags"),
            user_id=pd.get('id'),
            username=pd.get('username'),
        )

    def load_profile_picture(self, quality: int = 100, height: int | None = None) -> Image.Image:
        """
        Loads the Profile's profile picture into memory by making an HTTP request to Lapse's servers.
        :param quality: Quality of the image (1-100)
        seek https://cloudinary.com/documentation/transformation_reference#q_quality for more information.
        :param height: Height of the image in pixels, width is determined by image aspect ratio. Leave as None to get
        original height.

        :return: Pillow image.
        """
        url = f"https://image.production.journal-api.lapse.app/image/upload/q_{quality}"
        url += f",h_{height}" if height is not None else ""
        url += f"//{self.profile_photo_name}.jpg"

        logger.debug(f"Getting profile image from \"{url}\"")

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)
        image = Image.open(bytes_io)

        self.profile_picture = image

        return image

    def __str__(self):
        return f"<Lapse profile \"{self.username}\" {self.user_id}>"


class Snap:
    BASE_URL = "https://image.production.journal-api.lapse.app/image/upload/"

    def __init__(self, seen: bool, taken_at: datetime, develops_at: datetime, filtered_id: str | None,
                 original_id: str | None):
        self.seen: bool = seen
        self.taken_at: datetime = taken_at
        self.develops_at: datetime = develops_at
        self.filtered_id: str | None = filtered_id
        self.original_id: str | None = original_id

        self.filtered: Image.Image | None = None
        self.original: Image.Image | None = None

    @staticmethod
    def from_dict(snap_data: dict) -> "Snap":
        """
        Generates a Snap object from a dictionary with the necessary snap data
        :param snap_data: Dictionary containing the necessary data.
        :return: Snap object prefilled with the data.
        """

        logger.debug("Creating new Snap object from dictionary.")

        media = snap_data.get('media')
        return Snap(
            seen=snap_data.get('seen'),
            taken_at=_dt_from_iso(media.get("takenAt")['isoString']),
            develops_at=_dt_from_iso(media.get("developsAt")['isoString']),
            filtered_id=media['content'].get("filtered"),
            original_id=media['content'].get("original")
        )

    def load_filtered(self, quality: int, fl_keep_iptc: bool) -> Image.Image:
        """
        Loads the filtered Snap object's image into memory by making an HTTP request to Lapse's servers.
        :param quality: Quality of the image (1-100)
        seek https://cloudinary.com/documentation/transformation_reference#q_quality for more information.
        :param fl_keep_iptc: Whether to keep copyright related material seek
        https://cloudinary.com/documentation/transformation_reference#fl_keep_attribution for more information.

        :return: Pillow image.
        """
        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc/" if fl_keep_iptc else "/")
        url += f"{self.filtered_id}.jpeg"

        logger.debug(f"Getting image from \"{url}\"")

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)
        image = Image.open(bytes_io)
        return image

    def load_original(self, quality: int, fl_keep_iptc: bool) -> Image.Image:
        """
        Loads the original Snap object's image into memory by making an HTTP request to Lapse's servers.
        :param quality: Quality of the image (1-100)
        seek https://cloudinary.com/documentation/transformation_reference#q_quality for more information.
        :param fl_keep_iptc: Whether to keep copyright related material seek
        https://cloudinary.com/documentation/transformation_reference#fl_keep_attribution for more information.

        :return: Pillow image.
        """

        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc" if fl_keep_iptc else "")
        url += f"{self.original_id}/original_0.jpeg"

        logger.debug(f"Getting image from \"{url}\"")

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)

        image = Image.open(bytes_io)
        return image

    def load_snap(self, quality: int = 100, fl_keep_iptc: bool = True) -> Image.Image:
        """
        Returns a Pillow Image of either the filtered image or original image.
        :param quality: Quality of the image (1-100)
        seek https://cloudinary.com/documentation/transformation_reference#q_quality for more information.
        :param fl_keep_iptc: Whether to keep copyright related material seek
        https://cloudinary.com/documentation/transformation_reference#fl_keep_attribution for more information.

        :return: Pillow image.
        """
        if self.filtered_id is not None:
            logger.debug("Loading \"filtered\" image.")
            self.filtered = self.load_filtered(quality=quality, fl_keep_iptc=fl_keep_iptc)
            return self.filtered
        if self.original is not None:
            logger.debug("Loading \"original\" image.")
            self.original = self.load_original(quality=quality, fl_keep_iptc=fl_keep_iptc)
            return self.original
