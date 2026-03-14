
import keyboard
import win32clipboard
import time
from openai import OpenAI


API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

PROMPT_FILE = "promt_works/temp_promt.txt"
ANSWER_FILE = "promt_works/temp_answer.txt"


def get_clipboard_text():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def run_prompt():
    try:
        # copy selected text
        keyboard.press("ctrl")
        keyboard.press("c")
        keyboard.release("c")
        keyboard.release("ctrl")

        time.sleep(2)

        prompt = get_clipboard_text()

        # save prompt to file
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(prompt)

        print("PROMPT SENT TO MODEL:")
        print(prompt)

        response = client.chat.completions.create(
            model="liquid/lfm-2.5-1.2b-thinking:free",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content

        with open(ANSWER_FILE, "w", encoding="utf-8") as f:
            f.write(answer)

        print("Answer saved")

    except Exception as e:
        print("Error:", e)


keyboard.add_hotkey("alt+shift+p", run_prompt)

print("Listening...")

keyboard.wait()

"""
India is a democratic country ?
"""



