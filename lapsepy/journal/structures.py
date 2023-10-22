import io
from datetime import datetime

import PIL.Image
import requests


def _dt_from_iso(dt_str: str):
    return datetime.fromisoformat(dt_str)


class Profile:
    def __init__(self, user_id: str, username: str, display_name: str, profile_photo_name: str, bio: str):
        self.user_id: str = user_id
        self.username: str = username
        self.user_display_name = display_name
        self.profile_photo_name = profile_photo_name
        self.bio = bio
        self.media: list[Snap] = []

    @staticmethod
    def from_dict(profile_data: dict) -> "Profile":
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
        self.seen = seen
        self.taken_at: datetime = taken_at
        self.develops_at: datetime = develops_at
        self.filtered_id: str | None = filtered_id
        self.original_id: str | None = original_id

        self.filtered: Image.Image | None = None
        self.original: Image.Image | None = None

    @staticmethod
    def from_dict(snap_data: dict) -> "Snap":
        sd = snap_data
        md = snap_data.get('media')
        return Snap(
            seen=sd.get('seen'),
            taken_at=_dt_from_iso(md.get("takenAt")['isoString']),
            develops_at=_dt_from_iso(md.get("developsAt")['isoString']),
            filtered_id=md['content'].get("filtered"),
            original_id=md['content'].get("original")
        )

    def load_filtered(self, quality: int, fl_keep_iptc: bool):
        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc" if fl_keep_iptc else "")
        url += f"{self.filtered_id}/filtered_0.jpeg"

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)

        im = PIL.Image.open(bytes_io)
        return im

    def load_original(self, quality: int, fl_keep_iptc: bool):
        url = f"{self.BASE_URL}q_{quality}" + (",fl_keep_itc" if fl_keep_iptc else "")
        url += f"{self.original_id}/original_0.jpeg"

        request = requests.get(url)
        bytes_io = io.BytesIO(request.content)

        im = PIL.Image.open(bytes_io)
        return im

    def load_snap(self, quality: int = 100, fl_keep_iptc: bool = True):
        if self.filtered_id is not None:
            self.filtered = self.load_filtered(quality=quality, fl_keep_iptc=fl_keep_iptc)
        if self.original is not None:
            self.original = self.load_original(quality=quality, fl_keep_iptc=fl_keep_iptc)
