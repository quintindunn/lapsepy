"""
Author: Quintin Dunn
Date: 10/22/23
"""

from lapsepy.journal.factory.factory import BaseGQL


class FriendsFeedItemsGQL(BaseGQL):
    """
    Gets items from friends feed.
    """

    def __init__(self, last: int = 10):
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
                  "FriendsFeedItemStatusUpdatedV1 { ...FriendsFeedItemStatusUpdatedDetails } ... on "
                  "FriendsFeedItemTaggedMediaSharedV2 { ...FriendsFeedItemTaggedMediaSharedDetails } } comments("
                  "first: 3) { __typename edges { __typename cursor node { __typename ...MediaCommentDetails } } "
                  "totalCount } reactions { __typename ...MediaReactionDetails } user { __typename "
                  "...CoreProfileFragment } timestamp { __typename isoString } }\nfragment "
                  "FriendsFeedItemAlbumUpdatedDetails on FriendsFeedItemAlbumUpdatedV1 { __typename id title mediaIds "
                  "totalCount }\nfragment FriendsFeedItemBioUpdatedDetails on FriendsFeedItemBioUpdatedV1 { "
                  "__typename bio }\nfragment FriendsFeedItemEmojisUpdatedDetails on FriendsFeedItemEmojisUpdatedV1 { "
                  "__typename emojis }\nfragment FriendsFeedItemFriendSuggestionsDetails on "
                  "FriendsFeedItemFriendSuggestionsV1 { __typename suggestions { __typename "
                  "...FriendSuggestionDetails } }\nfragment FriendSuggestionDetails on FriendSuggestion { __typename "
                  "profile { __typename ...ViewProfileSummaryFragment invitedBy(last: 3) { __typename edges { "
                  "__typename cursor node { __typename ...CoreProfileFragment } } } } reason }\nfragment "
                  "ViewProfileSummaryFragment on Profile { __typename ...CoreProfileFragment "
                  "...ViewProfileSelectsFragment ...ViewProfileMusicFragment bio emojis { __typename emojis } kudos { "
                  "__typename emoji totalCount lastSentAt { __typename isoString } } tags { __typename type text } "
                  "}\nfragment CoreProfileFragment on Profile { __typename id displayName profilePhotoName username "
                  "friendStatus isBlocked blockedMe hashedPhoneNumber joinedAt { __typename isoString } }\nfragment "
                  "ViewProfileSelectsFragment on Profile { __typename selectsVideo { __typename "
                  "...CoreRecapVideoFragment } }\nfragment CoreRecapVideoFragment on RecapVideo { __typename id "
                  "videoFilename totalDuration interval }\nfragment ViewProfileMusicFragment on Profile { __typename "
                  "music { __typename ...ProfileMusicDetails } }\nfragment ProfileMusicDetails on ProfileMusic { "
                  "__typename artist artworkUrl duration songTitle songUrl }\nfragment "
                  "FriendsFeedItemFriendRequestsDetails on FriendsFeedItemFriendRequestsV1 { __typename requests { "
                  "__typename ...FriendRequestDetails } }\nfragment FriendRequestDetails on FriendRequest { "
                  "__typename profile { __typename ...ViewProfileSummaryFragment invitedBy(last: 3) { __typename "
                  "edges { __typename cursor node { __typename ...CoreProfileFragment } } } } }\nfragment "
                  "FriendsFeedItemKudosUpdatedDetails on FriendsFeedItemKudosUpdatedV1 { __typename empty }\nfragment "
                  "FriendsFeedItemMediaFeaturedDetails on FriendsFeedItemMediaFeaturedV1 { __typename media { "
                  "__typename ...CoreMediaFragment ...MediaWithReactionsFragment } }\nfragment CoreMediaFragment on "
                  "Media { __typename id takenAt { __typename isoString } takenBy { __typename ...CoreProfileFragment "
                  "} deletedAt { __typename isoString } }\nfragment MediaWithReactionsFragment on Media { __typename "
                  "reactions { __typename ...MediaReactionDetails } }\nfragment MediaReactionDetails on MediaReaction "
                  "{ __typename emoji hasReacted count }\nfragment FriendsFeedItemMediaSharedDetails on "
                  "FriendsFeedItemMediaSharedV1 { __typename entries { __typename "
                  "...FriendsFeedItemMediaSharedEntryDetails } }\nfragment FriendsFeedItemMediaSharedEntryDetails on "
                  "FriendsFeedItemMediaSharedEntryV1 { __typename id seen media { __typename "
                  "...FullMediaPreviewFragment } }\nfragment FullMediaPreviewFragment on Media { __typename "
                  "...CoreMediaFragment ...MediaWithMetadataFragment ...MediaWithCommentsPreviewFragment "
                  "...MediaWithReactionsFragment ...MediaWithTagsPreviewFragment }\nfragment "
                  "MediaWithMetadataFragment on Media { __typename developsAt { __typename isoString } timezone "
                  "content { __typename filtered original } submittedToTeam featured faceFrames { __typename xPos "
                  "yPos width height } }\nfragment MediaWithCommentsPreviewFragment on Media { __typename "
                  "commentsCount comments(first: 3) { __typename edges { __typename cursor node { __typename "
                  "...MediaCommentDetails } } } }\nfragment MediaCommentDetails on MediaComment { __typename id "
                  "author { __typename ...CoreProfileFragment } media { __typename id } createdAt { __typename "
                  "isoString } deletedAt { __typename isoString } text isLiked likeCount }\nfragment "
                  "MediaWithTagsPreviewFragment on Media { __typename tags(first: 3) { __typename edges { __typename "
                  "cursor node { __typename ...MediaTagDetails } } totalCount } }\nfragment MediaTagDetails on "
                  "MediaTag { __typename frame { __typename position { __typename xPos yPos } size { __typename width "
                  "height } } taggedAt { __typename isoString } taggedBy { __typename id } ... on MediaContactTag { "
                  "hashedPhoneNumber } ... on MediaProfileTag { profile { __typename id displayName username "
                  "profilePhotoName friendStatus } shared } }\nfragment FriendsFeedItemMusicUpdatedDetails on "
                  "FriendsFeedItemMusicUpdatedV1 { __typename artist artworkUrl songTitle }\nfragment "
                  "FriendsFeedItemProfileCompletedDetails on FriendsFeedItemProfileCompletedV1 { __typename photoName "
                  "selectsVideo { __typename ...CoreRecapVideoFragment } }\nfragment "
                  "FriendsFeedItemProfilePhotoUpdatedDetails on FriendsFeedItemProfilePhotoUpdatedV1 { __typename "
                  "profilePhotoName }\nfragment FriendsFeedItemSelectsUpdatedDetails on "
                  "FriendsFeedItemSelectsUpdatedV1 { __typename imageFilename selectsVideo { __typename "
                  "...CoreRecapVideoFragment } }\nfragment FriendsFeedItemStatusUpdatedDetails on "
                  "FriendsFeedItemStatusUpdatedV1 { __typename body { __typename text } }\nfragment "
                  "FriendsFeedItemTaggedMediaSharedDetails on FriendsFeedItemTaggedMediaSharedV2 { __typename "
                  "sharedMedia { __typename ...FriendsFeedItemMediaSharedDetails } }")

        self.last = last
        self.before = None

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables = {
            "before": self.before,
            "last": self.last
        }


