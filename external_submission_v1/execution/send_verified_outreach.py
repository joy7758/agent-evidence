#!/usr/bin/env python3
"""Generate verified outreach drafts and optionally send with hard gates."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "execution"
RECIPIENTS_FILE = EXEC / "private_outreach_recipients.json"
OUTBOX = EXEC / "outbox"
LOG = EXEC / "EMAIL_SEND_LOG.md"
REQUIRED_LINE = (
    "No endorsement or integration commitment is requested; technical feedback is sufficient."
)

TEMPLATES = {
    "cursor_email.md": "Feedback request: Origin AEP v0.1 local agent execution evidence model",
    "cursor_security_audit_feedback_email.md": (
        "Technical feedback request: agent execution evidence model for audit/replay boundaries"
    ),
    "graphite_email.md": (
        "Technical feedback request: PR evidence/replay model for stacked and agent-generated PRs"
    ),
    "mcp_email.md": (
        "Technical feedback request: MCP evidence-event boundary for agent tool execution"
    ),
}

SEND_GATES = {
    "security-reports@cursor.com": (
        "AEP_REAL_VULNERABILITY_REPORT",
        "security-reports@cursor.com is reserved for real vulnerability disclosure.",
    ),
    "security@cursor.com": (
        "AEP_ALLOW_CURSOR_SECURITY_RESEARCH_EMAIL",
        "security@cursor.com requires narrow agent security/audit architecture framing.",
    ),
    "security@graphite.dev": (
        "AEP_ALLOW_GRAPHITE_SECURITY_AUDIT_EMAIL",
        "security@graphite.dev is limited to security/audit report context.",
    ),
    "security@graphite.com": (
        "AEP_ALLOW_GRAPHITE_SECURITY_AUDIT_EMAIL",
        "security@graphite.com is limited to privacy/security policy context.",
    ),
    "hi@cursor.com": (
        "AEP_ALLOW_CURSOR_SUPPORT_EMAIL",
        "hi@cursor.com is support/privacy context, not default protocol outreach.",
    ),
}


def context() -> dict[str, str]:
    return {
        "{{PUBLIC_REPO_URL}}": os.environ.get(
            "AEP_PUBLIC_REPO_URL", "https://github.com/joy7758/agent-evidence"
        ),
        "{{RELEASE_URL}}": os.environ.get("AEP_RELEASE_URL", "PENDING_PUBLIC_RELEASE"),
        "{{REVIEW_ISSUE_URL}}": os.environ.get(
            "AEP_REVIEW_ISSUE_URL", "PENDING_PUBLIC_REVIEW_ISSUE"
        ),
    }


def send_gate_reason(email: str) -> str | None:
    gate = SEND_GATES.get(email)
    if not gate:
        return None
    env_name, reason = gate
    if os.environ.get(env_name) == "YES":
        return None
    return f"{reason} Required for sending: {env_name}=YES"


def validate_recipient(item: dict[str, object], seen: set[str]) -> tuple[str, str]:
    for field in ("name", "email", "target", "template", "source"):
        if not item.get(field):
            raise SystemExit(f"missing recipient field: {field}")

    email = str(item["email"]).strip().lower()
    if email in seen:
        raise SystemExit(f"duplicate recipient email: {email}")
    seen.add(email)

    if item["source"] != "manual_verified_by_user":
        raise SystemExit(f"{email}: source must equal manual_verified_by_user")
    if email.endswith("example.invalid"):
        raise SystemExit(f"{email}: example.invalid recipient is not sendable")

    template = str(item["template"])
    if template not in TEMPLATES:
        raise SystemExit(f"{email}: unsupported template {template}")
    if email == "security@cursor.com" and template != "cursor_security_audit_feedback_email.md":
        raise SystemExit("security@cursor.com requires cursor_security_audit_feedback_email.md")
    return email, template


def render_message(item: dict[str, object], email: str, template: str) -> tuple[EmailMessage, Path]:
    body = (ROOT / "cursor_outreach" / template).read_text(encoding="utf-8")
    for key, value in context().items():
        body = body.replace(key, value)
    if REQUIRED_LINE not in body:
        body = body.rstrip() + "\n\n" + REQUIRED_LINE + "\n"

    msg = EmailMessage()
    msg["To"] = str(item["email"])
    msg["Subject"] = TEMPLATES[template]
    msg.set_content(body)
    out = OUTBOX / (email.replace("@", "_at_") + ".eml")
    out.write_text(msg.as_string(), encoding="utf-8")
    return msg, out


def main() -> int:
    if not RECIPIENTS_FILE.exists():
        print("no verified recipients file; no email sent.")
        return 0

    data = json.loads(RECIPIENTS_FILE.read_text(encoding="utf-8"))
    recipients = data.get("recipients")
    if not isinstance(recipients, list):
        raise SystemExit("recipients must be a list")
    if len(recipients) > 5:
        raise SystemExit("max 5 recipients")

    seen: set[str] = set()
    drafts: list[tuple[dict[str, object], str, EmailMessage, Path]] = []
    send_refusals: list[str] = []
    OUTBOX.mkdir(parents=True, exist_ok=True)

    for item in recipients:
        if not isinstance(item, dict):
            raise SystemExit("each recipient must be an object")
        email, template = validate_recipient(item, seen)
        msg, out = render_message(item, email, template)
        drafts.append((item, email, msg, out))
        reason = send_gate_reason(email)
        if reason:
            send_refusals.append(f"{email}: {reason}")

    print(f"drafts_generated={len(drafts)}")
    for refusal in send_refusals:
        print(f"send_refusal={refusal}")

    if os.environ.get("I_APPROVE_EMAIL_SEND") != "YES":
        print("I_APPROVE_EMAIL_SEND is not YES; no email sent.")
        return 0
    if send_refusals:
        print("restricted recipient gate failed; no email sent.")
        return 1

    sendmail = shutil.which("sendmail")
    if not sendmail:
        raise SystemExit("sendmail binary missing; no email sent")

    lines = ["# Email Send Log", ""]
    for item, email, msg, out in drafts:
        subprocess.run([sendmail, "-t", "-oi"], input=msg.as_string(), text=True, check=True)
        lines.append(f"- sent: {email} template={item['template']} draft={out}")
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"emails_sent={len(drafts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
