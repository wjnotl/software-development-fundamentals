import os
import utils.core.Global as Global


def check_file_exists(filePath):
    if not os.path.exists(filePath):
        return False
    return True


def save_forum_account_token(token):
    try:
        with open(os.path.join(Global.CURRENT_PATH, "forum", "token.txt"), "w") as file:
            file.write(token)
    except PermissionError:
        return "Permission denied while saving the file"
    except IOError as e:
        return "IOError: " + str(e)
    return None


def load_forum_account_token():
    try:
        with open(os.path.join(Global.CURRENT_PATH, "forum", "token.txt"), "r") as file:
            return file.read()
    except PermissionError:
        return "Permission denied while loading the file"

    except IOError as e:
        return "IOError: " + str(e)
    except FileNotFoundError:
        save_forum_account_token("")  # add token.txt file if it doesn't exist

    return None
