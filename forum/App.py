import utils.core.Global as Global
from utils.core.PageManager import PageManager
from utils.ui.Message import ErrorMessage
from utils.processing.StorageProcessing import load_forum_account_token

from forum.data.AccountData import AccountData
from forum.data.PostData import PostData
from forum.data.ReplyData import ReplyData
from forum.data.LikeData import LikeData
from forum.pages.HomePage import HomePage
from forum.pages.LoginPage import LoginPage
from forum.controllers.AccountController import AccountController


def App(frame):
    """Main function of the student forum application."""

    # Get token
    token = load_forum_account_token()

    # Load storage data
    load_data()

    # Setup account
    if token:
        Global.forumAccount = AccountController.auth_by_token(token)

    # Setup page
    Global.pageManagers["forum"] = PageManager(frame)
    if Global.forumAccount:
        Global.pageManagers["forum"].show_page(HomePage, "")
    else:
        Global.pageManagers["forum"].show_page(LoginPage)


def load_data():
    """Load all data from storage."""

    error = AccountData.load()
    if error:
        ErrorMessage(error)

    error = PostData.load()
    if error:
        ErrorMessage(error)

    error = ReplyData.load(True)  # Load main replies
    if error:
        ErrorMessage(error)

    error = ReplyData.load(False)  # Load sub replies
    if error:
        ErrorMessage(error)

    error = LikeData.load()
    if error:
        ErrorMessage(error)
