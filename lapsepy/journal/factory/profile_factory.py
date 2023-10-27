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
