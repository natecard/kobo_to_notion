import click
from kobo import KoboDatabase
from notion import NotionExporter
from notion_insert import NotionInsert


@click.group()
def cli():
    """
    Command line tool for importing Kobo e-reader highlights into a Notion database.
    This tool allows you to connect your Kobo device, download highlights, and export them to a specified Notion database.
    """
    pass


click.Context(command=cli, max_content_width=1000)


@cli.command()
@click.option(
    "--filepath",
    prompt="File path to your Kobo",
    help="Connect your Kobo to your computer and note the file path to the Kobo, you can copy and paste the file path here. It should look something like D:/KOBOeReader or /Volumes/KOBOeReader. This path is used to access the SQLite database containing your highlights.",
    type=click.Path(exists=True),
)
@click.option(
    "--api-key",
    prompt="Your Notion API key",
    help="Enter your Notion API key. This key is necessary for authentication to access your Notion workspace.",
    hide_input=True,
    confirmation_prompt=True,
)
@click.option(
    "--db-id",
    prompt="Your Notion Database ID",
    help="Enter the ID of the Notion database where you want to export the highlights. Ensure that this database is set up to receive the data structure being exported.",
    confirmation_prompt=True,
)
def process_books(filepath, notion_api_key, notion_db_id):
    """Retrieve database from the Bookmarks SQLite database from the Kobo."""
    kobo_db = KoboDatabase(filepath)
    kobo_db.connect()
    click.echo("Successfully connected to Kobo.")
    books = kobo_db.get_highlights()
    kobo_db.close()
    click.echo("Kobo database connection complete.")

    """Set up the Notion exporter with API key and database ID"""
    notion_exporter = NotionExporter(notion_api_key, notion_db_id)
    click.echo(f"Notion setup complete with Database ID: {notion_db_id}")
    book_processor = NotionInsert(notion_exporter)
    book_processor.process_books(books)
    click.echo("Books successfully processed and added to Notion database.")
