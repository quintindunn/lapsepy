"""
Author: Quintin Dunn
Date: 10/22/23
"""

from datetime import datetime, timedelta


class BaseGQL:
    """
    Base class for GraphQL queries.
    """
    def __init__(self, operation_name: str, query: str):
        self.variables = None
        self.operation_name = operation_name
        self.query = query

    def to_dict(self):
        """
        :return: The GraphQL query as a dictionary, this is what is uploaded to the API.
        """
        return {
            "operationName": self.operation_name,
            "query": self.query,
            "variables": self.variables
        }


class CreateMediaGQL(BaseGQL):
    """
    Create the GraphQL Query for registering an image in the Lapse darkroom.
    """
    def __init__(self, file_uuid: str, taken_at: str, develop_in: int, color_temperature: float,
                 exposure_value: float, flash: bool, timezone: str):
        super().__init__(
            operation_name="CreateMediaGraphQLMutation",
            query="mutation CreateMediaGraphQLMutation($input: CreateMediaInput!) { createMedia(input: $input) " \
                  "{ __typename success } }"
        )
        self.file_uuid: str = file_uuid
        self.taken_at = taken_at
        self.develop_in: int = develop_in
        self.color_temperature: float = color_temperature
        self.exposure_value: float = exposure_value
        self.flash: bool = flash
        self.timezone = timezone

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "content": [
                {
                    "filtered": self.file_uuid + "/filtered_0",
                    "metadata": {
                        "colorTemperature": self.color_temperature,
                        "didFlash": self.flash,
                        "exposureValue": self.exposure_value
                    }
                }
            ],
            "developsAt": {
                "isoString": (datetime.utcnow() + timedelta(0, self.develop_in)).isoformat()[:-3] + "Z"
            },
            "faces": [],
            "mediaId": self.file_uuid,
            "takenAt": {
                "isoString": self.taken_at
            },
            "timezone": self.timezone
        }

    def to_dict(self):
        return {
            "operationName": self.operation_name,
            "query": self.query,
            "variables": self.variables,

        }


class ImageUploadURLGQL(BaseGQL):
    """
    Create the GraphQL Query for requesting an upload URL for the AWS server.
    """
    def __init__(self, file_uuid):
        """
        :param file_uuid: UUID of the file uploaded.
        """
        super().__init__(
            operation_name="ImageUploadURLGraphQLQuery",
            query="query ImageUploadURLGraphQLQuery($filename: String!) { imageUploadURL(filename: $filename) }"
        )

        self.file_uuid = file_uuid
        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables["filename"] = self.file_uuid + "/filtered_0.heic"

    def to_dict(self):
        return {
            "operationName": self.operation_name,
            "query": self.query,
            "variables": self.variables,
        }


