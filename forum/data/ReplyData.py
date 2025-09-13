import os
import csv

import utils.core.Global as Global

from forum.data.ContentData import ContentData
from forum.data.AccountData import AccountData
from forum.entities.Reply import Reply


class ReplyData(ContentData):
    # Storage
    def save():
        """Save all Reply object to the CSV file.
        :return: None if success, or error message string if failed.
        """

        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "forum", "storage", "replies.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for content in ContentData._contents:
                    if isinstance(content, Reply):
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
                                (
                                    content.get_parentContent().get_id()
                                    if content.get_parentContent()
                                    else ""
                                ),
                            ]
                        )
                writer.writerows(data)

        except PermissionError:
            return "Permission denied while saving the file"

        except IOError as e:
            return "IOError: " + str(e)

        return None

    def load(isParentPost):
        """Load all Reply object from the CSV file.
        :return: None if success, or error message string if failed.
        """

        errorMessage = None

        try:
            path = os.path.join(Global.CURRENT_PATH, "forum", "storage", "replies.csv")
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
                        content = ReplyData.get_content_by_id(int(row[4]))

                        if not content:
                            continue

                        # if the reply belongs to post (main comment), but the parent content is a reply, then ignore it
                        if isParentPost and isinstance(content, Reply):
                            continue

                        # if the reply belongs to reply (sub comment), but the parent content is a post, then ignore it
                        if not isParentPost and not isinstance(content, Reply):
                            continue

                        reply = Reply(
                            id=int(row[0]),
                            account=account,
                            text=row[2],
                            creationTime=int(row[3]),
                            parentContent=content,
                        )
                        ContentData.add_content(reply)
                    except:
                        errorMessage = "Some replies data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
