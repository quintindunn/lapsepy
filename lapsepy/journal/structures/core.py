import typing

if typing.TYPE_CHECKING:
    from lapsepy.lapse import Lapse


class Media:
    pass


class ReactableMedia(Media):
    def __init__(self, media_id):
        self.id = media_id

    def add_reaction(self, ctx: "Lapse", reaction: str):
        ctx.add_reaction(msg_id=self.id, reaction=reaction)

    def add_comment(self, ctx: "Lapse", text: str, comment_id: str | None = None):
        ctx.send_comment(msg_id=self.id, text=text, comment_id=comment_id)

    def remove_reaction(self, ctx: "Lapse", reaction: str):
        ctx.remove_reaction(msg_id=self.id, reaction=reaction)
