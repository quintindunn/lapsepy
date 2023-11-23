"""
Author: Quintin Dunn
Date: 10/22/23
"""

import io
import logging

import requests

from datetime import datetime, timedelta
from PIL import Image

from .core import Media, ReactableMedia

import typing

from lapsepy.journal.common.exceptions import SyncJournalException
from ..common.utils import format_iso_time

if typing.TYPE_CHECKING:
    from lapsepy.lapse import Lapse

logger = logging.getLogger("lapsepy.journal.structures.py")


def _dt_from_iso(dt_str: str):
    return datetime.fromisoformat(dt_str)


class Snap(ReactableMedia):
    BASE_URL = "https://image.production.journal-api.lapse.app/image/upload/"

    def __init__(self, seen: bool, taken_at: datetime, develops_at: datetime, filtered_id: str | None,
                 original_id: str | None):
        if filtered_id:
            mid = filtered_id.split("/filtered_0")[0]
        elif original_id:
            mid = original_id.split("/filtered_0")[0]
        else:
            raise SyncJournalException("Could not get ID of snap.")

        super().__init__(media_id=mid)

        self.seen: bool = seen
        self.taken_at: datetime = taken_at
        self.develops_at: datetime = develops_at
        self.filtered_id: str | None = filtered_id
        self.original_id: str | None = original_id

        self.id = mid

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

    def load_snap(self, quality: int = 65, fl_keep_iptc: bool = True) -> Image.Image:
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


class DarkRoomMedia(Media):
    BASE_URL = "https://image.production.journal-api.lapse.app/image/upload/"

    def __init__(self, develop_in: int | str, media_id: str, taken_at: datetime, im: Image.Image | None = None):

        self.im: None | Image.Image = im

        if isinstance(develop_in, int):
            self.develops_at: datetime = datetime.utcnow() + timedelta(seconds=develop_in)
        else:
            self.develops_at = _dt_from_iso(develop_in)

        self.media_id: str = media_id
        self.taken_at: datetime = taken_at

        self.im: Image.Image | None = None

        self._developed: bool = False

    @property
    def developed(self):
        self._developed = datetime.utcnow() >= self.develops_at
        return self._developed

    @property
    def reviewed(self):
        return self.review()

    def review(self, iso_string: str | None | datetime = None):
        if iso_string is None:
            iso_string = datetime.utcnow()
        return ReviewMediaPartition(media_id=self.media_id, iso_string=iso_string)

    def archive(self, ctx: "Lapse", iso_string: str | None | datetime = None):
        partition = self.review(iso_string=iso_string)
        return ctx.review_snaps(archived=[partition])

    def delete(self, ctx: "Lapse", iso_string: str | None | datetime = None):
        partition = self.review(iso_string=iso_string)
        return ctx.review_snaps(deleted=[partition])

    def share(self, ctx: "Lapse", iso_string: str | None | datetime = None):
        partition = self.review(iso_string=iso_string)
        return ctx.review_snaps(shared=[partition])

    def load(self, quality: int = 65, fl_keep_iptc: bool = True):
        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc/" if fl_keep_iptc else "/")
        url += f"{self.media_id}.jpeg"

        logger.debug(f"Getting image from \"{url}\"")

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)
        image = Image.open(bytes_io)
        self.im = image
        return image


class ReviewMediaPartition:
    def __init__(self, media_id: str, iso_string: str | None | datetime = None, tags: list = None):
        self.media_id = media_id
        iso_string = iso_string or datetime.utcnow()

        if not isinstance(iso_string, str):
            self.iso_string = format_iso_time(iso_string)
        else:
            self.iso_string = iso_string
        self.tags = tags

    def to_dict(self):
        return {
            "mediaId": self.media_id,
            "reviewedAt": {
                "isoString": self.iso_string
            },
            "tags": self.tags
        }
