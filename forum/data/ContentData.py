class ContentData:
    _contents = []

    # Getter
    def get_contents():
        return tuple(ContentData._contents)

    def get_content_by_id(id):
        """Get a content by ID.
        Find and return the content with the given ID.
        :param id: The ID of the content to find.
        :return: The content object if found, otherwise None.
        """

        for content in ContentData._contents:
            if content.get_id() == id:
                return content

        return None

    def get_details(account, content):
        """Get details of a content.
        Returns public data of the content along with like status and like count.
        :param account: The account requesting the details.
        :param content: The content object to get details from.
        :return: A dictionary containing content data, like status, and like count.
        """

        from forum.data.LikeData import LikeData

        data = content.get_public_data()
        data["isLiked"] = (
            False
            if not account
            else LikeData.get_like_by_account_and_content(account, content)
        )
        data["likesCount"] = LikeData.get_like_count(content)

        return data

    # Method
    def add_content(content):
        """Add a content.
        Appends a content object to the list of contents.
        :param content: The content object to add.
        :return: None
        """

        ContentData._contents.append(content)

    def delete_content(content):
        """Delete a content.
        Removes the given content object from the list if it exists.
        :param content: The content object to delete.
        :return: None
        """
        
        for cont in ContentData._contents:
            if cont == content:
                ContentData._contents.remove(cont)
                break
