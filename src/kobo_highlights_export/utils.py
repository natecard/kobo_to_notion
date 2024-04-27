class Utils:
    @staticmethod
    def extract_author(string):
        author_parts = string.split("/")
        name = author_parts[-1]
        author_name = name.split("-")
        author = author_name[0].strip()
        return author

    @staticmethod
    def extract_book(string):
        book_parts = string.split("/")
        name = book_parts[-1]
        book_name = name.split("-")
        book_name = book_name[1].split(".")
        book = book_name[0].lstrip()
        return book

    @staticmethod
    def extract_text(string):
        text = string.strip()
        return text