class FriendsFeedItemsGQL(BaseGQL):
    """
    Gets items from friends feed.
    """
    def __init__(self, start_cursor: str | None = None):
        super().__init__(
            operation_name="FriendsFeedItemsGraphQLQuery",
            query="query FriendsFeedItemsGraphQLQuery($first: Int, $after: String, $last: Int, $before: String) { "
                  "friendsFeedItems(first: $first, after: $after, last: $last, before: $before) { __typename edges { "
                  "__typename cursor node { __typename ...FriendsFeedItemDetails } } pageInfo { __typename "
                  "startCursor endCursor hasNextPage hasPreviousPage } } }\nfragment FriendsFeedItemDetails on "
                  "FriendsFeedItem { __typename id description content { __typename ... on "
                  "FriendsFeedItemAlbumUpdatedV1 { ...FriendsFeedItemAlbumUpdatedDetails } ... on "
                  "FriendsFeedItemBioUpdatedV1 { ...FriendsFeedItemBioUpdatedDetails } ... on "
                  "FriendsFeedItemEmojisUpdatedV1 { ...FriendsFeedItemEmojisUpdatedDetails } ... on "
                  "FriendsFeedItemFriendSuggestionsV1 { ...FriendsFeedItemFriendSuggestionsDetails } ... on "
                  "FriendsFeedItemFriendRequestsV1 { ...FriendsFeedItemFriendRequestsDetails } ... on "
                  "FriendsFeedItemKudosUpdatedV1 { ...FriendsFeedItemKudosUpdatedDetails } ... on "
                  "FriendsFeedItemMediaFeaturedV1 { ...FriendsFeedItemMediaFeaturedDetails } ... on "
                  "FriendsFeedItemMediaSharedV1 { ...FriendsFeedItemMediaSharedDetails } ... on "
                  "FriendsFeedItemMusicUpdatedV1 { ...FriendsFeedItemMusicUpdatedDetails } ... on "
                  "FriendsFeedItemProfileCompletedV1 { ...FriendsFeedItemProfileCompletedDetails } ... on "
                  "FriendsFeedItemProfilePhotoUpdatedV1 { ...FriendsFeedItemProfilePhotoUpdatedDetails } ... on "
                  "FriendsFeedItemSelectsUpdatedV1 { ...FriendsFeedItemSelectsUpdatedDetails } ... on "
                  "FriendsFeedItemTaggedMediaSharedV2 { ...FriendsFeedItemTaggedMediaSharedDetails } } comments("
                  "first: 3) { __typename edges { __typename node { __typename ...MediaCommentDetails } } totalCount "
                  "} reactions { __typename ...MediaReactionDetails } user { __typename ...ProfileDetails } timestamp "
                  "{ __typename isoString } }\nfragment FriendsFeedItemAlbumUpdatedDetails on "
                  "FriendsFeedItemAlbumUpdatedV1 { __typename id title mediaIds totalCount }\nfragment "
                  "FriendsFeedItemBioUpdatedDetails on FriendsFeedItemBioUpdatedV1 { __typename bio }\nfragment "
                  "FriendsFeedItemEmojisUpdatedDetails on FriendsFeedItemEmojisUpdatedV1 { __typename emojis "
                  "}\nfragment FriendsFeedItemFriendSuggestionsDetails on FriendsFeedItemFriendSuggestionsV1 { "
                  "__typename suggestions { __typename ...FriendSuggestionDetails } }\nfragment "
                  "FriendSuggestionDetails on FriendSuggestion { __typename profile { __typename ...ProfileDetails "
                  "invitedBy(last: 3) { __typename edges { __typename node { __typename ...ProfileDetails } } } } "
                  "reason }\nfragment ProfileDetails on Profile { __typename id displayName profilePhotoName username "
                  "bio emojis { __typename emojis } friendStatus isBlocked blockedMe hashedPhoneNumber joinedAt { "
                  "__typename isoString } kudos { __typename emoji totalCount lastSentAt { __typename isoString } } "
                  "selectsVideo { __typename ...RecapVideoDetails } music { __typename ...ProfileMusicDetails } tags "
                  "{ __typename type text } }\nfragment RecapVideoDetails on RecapVideo { __typename id videoFilename "
                  "totalDuration interval media { __typename imageFilename } }\nfragment ProfileMusicDetails on "
                  "ProfileMusic { __typename artist artworkUrl duration songTitle songUrl }\nfragment "
                  "FriendsFeedItemFriendRequestsDetails on FriendsFeedItemFriendRequestsV1 { __typename requests { "
                  "__typename ...FriendRequestDetails } }\nfragment FriendRequestDetails on FriendRequest { "
                  "__typename profile { __typename ...ProfileDetails invitedBy(last: 3) { __typename edges { "
                  "__typename cursor node { __typename ...ProfileDetails } } } } }\nfragment "
                  "FriendsFeedItemKudosUpdatedDetails on FriendsFeedItemKudosUpdatedV1 { __typename empty }\nfragment "
                  "FriendsFeedItemMediaFeaturedDetails on FriendsFeedItemMediaFeaturedV1 { __typename media { "
                  "__typename ...MediaDetails } }\nfragment MediaDetails on Media { __typename id takenAt { "
                  "__typename isoString } takenBy { __typename ...ProfileDetails } commentsCount developsAt { "
                  "__typename isoString } destroyedAt { __typename isoString } deletedAt { __typename isoString } "
                  "partyId timeCapsuleId timezone content { __typename filtered original } submittedToTeam reactions "
                  "{ __typename ...MediaReactionDetails } comments(first: 3) { __typename edges { __typename node { "
                  "__typename ...MediaCommentDetails } } } tags(first: 3) { __typename edges { __typename node { "
                  "__typename ...MediaTagDetails } } totalCount } featured faceFrames { __typename xPos yPos width "
                  "height } }\nfragment MediaReactionDetails on MediaReaction { __typename emoji hasReacted count "
                  "}\nfragment MediaCommentDetails on MediaComment { __typename id author { __typename "
                  "...ProfileDetails } media { __typename id } createdAt { __typename isoString } deletedAt { "
                  "__typename isoString } text isLiked likeCount }\nfragment MediaTagDetails on MediaTag { __typename "
                  "frame { __typename position { __typename xPos yPos } size { __typename width height } } taggedAt { "
                  "__typename isoString } taggedBy { __typename id } ... on MediaContactTag { hashedPhoneNumber } ... "
                  "on MediaProfileTag { profile { __typename id displayName username profilePhotoName friendStatus } "
                  "shared } }\nfragment FriendsFeedItemMediaSharedDetails on FriendsFeedItemMediaSharedV1 { "
                  "__typename entries { __typename ...FriendsFeedItemMediaSharedEntryDetails } }\nfragment "
                  "FriendsFeedItemMediaSharedEntryDetails on FriendsFeedItemMediaSharedEntryV1 { __typename id seen "
                  "media { __typename ...MediaDetails } }\nfragment FriendsFeedItemMusicUpdatedDetails on "
                  "FriendsFeedItemMusicUpdatedV1 { __typename artist artworkUrl songTitle }\nfragment "
                  "FriendsFeedItemProfileCompletedDetails on FriendsFeedItemProfileCompletedV1 { __typename photoName "
                  "selectsVideo { __typename ...RecapVideoDetails } }\nfragment "
                  "FriendsFeedItemProfilePhotoUpdatedDetails on FriendsFeedItemProfilePhotoUpdatedV1 { __typename "
                  "profilePhotoName }\nfragment FriendsFeedItemSelectsUpdatedDetails on "
                  "FriendsFeedItemSelectsUpdatedV1 { __typename imageFilename selectsVideo { __typename "
                  "...RecapVideoDetails } }\nfragment FriendsFeedItemTaggedMediaSharedDetails on "
                  "FriendsFeedItemTaggedMediaSharedV2 { __typename sharedMedia { __typename "
                  "...FriendsFeedItemMediaSharedDetails } }")

        self.last = 10
        self.before = start_cursor

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables = {
            "before": self.before,
            "last": self.last
        }

    def to_dict(self):
        return {
            "operationName": self.operation_name,
            "query": self.query,
            "variables": self.variables,
        }
