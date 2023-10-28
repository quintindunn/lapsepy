from datetime import datetime

from .profile import Profile
from .snap import Snap


def _dt_from_iso(dt_str: str):
    return datetime.fromisoformat(dt_str)


class FriendsFeed:
    def __init__(self, nodes: list["FriendNode"]):
        self.nodes: list[FriendNode] = nodes

    def __iter__(self):
        return iter(self.nodes)


class FriendNode:
    def __init__(self, profile: Profile, iso_string: str, entries: list[Snap]):
        self.profile = profile
        self.timestamp: datetime = _dt_from_iso(iso_string)
        self.entries: list[Snap] = entries
