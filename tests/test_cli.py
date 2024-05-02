from click.testing import CliRunner
from src.kobo_highlights_export.cli import cli


def test_process_books_success(mocker):
    # Mock the necessary dependencies
    mocker.patch("src.kobo_highlights_export.kobo.KoboDatabase")
    mocker.patch("src.kobo_highlights_export.notion.NotionExporter")
    mocker.patch("src.kobo_highlights_export.notion_insert.NotionInsert")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["process-books"],
        input="/path/to/kobo\nfake_api_key\nfake_api_key\nfake_db_id\n",
    )

    print("Exit code:", result.exit_code)
    print("Output:", result.output)

    assert result.exit_code == 0
    assert "Successfully connected to Kobo." in result.output
    assert "Kobo database connection complete." in result.output
    assert "Notion setup complete with Database ID: fake_db_id" in result.output
    assert "Books successfully processed and added to Notion database." in result.output


def test_process_books_invalid_filepath(mocker):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["process-books"],
        input="/invalid/path\nfake_api_key\nfake_api_key\nfake_db_id\n",
    )

    assert result.exit_code == 2
    assert (
        'Invalid value for "-Filepath" / "--filepath" / "-filepath": Path "/invalid/path" does not exist.'
        in result.output
    )


def test_process_books_missing_options(mocker):
    runner = CliRunner()
    result = runner.invoke(cli, ["process-books"], input="\n\n\n")

    assert result.exit_code == 1
    assert 'Missing option "-Filepath" / "--filepath" / "-filepath".' in result.output