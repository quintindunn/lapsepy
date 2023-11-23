import logging
import requests

from datetime import datetime

from PIL import Image
import io

from .snap import Snap

import typing

logger = logging.getLogger("lapsepy.journal.structures.py")

if typing.TYPE_CHECKING:
    from lapsepy.lapse import Lapse
    from lapsepy.journal.structures.album import Album


def _dt_from_iso(dt_str: str):
    return datetime.fromisoformat(dt_str)


class Profile:
    def __init__(self, user_id: str, username: str, display_name: str, profile_photo_name: str, bio: str | None,
                 emojis: list[str], is_friends: bool, blocked_me: bool, kudos: int, tags: list[dict],
                 hashed_phone_number: str, is_blocked: bool = False, friends: list["Profile"] = None,
                 profile_music: "ProfileMusic" = None, albums: list["Album"] | None = None):
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
        self.hashed_phone_number = hashed_phone_number
        self.user_id: str = user_id
        self.username: str = username
        self.media: list[Snap] = []
        self.is_blocked = is_blocked
        self.albums = albums

        self.friends: list["Profile"] = friends
        self.profile_music = profile_music

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

        music = pd.get("music")
        if music is not None:
            profile_music = ProfileMusic(
                artist=music.get("artist"),
                artwork_url=music.get("artworkUrl"),
                duration=music.get("duration"),
                song_title=music.get("songTitle"),
                song_url=music.get("songUrl")
            )
        else:
            profile_music = None

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
            hashed_phone_number=pd.get("hashedPhoneNumber"),
            profile_music=profile_music
        )

    def load_profile_picture(self, quality: int = 65, height: int | None = None) -> Image.Image:
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
        request.raise_for_status()
        
        bytes_io = io.BytesIO(request.content)
        image = Image.open(bytes_io)

        self.profile_picture = image

        return image

    def send_instant(self, ctx: "Lapse", im: Image, file_uuid: str | None = None, im_id: str | None = None,
                     caption: str | None = None, time_limit: int = 10):
        return ctx.upload_instant(im=im, user=self, file_uuid=file_uuid, im_id=im_id, caption=caption,
                                  time_limit=time_limit)

    def send_kudos(self, ctx: "Lapse"):
        return ctx.send_kudos(user=self)

    def block(self, ctx: "Lapse"):
        return ctx.block_profile(user=self)

    def unblock(self, ctx: "Lapse"):
        return ctx.unblock_profile(user=self)

    def __str__(self):
        return f"<Lapse profile \"{self.username}\" {self.user_id}>"


class ProfileMusic:
    def __init__(self, artist: str, artwork_url: str, duration: int, song_title: str, song_url: str):
        self.artist = artist
        self.artwork_url = artwork_url
        self.duration = duration
        self.song_title = song_title
        self.song_url = song_url

        self.song: None | bytes = None
        self.artwork: None | Image.Image = None

    def load(self):
        """
        Loads the song, and artwork into memory
        :return: None
        """
        # Get song
        request = requests.get(self.song_url)
        request.raise_for_status()
        self.song = request.content

        # Get artwork
        if self.artwork_url:
            request = requests.get(self.artwork_url)
            request.raise_for_status()

            bytes_io = io.BytesIO(request.content)
            self.artwork = Image.open(bytes_io)