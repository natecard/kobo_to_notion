from dotenv import load_dotenv
import os
from notion import NotionExporter
from notion_insert import NotionInsert
from kobo import KoboDatabase
# import utils


load_dotenv()
notion_api_key = os.environ.get("NOTION_API_KEY")
notion_db_id = os.environ.get("NOTION_DB_ID")
# notion = Client(auth=notion_api_key)
if os.environ.get("PROD") is True:
    ereader_db = os.environ.get("EREADER_DB")
else:
    db_path = os.environ.get("DEV_EREADER_DB")
    ereader_db = os.path.join(os.path.dirname(__file__), "..", "..", db_path)


def main():
    """Retrieve database from the Bookmarks SQLite database from the Kobo."""
    kobo_db = KoboDatabase(ereader_db)
    kobo_db.connect()
    books = kobo_db.get_highlights()
    kobo_db.close()

    """Set up the Notion exporter with API key and database ID"""
    notion_exporter = NotionExporter(notion_api_key, notion_db_id)
    book_processor = NotionInsert(notion_exporter)
    book_processor.process_books(books)


if __name__ == "__main__":
    main()
