"""
Author: Quintin Dunn
Date: 11/23/23
"""
from lapsepy.journal.factory.factory import BaseGQL


class AlbumMediaGQL(BaseGQL):
    def __init__(self, album_id: str, last: int):
        super().__init__("AlbumMediaGraphQLQuery",
                         "query AlbumMediaGraphQLQuery($id: ID!, $first: Int, $after: String, $last: Int, $before: "
                         "String) { album(id: $id) { __typename id media(first: $first, after: $after, last: $last, "
                         "before: $before) { __typename totalCount edges { __typename cursor node { __typename "
                         "...AlbumMediaDetails } } pageInfo { __typename startCursor endCursor hasNextPage "
                         "hasPreviousPage } } } }\nfragment AlbumMediaDetails on AlbumMedia { __typename addedAt { "
                         "__typename isoString } media { __typename ...CoreMediaFragment } }\nfragment "
                         "CoreMediaFragment on Media { __typename id takenAt { __typename isoString } takenBy { "
                         "__typename ...CoreProfileFragment } deletedAt { __typename isoString } }\nfragment "
                         "CoreProfileFragment on Profile { __typename id displayName profilePhotoName username "
                         "friendStatus isBlocked blockedMe hashedPhoneNumber joinedAt { __typename isoString } }")

        self.album_id = album_id
        self.last = last

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables = {
            "id": self.album_id,
            "last": self.last
        }
