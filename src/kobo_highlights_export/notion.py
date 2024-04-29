from notion_client import NotionClient

class NotionExporter:
    def __init__(self, token, db_id):
        self.notion = NotionClient(token=token)
        self.db_id = db_id
        
    def add_highlight(self, author, title, text):
        new_page = {
            "parent": {"database_id": self.db_id},
            "properties":{
                "Author": {"title": [{"text": {"content": author}}]},
                "Book Title": {"rich_text": [{"text": {"content": title}}]},
                "Text": {"rich_text": [{"text": {"content": text}}]}
        }}
        self.client.pages.create(**new_page)