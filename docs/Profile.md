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


### Pictures

#### Profile.load_profile_picture
Loads the accounts profile picture from Lapse's API.
```python3
    Profile.load_profile_picture(quality: int = 65, height: int | None = None)
```
* `quality: int = 65` - The quality of the image (1-100), Lapse uses 65 which should be sufficient, sometimes the server will return a 500 (internal server error). If this happens try lowering the quality..
* `height: int | None = None` - the height of the image to return, leave this to None to get the original image size. The Lapse servers will scale it down maintaining its aspect ratio.
* Returns a Pillow Image object.

#### Profile.send_instant(ctx: Lapse, im: Image, file_uuid: str | None = None, im_id: str | None = None, caption: str | None = None, time_limit: int = 10)
Sends an instant to a Lapse profile
```python3
    Profile.send_instant(ctx: "Lapse", im: Image, file_uuid: str | None = None, im_id: str | None = None, caption: str | None = None, time_limit: int = 10)
```
* `ctx: Lapse` - Your [Lapse](./Lapse.md) object, the instant will be sent from this account.
* `im: Image` - Pillow image that you want to send.
* `file_uuid: str | None = None` - The uuid of the file of the image to send, for the most part you can leave this as None, Lapsepy will automatically generate an uuid for you.
* `im_id: str | None = None` - The uuid of the actual image/message, for the most part you can leave this as None, Lapsepy will automatically generate an uuid for you.
* `caption: str | None` - The caption of the instant.
* `time_limit: int = 10` - The time limit for the image.

#### Profile.send_kudos(ctx: Lapse)
Sends kudos (a vibe) to the Profile
```python3
    Profile.send_kudos(ctx: "Lapse")
```
* `ctx: Lapse` - Your [Lapse](./Lapse.md) object, the vibe will be sent from this account.

#### Profile.block(ctx: Lapse)
Blocks the Profile
```python3
    Profile.block(ctx: "Lapse")
```
* `ctx: Lapse` - Your [Lapse](./Lapse.md) object, the Profile will be blocked from this account.

#### Profile.unblock(ctx: Lapse)
Unblocks the Profile
```python3
    Profile.unblock(ctx: "Lapse")
```
* `ctx: Lapse` - Your [Lapse](./Lapse.md) object, the Profile will be unblocked from this account.
