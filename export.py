import sqlite3
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

def extract_author(string):
    author_parts = string.split("/")
    name = author_parts[-1]
    author_name = name.split("-")
    author = author_name[0].strip()
    return author

def extract_book(string):
    book_parts = string.split("/")
    name = book_parts[-1]
    book_name = name.split("-")
    book_name = book_name[1].split(".")
    book = book_name[0].lstrip()
    return book

def extract_text(string):
    text = string.lstrip()
    text = string.strip()
    return text

conn = sqlite3.connect(ereader_db)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""select BookmarkID, VolumeID, ContentID, 
                Text, Annotation, Type, DateCreated, DateModified
                from Bookmark
                where Type IN ("highlight", "note")
                order by VolumeId, ContentId, ChapterProgress """)
rows = cursor.fetchall()

page = notion.pages.create(
    parent={"database_id": notion_db_id},
    properties={
        "title": {
            "title": [
                {
                    "text": {
                        "content": "Notion Notes from Kobo Highlights"
                    }
                }
            ]
        }
    }
)

for row in rows:
    book_unformatted = row["VolumeID"]
    book = extract_book(book_unformatted)
    text_unformatted = row["Text"]
    text = extract_text(text_unformatted)
    author = extract_author(book_unformatted)
    # progress = row["ChapterProgress"]
    date_created = row["DateCreated"]
    
    notion.blocks.children.append(
        block_id=page["id"],
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": book}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": progress}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": author}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": date_created}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": text}}]
                }
            }
        ]
    )