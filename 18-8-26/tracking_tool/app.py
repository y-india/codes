import os, re, uuid, html
from datetime import datetime, timezone
from urllib.parse import urlencode

from flask import Flask, request, render_template, redirect, url_for, Response, flash
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me")

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000").rstrip("/")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL", "")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME", "Recruiting")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Contacts")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = [
    "email", "token", "status", "sent_at", "opened_at", "open_count",
    "clicked_at", "click_count", "last_click_url", "unsubscribed"
]

def now():
    return datetime.now(timezone.utc).isoformat()

def sheet():
    if not SHEET_ID:
        raise RuntimeError("GOOGLE_SHEET_ID is missing.")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    try:
        ws = sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(HEADERS))
        ws.append_row(HEADERS)
    if not ws.row_values(1):
        ws.append_row(HEADERS)
    return ws

def ensure_headers(ws):
    current = ws.row_values(1)
    if current != HEADERS:
        ws.update("A1:J1", [HEADERS])

def records():
    ws = sheet()
    ensure_headers(ws)
    return ws.get_all_records()

def find_row(ws, token):
    vals = ws.get_all_values()
    for i, row in enumerate(vals[1:], start=2):
        if len(row) > 1 and row[1] == token:
            return i
    return None

def valid_email(x):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", x.strip()))

def import_emails(raw):
    emails = []
    for line in raw.splitlines():
        e = line.strip().lower()
        if e and valid_email(e) and e not in emails:
            emails.append(e)

    ws = sheet()
    ensure_headers(ws)
    existing = {r.get("email","").lower() for r in ws.get_all_records()}
    rows = []
    for e in emails:
        if e not in existing:
            rows.append([e, uuid.uuid4().hex, "ready", "", "", 0, "", 0, "", "no"])
    if rows:
        ws.append_rows(rows)
    return len(rows), len(emails) - len(rows)

def tracked_html(body, token):
    safe_body = html.escape(body).replace("\n", "<br>")
    # Convert plain URLs into tracked links. Only http/https links are supported.
    url_re = re.compile(r'(https?://[^\s<]+)')
    def repl(m):
        target = m.group(1).rstrip(".,);")
        q = urlencode({"id": token, "url": target})
        return f'<a href="{BASE_URL}/click?{q}">{html.escape(target)}</a>'
    safe_body = url_re.sub(repl, safe_body)
    pixel = f'<img src="{BASE_URL}/open?id={token}" width="1" height="1" alt="" style="display:block;border:0;" />'
    return f"<div style='font-family:Arial,sans-serif;line-height:1.5'>{safe_body}</div>{pixel}"

def send_brevo(to_email, subject, html_content):
    if not BREVO_API_KEY:
        raise RuntimeError("BREVO_API_KEY is missing.")
    payload = {
        "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }
    r = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={"accept": "application/json", "api-key": BREVO_API_KEY,
                 "content-type": "application/json"},
        json=payload, timeout=30
    )
    if r.status_code >= 300:
        raise RuntimeError(f"Brevo error {r.status_code}: {r.text}")
    return r.json()

@app.route("/")
def index():
    try:
        rs = records()
    except Exception as e:
        return render_template("error.html", error=str(e))
    total = len(rs)
    sent = sum(1 for r in rs if r.get("sent_at"))
    opened = sum(1 for r in rs if r.get("opened_at"))
    clicked = sum(1 for r in rs if r.get("clicked_at"))
    unsub = sum(1 for r in rs if str(r.get("unsubscribed","")).lower() == "yes")
    return render_template("index.html", total=total, sent=sent, opened=opened,
                           clicked=clicked, unsub=unsub, contacts=rs)

@app.route("/import", methods=["POST"])
def do_import():
    try:
        raw = request.form.get("emails", "")
        added, skipped = import_emails(raw)
        flash(f"Imported {added} new addresses. Skipped {skipped} duplicates/invalid lines.", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/send", methods=["POST"])
def do_send():
    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()
    if not subject or not body:
        flash("Subject and body are required.", "error")
        return redirect(url_for("index"))

    try:
        ws = sheet()
        rs = ws.get_all_records()
        sent_count = 0
        for idx, r in enumerate(rs, start=2):
            if r.get("sent_at") or str(r.get("unsubscribed","")).lower() == "yes":
                continue
            email = r.get("email","").strip()
            token = r.get("token","").strip()
            if not email or not token:
                continue
            try:
                send_brevo(email, subject, tracked_html(body, token))
                ws.update(f"C{idx}:D{idx}", [["sent", now()]])
                sent_count += 1
            except Exception as e:
                ws.update(f"C{idx}", [[f"error: {str(e)[:120]}"]])
        flash(f"Attempted {sent_count} sends. Check the sheet for errors.", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/open")
def opened():
    token = request.args.get("id", "")
    if token:
        try:
            ws = sheet()
            row = find_row(ws, token)
            if row:
                vals = ws.row_values(row)
                # F=opened_at, G=open_count based on A:J header layout
                opened_at = vals[4] if len(vals) >= 5 else ""
                count = int(vals[5] or 0) if len(vals) >= 6 and str(vals[5]).isdigit() else 0
                ws.update(f"E{row}:F{row}", [[opened_at or now(), count + 1]])
        except Exception:
            pass
    # 1x1 transparent GIF
    return Response(
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
        b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
        b"\x00\x02\x02D\x01\x00;",
        mimetype="image/gif",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"}
    )

@app.route("/click")
def clicked():
    token = request.args.get("id", "")
    target = request.args.get("url", "")
    if not re.match(r"^https?://", target):
        return "Invalid destination", 400
    if token:
        try:
            ws = sheet()
            row = find_row(ws, token)
            if row:
                vals = ws.row_values(row)
                count = int(vals[7] or 0) if len(vals) >= 8 and str(vals[7]).isdigit() else 0
                ws.update(f"G{row}:I{row}", [[vals[6] if len(vals) >= 7 and vals[6] else now(),
                                              count + 1, target]])
        except Exception:
            pass
    return redirect(target)

@app.route("/unsubscribe")
def unsubscribe():
    token = request.args.get("id", "")
    if token:
        try:
            ws = sheet()
            row = find_row(ws, token)
            if row:
                ws.update(f"J{row}", [["yes"]])
        except Exception:
            pass
    return "You have been unsubscribed from future messages."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
