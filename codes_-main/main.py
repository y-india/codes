

import requests

API_KEY = "<>"

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "google/gemma-3n-e4b-it:free",
        "messages": [
            {
                "role": "user",
                "content": "Who is the president of India?"
            }
        ]
    }
)

data = response.json()

if response.status_code != 200:
    raise RuntimeError(data)

print(data["choices"][0]["message"]["content"])