class ProfileDetailsGQL(BaseGQL):
    def __init__(self, user_id: str, album_limit: int = 6, friends_limit: int = 10, mutual_limit: int = 3,
                 popular_limit: int = 10):
        super().__init__("ProfileDetailsGraphQLQuery", "query ProfileDetailsGraphQLQuery($id: ID!, $friendsLimit: "
                                                       "Int!, $popularLimit: Int!, $mutualLimit: Int!, "
                                                       "$albumsLimit: Int!) { profile(id: $id) { __typename "
                                                       "...ProfileDetails friends(first: $friendsLimit) { "
                                                       "__typename totalCount edges { __typename node { "
                                                       "__typename ...ProfileDetails } } } popularFriends(first: "
                                                       "$popularLimit) { __typename edges { __typename cursor "
                                                       "node { __typename ...ProfileDetails } } } mutuals(first: "
                                                       "$mutualLimit) { __typename totalCount edges { __typename "
                                                       "node { __typename ...ProfileDetails } } } monthlyRecaps { "
                                                       "__typename edges { __typename cursor node { __typename "
                                                       "...MonthlyRecapDetails } } } albums(last: $albumsLimit) { "
                                                       "__typename totalCount edges { __typename node { "
                                                       "__typename ...AlbumDetails } } } } }\nfragment "
                                                       "ProfileDetails on Profile { __typename id displayName "
                                                       "profilePhotoName username bio emojis { __typename emojis "
                                                       "} friendStatus isBlocked blockedMe hashedPhoneNumber "
                                                       "joinedAt { __typename isoString } kudos { __typename "
                                                       "emoji totalCount lastSentAt { __typename isoString } } "
                                                       "selectsVideo { __typename ...RecapVideoDetails } music { "
                                                       "__typename ...ProfileMusicDetails } tags { __typename "
                                                       "type text } }\nfragment RecapVideoDetails on RecapVideo { "
                                                       "__typename id videoFilename totalDuration interval media "
                                                       "{ __typename imageFilename } }\nfragment "
                                                       "ProfileMusicDetails on ProfileMusic { __typename artist "
                                                       "artworkUrl duration songTitle songUrl }\nfragment "
                                                       "MonthlyRecapDetails on MonthlyRecapVideo { __typename "
                                                       "isCustomOrder visibility month { __typename date } music "
                                                       "{ __typename ...ProfileMusicDetails } recapVideo { "
                                                       "__typename ...RecapVideoDetails } }\nfragment "
                                                       "AlbumDetails on Album { __typename id name visibility "
                                                       "createdAt { __typename isoString } updatedAt { __typename "
                                                       "isoString } createdBy { __typename ...ProfileDetails } "
                                                       "media(first: 3) { __typename totalCount edges { "
                                                       "__typename cursor node { __typename ...AlbumMediaDetails "
                                                       "} } } }\nfragment AlbumMediaDetails on AlbumMedia { "
                                                       "__typename addedAt { __typename isoString } media { "
                                                       "__typename id } }")
        self.user_id = user_id
        self.album_limit = album_limit
        self.friends_limit = friends_limit
        self.mutual_limit = mutual_limit
        self.popular_limit = popular_limit

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables = {
              "albumsLimit": self.album_limit,
              "friendsLimit": self.friends_limit,
              "id": self.user_id,
              "mutualLimit": self.mutual_limit,
              "popularLimit": self.popular_limit
        }


class SendKudosGQL(BaseGQL):
    def __init__(self, user_id: str):
        super().__init__("SendKudosGraphQLMutation", "mutation SendKudosGraphQLMutation($input: SendKudosInput!) "
                                                     "{ sendKudos(input: $input) { __typename success } }")

        self.user_id = user_id

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.user_id
        }


class SearchUsersGQL(BaseGQL):
    def __init__(self, term: str, first: int = 10):
        super().__init__("SearchUsersGraphQLQuery",
                         "query SearchUsersGraphQLQuery($searchTerm: String!, $first: Int, $after: String, "
                         "$last: Int, $before: String) { searchUsers( searchTerm: $searchTerm first: $first after: "
                         "$after last: $last before: $before ) { __typename edges { __typename cursor node { "
                         "__typename id displayName profilePhotoName username friendStatus blockedMe isBlocked } } "
                         "pageInfo { __typename startCursor endCursor hasNextPage hasPreviousPage } } }")

        self.first = first
        self.term = term

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables = {
            "first": self.first,
            "searchTerm": self.term
        }
