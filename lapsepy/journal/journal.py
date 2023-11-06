"""
Author: Quintin Dunn
Date: 10/22/23
"""

import io
import uuid

from .common.exceptions import sync_journal_exception_router, SyncJournalException

from uuid import uuid4
from datetime import datetime
from PIL import Image

import requests

from .factory.friends_factory import FriendsFeedItemsGQL, ProfileDetailsGQL, SendKudosGQL
from .factory.media_factory import ImageUploadURLGQL, CreateMediaGQL, SendInstantsGQL, StatusUpdateGQL, \
    RemoveFriendsFeedItemGQL, AddReactionGQL, RemoveReactionGQL, SendCommentGQL, DeleteCommentGQL
from lapsepy.journal.factory.profile_factory import SaveBioGQL, SaveDisplayNameGQL, SaveUsernameGQL, SaveEmojisGQL, \
    SaveDOBGQL

from .structures import Snap, Profile, ProfileMusic, FriendsFeed, FriendNode

import logging

logger = logging.getLogger("lapsepy.journal.journal.py")


def format_iso_time(dt: datetime) -> str:
    """
    Takes in a datetime object and returns a str of the iso format Lapse uses.
    :param dt: datetime object to convert.
    :return: Formatted datetime object.
    """
    return dt.isoformat()[:-3] + "Z"


