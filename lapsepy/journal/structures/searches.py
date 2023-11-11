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
