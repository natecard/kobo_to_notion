import os
from dotenv import load_dotenv
from notion_client import Client

from kobo_highlights_export.kobo import KoboDatabase
from kobo_highlights_export.utils import Utils
from kobo_highlights_export.notion import NotionExporter


load_dotenv()
notion_api_key = os.environ.get('NOTION_API_KEY')
notion_db_id = os.environ.get('NOTION_DB_ID')
notion = Client(auth=notion_api_key)
if os.environ.get('PROD') is True:
    ereader_db = os.environ.get('EREADER_DB')
else:
    db_path = os.environ.get('DEV_EREADER_DB')
    ereader_db = os.path.join(os.path.dirname(__file__), '..', '..', db_path)


def main():
    kobo_db = KoboDatabase(ereader_db)
    kobo_db.connect()
    highlights = kobo_db.get_highlights()
    kobo_db.close()
    
    for highlight in highlights:
        author = Utils.extract_author(highlight)
        book = Utils.extract_book(highlight)
        text = Utils.extract_text(highlight)
        print(author, book, text)
    notion = NotionExporter(notion_api_key, notion_db_id)
    for highlight in highlights:
        author = Utils.extract_author(highlight)
        book = Utils.extract_book(highlight)
        text = Utils.extract_text(highlight)
        notion.add_highlight(author, book, text)

if __name__ == "__main__":
    main()