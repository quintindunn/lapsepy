import os

from lapsepy import Lapse

from unittest import TestCase

lapse = Lapse(os.getenv("LAPSE-TEST-REFRESH"))

test_lapse_profile = lapse.get_current_user()


class TestFetching(TestCase):
    def test_current_user(self):
        lapse.get_current_user()

    def test_get_profile_by_id(self):
        user_id = test_lapse_profile.user_id

        user_profile = lapse.get_profile_by_id(user_id=user_id)

        assert user_profile.username == test_lapse_profile.username

    def test_fetch_profile_image(self):
        test_lapse_profile.load_profile_picture(quality=100, height=200)
