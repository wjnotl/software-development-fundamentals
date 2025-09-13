import os
import csv

import utils.core.Global as Global

from forum.data.AccountData import AccountData
from forum.data.ContentData import ContentData
from forum.entities.Like import Like


class LikeData:
    __likes = []

    # Getter
    def get_likes():
        return tuple(LikeData.__likes)

    def get_like_count(content):
        """Count how many likes a content has.
        :param content: The Content object to check.
        :return: Number of likes for the given content.
        """

        count = 0

        for like in LikeData.__likes:
            if like.get_content() == content:
                count += 1

        return count

    def get_like_by_account_and_content(account, content):
        """Check whether account have liked a content.
        :param account: The Account object.
        :param content: The Content object.
        :return: The Like object if found, else None.
        """

        for like in LikeData.__likes:
            if account == like.get_account() and content == like.get_content():
                return like

        return None

    # Method
    def add_like(like):
        """Add Like object to the list.
        :param like: The Like object to add.
        """

        LikeData.__likes.append(like)

    def delete_like(like):
        """Delete Like object from the list.
        :param like: The Like object to delete.
        """

        for l in LikeData.__likes:
            if l == like:
                LikeData.__likes.remove(l)
                break

    # Create
    def create(account, content):
        """Create and save a new Like object.
        :param account: The Account object.
        :param content: The Content object.
        :return: None if success, error message string if failed.
        """

        like = Like(account, content)
        LikeData.add_like(like)

        error = LikeData.save()
        if error:
            return error

        return None

    # Delete
    def delete(like, save=True):
        """Delete a Like object and optionally persist changes.
        :param like: The Like object to delete.
        :param save: Whether to save to file after deletion.
        :return: None if success, error message string if failed.
        """

        LikeData.delete_like(like)

        if save:
            error = LikeData.save()
            if error:
                return error

        return None

    # Storage
    def save():
        """Save all likes to a CSV file.
        :return: None if success, error message string if failed.
        """

        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "forum", "storage", "likes.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for like in LikeData.__likes:
                    data.append(
                        [
                            like.get_account().get_id(),
                            like.get_content().get_id(),
                        ]
                    )
                writer.writerows(data)
        except PermissionError:
            return "Permission denied while saving the file"
        except IOError as e:
            return "IOError: " + str(e)
        return None

    def load():
        """ Load likes from the CSV file.
        :return: None if success, or an error message string.
        """

        errorMessage = None

        try:
            path = os.path.join(Global.CURRENT_PATH, "forum", "storage", "likes.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        account = AccountData.get_account_by_id(int(row[0]))
                        content = ContentData.get_content_by_id(int(row[1]))

                        if account and content:
                            like = Like(account, content)
                            LikeData.add_like(like)
                    except:
                        errorMessage = "Some likes data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
