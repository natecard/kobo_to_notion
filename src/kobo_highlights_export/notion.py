from notion_client import Client
import utils


class NotionExporter:
    def __init__(self, token, db_id):
        self.notion = Client(auth=token)
        self.db_id = db_id

    def book_exists(self, title):
        query_response = self.notion.blocks.children.list(
            block_id=self.db_id, page_size=100
        )
        for result in query_response["results"]:
            if (
                result["type"] == "child_database"
                and "title" in result["child_database"]
            ):
                child_title = result["child_database"]["title"]
                if child_title == title:
                    return result["id"]
        return False

    def highlight_exists(self, book_db_id, date_created, book_progress):
        # formatted_book_db_id = utils.format_db_id(book_db_id)
        try:
            query_response = self.notion.databases.query(
                database_id=book_db_id,
                filter={
                    "and": [
                        {"property": "Date Created", "date": {"equals": date_created}},
                        {
                            "or"[
                                {
                                    "property": "Book Progress",
                                    "number": {"equals": book_progress},
                                }
                            ]
                        },
                    ]
                },
            )
            print(query_response)
        except Exception as e:
            print(f"Error retrieving page properties: {e}")
            return None

    def create_book_database(self, title, author):
        formatted_title = utils.format_db_title(title, author)
        existing_id = self.book_exists(formatted_title)
        if existing_id:
            print(
                f"'{title} by {author}' already exists. Using existing database entry."
            )
            return existing_id

        else:
            new_database = {
                "parent": {"page_id": self.db_id},
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"{title} by {author}",
                        },
                    }
                ],
                "properties": {
                    "Text": {"title": {}},
                    "Book Progress": {"number": {}},
                    "Date Created": {"date": {}},
                },
            }
            try:
                print(
                    f"'{title} by {author}' is not in the database. Creating a database entry."
                )
                response = self.notion.databases.create(**new_database)
                return response["id"]
            except Exception as e:
                print(f"Error creating database: {e}")
                return None

    def add_highlight(self, book_db_id, text, book_progress, date_created):
        self.highlight_exists(book_db_id, date_created, book_progress)
        # print(existing_highlight)
        # if existing_highlight:
        #     print("Highlight already exists.")
        #     return

        # new_page = {
        #     "parent": {"database_id": book_db_id},
        #     "properties": {
        #         "Text": {"title": [{"text": {"content": text}}]},
        #         "Book Progress": {"number": book_progress},
        #         "Date Created": {"date": {"start": date_created}},
        #     },
        # }
        # self.notion.pages.create(**new_page)
