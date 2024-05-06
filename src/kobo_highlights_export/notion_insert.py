class NotionInsert:
    def __init__(self, notion_exporter):
        self.notion_exporter = notion_exporter
        self.db_id = notion_exporter.db_id

    def process_books(self, books):
        if not books or not isinstance(books, dict):
            print("Invalid or empty books data.")
            return

        for title, book_info in books.items():
            book_db_id = self.notion_exporter.create_book_database(
                title, book_info["author"]
            )

            for highlight in book_info["highlights"]:
                self.notion_exporter.add_highlight(
                    book_db_id,
                    highlight["text"],
                    highlight["chapter_progress"],
                    highlight["date_created"],
                )
