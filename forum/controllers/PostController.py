import os
import time

import utils.core.Global as Global
from utils.processing.ImageProcessing import (
    limit_image_size,
    save_image_to_storage,
    remove_image_from_storage,
)

from forum.data.PostData import PostData
from forum.data.LikeData import LikeData
from forum.data.ReplyData import ReplyData
from forum.data.AccountData import AccountData
from forum.entities.Post import Post
from forum.controllers.ContentController import ContentController


class PostController(ContentController):
    # Getter
    def get_home_posts(token, keyword=""):
        """Get home posts
        Get all posts from database and sort them by creation time in descending order.
        If a keyword is provided, only posts that contain the keyword will be returned.
        :param token: Token of the user
        :param keyword: Keyword to search for
        :return: List of posts
        """
        account = AccountData.get_account_by_token(token)

        posts = []
        for post in PostData.get_contents():
            if isinstance(post, Post):
                if keyword.lower() in post.get_title().lower():
                    posts.append(PostData.get_details(account, post))

        posts.sort(key=lambda post: post["creationTime"], reverse=True)
        return posts

    def get_post_public_data(token, postId):
        """Get public data of a post
        Get public data of a post. Public data includes id, title, creation time, author username, likes count,
        replies count and whether the current user has liked the post or not.
        :param token: Token of the user
        :param postId: Id of the post
        :return: Dictionary containing public data of the post
        """

        account = AccountData.get_account_by_token(token)
        post = PostData.get_content_by_id(postId)
        if not post:
            return None

        return PostData.get_details(account, post)

    # Create
    def create(token, title, content, image):
        """Create a new post
        Create a new post with the given title, content and image.
        :param token: Token of the user
        :param title: Title of the post
        :param content: Content of the post
        :param image: Image of the post (optional)
        :return: Error message if any, otherwise None
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        title = title.strip()
        error = PostController.__is_title_valid(title)
        if error:
            return error

        content = content.strip()
        error = PostController.is_text_valid(content)
        if error:
            return error

        id = PostController._next_id()

        if image:
            error = limit_image_size(image, 10)
            if error:
                return error

            error = save_image_to_storage(
                image,
                os.path.join(Global.CURRENT_PATH, "forum", "uploads", "post", f"{id}.png"),
            )
            if error:
                return error

        post = Post(
            id=id,
            account=account,
            text=content,
            creationTime=int(time.time()),
            title=title,
        )

        PostData.add_content(post)

        error = PostData.save()
        if error:
            return error
        return None

    # Delete
    def delete(token, postId):
        """Delete a post
        Delete a post with the given id.
        :param token: Token of the user
        :param postId: Id of the post
        :return: Error message if any, otherwise None
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        post = PostData.get_content_by_id(postId)
        if not post:
            return "Post does not exist"

        if post.get_account() != account:
            return "You cannot delete this post"

        ContentController._delete_associated_replies(post)
        ContentController.delete(post)

        error = LikeData.save()
        if error:
            return error

        error = ReplyData.save()
        if error:
            return error

        error = PostData.save()
        if error:
            return error

        error = remove_image_from_storage(os.path.join("forum", "uploads", "post", f"{post.get_id()}.png"))
        if error:
            return error

        return None

    # Validation
    def __is_title_valid(title):
        """Check if the title is valid
        Check if the title is valid. A title must have at least one character and less than 50 characters.
        :param title: Title of the post
        :return: Error message if any, otherwise None
        """

        if title == "":
            return "Title cannot be empty"

        if len(title) > 50:
            return "Title cannot be longer than 50 characters"

        return None
