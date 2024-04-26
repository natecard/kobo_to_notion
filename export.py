import sqlite3
from os import environ
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion_api_key = environ.get('NOTION_API_KEY')
notion_db_id = environ.get('NOTION_DB_ID')
notion = Client(auth=notion_api_key)

conn = sqlite3.connect('/Volumes/KOBOeReader/.kobo/KoboReader.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""select BookmarkID, VolumeID, ContentID, 
                Text, Annotation, Type, DateCreated, DateModified
                from Bookmark
                where Type IN ("highlight", "note")
                order by VolumeId, ContentId, ChapterProgress """)
rows = cursor.fetchall()

# books_added = set()

for row in rows:
    book_unformatted = row["VolumeID"]
    text = row["Text"]
    print(f"""Book: {book_unformatted}
          Text: {text}""")


page = notion.pages.create(
    parent={"database_id": notion_db_id},
    properties={
        "title": [{"text": {"Kobo Highlights and Notes"}}]
    }
)
    