class Journal:
    def __init__(self, authorization: str):
        self.request_url = "https://sync-service.production.journal-api.lapse.app/graphql"
        self.base_headers = {
            "authorization": authorization
        }

    def _sync_journal_call(self, query: dict) -> dict:
        """
        Makes an API call to "https://sync-service.production.journal-api.lapse.app/graphql" with an arbitrary query.
        :param query: The query to send to the API.
        :return: dict of the HTTP response.
        """

        logger.debug(f"Making request to {self.request_url}")

        request = requests.post(self.request_url, headers=self.base_headers, json=query)
        try:
            request.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.exceptions.HTTPError(request.text)

        errors = request.json().get("errors", [])
        if len(errors) > 0:
            logger.error(f"Got error from request to {self.request_url} with query {query}.")
            raise sync_journal_exception_router(error=errors[0])

        return request.json()

    @staticmethod
    def _upload_image_to_aws(im: Image, upload_url: str):
        """
        Uploads an image to the Lapse AWS server.
        :param im: Image to upload to server
        :param upload_url: Url to upload to
        :return:
        """
        # Save the image as a jpeg in memory, this is what will get sent to AWS.
        logger.debug("Saving image content to buffer.")
        bytes_io = io.BytesIO()
        im.save(bytes_io, format="jpeg")
        im_data = bytes_io.getvalue()

        # Send image to AWS server
        aws_headers = {
            "User-Agent": "Lapse/20651 CFNetwork/1408.0.4 Darwin/22.5.0"
        }

        logger.debug("Uploading image to AWS server.")
        aws_request = requests.put(upload_url, headers=aws_headers, data=im_data)
        aws_request.raise_for_status()

    def refresh_authorization(self, new_token: str):
        self.base_headers['authorization'] = new_token
        logger.debug("Refreshed authorization in Journal")

    def image_upload_url_call(self, file_uuid: str, is_instant: bool = False) -> str:
        """
        Creates an API call to the sync-service graphql API to start the image upload process
        :param file_uuid: uuid of image to upload.
        :param is_instant: Whether the image being uploaded is for an instant
        :return: AWS URL the PUT the image on.
        """
        query = ImageUploadURLGQL(file_uuid=file_uuid, is_instant=is_instant).to_dict()
        return self._sync_journal_call(query=query).get("data").get("imageUploadURL")

    def upload_photo(self, im: Image.Image, develop_in: int, file_uuid: str | None = None,
                     taken_at: datetime | None = None, color_temperature: float = 6000, exposure_value: float = 9,
                     flash: bool = False, timezone: str = "America/New_York") -> None:
        """
        Upload an image to your Lapse darkroom
        :param im: Pillow object of the Image.
        :param develop_in: How many seconds until the Image should develop.
        :param file_uuid: UUID of the image for backend storage, leave at None unless you know what you're doing.
        :param taken_at: Datetime object of when the image was taken, can be left None to be set automatically to now.
        :param color_temperature: Backend number of the color temperature, most likely from when Lapse applies a filter
        to the image, most likely doesn't change anything. Leaving at 6000 however could help Lapse add bot detection.
        :param exposure_value: Backend number of the exposure value, most likely from when the image is taken,
         most likely doesn't change anything. Leaving at 9 however could help Lapse add bot detection.
        :param flash: Backend boolean of if the image was taken with flash, most likely won't change anything. Leaving
        as False **could** help Lapse with bot detection, though it's a boolean so won't narrow it down for them too
        much
        :param timezone: Timezone that lapse thinks you're using.
        :return: None
        """
        if file_uuid is None:
            # UUID in testing always started with "01HDBZ" with a total length of 26 chars.
            file_uuid = "01HDBZ" + str(uuid4()).upper().replace("-", "")[:20]

        if taken_at is None:
            taken_at = datetime.utcnow()
        taken_at = format_iso_time(taken_at)

        # Get AWS upload url from Lapse API.
        logger.debug("Getting AWS url from Lapse API.")
        upload_url = self.image_upload_url_call(file_uuid=file_uuid)

        # Upload to AWS
        self._upload_image_to_aws(im=im, upload_url=upload_url)

        # Register image in darkroom
        logger.debug("Registering image in Lapse darkroom.")
        query = CreateMediaGQL(
            file_uuid=file_uuid,
            taken_at=taken_at,
            develop_in=develop_in,
            color_temperature=color_temperature,
            exposure_value=exposure_value,
            flash=flash,
            timezone=timezone,
        ).to_dict()
        self._sync_journal_call(query=query)
        logger.debug(f"Finished uploading image {file_uuid}.")

    def upload_instant(self, im: Image.Image, user_id: str, file_uuid: str | None = None, im_id: str | None = None,
                       caption: str | None = None, time_limit: int = 10):
        """
        Uploads an instant and sends it to a user
        :param im: Pillow Image object of the image.
        :param user_id: ID of user to send it to.
        :param file_uuid: UUID of the file, leave this to None unless you know what you're doing
        :param im_id: UUID of the instant, leave this to None unless you know what you're doing
        :param caption: Caption of the instant
        :param time_limit: How long they can view the instant for
        :return:
        """

        if file_uuid is None:
            # UUID in testing always started with "01HDCWT" with a total length of 26 chars.
            file_uuid = "01HDCWT" + str(uuid4()).upper().replace("-", "")[:19]

        if im_id is None:
            # UUID in testing always started with "01HDCWT" with a total length of 26 chars.
            im_id = "01HDCWT" + str(uuid4()).upper().replace("-", "")[:19]

        upload_url = self.image_upload_url_call(file_uuid=file_uuid, is_instant=True)

        self._upload_image_to_aws(im=im, upload_url=upload_url)

        query = SendInstantsGQL(user_id=user_id, file_uuid=file_uuid, im_id=im_id, caption=caption,
                                time_limit=time_limit).to_dict()
        self._sync_journal_call(query)

    def create_status_update(self, text: str, msg_id: str | None):
        """
        Creates a status update on your Journal
        :param text: Msg of the text to send
        :param msg_id: Leave None if you don't know what you're doing. FORMAT: STATUS_UPDATE:<(str(uuid.uuid4))>
        :return:
        """
        if msg_id is None:
            msg_id = f"STATUS_UPDATE:{uuid.uuid4()}"
        query = StatusUpdateGQL(text=text, msg_id=msg_id).to_dict()
        response = self._sync_journal_call(query)

        if not response.get("data", {}).get("createStatusUpdate", {}).get("success"):
            raise SyncJournalException("Error create new status.")

    def remove_status_update(self, msg_id: str, removed_at: datetime | None):
        """
        Removes a status update
        :param msg_id: ID of the status update
        :param removed_at: datetime object of when it was removed
        :return:
        """
        if removed_at is None:
            removed_at = datetime.now()
        removed_at = format_iso_time(removed_at)

        query = RemoveFriendsFeedItemGQL(msg_id=msg_id, iso_string=removed_at).to_dict()
        response = self._sync_journal_call(query)

        if not response.get("data", {}).get("removeFriendsFeedItem", {}).get("success"):
            raise SyncJournalException("Failed removing status.")

    def send_kudos(self, user_id: str):
        """
        Sends kudos (vibes) to a given user
        :param user_id: id of the user to send kudos to.
        :return:
        """
        query = SendKudosGQL(user_id=user_id).to_dict()
        response = self._sync_journal_call(query)

        if not response.get("data", {}).get("sendKudos", {}).get("success"):
            raise SyncJournalException("Error sending kudos, could you already have reached your daily limit?")

    def get_friends_feed(self, count: int = 10) -> FriendsFeed:
        """
        Gets your friend upload feed.
        :param count: How many collection to grab.
        :return: A list of profiles
        """

        # Get all the user's friends in the range.
        query = FriendsFeedItemsGQL(last=count).to_dict()
        response = self._sync_journal_call(query)

        nodes: list[dict] = [i['node'] for i in response['data']['friendsFeedItems']['edges']]

        friend_nodes = []

        for node in nodes:
            profile_data = node.get("user")
            profile = Profile.from_dict(profile_data)

            timestamp = node.get("timestamp", {}).get("isoString")

            entries = node.get("content").get("entries")

            node_entry_objs = []
            for entry in entries:
                snap = Snap.from_dict(entry)
                node_entry_objs.append(snap)
                profile.media.append(snap)

            friend_nodes.append(FriendNode(profile=profile, iso_string=timestamp, entries=node_entry_objs))

        return FriendsFeed(friend_nodes)

    def get_profile_by_id(self, user_id: str, album_limit: int = 6, friends_limit: int = 10) -> Profile:
        """
        Get a Profile object
        :param user_id: ID the user of the profile you want to query.
        :param album_limit: Max amount of albums to get.
        :param friends_limit: Max amount of friends to get.
        :return:
        """
        query = ProfileDetailsGQL(
            user_id=user_id,
            album_limit=album_limit,
            friends_limit=friends_limit,
            mutual_limit=1,
            popular_limit=1
        ).to_dict()
        response = self._sync_journal_call(query)
        pd = response.get("data", {}).get("profile", {})

        def generate_profile_object(profile_data: dict) -> Profile:
            music = profile_data.get("music")
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
                bio=profile_data.get('bio'),
                blocked_me=profile_data.get('blockedMe'),
                display_name=profile_data.get('displayName'),
                emojis=profile_data.get("emojis", {}).get("emojis"),
                is_blocked=profile_data.get("isBlocked"),
                is_friends=profile_data.get("friendStatus") == "FRIENDS",
                kudos=profile_data.get("kudos", {}).get("totalCount", -1),
                profile_photo_name=profile_data.get('profilePhotoName'),
                tags=profile_data.get("tags"),
                user_id=profile_data.get('id'),
                username=profile_data.get('username'),
                profile_music=profile_music
            )

        profile = generate_profile_object(pd)

        # Generate friend objects
        for friend in pd.get("friends", {}).get("edges"):
            friend = generate_profile_object(friend.get("node", {}))
            profile.friends.append(friend)

        return profile

    def modify_bio(self, bio: str):
        """
        Modifies your Lapse bio.
        :param bio: Lapse bio to change to.
        :return: None
        """
        query = SaveBioGQL(bio=bio).to_dict()
        response = self._sync_journal_call(query)

        logger.debug("Updated Profile Bio.")

        if not response.get('data', {}).get("saveBio", {}).get("success"):
            raise SyncJournalException("Error saving bio.")

    def modify_display_name(self, display_name: str):
        """
        Modifies your lapse display name.
        :param display_name: Lapse display name to change to.
        :return: None
        """
        query = SaveDisplayNameGQL(display_name=display_name).to_dict()
        response = self._sync_journal_call(query)

        logger.debug("Updated Display Name.")

        if not response.get('data', {}).get("saveDisplayName", {}).get("success"):
            raise SyncJournalException("Error saving display name")

    def modify_username(self, username: str):
        """
        Modifies your lapse username.
        :param username: Lapse username to change to.
        :return: None
        """
        query = SaveUsernameGQL(username=username).to_dict()
        response = self._sync_journal_call(query)

        logger.debug("Updated Username.")

        if not response.get('data', {}).get("saveUsername", {}).get("success"):
            raise SyncJournalException("Error saving username.")

    def modify_emojis(self, emojis: list[str]):
        """
        Modifies your Lapse emojis
        :param emojis: list with a max len of 5 with emojis or text.
        :return: None
        """
        query = SaveEmojisGQL(emojis=emojis).to_dict()
        response = self._sync_journal_call(query)

        logger.debug("Updated Emojis.")

        if not response.get('data', {}).get("saveEmojis", {}).get("success"):
            raise SyncJournalException("Error saving emojis.")

    def modify_dob(self, dob: str):
        """
        Modifies your Lapse date of birth
        :param dob: Date of birth (yyyy-mm-dd)
        :return: None
        """
        query = SaveDOBGQL(dob=dob).to_dict()
        response = self._sync_journal_call(query)

        logger.debug("Updated Date Of Birth.")

        if not response.get('data', {}).get("saveDateOfBirth", {}).get("success"):
            raise SyncJournalException("Error saving date of birth.")

    def add_reaction(self, msg_id: str, reaction: str):
        """
        Adds a reaction to a message
        :param msg_id: ID of msg to send reaction to.
        :param reaction: Reaction to send.
        :return:
        """
        query = AddReactionGQL(msg_id=msg_id, reaction=reaction).to_dict()
        response = self._sync_journal_call(query)

        if not response.get('data', {}).get("addMediaReaction", {}).get("success"):
            raise SyncJournalException("Error adding reaction.")

    def remove_reaction(self, msg_id: str, reaction: str):
        """
        removes a reaction from a message
        :param msg_id: ID of msg to remove reaction from.
        :param reaction: Reaction to remove.
        :return:
        """
        query = RemoveReactionGQL(msg_id=msg_id, reaction=reaction).to_dict()
        response = self._sync_journal_call(query)

        if not response.get('data', {}).get("removeMediaReaction", {}).get("success"):
            raise SyncJournalException("Error removing reaction.")

    def create_comment(self, msg_id: str, text: str, comment_id: str | None = None):
        """
        Adds a comment to a post
        :param comment_id: id of the comment, leave as None unless you know what you're doing
        :param msg_id: id of the message
        :param text: text to send in the comment
        :return:
        """
        if comment_id is None:
            comment_id = "01HEH" + str(uuid4()).upper().replace("-", "")[:20]
        query = SendCommentGQL(comment_id=comment_id, msg_id=msg_id, text=text).to_dict()
        response = self._sync_journal_call(query)

        if not response.get('data', {}).get("sendMediaComment", {}).get("success"):
            raise SyncJournalException("Error sending comment.")

    def delete_comment(self, msg_id: str, comment_id: str):
        """
        Deletes a comment from a lapsepy post
        :param msg_id: ID of the post
        :param comment_id: ID of the comment
        :return:
        """
        query = DeleteCommentGQL(msg_id=msg_id, comment_id=comment_id).to_dict()
        response = self._sync_journal_call(query)

        if not response.get('data', {}).get("deleteMediaComment", {}).get("success"):
            raise SyncJournalException("Error deleting comment.")
