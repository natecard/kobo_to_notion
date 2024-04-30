import os
import sqlite3
from utils import extract_author, extract_book, extract_text, round_progress


class KoboDatabase:
    def __init__(self, db_path):
        ereader_db = os.path.join(db_path, "./kobo/KoboReader.sqlite")
        self.db_path = ereader_db

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_highlights(self):
        query = """select BookmarkID, VolumeID, ContentID, 
                        Text, Annotation, Type, DateCreated, DateModified, ChapterProgress
                        from Bookmark
                        where Type IN ("highlight", "note")
                        order by VolumeId, ContentId, ChapterProgress """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        books = {}

        for row in rows:
            book_unformatted = row["VolumeID"]
            book = extract_book(book_unformatted)
            text_unformatted = row["Text"]
            text = extract_text(text_unformatted)
            author = extract_author(book_unformatted)
            date_created = row["DateCreated"]
            progress = row["ChapterProgress"]
            chapter_progress = round_progress(progress)
            if book not in books:
                books[book] = {"author": author, "highlights": []}

            highlight_detail = {
                "text": text,
                "date_created": date_created,
                "chapter_progress": chapter_progress,
            }

            books[book]["highlights"].append(highlight_detail)

        return books
