"""
Author: Quintin Dunn
Date: 10/22/23
"""
from typing import TYPE_CHECKING

from lapsepy.journal.factory.factory import BaseGQL

from datetime import datetime, timedelta

import logging

if TYPE_CHECKING:
    from lapsepy.journal.structures import ReviewMediaPartition

logger = logging.getLogger("lapsepy.journal.factory.media_factory.py")


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


class ReviewMediaGQL(BaseGQL):
    def __init__(self, archived: list["ReviewMediaPartition"], deleted: list["ReviewMediaPartition"],
                 shared: list["ReviewMediaPartition"]):
        super().__init__("ReviewMediaGraphQLMutation",
                         "mutation ReviewMediaGraphQLMutation($input: ReviewMediaInput!) "
                         "{ reviewMedia(input: $input) { __typename success } }")
        self.archived = [archive.to_dict() for archive in archived]
        self.deleted = [deleted.to_dict() for deleted in deleted]
        self.shared = [shared.to_dict() for shared in shared]

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "archivedMedia": self.archived,
            "deletedMedia": self.deleted,
            "sharedMedia": self.shared
        }


class DarkroomGQL(BaseGQL):
    def __init__(self):
        super().__init__("DarkroomGraphQLQuery", "query DarkroomGraphQLQuery { darkroom { __typename "
                                                 "...DarkroomMediaDetails } }\nfragment DarkroomMediaDetails on "
                                                 "DarkroomMedia { __typename mediaId takenAt { __typename isoString } "
                                                 "developsAt { __typename isoString } }")


class SendInstantsGQL(BaseGQL):
    def __init__(self, user_id: str, file_uuid: str, im_id: str, caption: str, time_limit: int):
        super().__init__(
            operation_name="SendInstantsGraphQLMutation",
            query="mutation SendInstantsGraphQLMutation($input: SendInstantsInput!) { sendInstants(input: $input) "
                  "{ __typename success } }"
        )

        self.user_id = user_id
        self.file_uuid = file_uuid
        self.im_id = im_id
        self.caption = caption
        self.time_limit = time_limit

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "instants": [
                {
                    "destination": {
                        "profile": {
                            "userId": self.user_id
                        }
                    },
                    "filename": f"instant/{self.file_uuid}",
                    "id": self.im_id,
                    "metadata": {
                        "caption": self.caption,
                        "frame": "ORIGINAL"
                    },
                    "timeLimit": self.time_limit

                }
            ]
        }


class ImageUploadURLGQL(BaseGQL):
    """
    Create the GraphQL Query for requesting an upload URL for the AWS server.
    """

    def __init__(self, file_uuid, is_instant: bool = False):
        """
        :param file_uuid: UUID of the file uploaded.
        :param is_instant: Whether the image uploaded is supposed to be an instant.
        """
        super().__init__(
            operation_name="ImageUploadURLGraphQLQuery",
            query="query ImageUploadURLGraphQLQuery($filename: String!) { imageUploadURL(filename: $filename) }"
        )

        self.is_instant = is_instant
        self.file_uuid = file_uuid
        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        logger.info(self.file_uuid)
        if not self.is_instant:
            self.variables["filename"] = f"{self.file_uuid}/filtered_0.heic"
        else:
            self.variables["filename"] = f"instant/{self.file_uuid}.heic"


class StatusUpdateGQL(BaseGQL):
    def __init__(self, text: str, msg_id: str):
        super().__init__("CreateStatusUpdateGraphQLMutation",
                         "mutation CreateStatusUpdateGraphQLMutation($input: CreateStatusUpdateInput!) "
                         "{ createStatusUpdate(input: $input) { __typename success } }")
        self.text = text
        self.msg_id = msg_id

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "body": {
                "text": self.text
            },
            "id": self.msg_id
        }


class RemoveFriendsFeedItemGQL(BaseGQL):
    def __init__(self, msg_id: str, iso_string: str):
        super().__init__("RemoveFriendsFeedItem",
                         "mutation RemoveFriendsFeedItem($input: RemoveFriendsFeedItemInput!) "
                         "{ removeFriendsFeedItem(input: $input) { __typename success } }")
        self.msg_id = msg_id
        self.iso_string = iso_string

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.msg_id,
            "removedAt": {
                "isoString": self.iso_string
            }
        }


class AddReactionGQL(BaseGQL):
    def __init__(self, msg_id: str, reaction: str):
        super().__init__("AddReactionGraphQLMutation",
                         "mutation AddReactionGraphQLMutation($input: AddMediaReactionInput!) "
                         "{ addMediaReaction(input: $input) { __typename success } }")
        self.msg_id = msg_id
        self.reaction = reaction

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.msg_id,
            "reaction": self.reaction
        }


class RemoveReactionGQL(BaseGQL):
    def __init__(self, msg_id: str, reaction: str):
        super().__init__("RemoveReactionGraphQLMutation",
                         "mutation RemoveReactionGraphQLMutation($input: RemoveMediaReactionInput!) "
                         "{ removeMediaReaction(input: $input) { __typename success } }")
        self.msg_id = msg_id
        self.reaction = reaction

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.msg_id,
            "reaction": self.reaction
        }


class SendCommentGQL(BaseGQL):
    def __init__(self, comment_id: str, msg_id: str, text: str):
        super().__init__("SendCommentGraphQLMutation",
                         "mutation SendCommentGraphQLMutation($input: SendMediaCommentInput!) "
                         "{ sendMediaComment(input: $input) { __typename success } }")
        self.comment_id = comment_id
        self.msg_id = msg_id
        self.text = text

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.comment_id,
            "mediaId": self.msg_id,
            "text": self.text
        }


class DeleteCommentGQL(BaseGQL):
    def __init__(self, comment_id: str, msg_id: str):
        super().__init__("DeleteCommentGraphQLMutation",
                         "mutation DeleteCommentGraphQLMutation($input: DeleteMediaCommentInput!) "
                         "{ deleteMediaComment(input: $input) { __typename success } }")
        self.comment_id = comment_id
        self.msg_id = msg_id

        self.variables = {}

        self._render_variables()

    def _render_variables(self):
        self.variables['input'] = {
            "id": self.comment_id,
            "mediaId": self.msg_id,
        }
