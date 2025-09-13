from forum.data.LikeData import LikeData
from forum.data.ContentData import ContentData
from forum.data.AccountData import AccountData
from forum.entities.Reply import Reply


class ContentController:
    # Getter
    def get_replies(contentId, token):
        """Get all replies of a content.
        Get all replies associated with the specified content ID.
        :param contentId: The unique identifier of the content whose replies are being retrieved.
        :param token: Token used to authenticate user's access rights.
        :return: List of details about each reply, or an error message if any occurred during retrieval process.
        """

        account = AccountData.get_account_by_token(token)
        replies = []

        for reply in ContentData.get_contents():
            if (
                isinstance(reply, Reply)
                and reply.get_parentContent().get_id() == contentId
            ):
                replies.append(ContentData.get_details(account, reply))

        return replies

    # Delete
    def delete(content):
        """Delete a content from database.
        Deletes the given content object from both ContentData and LikeData databases,
        along with its associated replies (if applicable).
        :param content: Object representing the content that needs to be deleted.
        """

        # Delete likes
        for like in LikeData.get_likes():
            if like.get_content() == content:
                LikeData.delete(like, False)

        ContentData.delete_content(content)

    def _delete_associated_replies(content):
        """Recursively deletes all replies associated with the given content.
        Deletes all replies associated with the given content recursively. This method will also call itself
        on each reply it finds until no more replies can be found. It then calls the `delete` method to remove
        the original content from the system.
        :param content: The content whose replies need to be deleted.
        """

        for reply in ContentData.get_contents():
            if isinstance(reply, Reply) and reply.get_parentContent() == content:
                ContentController._delete_associated_replies(reply)

        ContentController.delete(content)

    # Method
    def toggle_like(token, contentId):
        """Toggle like status of a specific content based on provided token and content ID.
        Toggles the like status of a specific piece of content (either a post or reply) identified by its ID using the provided authentication
        token. If there already exists a like record between this particular account and said content, it gets removed;
        otherwise, one gets created instead.
        :param token: Authentication token required to identify current user making request.
        :param contentId: Unique identifier assigned to targetted post which requires toggling its liked state.
        :return: Details regarding updated state after successful operation; Error message upon failure.
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        content = ContentData.get_content_by_id(contentId)
        if not content:
            return "Content does not exist"

        like = LikeData.get_like_by_account_and_content(account, content)
        if like:
            error = LikeData.delete(like)
            if error:
                return error
        else:
            error = LikeData.create(account, content)
            if error:
                return error

        return ContentData.get_details(account, content)

    # Validation
    def is_text_valid(text):
        """Check whether input string meets certain criteria.
        Checks if the provided text adheres to predefined constraints such as maximum length limit.
        :param text: Input value to validate against established rules.
        :return: Error message on failure; otherwise None.
        """

        if not text:
            return "Content cannot be empty"

        try:
            if len(text) > 1000:
                raise ValueError("Content cannot be longer than 1000 characters")
        except ValueError as e:
            return str(e)
        return None

    # Utils
    def _next_id():
        """Get next ID.
        Get the next available ID for new content.
        :return: Next available ID.
        """

        if not ContentData.get_contents():
            return 1

        return max(content.get_id() for content in ContentData.get_contents()) + 1
