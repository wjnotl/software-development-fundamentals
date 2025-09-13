import os
import random
import string
import bcrypt

import utils.core.Global as Global
from utils.processing.ImageProcessing import (
    remove_image_from_storage,
    limit_image_size,
    save_image_to_storage,
)

from forum.data.PostData import PostData
from forum.data.LikeData import LikeData
from forum.data.ReplyData import ReplyData
from forum.data.AccountData import AccountData
from forum.data.ContentData import ContentData
from forum.entities.Account import Account


class AccountController:
    # Create
    def create_account(username, password, confirmPassword):
        """Create a new account.
        Create an account with the given username and password.
        The password must be confirmed by the user.
        :param username: Username of the account to create.
        :param password: Password of the account to create.
        :param confirmPassword: Confirm password of the account to create.
        :return: Private data of the created account on success, otherwise an error message.
        """

        username = username.strip()
        error = AccountController.__is_username_valid(username)
        if error:
            return error

        if AccountData.get_account_by_username(username):
            return "Username already exists"

        error = AccountController.__is_password_valid(password)
        if error:
            return error

        if password != confirmPassword:
            return "Confirm password does not match"

        account = Account(
            id=AccountController.__next_id(),
            username=username,
            passwordHash=AccountController.__generate_password_hash(password),
            token=AccountController.__generate_token(),
            name=username,  # set default name to username first
        )

        AccountData.add_account(account)

        error = AccountData.save()
        if error:
            return error
        return account.get_private_data()

    # Delete
    def delete_account(token):
        """Delete an account.
        Delete an account with the given token.
        :param token: Token of the account to delete.
        :return: Error message on failure, otherwise None.
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        for like in LikeData.get_likes():
            if like.get_account() == account:
                LikeData.delete(like, False)

        for content in ContentData.get_contents():
            if content.get_account() == account:
                content.set_account(None)

        AccountData.delete_account(account)

        error = LikeData.save()
        if error:
            return error

        error = PostData.save()
        if error:
            return error

        error = ReplyData.save()
        if error:
            return error

        error = AccountData.save()
        if error:
            return error

        error = remove_image_from_storage(
            os.path.join("forum", "uploads", "pfp", f"{account.get_id()}.png")
        )
        if error:
            return error

        return None

    # Edit
    def edit_profile(token, name, ctk_image, changePfp):
        """Edit profile.
        Edit the profile of the account with the given token.
        :param token: Token of the account to edit.
        :param name: Name of the account to edit.
        :param ctk_image: Image of the account to edit.
        :param changePfp: Whether to change the image of the account to edit.
        :return: Private data of the edited account on success, otherwise an error message.
        """

        account = AccountData.get_account_by_token(token)
        if not account:
            return "Account does not exist"

        name = name.strip()
        error = AccountController.__is_name_valid(name)
        if error:
            return error

        account.set_name(name)

        try:
            if changePfp:
                pfp_dir = os.path.join(Global.CURRENT_PATH, "forum", "uploads", "pfp")
                pfp_path = os.path.join(pfp_dir, f"{account.get_id()}.png")

                # remove pfp if it exists
                error = remove_image_from_storage(pfp_path)
                if error:
                    return error

                # save pfp
                if ctk_image:
                    error = limit_image_size(ctk_image, 2)
                    if error:
                        return error

                    error = save_image_to_storage(ctk_image, pfp_path)
                    if error:
                        return error

        except FileNotFoundError as e:
            return "File or directory not found: " + str(e)
        except Exception as e:
            return "Unexpected error: " + str(e)

        error = AccountData.save()
        if error:
            return error

        return account.get_private_data()

    # Authentication
    def auth_by_token(token):
        """Authenticate an account.
        Authenticate an account with the given token.
        :param token: Token of the account to authenticate.
        :return: Public data of the authenticated account on success, otherwise None.
        """

        account = AccountData.get_account_by_token(token)
        if account:
            return account.get_private_data()

        return None

    def process_login(username, password):
        """Process login.
        Process the login request from the client.
        :param username: Username of the account to log in.
        :param password: Password of the account to log in.
        :return: Private data of the logged-in account on success, otherwise an error message.
        """

        error = AccountController.__is_username_valid(username, login=True)
        if error:
            return error

        account = AccountData.get_account_by_username(username)
        if not account:
            return "Username does not exist"
        
        error = AccountController.__is_password_valid(password, login=True)
        if error:
            return error

        if not account.is_password_correct(password):
            return "Password is incorrect"

        AccountController.__regenerate_token(account)
        return account.get_private_data()

    def process_logout(token):
        """Process logout.
        Process the logout request from the client.
        :param token: Token of the account to log out.
        """

        account = AccountData.get_account_by_token(token)
        if account:
            account.set_token("")

        error = AccountData.save()
        if error:
            return error

    # Token Management
    def __generate_token():
        """Generate a token.
        Generate a token that is unique among all accounts.
        :return: A generated token.
        """
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=50))

    def __regenerate_token(account):
        """Regenerate token.
        Regenerate the token of the account.
        :param account: Account whose token will be regenerated.
        """

        token = AccountController.__generate_token()
        while AccountData.get_account_by_token(token):
            token = AccountController.__generate_token()

        account.set_token(token)
        AccountData.save()

    # Utils
    def __next_id():
        """Get next ID.
        Get the next available ID for a new account.
        :return: Next available ID.
        """
        if not AccountData.get_accounts():
            return 1

        return max(account.get_id() for account in AccountData.get_accounts()) + 1

    def __generate_password_hash(password):
        """Generate password hash.
        Generate a hashed version of the given password using bcrypt.
        :param password: Password to generate hash for.
        :return: Hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Validations
    def __is_username_valid(username, login=False):
        """Check if username is valid.
        Check if the given username meets certain criteria such as length and format.
        :param username: Username to check validity for.
        :return: Error message on failure, otherwise None.
        """

        # Rule 1: Cannot be empty
        if username == "":
            return "Username cannot be empty"
        
        # Validation for login ended
        if login:
            return None

        # Rule 2: Cannot be more than 20 characters
        if len(username) > 20:
            return "Username cannot be longer than 20 characters"

        # Rule 3: Cannot be less than 3 characters
        if len(username) < 3:
            return "Username cannot be shorter than 3 characters"

        # Rule 4: Must start with a letter
        if username[0] not in string.ascii_lowercase:
            return "Username must start with a small letter"

        # Rule 5: Can only contain letters, numbers, underscores, and periods
        allowed_chars = string.ascii_lowercase + string.digits + "._"
        for ch in username:
            if ch not in allowed_chars:
                return "Username can only contain small letters, numbers, underscores, and periods"

        # Rule 6: Cannot start or end with dot/underscore
        if username.startswith(".") or username.endswith("."):
            return "Username cannot start or end with a period"
        elif username.startswith("_") or username.endswith("_"):
            return "Username cannot start or end with an underscore"

        # Rule 7: Cannot have two consecutive dots/underscores
        for i in range(len(username) - 1):
            if username[i] in "._" and username[i + 1] in "._":
                return "Username cannot have two consecutive periods or underscores"

        return None

    def __is_password_valid(password, login=False):
        """Check if password is valid.
        Check if the given password meets certain criteria such as length and format.
        :param password: Password to check validity for.
        :return: Error message on failure, otherwise None.
        """

        # Rule 1: Cannot be empty
        strippedPassword = password.strip()
        if strippedPassword == "":
            return "Password cannot be empty"
        
        # Validation for login ended
        if login:
            return None

        # Rule 2: Cannot contain whitespaces at the beginning or end
        if password != strippedPassword:
            return "Password cannot contain whitespaces at the beginning or end"

        # Rule 3: Must contain at 8 characters
        if len(password) < 8:
            return "Password cannot be shorter than 8 characters"

        # Rule 4: Cannot be more than 20 characters
        if len(password) > 20:
            return "Password cannot be longer than 20 characters"

        # Allowed special characters
        specials = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
        allowed_chars = string.ascii_letters + string.digits + specials

        # Rule 5: Only allowed letters, digits, and special characters
        for ch in password:
            if ch not in allowed_chars:
                return "Password can only contain letters, digits, and special characters in (!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~)"

        # Track conditions
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False

        for ch in password:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
            elif ch in specials:
                has_special = True

        # Rule 6: Must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not (has_upper and has_lower and has_digit and has_special):
            return "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"

        return None

    def __is_name_valid(name):
        """Check if name is valid.
        Check if the given name meets certain criteria such as length and format.
        :param name: Name to check validity for.
        :return: Error message on failure, otherwise None.
        """

        if name == "":
            return "Name cannot be empty"

        if len(name) > 50:
            return "Name cannot be longer than 50 characters"

        return None
