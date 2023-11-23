from datetime import datetime

from .core import Media

import typing

if typing.TYPE_CHECKING:
    from lapsepy.lapse import Lapse
    from lapsepy.journal.structures.profile import Profile


# ToDo: Add this function in a common file instead of copying & pasting.
def _parse_iso_time(iso_str: str) -> datetime:
    iso_str = iso_str.removesuffix("Z")
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt
    except ValueError:
        raise ValueError("Invalid ISO format. The input should be in the format 'YYYY-MM-DDTHH:MM:SSZ'.")


class AlbumMedia(Media):
    def __init__(self, added_at: datetime, media_id: str, taken_at: datetime, capturer: "Profile"):
        super().__init__()

        self.added_at: datetime = added_at
        self.id: str = media_id
        self.taken_at: datetime = taken_at
        self.taken_by: Profile = capturer

    @staticmethod
    def from_dict(ctx: "Lapse", album_data: dict):
        media_data = album_data.get("media", {})
        capturer = ctx.get_profile_by_id(media_data.get("takenBy", {}).get("id"))

        return AlbumMedia(
            added_at=_parse_iso_time(album_data.get('addedAt', {}).get("isoString")),
            media_id=media_data.get("id", None),
            taken_at=_parse_iso_time(media_data.get("takenAt", {}).get("isoString")),
            capturer=capturer
        )


class Album:
    def __init__(self, album_id, media: list[AlbumMedia]):
        self.album_id = album_id
        self.media = media


