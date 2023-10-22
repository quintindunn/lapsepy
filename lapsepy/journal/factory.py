# Author: Quintin Dunn
# Date: 10/22/23

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
