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
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY
)

def improve_prompt(prompt):
    words = prompt.split()
    word_count = len(words)
    limit = word_count * 5

    instruction = f"""
Rewrite the user’s prompt to make it clearer, more precise, and better structured for a coder or corporate professional.
Do not change the original intent.
Return only the improved prompt with no explanations or extra text.
Keep the meaning unchanged while adding relevant detail and specificity.
Limit the response to {limit} words.


User prompt:
{prompt}
"""

    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.2",
        messages=[{"role": "user", "content": instruction}],
        temperature=0.7,
        top_p=0.95,
        max_tokens=512,
        stream=True
    )

    improved_prompt = ""

    for chunk in completion:
        if not getattr(chunk, "choices", None):
            continue

        delta = chunk.choices[0].delta

        if delta.content:
            improved_prompt += delta.content

    return improved_prompt.strip()







def process_prompt(prompt):

    print("\nPrompt captured from clipboard.\n")

    improved_prompt = improve_prompt(prompt)

    with open(ANSWER_FILE, "a", encoding="utf-8") as f:
        f.write(improved_prompt + "\n\n")

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
what will happen if plant remove form earth in one secondd ???
""" 


"""
pakistan popluation who much in 2024 ??
"""

"""
give me code to connvert this txt file into md , i have many files , so code will be working also on folder , but some time in only single file 
and also i want to add some extra line in start and end of file and they are same for all files 
start line is "### This file is converted from txt to md ###" and end line is "### End of file ###"
"""