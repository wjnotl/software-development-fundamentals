import time

from forum.data.LikeData import LikeData
from forum.data.ReplyData import ReplyData
from forum.data.AccountData import AccountData
from forum.data.ContentData import ContentData
from forum.entities.Reply import Reply
from forum.controllers.ContentController import ContentController


class ReplyController(ContentController):
    # Create
    def create(token, text, parentContentId):
        """Create a new reply.
        Create a new reply and associate it with the specified parent content.
        :param token: The user's authentication token.
        :param text: The text of the reply.
        :param parentContentId: The ID of the parent content.
        :return: A dictionary containing the public data of the created reply or an error message.
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        parentContent = ContentData.get_content_by_id(parentContentId)
        if not parentContent:
            return "Parent content does not exist"

        error = ReplyController.is_text_valid(text)
        if error:
            return error

        if not parentContent.get_can_reply():
            return "You cannot reply to this content!"

        reply = Reply(
            ReplyController._next_id(), account, text, int(time.time()), parentContent
        )
        ReplyData.add_content(reply)

        error = ReplyData.save()
        if error:
            return error

        return ReplyData.get_details(account, reply)

    # Delete
    def delete(token, replyId):
        """Delete a reply.
        Delete a reply associated with the specified ID.
        :param token: The user's authentication token.
        :param replyId: The ID of the reply to be deleted.
        :return: Error message if any; otherwise None.
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        reply = ReplyData.get_content_by_id(replyId)
        if not reply:
            return "Reply does not exist"

        if reply.get_account() != account:
            return "You cannot delete this reply"

        ContentController._delete_associated_replies(reply)
        ContentController.delete(reply)

        error = LikeData.save()
        if error:
            return error

        error = ReplyData.save()
        if error:
            return error

        return None
