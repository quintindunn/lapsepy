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
    def __init__(self, user_id: str, username: str, display_name: str, profile_photo_name: str, bio: str):
        self.user_id: str = user_id
        self.username: str = username
        self.user_display_name: str = display_name
        self.profile_photo_name: str = profile_photo_name
        self.bio: str = bio
        self.media: list[Snap] = []

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
            user_id=pd.get('id'),
            username=pd.get('username'),
            display_name=pd.get('displayName'),
            profile_photo_name=pd.get('profilePhotoName'),
            bio=pd.get('bio')
        )

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
