import click
from kobo import KoboDatabase
from notion import NotionExporter


@click.group()
def cli():
    """Command line tool for importing Kobo e-reader highlights into a Notion database"""
    pass


@cli.command()
@click.option(
    "--filepath",
    prompt="File path to your Kobo",
    help="""Connect your Kobo to your computer and note the file path to the Kobo, you can copy and paste the file path here. It should look something like D:/KOBOeReader or /Volumes/KOBOeReader""",
)
def database_path(filepath):
    """Retrieve database from the Bookmarks SQLite database from the Kobo."""
    kobo_db = KoboDatabase(filepath)
    kobo_db.connect()
    click.echo("Successfully connected to Kobo.")
    books = kobo_db.get_highlights()
    print(books)
    kobo_db.close()
    click.echo("Kobo database connection complete.")
