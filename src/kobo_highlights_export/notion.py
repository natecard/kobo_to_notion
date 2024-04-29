from notion_client import Client


class NotionExporter:
    def __init__(self, token, db_id):
        self.notion = Client(auth=token)
        self.db_id = db_id

    def create_book_database(self, title, author):
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
        response = self.notion.databases.create(**new_database)
        return response["id"]

    def add_highlight(self, book_db_id, text, book_progress, date_created):
        new_page = {
            "parent": {"database_id": book_db_id},
            "properties": {
                # "Author": {"title": [{"text": {"content": author}}]},
                # "Book Title": {"rich_text": [{"text": {"content": title}}]},
                "Text": {"title": [{"text": {"content": text}}]},
                "Book Progress": {"number": book_progress},
                "Date Created": {"date": {"start": date_created}},
            },
        }
        self.notion.pages.create(**new_page)
