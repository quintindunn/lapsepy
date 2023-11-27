# lapsepy.journal.structures.profile.Profile
The Profile class for Lapse profiles.
<hr>

### Profile
```python3
    Profile(user_id: str, username: str, display_name: str, profile_photo_name: str, bio: str | None,
                 emojis: list[str], is_friends: bool, blocked_me: bool, kudos: int, tags: list[dict],
                 hashed_phone_number: str, is_blocked: bool = False, friends: list["Profile"] = None,
                 profile_music: "ProfileMusic" = None, albums: list["Album"] | None = None)
```
**I will be using profile and account interchangeably**
* `user_id: str` - The UUID of the profile.
* `username: str` - The username of the account.
* `display_name: str` - The display name of the account.
* `profile_photo_name: str` - The path to the profile photo (internal usage).
* `bio: str | None` - The bio of the account.
* `emojis: list[str]` - A list of strings containing the emojis of the account **Due to the way Lapse verifies data this doesn't necessarily have to be emojis.**
* `is_friends: bool` - Whether the profile is friends with your Lapse profile
* `blocked_me: bool` - Whether you're blocked by the profile.
* `kudos: int` - How many kudos (vibes) the account has.
* `tags: list[dict]` - The tags of the account, these consist of the age, star sign, etc.
* `hashed_phone_number: str` - The hashed phone number of the account.
* `is_blocked: bool = False` - Whether the account is blocked.
* `friends: list[Profile]` - List of Profile objects that the user is friends with. If none, it gets initialized with a empty list.
* `profile_music: ProfileMusic` - The profile's music as a [ProfileMusic](#) object.
* `albums: list["Album"] | None` - The albums the account has. 
