from notion_client import Client


class NotionExporter:
    def __init__(self, token, db_id):
        self.notion = Client(auth=token)
        self.db_id = db_id

    def book_exists(self, title):
        query_response = self.notion.search(
            {
                "query": title,
                "filter": {"value": {"type": "page_id", "page_id": self.db_id}},
            }
        )
        print(query_response)

    def create_book_database(self, title, author):
        existing_id = self.book_exists(title)
        if existing_id:
            print(
                f"Book '{title} by {author}' already exists. Using existing database entry."
            )
            return existing_id

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
            response = self.notion.databases.create(**new_database)
            return response["id"]
        except Exception as e:
            print(f"Error creating database: {e}")
            return None

    def add_highlight(self, book_db_id, text, book_progress, date_created):
        new_page = {
            "parent": {"database_id": book_db_id},
            "properties": {
                "Text": {"title": [{"text": {"content": text}}]},
                "Book Progress": {"number": book_progress},
                "Date Created": {"date": {"start": date_created}},
            },
        }
        self.notion.pages.create(**new_page)
