"""Valikulised e-posti ja webhooki teavitused 8. nadala pipeline'idele."""

from __future__ import annotations

import json
import logging
import mimetypes
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from urllib import request

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


def format_kpi_table(summary: dict[str, Any]) -> str:
    """Render the main KPIs as a compact Markdown table."""
    rows = []
    if "total_revenue" in summary:
        rows.append(("Kogutulu", f"{float(summary['total_revenue']):.2f} EUR"))
    if "orders" in summary:
        rows.append(("Tellimused", str(summary["orders"])))
    if "unique_customers" in summary:
        rows.append(("Unikaalsed kliendid", str(summary["unique_customers"])))
    if "avg_order_value" in summary:
        rows.append(("Keskmine tellimus", f"{float(summary['avg_order_value']):.2f} EUR"))
    if "revenue_per_customer" in summary:
        rows.append(("Tulu kliendi kohta", f"{float(summary['revenue_per_customer']):.2f} EUR"))

    if not rows:
        return ""

    table = ["| KPI | Vaartus |", "| --- | --- |"]
    table.extend(f"| {label} | {value} |" for label, value in rows)
    return "\n".join(table)


def format_summary(summary: dict[str, Any]) -> str:
    """Koosta luhike ja loetav kokkuvote."""
    lines = []
    kpi_table = format_kpi_table(summary)
    if kpi_table:
        lines.append("KPI tabel:")
        lines.append(kpi_table)
    if "rfm_segments" in summary:
        lines.append(f"RFM segmente: {summary['rfm_segments']}")
    if "top_segment" in summary:
        lines.append(f"Suurim segment: {summary['top_segment']}")
    if "top_city" in summary:
        lines.append(f"Suurim linn: {summary['top_city']}")
    if "best_month" in summary:
        lines.append(f"Parim kuu: {summary['best_month']}")
    if "data_source" in summary:
        lines.append(f"Andmeallikas: {summary['data_source']}")
    return "\n".join(lines) if lines else "Kokkuvotvad numbrid puuduvad."


def build_message(
    status: str,
    summary: dict[str, Any],
    pipeline_name: str,
    elapsed_seconds: float | None = None,
    output_dir: str | None = None,
) -> str:
    """Loo teavituse sisu."""
    status_label = "onnestus" if status.upper() == "SUCCESS" else "ebaonnestus"
    lines = [f"{pipeline_name} {status_label}."]
    if elapsed_seconds is not None:
        lines.append(f"Kestus: {elapsed_seconds:.1f} sekundit")
    if output_dir:
        lines.append(f"Valjundid: {output_dir}")
    lines.append("")
    lines.append(format_summary(summary))
    return "\n".join(lines)


def send_webhook(message: str) -> bool:
    """Saada lihtne JSON-tekstiteavitus Google Chati voi teise webhooki."""
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


def send_email(subject: str, message: str, attachments: list[Path] | None = None) -> bool:
    """Saada e-posti teavitus, kui SMTP seaded on olemas."""
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
        logger.warning("[NOTIFY] SMTP_FROM voi SMTP_USER puudub, emaili ei saadetud.")
        return False

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = from_address
    email["To"] = ", ".join(to_addresses)
    email.set_content(message)

    for attachment in attachments or []:
        if not attachment.exists() or not attachment.is_file():
            logger.warning("[NOTIFY] Manust ei leitud: %s", attachment)
            continue
        content_type, _ = mimetypes.guess_type(attachment)
        maintype, subtype = (content_type or "application/octet-stream").split("/", 1)
        email.add_attachment(
            attachment.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment.name,
        )

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
    attachments: list[str | Path] | None = None,
) -> None:
    """Saada seadistatud teavitused ja hoia pipeline alati toos."""
    load_dotenv()
    message = build_message(status, summary, pipeline_name, elapsed_seconds, output_dir)
    attachment_paths = [Path(path) for path in attachments or []]
    sent_any = False

    try:
        sent_any = send_webhook(message) or sent_any
    except Exception as exc:
        logger.warning("[NOTIFY] Webhooki saatmine ebaonnestus: %s", exc)

    try:
        subject = f"{pipeline_name}: {status.upper()}"
        sent_any = send_email(subject, message, attachment_paths) or sent_any
    except Exception as exc:
        logger.warning("[NOTIFY] Emaili saatmine ebaonnestus: %s", exc)

    if not sent_any:
        logger.info("[NOTIFY] Teavituskanalit pole seadistatud; kokkuvote:\n%s", message)
