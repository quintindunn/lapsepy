import random
import uuid

IOS_VERSIONS = ["16", "16.0.1", "16.0.2", "16.0.3", "16.1", "16.1.1", "16.1.2", "16.2", "16.3", "16.3.1", "16.4",
                "16.4.1", "16.5", "16.5.1", "16.6", "16.6.1", "16.7", "16.7.1", "16.7.2"]

# Devices CREDIT: https://gist.github.com/adamawolf/3048717
DEVICES = ["iPhone10,4", "iPhone10,5", "iPhone10,6", "iPhone11,2", "iPhone11,4", "iPhone11,6", "iPhone11,8",
           "iPhone12,1", "iPhone12,3", "iPhone12,5", "iPhone12,8", "iPhone13,1", "iPhone13,2", "iPhone13,3",
           "iPhone13,4", "iPhone14,2", "iPhone14,3", "iPhone14,4", "iPhone14,5", "iPhone14,6", "iPhone14,7",
           "iPhone14,8", "iPhone15,2", "iPhone15,3", "iPhone15,4", "iPhone15,5", "iPhone16,1", "iPhone16,2"]


class BaseOptions:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, f"HEADER_{k}", v)

        if not hasattr(self, "HEADER_x_device_id"):
            self.HEADER_x_device_id = self.generate_device_id()

    @staticmethod
    def generate_device_id():
        return str(uuid.uuid4())

    @staticmethod
    def format_header(key):
        # Remove 'HEADER_' prefix.
        key = key[len("HEADER_"):]

        # remove underscores, replace with dashes.
        key = key.replace("_", "-")

        # replace dunder dashes with underscores incase there's some weird headers.
        key = key.replace("--", "_")

        return key

    def to_headers(self, operation_name: str, authorization_token: str):
        attrs = list(filter(lambda x: x.startswith("HEADER_"), dir(self)))
        key_value_pairs = {self.format_header(attr): str(self.__getattribute__(attr)) for attr in attrs}

        x_emb_path = f"/graphql/{operation_name}"

        rendered = {
            "x-apollo-operation-name": operation_name,
            "x-emb-path": x_emb_path,
            "authorization": authorization_token
        }

        key_value_pairs.update(rendered)

        return key_value_pairs


class Options(BaseOptions):
    def __init__(self,
                 x_ios_version_number: str | None = None,
                 x_device_name: str | None = None,
                 user_agent: str | None = None,
                 x_app_version_number: str = "2.98.0",
                 x_timezone: str = "America/New_York",
                 x_device_id: str | None = None,
                 x_app_build_number: int = 21975,
                 apollographql_client_name: str = "com.lapse.journal-apollo-ios",
                 apollographql_client_version: str | None = None,
                 accept_language: str = "en-US,en;q=0.9",
                 ):
        self.x_ios_version_number = x_ios_version_number
        self.x_device_name = x_device_name
        self.user_agent = user_agent
        self.x_app_version_number = x_app_version_number
        self.x_timezone = x_timezone
        # x_apollo_operation_name (set by journal.sync_journal_call)
        self.x_device_id = x_device_id
        self.x_app_build_number = x_app_build_number
        self.apollographql_client_name = apollographql_client_name
        self.apollographql_client_version = apollographql_client_version
        # x_emb_path (set by BaseOptions.to_headers)
        # authorization (set by BaseOptions.to_headers)
        self.accept_language = accept_language
        self.accept = "*/*"
        self.content_type = "application/json"
        self.accept_encoding = "gzip, deflate, br"
        self.x_apollo_operation_type = "query"

        if self.user_agent is None:
            self.user_agent = f"Lapse/{self.x_app_version_number}/{x_app_build_number} iOS"

        if self.x_device_id is None:
            self.x_device_id = self.generate_device_id()

        if self.apollographql_client_version is None:
            self.apollographql_client_version = f"{self.x_app_version_number}-{self.x_app_build_number}"

        # x_device_name and x_ios_version_number can probably give conflicting information
        if self.x_device_name is None:
            self.x_device_name = random.choice(DEVICES)

        if self.x_ios_version_number is None:
            self.x_ios_version_number = random.choice(IOS_VERSIONS)

        super().__init__(
            x_ios_version_number=self.x_ios_version_number,
            x_device_name=self.x_device_name,
            user_agent=self.user_agent,
            x_app_version_number=self.x_app_version_number,
            x_timezone=self.x_timezone,
            x_device_id=self.x_device_id,
            x_app_build_number=self.x_app_build_number,
            apollographql_client_name=self.apollographql_client_name,
            apollographql_client_version=self.apollographql_client_version,
            accept_language=self.accept_language,
            accept=self.accept,
            content_type=self.content_type,
            accept_encoding=self.accept_encoding,
            x_apollo_operation_type=self.x_apollo_operation_type
        )


if __name__ == '__main__':
    options = Options()
    headers = options.to_headers("SendKudosGQL", "SampleToken")

    print(headers)
