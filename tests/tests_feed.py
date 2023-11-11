import os
import time
import uuid

from lapsepy import Lapse

from unittest import TestCase

lapse = Lapse(os.getenv("LAPSE-TEST-REFRESH"))

test_lapse_profile = lapse.get_current_user()


thought_id = None


class TestFeeds(TestCase):
    def test_create_thought_generic(self):
        global thought_id

        if thought_id is None:
            thought_id = f"STATUS_UPDATE:{uuid.uuid4()}"
            lapse.create_status_update("This is my generic test for thoughts.", msg_id=thought_id)

    def test_create_thought_long(self):
        lapse.create_status_update("This is a test for long thoughts, thoughts on Lapse are not supposed to be able to "
                                   "to pass 90 characters, however through sending them directly from the API this can"
                                   "be avoided as of 11/8/2023, not that you care, I just needed something to write for"
                                   "this test...")

    def test_delete_thought(self):
        msg_id = f"STATUS_UPDATE:{uuid.uuid4()}"
        lapse.create_status_update("This is a thought that will be deleted.", msg_id=msg_id)
        time.sleep(5)  # Let the status update reach Lapse servers.
        lapse.remove_status_update(msg_id=msg_id)

    def test_react_thought_generic(self):
        global thought_id

        if thought_id is None:
            thought_id = f"STATUS_UPDATE:{uuid.uuid4()}"
            lapse.create_status_update("This is my generic test for thoughts.", msg_id=thought_id)

        lapse.add_reaction(thought_id, "😀")

    def test_react_thought_multiple(self):
        global thought_id

        if thought_id is None:
            thought_id = f"STATUS_UPDATE:{uuid.uuid4()}"
            lapse.create_status_update("This is my generic test for thoughts.", msg_id=thought_id)

        for _ in range(5):
            lapse.add_reaction(thought_id, "😄")

    def test_react_thought_text(self):
        global thought_id

        if thought_id is None:
            thought_id = f"STATUS_UPDATE:{uuid.uuid4()}"
            lapse.create_status_update("This is my generic test for thoughts.", msg_id=thought_id)

        lapse.add_reaction(thought_id, "does this work?")

    def test_remove_reaction(self):
        global thought_id

        if thought_id is None:
            thought_id = f"STATUS_UPDATE:{uuid.uuid4()}"
            lapse.create_status_update("This is my generic test for thoughts.", msg_id=thought_id)

        lapse.add_reaction(thought_id, "😆")
        time.sleep(2.5)  # Give reaction time for Lapse server to receive reaction
        lapse.remove_reaction(thought_id, "😆")
