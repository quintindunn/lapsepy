import os

from lapsepy import Lapse

from unittest import TestCase

lapse = Lapse(os.getenv("LAPSE-TEST-REFRESH"))

test_lapse_profile = lapse.get_current_user()


class TestDOB(TestCase):
    def test_modify_dob_year_greater_than_current(self):
        lapse.update_dob("9999-01-01")

    def test_modify_dob_younger_than_thirteen(self):
        lapse.update_dob("2023-01-01")

    def test_modify_dob_generic(self):
        lapse.update_dob("2005-05-05")


class TestUsername(TestCase):
    def test_modify_username_generic(self):
        lapse.update_username("quintinbot")


class TestBio(TestCase):
    def test_bio_generic(self):
        lapse.update_bio("Hello, this bio is an automated test using Lapsepy (https://github.com/quintindunn/lapsepy)")


class TestDisplayName(TestCase):
    def test_display_name_generic(self):
        lapse.update_display_name("Automated DisplayName")

    def test_display_name_long(self):
        lapse.update_display_name(
            "Hello, this bio is another step in of the automated test for my project Lapsepy, more "
            "information on this project can be found on my Github profile, at "
            "https://github.com/quintindunn/lapsepy, if you have any questions feel free to reach out "
            "to me")


class TestEmojis(TestCase):
    def test_emojis_generic(self):
        lapse.update_emojis(["😀", "😃", "😄", "😁", "😆"])

    def test_emojis_n_amount(self):
        content = "😀😃😄😁😆"
        for i in range(1, 6):
            lapse.update_emojis(list(content[:i]))

    def test_emojis_text(self):
        lapse.update_emojis(["This is a test", "This is also part of the test", "This too", "And this", "Me too!"])


class TestKudos(TestCase):
    def test_kudos(self):
        uid = test_lapse_profile.user_id
        lapse.send_kudos(uid)
        lapse.send_kudos(uid)


class TestBlock(TestCase):
    def test_block_unblock(self):
        uid = test_lapse_profile.user_id
        lapse.block_profile(uid)
        lapse.unblock_profile(uid)
