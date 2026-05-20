"""Optional email and webhook notifications for Week 8 pipelines."""

from __future__ import annotations

import json
import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any
from urllib import request

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


def format_summary(summary: dict[str, Any]) -> str:
    """Build a short human-readable KPI summary."""
    lines = []
    if "total_revenue" in summary:
        lines.append(f"Kogutulu: {float(summary['total_revenue']):.2f} EUR")
    if "orders" in summary:
        lines.append(f"Tellimused: {summary['orders']}")
    if "unique_customers" in summary:
        lines.append(f"Unikaalsed kliendid: {summary['unique_customers']}")
    if "avg_order_value" in summary:
        lines.append(f"Keskmine tellimus: {float(summary['avg_order_value']):.2f} EUR")
    if "rfm_segments" in summary:
        lines.append(f"RFM segmente: {summary['rfm_segments']}")
    if "top_city" in summary:
        lines.append(f"Suurim linn: {summary['top_city']}")
    if "best_month" in summary:
        lines.append(f"Parim kuu: {summary['best_month']}")
    return "\n".join(lines) if lines else "Kokkuvõtvad numbrid puuduvad."


def build_message(
    status: str,
    summary: dict[str, Any],
    pipeline_name: str,
    elapsed_seconds: float | None = None,
    output_dir: str | None = None,
) -> str:
    """Create the notification body."""
    status_label = "õnnestus" if status.upper() == "SUCCESS" else "ebaõnnestus"
    lines = [f"{pipeline_name} {status_label}."]
    if elapsed_seconds is not None:
        lines.append(f"Kestus: {elapsed_seconds:.1f} sekundit")
    if output_dir:
        lines.append(f"Väljundid: {output_dir}")
    lines.append("")
    lines.append(format_summary(summary))
    return "\n".join(lines)


def send_webhook(message: str) -> bool:
    """Send a simple JSON text notification to Google Chat or another webhook."""
    webhook_url = os.getenv("NOTIFY_WEBHOOK_URL") or os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        return False

    payload = json.dumps({"text": message}).encode("utf-8")
    webhook_request = request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with request.urlopen(webhook_request, timeout=15) as response:
        logger.info("[NOTIFY] Webhook vastus: HTTP %s", response.status)
    return True


def send_email(subject: str, message: str) -> bool:
    """Send an email notification when SMTP settings are present."""
    host = os.getenv("SMTP_HOST")
    to_addresses = [item.strip() for item in os.getenv("NOTIFY_EMAIL_TO", "").split(",") if item.strip()]
    if not host or not to_addresses:
        return False

    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    from_address = os.getenv("SMTP_FROM") or username
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() != "false"

    if not from_address:
        logger.warning("[NOTIFY] SMTP_FROM või SMTP_USER puudub, emaili ei saadetud.")
        return False

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = from_address
    email["To"] = ", ".join(to_addresses)
    email.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=15) as smtp:
        if use_tls:
            smtp.starttls(context=context)
        if username and password:
            smtp.login(username, password)
        smtp.send_message(email)
    logger.info("[NOTIFY] Email saadetud: %s", ", ".join(to_addresses))
    return True


def send_pipeline_notification(
    status: str,
    summary: dict[str, Any],
    pipeline_name: str,
    elapsed_seconds: float | None = None,
    output_dir: str | None = None,
) -> None:
    """Send configured notifications and always keep the pipeline running."""
    load_dotenv()
    message = build_message(status, summary, pipeline_name, elapsed_seconds, output_dir)
    sent_any = False

    try:
        sent_any = send_webhook(message) or sent_any
    except Exception as exc:
        logger.warning("[NOTIFY] Webhooki saatmine ebaõnnestus: %s", exc)

    try:
        subject = f"{pipeline_name}: {status.upper()}"
        sent_any = send_email(subject, message) or sent_any
    except Exception as exc:
        logger.warning("[NOTIFY] Emaili saatmine ebaõnnestus: %s", exc)

    if not sent_any:
        logger.info("[NOTIFY] Teavituskanalit pole seadistatud; kokkuvõte:\n%s", message)
