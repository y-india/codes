import keyboard
import time
from openai import OpenAI
import win32clipboard



API_KEY = "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"
if API_KEY == 1:
    print("Please set your API key in the code.")
    exit(1)


PROMPT_FILE = "promt_works/temp_promt.txt"
ANSWER_FILE = "promt_works/better_promt.md"




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

# 




client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)












def improve_prompt(prompt):
    words = prompt.split()
    word_count = len(words)
    limit = word_count * 3

    instruction = f"""
Rewrite the user's prompt to make it clearer and more effective.
Do not change the intent.

Constraints:
- Maximum {limit} words
- Keep meaning same
- Make it clearer and more specific
- Return ONLY the improved prompt.

User prompt:
{prompt}
"""

    response = client.chat.completions.create(
        model="openrouter/hunter-alpha",
        messages=[
            {"role": "user", "content": instruction}
        ]
    )

    improved_prompt = response.choices[0].message.content.strip()
    return improved_prompt











def process_prompt(prompt):

    print("\nPrompt captured from clipboard.\n")

    improved_prompt = improve_prompt(prompt)

    with open(ANSWER_FILE, "w", encoding="utf-8") as f:
        f.write(improved_prompt)

    print("IMPROVED PROMPT:\n")
    print(improved_prompt)

    print("\nSaved to:", ANSWER_FILE)
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
who i can connect with pm of india??
""" 
