import sqlite3

class KoboDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
            
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def get_highlights(self):
        query = ("""select BookmarkID, VolumeID, ContentID, 
                        Text, Annotation, Type, DateCreated, DateModified
                        from Bookmark
                        where Type IN ("highlight", "note")
                        order by VolumeId, ContentId, ChapterProgress """)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    