class NotionInsert:
    def __init__(self, notion_client):
        self.notion = notion_client

    def process_books(self, books):
        for book, book_info in books.items():
            book_db_id = self.notion.create_book_database(book, book_info["author"])

            for highlight in book_info["highlights"]:
                self.notion.add_highlight(
                    book_db_id,
                    highlight["text"],
                    highlight["chapter_progress"],
                    highlight["date_created"],
                )
