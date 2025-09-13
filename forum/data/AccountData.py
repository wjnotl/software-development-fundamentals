import os
import csv

import utils.core.Global as Global

from forum.entities.Account import Account


class AccountData:
    __accounts = []

    # Getter
    def get_accounts():
        return tuple(AccountData.__accounts)

    def get_account_by_id(id):
        """Find an account by its ID.
        :param id: The account ID to search for.
        :return: The account if found, otherwise None.
        """

        for account in AccountData.get_accounts():
            if account.get_id() == id:
                return account

        return None

    def get_account_by_username(username):
        """Find an account by username.
        :param username: The username to search for.
        :return: The account if found, otherwise None.
        """

        for account in AccountData.get_accounts():
            if account.get_username() == username:
                return account

        return None

    def get_account_by_token(token):
        """Find an account by token.
        :param token: The token to search for.
        :return: The account if found, otherwise None.
        """

        for account in AccountData.get_accounts():
            if account.get_token() == token:
                return account

        return None

    # Method
    def add_account(account):
        """Add a new account to the list.
        :param account: The account object to add.
        """

        AccountData.__accounts.append(account)

    def delete_account(account):
        """Delete an account from the list.
        :param account: The account object to delete.
        """

        for acc in AccountData.__accounts:
            if acc == account:
                AccountData.__accounts.remove(acc)
                break

    # Storage
    def save():
        """Save all accounts to the CSV file.
        :return: None if success, or error message string if failed.
        """

        try:
            with open(
                os.path.join(Global.CURRENT_PATH, "forum", "storage", "accounts.csv"),
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                data = []
                for account in AccountData.__accounts:
                    data.append(
                        [
                            account.get_id(),
                            account.get_username(),
                            account.get_passwordHash(),
                            account.get_token(),
                            account.get_name(),
                        ]
                    )
                writer.writerows(data)
        except PermissionError:
            return "Permission denied while saving the file"
        except IOError as e:
            return "IOError: " + str(e)
        return None

    def load():
        """Load all accounts from the CSV file.
        :return: None if success, or error message string if failed.
        """

        errorMessage = None

        try:
            path = os.path.join(Global.CURRENT_PATH, "forum", "storage", "accounts.csv")
            if not os.path.exists(path):
                with open(path, "w", newline="") as file:
                    pass

            with open(path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        account = Account(
                            id=int(row[0]),
                            username=row[1],
                            passwordHash=row[2],
                            token=row[3],
                            name=row[4],
                        )
                        AccountData.__accounts.append(account)
                    except:
                        errorMessage = "Some accounts data are corrupted"
                        continue

        except PermissionError:
            return "Permission denied while loading the file"
        except IOError as e:
            return "IOError: " + str(e)
        return errorMessage
