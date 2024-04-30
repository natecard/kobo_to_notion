import os
from dotenv import load_dotenv
from notion_client import Client

from cli import cli
from kobo import KoboDatabase
from notion import NotionExporter


load_dotenv()
notion_api_key = os.environ.get("NOTION_API_KEY")
notion_db_id = os.environ.get("NOTION_DB_ID")
notion = Client(auth=notion_api_key)
if os.environ.get("PROD") is True:
    ereader_db = os.environ.get("EREADER_DB")
else:
    db_path = os.environ.get("DEV_EREADER_DB")
    ereader_db = os.path.join(os.path.dirname(__file__), "..", "..", db_path)


def main():
    kobo_db = KoboDatabase(ereader_db)
    kobo_db.connect()
    books = kobo_db.get_highlights()
    print(books)
    kobo_db.close()

    notion = NotionExporter(notion_api_key, notion_db_id)

    for book, book_info in books.items():
        book_db_id = notion.create_book_database(book, book_info["author"])

        for highlight in book_info["highlights"]:
            notion.add_highlight(
                book_db_id,
                highlight["text"],
                highlight["chapter_progress"],
                highlight["date_created"],
            )


if __name__ == "__main__":
    cli()
