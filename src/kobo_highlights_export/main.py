from kobo_highlights_export.kobo import KoboDatabase
from kobo_highlights_export.utils import Utils
from os import environ
from dotenv import load_dotenv
from notion_client import Client

from src.kobo_highlights_export.notion import NotionExporter

load_dotenv()
notion_api_key = environ.get('NOTION_API_KEY')
notion_db_id = environ.get('NOTION_DB_ID')
notion = Client(auth=notion_api_key)
if environ.get('PROD') is True:
    ereader_db = environ.get('EREADER_DB')
else:
    ereader_db = environ.get('DEV_EREADER_DB')


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