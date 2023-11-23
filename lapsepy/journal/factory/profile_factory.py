"""
Author: Quintin Dunn
Date: 10/22/23
"""

from lapsepy.journal.factory.factory import BaseGQL


class SaveBioGQL(BaseGQL):
    def __init__(self, bio: str):
        super().__init__(
            operation_name="SaveBioGraphQLMutation",
            query="mutation SaveBioGraphQLMutation($input: SaveBioInput!) { saveBio(input: $input) "
                  "{ __typename success } }")

        self.bio = bio

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "bio": self.bio
        }


class SaveDisplayNameGQL(BaseGQL):
    def __init__(self, display_name: str):
        super().__init__(
            operation_name="SaveDisplayNameGraphQLMutation",
            query="mutation SaveDisplayNameGraphQLMutation($input: SaveDisplayNameInput!) "
                  "{ saveDisplayName(input: $input) { __typename success } }")

        self.display_name = display_name

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "displayName": self.display_name
        }


class SaveUsernameGQL(BaseGQL):
    def __init__(self, username: str):
        super().__init__(
            operation_name="SaveUsernameGraphQLMutation",
            query="mutation SaveUsernameGraphQLMutation($input: SaveUsernameInput!) "
                  "{ saveUsername(input: $input) { __typename success } }")

        self.username = username

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "username": self.username
        }


class SaveEmojisGQL(BaseGQL):
    def __init__(self, emojis: list[str]):
        super().__init__(
            operation_name="SaveEmojisGraphQLMutation",
            query="mutation SaveEmojisGraphQLMutation($input: SaveEmojisInput!) { saveEmojis(input: $input) "
                  "{ __typename success } }")

        self.emojis = emojis

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "emojis": self.emojis
        }


class SaveDOBGQL(BaseGQL):
    def __init__(self, dob: str, public: bool = True):
        super().__init__(
            operation_name="SaveDOBGraphQLMutation",
            query="mutation SaveDOBGraphQLMutation($input: SaveDateOfBirthInput!) "
                  "{ saveDateOfBirth(input: $input) { __typename success } }")

        self.dob = dob
        self.visibility = "PUBLIC" if public else "PRIVATE"

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "dob": {
                "date": self.dob
            },
            "visibility": self.visibility
        }


class CurrentUserGQL(BaseGQL):
    def __init__(self):
        super().__init__("CurrentUserGraphQLQuery",
                         "query CurrentUserGraphQLQuery { user { __typename ...UserDetails } }\nfragment UserDetails "
                         "on User { __typename profile { __typename ...ViewProfileSummaryFragment selectsVideo { "
                         "__typename media { __typename imageFilename } } } profileSettings { __typename displayName "
                         "{ __typename displayName lastUpdatedAt { __typename isoString } } username { __typename "
                         "username lastUpdatedAt { __typename isoString } } emojis { __typename emojis lastUpdatedAt "
                         "{ __typename isoString } } bio { __typename bio lastUpdatedAt { __typename isoString } } "
                         "dob { __typename dob { __typename date } visibility lastUpdatedAt { __typename isoString } "
                         "} } inviteTags { __typename message profileImageUrls mediaPreviewUrls taggedMediaCount } "
                         "onboardingState { __typename hasCompletedAddFriends hasCompletedInviteFriends "
                         "hasCompletedLockscreenWidget } invites { __typename requiresInvite "
                         "additionalInvitesRequested { __typename isoString } inviteCodes { __typename code createdAt "
                         "{ __typename isoString } sentTo { __typename sent hashedPhoneNumber sentVia } } usedCodes { "
                         "__typename code usedBy { __typename ...CoreProfileFragment } usedAt { __typename isoString "
                         "} } inviteCopy { __typename codes score } } }\nfragment ViewProfileSummaryFragment on "
                         "Profile { __typename ...CoreProfileFragment ...ViewProfileSelectsFragment "
                         "...ViewProfileMusicFragment bio emojis { __typename emojis } kudos { __typename emoji "
                         "totalCount lastSentAt { __typename isoString } } tags { __typename type text } }\nfragment "
                         "CoreProfileFragment on Profile { __typename id displayName profilePhotoName username "
                         "friendStatus isBlocked blockedMe hashedPhoneNumber joinedAt { __typename isoString } "
                         "}\nfragment ViewProfileSelectsFragment on Profile { __typename selectsVideo { __typename "
                         "...CoreRecapVideoFragment } }\nfragment CoreRecapVideoFragment on RecapVideo { __typename "
                         "id videoFilename totalDuration interval }\nfragment ViewProfileMusicFragment on Profile { "
                         "__typename music { __typename ...ProfileMusicDetails } }\nfragment ProfileMusicDetails on "
                         "ProfileMusic { __typename artist artworkUrl duration songTitle songUrl }")


class SaveMusicGQL(BaseGQL):
    def __init__(self, artist: str, artwork_url: str, duration: int, song_title: str, song_url: str):
        super().__init__("SaveMusicGraphQLMutation",
                         "mutation SaveMusicGraphQLMutation($input: SaveMusicInput) { saveMusic(input: $input) "
                         "{ __typename success } }")
        self.artist = artist
        self.artwork_url = artwork_url
        self.duration = duration
        self.song_title = song_title
        self.song_url = song_url

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "artist": self.artist,
            "artworkUrl": self.artwork_url,
            "duration": self.duration,
            "songTitle": self.song_title,
            "songUrl": self.song_url
        }


class BlockProfileGQL(BaseGQL):
    def __init__(self, user_id: str):
        super().__init__("BlockProfileGraphQLMutation",
                         "mutation BlockProfileGraphQLMutation($input: BlockProfileInput!) "
                         "{ blockProfile(input: $input) { __typename success } }")
        self.user_id = user_id

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.user_id
        }


class UnblockProfileGQL(BaseGQL):
    def __init__(self, user_id: str):
        super().__init__("UnblockProfileGraphQLMutation",
                         "mutation UnblockProfileGraphQLMutation($input: UnblockProfileInput!) "
                         "{ unblockProfile(input: $input) { __typename success } }")
        self.user_id = user_id

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.user_id
        }
