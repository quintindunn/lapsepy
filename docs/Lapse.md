## lapsepy.lapse.Lapse
The Lapse class is the core class for Lapsepy, it covers all the heavylifting for using the library.
<hr>

### Lapse.Lapse
```python3
    Lapse(refresh_token: str)
```
* `refresh_token: str` - The refresh token is the key that Lapse uses for all communications with the Lapse servers. Unfortunately this is purposefully guarded by the developers (see [issue 11](https://github.com/quintindunn/lapsepy/issues/11)). Due to this you cannot directly log in to lapse. Follow the instructions [here](./GettingRefreshToken.md) to get your refresh token.

### Profile Modification:

#### Lapse.update_bio
Updates your Lapse profile's bio to the text specified.
```python3
    Lapse.update_bio(bio: str)
```
* `bio: str` - Text that you want to update your bio with, this text does conform with some rules, though there may be some you can bypass that you would otherwise run into issues with on the app.

#### Lapse.update_display_name
Updates your Lapse profile's display name to the text specified.
```python3
    Lapse.update_display_name(display_name: str)
```
* `display_name: str` - Text that you want to set your display name to, this text does have a couple rules, however you can easily exceed the character limit and other limitations on the Lapse app.

#### Lapse.update_dob
Updates your Lapse date of birth to the date specified.
```python3
    Lapse.update_dob(dob: str)
```
* `dob: str` - Date of birth you would like your profile to be set to, the format of the parameter should be `yyyy-mm-dd`, with everything zero padded when needed to conform with that format. This can bypass rules on Lapse, allowing you to make your age go into the negatives, or make you over 2000 years old.

#### Lapse.update_emojis
Updates your Lapse profile's emojis displayed around your profile picture to the emojis specified.
```python3
    Lapse.update_emojis(emojis: list[str])
```
* `emojis: list[str]` - List of emojis to set as your profile emojis. This is still restricted to 5 strings at most, however you can bypass it forcing you to only use emojis, multi-character text does in fact work.


#### Lapse.update_username
Updates your Lapse profile's username to the text specified.
```python3
    Lapse.update_username(username: str)
```
* `username: str` - The username you'd like to set for your account. It seems to conform to the same rules that are present on the app.


### Friends

#### Lapse.get_friends_feed
Gets your friends feed from Lapse.
```python3
    Lapse.get_friends_feed(count: int) -> FriendsFeed
```
* `count: int` - The amount of items to retrieve from your friends feed. An item is the same as one of the cards on the app.
* Returns a [FriendsFeed](#) object.

#### Lapse.get_profile_by_id
Gets a Lapse profile object by the user's ID.
```python3
    Lapse.get_profile_by_id(user_id: str, album_limit: int = 6, friends_limit: int = 10) -> Profile
```
* `user_id: str` - The ID of the user's profile that you would like to retrieve.
* `album_limit: int = 6` - The maximum amount of albums to retrieve from the profile. The default is `6`, the same as the Lapse app.
* `friends_limit: int = 10` - The maximum amount of friends to return. The default is `10`, the same as the Lapse app.
* Returns a [Profile](#) object.

#### Lapse.send_kudos
Sends kudos (on the app known as vibes) to a user.
```python3
    Lapse.send_kudos(user: str | Profile)
```
* `user: str | Profile` - The user to send the kudos to, you can either pass through a string containing the user's ID, or you can pass through a [Profile](#) object. There is currently no way to see how many vibes you have left, though if it fails it will send a generic [SyncJournalException](#).

#### Lapse.upload_instant
Uploads an instant and sends it to a user.
```python3
    Lapse.upload_instant(im: Image, user: str | Profile, file_uuid: str | None = None, im_id: str | None = None,
                       caption: str | None = None, time_limit: int = 10)
```
* `im: Image` - A Pillow image object of the image you would like to send as an instant.
* `user: str | Profile` - The user to send the instant to, you can either pass through a string containing the user's ID, or you can pass through a [Profile](#) object.
* `file_uuid: str | None = None` - Server-side UUID of the file you want to upload, there is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.
* `im_id: str | None = None` - Server-side UUID that represents the image, there is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.
* `caption: str | None = None` - Caption of the image to be displayed.
* `time_limit: int = 10` - Current usage unknown.

### Feed
#### Lapse.upload_photo
Uploads a photo to you Lapse darkroom.
```python3
    Lapse.upload_photo(im: Image, develop_in: int, file_uuid: str | None = None, taken_at: datetime | None = None, color_temperature: float = 6000, exposure_value: float = 9, flash: bool = False, timezone: str = "America/New_York")
```
* `im: Image` - A Pillow image object of the image you would like to upload.
* `develop_in: int` - How long in seconds until you want the image to develop, be careful with this number as once an item is in your darkroom it cannot be removed.
* `file_uuid: str | None = None` - Server-side UUID of the file you want to upload, there is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.
* `taken_at: datetime | None` - The timestamp to tell Lapse the photo was taken at, leaving this as None will make it default to the current time.
* `color_temperature: float = 6000` - The "temperature" to tell Lapse the image was taken with, usage of this is unknown, though might be for Lapse's server-side algorithms.
* `exposure_value: float = 9` - The "exposure" to tell Lapse the image was taken with, usage of this is unknown, though might be for Lapse's server-side algorithms.
* `flash: bool = False` - Whether to tell Lapse the image was taken with flash or not, usage of this is unknown, though might be for Lapse's server-side algorithms.
* `timezone: str = "America/New_York"` - The timezone to report to Lapse that the image was taken in.

#### Lapse.send_comment
Replies to media with a comment.
```python3
    Lapse.send_comment(msg_id: str, text: str, comment_id: str | None = None)
```
* `msg_id: str` - The ID of the media you want to send a comment to.
* `text: str` - The content you want to put in the comment, limitations of this are currently unknown.
* `comment_id: str | None = None` - Server-side UUID of the comment you want to send, there is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.

#### Lapse.delete_comment
Deletes a comment from media.
```python3
    Lapse.delete_comment(msg_id: str, comment_id: str)
```
* `msg_id: str` - The ID of the media that contains the comment you want to delete.
* `comment_id: str` - The ID of the comment that you want to delete, limitations of this are currently unknown.

#### Lapse.create_status_update
Creates a status update (thought).
```python3
    Lapse.create_status_update(text: str, msg_id: str | None = None)
```
* `text: str` - The text you want in the status update, you can bypass the 90 character limit using this API call.
* `msg_id: str | None = None` - The ID of the status update you want to send, there is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.

#### Lapse.remove_status_update
Removes a status update (and more than just status, though this isn't documented yet).
```python3
    Lapse.remove_status_update(msg_id: str, removed_at: datetime | None = None)
```
* `msg_id: str` - The ID of the status update you want to remove.
* `removed_at: datetime | None = None` - The time you want it to have been deleted at, this doesn't seem to be actually used on the Server. There is no real need to change this from the default of None, as when it is None it will automatically generate in the same format that is used on the Lapse app.

#### Lapse.add_reaction
Adds a reaction to media. Using this you can add the same reaction multiple times.
```python3
    Lapse.add_reaction(msg_id: str, reaction: str)
```
* `msg_id: str` - The ID of the media you want to react to.
* `reaction: str` - What you want to react to the media with, using this you can react with more than just emojis, in fact you can write whole sentences. The limitations of this are unknown.

#### Lapse.remove_reaction
Removes a reaction from media. Using this you can remove other people's reactions.
```python3
    Lapse.remove_reaction(msg_id: str, reaction: str)
```
* `msg_id: str` - The ID of the media you want to remove a reaction from.
* `reaction: str` - The content of the reaction you would like to remove.
