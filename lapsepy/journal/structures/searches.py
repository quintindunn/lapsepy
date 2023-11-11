from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lapsepy.lapse import Lapse


class SearchUser:
    def __init__(self, user_id, display_name: str, profile_photo_name: str, username: str, friend_status: str,
                 blocked_me: bool, is_blocked: bool):

        self.user_id = user_id
        self.display_name = display_name,
        self.profile_photo_name = profile_photo_name
        self.username = username
        self.friend_status = friend_status
        self.blocked_me = blocked_me
        self.is_blocked = is_blocked

    def to_profile(self, ctx: "Lapse", album_limit: int = 6, friends_limit: int = 10):
        return ctx.get_profile_by_id(user_id=self.user_id, album_limit=album_limit, friends_limit=friends_limit)

    def __str__(self):
        return f"<SearchUser username=\"{self.username}\" user_id=\"{self.user_id}\">"

    __repr__ = __str__
