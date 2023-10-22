import io
import os

from .common.exceptions import sync_journal_exception_router

from uuid import uuid4
from datetime import datetime
from PIL import Image

import requests

from .factory import ImageUploadURLGQL, CreateMediaGQL


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

    def image_upload_url_call(self, file_uuid: str):
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
                     ):
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


if __name__ == '__main__':
    journal = Journal(authorization=os.getenv("TOKEN"))
    im_ = Image.open("../../examples/imgs/example_1.jpg")
    journal.upload_photo(im_, 10)
