import re


def format_author_name(input_string):
    # Check if there is a comma in the string
    if "," in input_string:
        # Split the string by comma, but do not split hyphenated parts
        parts = re.split(r",\s*(?![^\-]*\-)", input_string)
        # Reverse the parts and join them without a comma
        return " ".join(parts[::-1]).strip()
    # If no comma, return the string as is
    return input_string


def extract_author(string):
    # Split the string by "/" and get the last part
    author_parts = string.split("/")
    name = author_parts[-1]
    # Remove the book name portion of the string
    name = name.split("-")
    # Strip any whitespace or newline characters
    name = name[0].strip()
    # Swap the parts of the name if there is a comma
    # So the name returns John Doe instead of Doe, John
    author = format_author_name(name)
    return author


def extract_book(string):
    # Split the string by "/" and get the last part
    book_parts = string.split("/")
    name = book_parts[-1]
    # Remove the author portion of the string
    book_name = name.split("-")
    # Drop the file extension and strip any whitespace or newline characters
    book_name = book_name[1].split(".")
    book = book_name[0].lstrip()
    return book


def extract_text(string):
    # Strip any whitespace or newline characters
    text = string.strip()
    return text


def format_db_title(title, author):
    return f"{title} by {author}"


# Round the progress to three decimal places
def round_progress(n, decimals=3):
    n = round(n * 100, decimals)
    return n
