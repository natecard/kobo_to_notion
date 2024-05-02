import pytest
from click.testing import CliRunner
from kobo_highlights_export.cli import cli


def test_process_books():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "process-books",
            "--filepath",
            "/Volumes/KOBOeReader/",
            "--api-key",
            "fake_api_key",
            "--db-id",
            "fake_db_id",
        ],
    )

    assert result.exit_code == 0
    assert "Successfully connected to Kobo." in result.output
    assert "Books successfully processed and added to Notion database." in result.output
