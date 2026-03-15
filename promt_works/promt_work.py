import keyboard
import time
import sqlite3
from openai import OpenAI


API_KEY = 1

if API_KEY == 1:
    print("Please set your API key in the code.")
    exit(1)


import win32clipboard



def show_instructions():
    print("\n=== PROMPT LISTENER STARTED ===\n")

    print("User workflow:\n")

    print("1. Select text anywhere in Windows")
    print("2. Press CTRL + C")
    print("3. Press ALT + CTRL + SPACE")
    print("4. Script sends prompt to model")
    print("5. Answer saved to file\n")

    print("Prompt file :", PROMPT_FILE)
    print("Answer file :", ANSWER_FILE)

    print("\nWaiting for hotkey...\n")

def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    finally:
        win32clipboard.CloseClipboard()

    return data



client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

PROMPT_FILE = "promt_works/temp_promt.txt"
ANSWER_FILE = "promt_works/temp_answer.txt"

DITTO_DB = r"C:\Users\User\AppData\Roaming\Ditto\Ditto.db"


def get_latest_id():
    conn = sqlite3.connect(DITTO_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT lID FROM Main ORDER BY lID DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else 0


last_id = get_latest_id()


def get_ditto_text():
    global last_id

    conn = sqlite3.connect(DITTO_DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lID, mText
        FROM Main
        WHERE mText IS NOT NULL
        ORDER BY lID DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        clip_id, text = row

        if clip_id > last_id:
            last_id = clip_id
            return text

    return None


def process_prompt(prompt):

    print("\nPrompt captured from clipboard.\n")

    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write(prompt)

    print("PROMPT SENT TO MODEL:\n")
    print(prompt)
    print("\nRunning model with reasoning...\n")

    response = client.chat.completions.create(
        model="openrouter/hunter-alpha",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_body={
            "reasoning": {"enabled": True}
        }
    )

    message = response.choices[0].message
    answer = message.content

    with open(ANSWER_FILE, "w", encoding="utf-8") as f:
        f.write(answer)

    print("Model finished.")
    print("Answer saved to:", ANSWER_FILE)
    print("\nReady for next prompt.\n")


def run_prompt():
    try:

        print("\nHotkey detected. Reading clipboard...\n")

        prompt = get_clipboard_text()

        if not prompt:
            print("Clipboard is empty. Copy text first.\n")
            return

        process_prompt(prompt)

    except Exception as e:
        print("Error:", e)



show_instructions()

keyboard.add_hotkey("alt+ctrl+space", run_prompt)

keyboard.wait()



""" 
India is a democratic country ? 
""" 



""" 
again incoorect answer 
"""

