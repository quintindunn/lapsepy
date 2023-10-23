"""
Author: Quintin Dunn
Date: 10/22/23
"""

import io

from .common.exceptions import sync_journal_exception_router

from uuid import uuid4
from datetime import datetime
from PIL import Image

import requests

from .factory import ImageUploadURLGQL, CreateMediaGQL, SendInstantsGQL, FriendsFeedItemsGQL
from .structures import Profile, Snap

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

    def refresh_authorization(self, new_token: str):
        self.base_headers['authorization'] = new_token
        logger.debug("Refreshed authorization in Journal")

    def _sync_journal_call(self, query: dict) -> dict:
        """
        Makes an API call to "https://sync-service.production.journal-api.lapse.app/graphql" with an arbitrary query.
        :param query: The query to send to the API.
        :return: dict of the HTTP response.
        """

        logger.debug(f"Making request to {self.request_url}")

        request = requests.post(self.request_url, headers=self.base_headers, json=query)
        request.raise_for_status()

        errors = request.json().get("errors", [])
        if len(errors) > 0:
            logger.error(f"Got error from request to {self.request_url} with query {query}.")
            raise sync_journal_exception_router(error=errors[0])

        return request.json()

    def image_upload_url_call(self, file_uuid: str, is_instant: bool = False) -> str:
        """
        Creates an API call to the sync-service graphql API to start the image upload process
        :param file_uuid: uuid of image to upload.
        :param is_instant: Whether the image being uploaded is for an instant
        :return: AWS URL the PUT the image on.
        """
        query = ImageUploadURLGQL(file_uuid=file_uuid, is_instant=is_instant).to_dict()
        return self._sync_journal_call(query=query).get("data").get("imageUploadURL")

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

    def upload_photo(self,
                     im: Image.Image,
                     develop_in: int,
                     file_uuid: str | None = None,
                     taken_at: datetime | None = None,
                     color_temperature: float = 6000,
                     exposure_value: float = 9,
                     flash: bool = False,
                     timezone: str = "America/New_York"
                     ) -> None:
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
            print(file_uuid)

        if im_id is None:
            # UUID in testing always started with "01HDCWT" with a total length of 26 chars.
            im_id = "01HDCWT" + str(uuid4()).upper().replace("-", "")[:19]

        upload_url = self.image_upload_url_call(file_uuid=file_uuid, is_instant=True)

        self._upload_image_to_aws(im=im, upload_url=upload_url)

        query = SendInstantsGQL(user_id=user_id, file_uuid=file_uuid, im_id=im_id, caption=caption,
                                time_limit=time_limit).to_dict()
        self._sync_journal_call(query)

    def get_friends_feed(self, count: int = 10) -> list[Profile]:
        """
        Gets your friend upload feed.
        :param count: How many collection to grab.
        :return: A list of profiles
        """

        cursor = None

        profiles = {}
        entry_ids = []

        # If it started to repeat itself.
        maxed = False
        for _ in range(1, count, 10):
            logger.debug(f"Getting friends feed starting from cursor: {cursor or 'INITIAL'}")
            query = FriendsFeedItemsGQL(cursor).to_dict()
            response = self._sync_journal_call(query)

            # Where to query the new data from
            cursor = response['data']['friendsFeedItems']['pageInfo']['endCursor']
            if cursor is None:
                logger.debug("Reached max cursor depth.")
                break

            # Trim useless data from response
            feed_data = [i['node'] for i in response['data']['friendsFeedItems']['edges']]

            # Create Profile objects which hold the media data in Profile.media
            for node in feed_data:
                username = node.get('user').get('username')
                if username in profiles.keys():
                    profile = profiles[username]
                else:
                    profile = Profile.from_dict(node.get("user"))
                    profiles[username] = profile

                for entry in node['content']['entries']:
                    eid = entry['id']
                    if eid in entry_ids:
                        logger.warn("Found duplicate of media, must've reached the end already...")
                        maxed = True
                        break
                    entry_ids.append(eid)
                    snap = Snap.from_dict(entry)
                    profile.media.append(snap)

            if maxed:
                break

        return list(profiles.values())
