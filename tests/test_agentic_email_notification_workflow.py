from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/weekly-agentic-email-notification.yml"
PROTOCOL = ROOT / "docs/agentic-intelligence/email-notification-protocol.md"
WEEKLY_LOOP = ROOT / "docs/agentic-intelligence/weekly-agentic-compatibility-loop.md"


def test_weekly_agentic_email_notification_workflow_exists_and_triggers() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "0 1 * * 1" in text
    assert "workflow_dispatch" in text
    assert "push:" in text
    assert "docs/agentic-intelligence/reports/**-weekly-agentic-compatibility.md" in text


def test_weekly_agentic_email_notification_workflow_permissions_and_token() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "contents: read" in text
    assert "issues: write" in text
    assert "GH_TOKEN: ${{ github.token }}" in text
    assert "actions/checkout@v4" in text


def test_weekly_agentic_email_notification_workflow_issue_content() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Agentic 周报" in text
    assert "joy7758" in text
    assert "--assignee joy7758" in text
    assert "不自动改仓库" in text
    assert "不自动开 PR" in text
    assert "不自动发版" in text
    assert "不自动推广" in text
    assert "不制造 fake adoption" in text
    assert "不要求 star/follow/fork" in text


def test_weekly_agentic_email_notification_workflow_avoids_email_secrets() -> None:
    text = WORKFLOW.read_text(encoding="utf-8").lower()

    for banned in [
        "smtp_password",
        "email_password",
        "sendgrid",
        "mailgun",
        "twine_password",
        "pypi",
    ]:
        assert banned not in text


def test_email_notification_protocol_documents_boundaries() -> None:
    text = PROTOCOL.read_text(encoding="utf-8").lower()

    for phrase in [
        "github issue",
        "no direct smtp",
        "human decision",
        "no automatic pr",
        "no automatic release",
        "no automatic promotion",
    ]:
        assert phrase in text


def test_weekly_loop_links_email_notification_protocol() -> None:
    text = WEEKLY_LOOP.read_text(encoding="utf-8")

    assert "docs/agentic-intelligence/email-notification-protocol.md" in text
    assert "auto-generate reports" in text
