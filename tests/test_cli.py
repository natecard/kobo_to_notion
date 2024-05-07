import pytest
from pytest_mock import mocker
from click.testing import CliRunner
from src.kobo_highlights_export.cli import cli
from src.kobo_highlights_export.kobo import KoboDatabase
from src.kobo_highlights_export.notion import NotionExporter
from src.kobo_highlights_export.notion_insert import NotionInsert
from src.kobo_highlights_export.utils import (
    extract_author,
    format_author_name,
    extract_book,
    extract_text,
    format_db_title,
    format_db_id,
    round_progress,
)
import tempfile


@pytest.fixture
def temp_filepath():
    with tempfile.NamedTemporaryFile() as temp_file:
        yield temp_file.name


def test_process_books_success(mocker, temp_filepath):
    # Mock the necessary dependencies
    mocker.patch("src.kobo_highlights_export.kobo.KoboDatabase")
    mock_notion_exporter = mocker.patch(
        "src.kobo_highlights_export.notion.NotionExporter"
    )
    mock_notion_exporter.return_value.export_highlights.return_value = {}

    mock_notion_insert = mocker.patch(
        "src.kobo_highlights_export.notion_insert.NotionInsert"
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "process-books",
            "--filepath",
            temp_filepath,
            "--api-key",
            "fake_api_key",
            "--db-id",
            "fake_db_id",
        ],
        input="fake_api_key\n",
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
