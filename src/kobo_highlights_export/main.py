from kobo_highlights_export.kobo import KoboDatabase
from kobo_highlights_export.utils import Utils
from os import environ
from dotenv import load_dotenv
from notion_client import Client

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


if __name__ == "__main__":
    main()