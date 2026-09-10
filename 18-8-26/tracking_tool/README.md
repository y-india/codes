# Simple recruiting outreach app

This is a small Flask application that uses Google Sheets as its database and Brevo as the email delivery provider.

It supports:
- importing one email per line
- sending the same campaign individually to unsent contacts
- approximate open tracking with a 1x1 tracking pixel
- click tracking with a redirect URL
- unsubscribe status
- a simple dashboard

## 1. Create the Google Sheet

Create a Google Sheet. Copy its ID from the URL:

`https://docs.google.com/spreadsheets/d/THIS_IS_THE_SHEET_ID/edit`

Put that ID in `.env` as `GOOGLE_SHEET_ID`.

## 2. Create a Google service account

In Google Cloud:
- Create/select a project.
- Enable the Google Sheets API.
- Create a service account.
- Create a JSON key for that service account.
- Save the JSON file in this project folder as `service-account.json`.

Open the Google Sheet's Share dialog and share the sheet with the service-account email address as Editor.

Do not upload `service-account.json` to GitHub.

## 3. Create a Brevo account and API key

Create a Brevo account, verify the sender/domain you will use, and create an API key.

Put the key and verified sender address in `.env`.

## 4. Configure the app

Copy `.env.example` to `.env` and fill in the values.

For local testing, `BASE_URL` can be `http://localhost:5000`, but tracking will not work for recipients on the public internet because their email clients cannot reach your local computer.

For real tracking, deploy the app to a public HTTPS URL and set `BASE_URL` to that URL.

## 5. Install and run

Python 3.10+ is recommended.

Windows:
```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## 6. Import your text file

Open the text file, copy the addresses, paste them into the Import box, and click Import.

The app creates a unique token for each address and stores it in Google Sheets.

## 7. Send

Enter a subject and body. Any `http://` or `https://` URL in the body is converted to a tracked redirect.

The Send button only sends to contacts that have not already been marked as sent and are not unsubscribed.

## Important tracking limitations

Open tracking is approximate. Modern email privacy systems, image blocking, security scanners, and automated systems can cause false opens or missed opens.

Click tracking is more meaningful, but security scanners can sometimes prefetch links too. Treat analytics as signals rather than proof that a person read the email.

## Important operational notes

Do not use this application to send unsolicited bulk mail or to evade provider spam controls. Contact people only where you have a legitimate basis to contact them, keep the message relevant, and honor unsubscribe requests.

For a production system, add rate limiting, authentication, CSRF protection, retry/backoff handling, provider webhooks for delivery/bounce events, and stronger input validation.

## Suggested next upgrades

If you want this to become a real recruiting tool, the next useful additions are:
1. campaign history
2. CSV export
3. delivery/bounce tracking
4. a proper unsubscribe page
5. authentication/login
6. scheduled sending
7. per-campaign analytics
