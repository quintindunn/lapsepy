from datetime import datetime

from .core import ReactableMedia

from PIL import Image

import io
import requests
import logging
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from lapsepy.journal.structures.profile import Profile

logger = logging.getLogger("lapsepy.journal.structures.album.py")


# ToDo: Add this function in a common file instead of copying & pasting.
def _parse_iso_time(iso_str: str) -> datetime:
    iso_str = iso_str.removesuffix("Z")
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt
    except ValueError:
        raise ValueError("Invalid ISO format. The input should be in the format 'YYYY-MM-DDTHH:MM:SSZ'.")


class AlbumMedia(ReactableMedia):
    BASE_URL = "https://image.production.journal-api.lapse.app/image/upload/"

    def __init__(self, added_at: datetime, media_id: str, taken_at: datetime, capturer_id: str):
        super().__init__(media_id=media_id)

        self.added_at: datetime = added_at
        self.id: str = media_id
        self.taken_at: datetime = taken_at
        self.capturer_id: str = capturer_id

        self.im: Image.Image | None

    def load(self, quality: int = 65, fl_keep_iptc: bool = True) -> Image.Image:
        """
        Loads the filtered Snap object's image into memory by making an HTTP request to Lapse's servers.
        :param quality: Quality of the image (1-100)
        seek https://cloudinary.com/documentation/transformation_reference#q_quality for more information.
        :param fl_keep_iptc: Whether to keep copyright related material seek
        https://cloudinary.com/documentation/transformation_reference#fl_keep_attribution for more information.

        :return: Pillow image.
        """
        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc/" if fl_keep_iptc else "/")
        url += f"{self.id}.jpeg"

        logger.debug(f"Getting image from \"{url}\"")

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)
        image = Image.open(bytes_io)
        return image

    @staticmethod
    def from_dict(album_data: dict) -> "AlbumMedia":
        media_data = album_data.get("media", {})
        return AlbumMedia(
            added_at=_parse_iso_time(album_data.get('addedAt', {}).get("isoString")),
            media_id=media_data.get("id", None),
            taken_at=_parse_iso_time(media_data.get("takenAt", {}).get("isoString", "")),
            capturer_id=media_data.get("takenBy", {}).get("id", "")
        )

    def __str__(self):
        return f"<Lapse AlbumMedia id=\"{self.id}\" capturer={self.capturer_id}>"

    __repr__ = __str__


class Album:
    def __init__(self, album_id, media: list[AlbumMedia], album_name: str | None = None, visibility: str | None = None,
                 created_at: datetime | None = None, updated_at: datetime = None, owner: Union["Profile", None] = None):
        self.album_id = album_id
        self.media = media

        self.album_name = album_name
        self.visibility = visibility
        self.created_at = created_at
        self.updated_at = updated_at

        self.owner = owner

    def __str__(self):
        return f"<Lapse album id=\"{self.album_id}\" size={len(self.media)}>"

    __repr__ = __str__
