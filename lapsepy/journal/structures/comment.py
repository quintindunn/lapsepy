from datetime import datetime

from .core import Media

from .profile import Profile


class Comment:
    def __init__(self, author: Profile, create_at: datetime, comment_id: str, likes: int, is_liked: bool, media:
                 Media, text: str):
        self.author: Profile = author
        self.created_at: create_at = create_at
        self.comment_id: comment_id = comment_id
        self.likes: int = likes
        self.is_liked: bool = is_liked
        self.media: Media = media
        self.text: str = text
