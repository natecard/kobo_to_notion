import pytest
from click.testing import CliRunner
from src.kobo_highlights_export.cli import cli
import tempfile


@pytest.fixture
def temp_filepath():
    with tempfile.NamedTemporaryFile() as temp_file:
        yield temp_file.name


def test_main_success(mocker, temp_filepath):
    # Mock the necessary dependencies
    mocker.patch("src.kobo_highlights_export.kobo.KoboDatabase")
    mock_notion_exporter = mocker.patch(
        "src.kobo_highlights_export.notion.NotionExporter"
    )

    mock_notion_exporter.return_value.export_highlights.return_value = {}

    mocker.patch("src.kobo_highlights_export.notion_insert.NotionInsert")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["main"],
        input=f"{temp_filepath}\nfake_db_id\nfake_api_key\nfake_api_key\n",
    )

    assert result.exit_code == 0, result.output
    assert "Successfully connected to Kobo." in result.output
    assert "Kobo database connection complete." in result.output
    assert "Notion setup complete with Database ID: fake_db_id" in result.output
    assert "Books successfully processed and added to Notion database." in result.output


def test_main_invalid_filepath(mocker, temp_filepath):
    runner = CliRunner()
    # Simulate user entering an invalid path then a valid temporary file path
    result = runner.invoke(
        cli,
        ["main"],
        input=f"/bad/path/that/is/not/valid\br{temp_filepath}\nfake_db_id\nfake_api_key\nfake_api_key\n",
        timeout=5,
    )

    assert result.exit_code == 0, result.output
    assert (
        "Error: Invalid value for 'FILEPATH'" not in result.output
    )  # Check if your CLI handles this gracefully
    assert "Successfully connected to Kobo." in result.output


def test_main_missing_options(mocker, temp_filepath):
    runner = CliRunner()
    result = runner.invoke(cli, ["main"], input=f"{temp_filepath}\n\n\n\n")

    # Check for a common error when options are missing
    assert result.exit_code == 2, result.output
    assert (
        'Error: Missing option "--filepath"' in result.output
        or "Missing option" in result.output
    )
