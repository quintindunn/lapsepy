# Get started!

First, you'll have to install `LapsePy` using pip:
```
pip install rustplus
```
Next you need to obtain your refresh token, this is most likely the most challenging part of this library. How to get it is shown [here]().

To upload a photo to Lapse, you'll want to use the `Lapse.upload_photo` method.
```python3
from lapsepy.lapse import Lapse

from PIL import Image
import os

# Create a Lapse object
lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

# Load the image into a Pillow Image.
upload_im = Image.open("./example_img.jpg")

# Send the photo to your Lapse black room, setting `develop_in` to 15 will make the image develop in 15 seconds.
lapse.upload_photo(im=upload_im, develop_in=15)
```
And that's it! Using this code it will upload the image `./example_img.jpg` (You have to create this file yourself) to you Lapse black room! It will develop in 15 seconds, you can change this number but once you send it to the black room it has to wait to develop.
