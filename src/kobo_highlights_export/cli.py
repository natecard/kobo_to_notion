import click
from .kobo import KoboDatabase
from .notion import NotionExporter
from .notion_insert import NotionInsert


@click.group()
def cli():
    click.Context(command=cli, max_content_width=80)
    print(r"""
        ██╗  ██╗ ██████╗ ██████╗  ██████╗      ████████╗ ██████╗ 
        ██║ ██╔╝██╔═══██╗██╔══██╗██╔═══██╗     ╚══██╔══╝██╔═══██╗
        █████╔╝ ██║   ██║██████╔╝██║   ██║        ██║   ██║   ██║
        ██╔═██╗ ██║   ██║██╔══██╗██║   ██║        ██║   ██║   ██║
        ██║  ██╗╚██████╔╝██████╔╝╚██████╔╝        ██║   ╚██████╔╝
        ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝         ╚═╝    ╚═════╝ 
                                
            ███╗   ██╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗
            ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
            ██╔██╗ ██║██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
            ██║╚██╗██║██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
            ██║ ╚████║╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
            ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """)
    print("""                                         
Command line tool for importing Kobo e-reader highlights into a Notion database.
This tool allows you to connect your Kobo device, access the SQLite database on
your Kobo, extract the highlights, and export them to a specified Notion database. 
The highlights from each book are then saved in an individual page within the Notion
database. All you need to do is follow the instructions provided by the command line 
tool, and your highlights will be automatically imported into your Notion workspace.
""")
    pass


@cli.command()
def main():
    # Echo the values to the user to confirm the input
    filepath = click.prompt(
        """
Connect your Kobo to your computer and note the file path to the Kobo,
you can copy and paste the file path here. It should look something like

D:/KOBOeReader or /Volumes/KOBOeReader    

This path is used to access the SQLite database containing your highlights.
Enter the file path here""",
        type=click.Path(exists=True),
    )
    click.echo(f"File Path: {filepath}")
    db_id = click.prompt("""
                         Enter your Notion Database ID here,
this is a part of the URL of your Notion database.

For example this is the URL for a Notion database:
https://www.notion.so/Kobo-954e1825aae14feaa6960ea59c923v24

The Database ID would be: 954e1825aae14feaa6960ea59c923v24
If you have more than one database, ensure you are using the correct one.
You can always delete the data if it is imported into the wrong Notion database,
so don't worry too much about making a mistake.
Enter the Database ID""")
    click.echo(f"Database ID: {db_id}")
    api_key = click.prompt(
        """
Enter your Notion API key, this needs to be created in your Notion workspace.
You can find it in the Integrations section of your workspace settings. 
Once created, make sure you give the page access to the integration,
this is done through the "Connect to" drop down in the Notion page settings.

Hint: It should start with "secret_".

Note: This key is sensitive and should not be shared with others. 
When you enter the key, it will ask for it to be submitted twice for confirmation.
Enter the API key here""",
        confirmation_prompt=True,
    )
    """Retrieve database from the Bookmarks SQLite database from the Kobo."""
    kobo_db = KoboDatabase(filepath)
    kobo_db.connect()
    click.echo("Successfully connected to Kobo.")
    books = kobo_db.get_highlights()
    kobo_db.close()
    click.echo("Kobo database connection complete.")

    """Set up the Notion exporter with API key and database ID"""
    notion_exporter = NotionExporter(api_key, db_id)
    click.echo(f"Notion setup complete with Database ID: {db_id}")
    book_processor = NotionInsert(notion_exporter)
    book_processor.process_books(books)
    click.echo("Books successfully processed and added to Notion database.")
