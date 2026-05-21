import os
import pyperclip
import keyboard
from groq import Groq

# ── Config ──────────────────────────────────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
OUTPUT_FILE = "improved_prompts.txt"

# ── State ────────────────────────────────────────────────────────────────────
captured_text = ""          # holds whatever Ctrl+C copied


# ── Core logic ───────────────────────────────────────────────────────────────
def improve_prompt(text: str) -> str:
    """Send text to Groq and return the improved prompt."""
    instruction = f"""
Rewrite the given prompt to make it clearer, more specific, and easier for a
beginner-level coder or data learner to understand.

Strict Rules:
1. Do NOT answer the original prompt.
2. Do NOT explain the prompt.
3. Do NOT add extra commentary, notes, examples, or opinions.
4. Keep the original intent, meaning, and goal exactly the same.
5. Improve clarity, structure, and precision.
6. Use simple, direct, beginner-friendly language.
7. Convert vague instructions into practical and actionable wording.
8. Use step-by-step format or bullet points if it improves readability.
9. Ensure the output is only a rewritten version of the prompt.
10. Prevent generating solutions, explanations, or unrelated text.

Output Requirements:
- Return only the rewritten prompt.
- Keep it concise, complete, and easy to follow.

Prompt:
{text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": instruction}],
    )
    return response.choices[0].message.content.strip()


# ── Hotkey handlers ───────────────────────────────────────────────────────────
def on_copy():
    """Ctrl+C — let the OS copy as normal, then snapshot the clipboard."""
    global captured_text
    # Give the OS a moment to update the clipboard before we read it
    import time
    time.sleep(0.15)
    captured_text = pyperclip.paste()
    if captured_text.strip():
        print(f"\n[Captured] {len(captured_text)} characters. "
              "Press Ctrl+Shift+Y to improve.")
    # Note: we do NOT suppress Ctrl+C so normal copy behaviour is preserved.


def on_improve():
    """Ctrl+Shift+Y — improve the last captured text and display + save it."""
    global captured_text

    if not captured_text.strip():
        print("\n[!] Nothing captured yet. "
              "Select text, press Ctrl+C, then Ctrl+Shift+Y.")
        return

    print("\n[~] Improving prompt, please wait…")
    try:
        improved = improve_prompt(captured_text)
    except Exception as exc:
        print(f"[Error] Groq API call failed: {exc}")
        return

    # ── Display ──
    separator = "─" * 60
    print(f"\n{separator}")
    print("IMPROVED PROMPT")
    print(separator)
    print(improved)
    print(separator)

    # ── Copy improved prompt to clipboard ──
    pyperclip.copy(improved)
    print("[✓] Improved prompt copied to clipboard.")

    # ── Save to file ──
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n--- Original ---\n")
        f.write(captured_text.strip())
        f.write("\n--- Improved ---\n")
        f.write(improved)
        f.write("\n")
    print(f"[✓] Saved to '{OUTPUT_FILE}'.")

    # Reset so the same text isn't accidentally re-processed
    captured_text = ""


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    # suppress=False keeps default Ctrl+C copy behaviour intact
    keyboard.add_hotkey("ctrl+c", on_copy, suppress=False)
    keyboard.add_hotkey("ctrl+shift+y", on_improve, suppress=True)

    print("=" * 60)
    print("  Prompt Improver  —  running")
    print("=" * 60)
    print("  Step 1 : Select any text, then press  Ctrl+C")
    print("  Step 2 : Press  Ctrl+Shift+Y  to improve & display")
    print("  Quit   : Ctrl+Shift+Q  (or close this window)")
    print("=" * 60)

    keyboard.wait("ctrl+shift+q")   # block until user quits
    print("\nBye!")


if __name__ == "__main__":
    main()


