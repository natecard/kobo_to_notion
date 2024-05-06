class NotionInsert:
    def __init__(self, notion_client):
        self.notion = notion_client

    def process_books(self, books):
        if not books or not isinstance(books, dict):
            print("Invalid or empty books data.")
            return

        for title, book_info in books.items():
            book_db_id = self.notion.create_book_database(title, book_info["author"])
            if not book_db_id:
                continue

            for highlight in book_info["highlights"]:
                self.notion.add_highlight(
                    book_db_id,
                    highlight["text"],
                    highlight["chapter_progress"],
                    highlight["date_created"],
                )
