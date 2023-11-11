import os
import time
import uuid

from PIL import Image

from lapsepy import Lapse

from unittest import TestCase

lapse = Lapse(os.getenv("LAPSE-TEST-REFRESH"))

test_lapse_profile = lapse.get_current_user()

example_im = Image.open("./assets/example_1.jpg")


im_uuid = None


class TestUploading(TestCase):
    def test_upload(self):
        global im_uuid

        if im_uuid is None:
            im_uuid = "01HDBZ" + str(uuid.uuid4()).upper().replace("-", "")[:20]
            lapse.upload_photo(im=example_im, develop_in=15, file_uuid=im_uuid)

    def test_darkroom_query(self):
        global im_uuid

        if im_uuid is None:
            im_uuid = "01HDBZ" + str(uuid.uuid4()).upper().replace("-", "")[:20]
            lapse.upload_photo(im=example_im, develop_in=15, file_uuid=im_uuid)
            time.sleep(2.5)  # Wait for lapse servers to process image.

        lapse.query_darkroom()

    def test_review(self):
        def generate_drm():
            drm_id = "01HDBZ" + str(uuid.uuid4()).upper().replace("-", "")[:20]
            lapse.upload_photo(im=example_im, develop_in=15, file_uuid=drm_id)
            time.sleep(2.5)  # Wait for lapse servers to process image.
            return drm_id

        [generate_drm() for _ in range(3)]

        drm = list(lapse.query_darkroom())

        drm[0].archive(lapse)
        drm[1].delete(lapse)
        drm[2].share(lapse)

    def test_upload_instant(self):
        test_lapse_profile.send_instant(ctx=lapse, im=example_im, caption="Automated test")
