import keyboard
from openai import OpenAI

API_KEY = ""

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

PROMPT_FILE = "promt_works/small_promt_task/prompt.txt"
ANSWER_FILE = "promt_works/small_promt_task/answer.txt"


def run_prompt():

    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt = f.read()

        response = client.chat.completions.create(
            model="liquid/lfm-2.5-1.2b-thinking:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        with open(ANSWER_FILE, "w", encoding="utf-8") as f:
            f.write(answer)

        print("Answer saved to answer.txt")
        # print("Answer saved to answer.txt")

    except Exception as e:
        print("Error:", e)


keyboard.add_hotkey("alt+shift+p", run_prompt)

print("Listening... Press Alt+Shift+P")

keyboard.wait()


