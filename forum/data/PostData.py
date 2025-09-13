import os
import csv

import utils.core.Global as Global

from forum.data.AccountData import AccountData
from forum.data.ContentData import ContentData
from forum.entities.Post import Post


class PostData(ContentData):
    # Storage
    def save():
        """Save all Post object to the CSV file.
        :return: None if success, or error message string if failed.
        """

        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "forum", "storage", "posts.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)
                data = []

                for content in ContentData._contents:
                    if isinstance(content, Post):
                        data.append(
                            [
                                content.get_id(),
                                (
                                    content.get_account().get_id()
                                    if content.get_account()
                                    else ""
                                ),
                                content.get_text(),
                                content.get_creationTime(),
                                content.get_title(),
                            ]
                        )

                writer.writerows(data)

        except PermissionError:
            return "Permission denied while saving the file"

        except IOError as e:
            return "IOError: " + str(e)

        return None

    def load():
        """Load all Post object from the CSV file.
        :return: None if success, or error message string if failed.
        """

        errorMessage = None

        try:
            path = os.path.join(Global.CURRENT_PATH, "forum", "storage", "posts.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass
            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:

                        account = (
                            AccountData.get_account_by_id(int(row[1]))
                            if row[1]
                            else None
                        )
                        post = Post(
                            id=int(row[0]),
                            account=account,
                            text=row[2],
                            creationTime=int(row[3]),
                            title=row[4],
                        )
                        ContentData.add_content(post)
                    except:
                        errorMessage = "Some posts data are corrupted"
                        continue
        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
