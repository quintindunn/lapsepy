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

from .factory import ImageUploadURLGQL, CreateMediaGQL, FriendsFeedItemsGQL


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

        request = requests.post(self.request_url, headers=self.base_headers, json=query)
        request.raise_for_status()

        errors = request.json().get("errors", [])
        if len(errors) > 0:
            raise sync_journal_exception_router(error=errors[0])

        return request.json()

    def image_upload_url_call(self, file_uuid: str) -> str:
        """
        Creates an API call to the sync-service graphql API to start the image upload process
        :param file_uuid: uuid of image to upload.
        :return: AWS URL the PUT the image on.
        """
        query = ImageUploadURLGQL(file_uuid=file_uuid).to_dict()
        return self._sync_journal_call(query=query).get("data").get("imageUploadURL")

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
        upload_url = self.image_upload_url_call(file_uuid=file_uuid)

        # Save the image as a jpeg in memory, this is what will get sent to AWS.
        bytes_io = io.BytesIO()
        im.save(bytes_io, format="jpeg")
        im_data = bytes_io.getvalue()

        # Send image to AWS server
        aws_headers = {
            "User-Agent": "Lapse/20651 CFNetwork/1408.0.4 Darwin/22.5.0"
        }
        aws_request = requests.put(upload_url, headers=aws_headers, data=im_data)
        aws_request.raise_for_status()

        # Register image in darkroom
        query = CreateMediaGQL(
            file_uuid=file_uuid,
            taken_at=taken_at,
            develop_in=develop_in,
            color_temperature=color_temperature,
            exposure_value=exposure_value,
            flash=flash,
            timezone=timezone
        ).to_dict()
        self._sync_journal_call(query=query)

    def get_friends_feed(self, count: int = 10):
        current_count = 0

        cursor = None
        while current_count <= count:
            current_count += 10
            query = FriendsFeedItemsGQL(cursor).to_dict()
            response = self._sync_journal_call(query)

            cursor = response['data']['friendsFeedItems']['pageInfo']['endCursor']

            print(response)
