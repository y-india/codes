import os
import time
import threading
import tkinter as tk
from tkinter import ttk
import pyperclip
import keyboard
from groq import Groq

# ── Config ───────────────────────────────────────────────────────────────────
client     = Groq(api_key=os.getenv("GROQ_API_KEY"))
OUTPUT_FILE = r"D:\codes_vs\pretotype_promt_polish_for_me\improved_prompts.txt"

# ── Shared state ─────────────────────────────────────────────────────────────
captured_text = ""


# ── Prompt improvement ────────────────────────────────────────────────────────
def improve_prompt(text: str) -> str:
    instruction = f"""
Rewrite the given prompt so it matches my personality, learning style, and workflow as an AI-assisted video coder and beginner data engineering learner.

About Me:
- I am 18 years old.
- I am self-learning coding and technology without paid resources.
- I learn best by building real projects and prototypes.
- Whatever I learn, I immediately practice through coding.
- I use AI tools to speed up learning, coding, debugging, and prototype development.
- I am following a data engineering roadmap step by step.
- I like practical learning more than theory.
- I prefer clear, direct, implementation-focused instructions.
- I often work with limited time, limited money, and limited resources, so solutions should stay efficient and beginner-friendly.
- I want outputs that help me improve skills, build projects, and grow faster as a developer.

Strict Rules:
1. Do NOT answer the original prompt.
2. Do NOT explain the prompt.
3. Do NOT add extra commentary, opinions, or unrelated information.
4. Keep the original meaning, intent, and goal exactly the same.
5. Rewrite the prompt in a clearer, more structured, and beginner-friendly way.
6. Use simple and direct language.
7. Convert vague instructions into actionable wording.
8. Use bullet points or step-by-step formatting if it improves readability.
9. Keep the rewritten prompt concise, practical, and easy to follow.
10. Do NOT generate solutions, code, or explanations.
11. Optimize the rewritten prompt for AI-assisted coding, project-building, and data engineering practice.
12. Make the wording practical for someone who learns by doing and building prototypes.
13. Ensure the final output is clean and easy to copy.

Output Requirements:
- Return only the rewritten prompt.
- Keep it concise, complete, and implementation-focused.
- Ensure it is optimized for self-learning, coding practice, and project execution.
Prompt:
{text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": instruction}],
    )
    return response.choices[0].message.content.strip()


# ── Popup window ──────────────────────────────────────────────────────────────
class PromptPopup:
    # Colours matching the Chrome extension
    BG          = "#1e1e1e"
    CARD_ORIG   = "#2a2a2a"
    CARD_IMPR   = "#1f3a2f"
    BTN_COPY    = "#4CAF50"
    BTN_REPLACE = "#2196F3"
    BTN_CLOSE   = "#444444"
    TEXT_DIM    = "#999999"
    TEXT_MAIN   = "#ffffff"
    FONT_BODY   = ("Segoe UI", 11)
    FONT_LABEL  = ("Segoe UI", 9)
    FONT_TITLE  = ("Segoe UI", 13, "bold")

    def __init__(self, original: str, improved: str):
        self.original = original
        self.improved = improved
        self._build()

    def _build(self):
        root = tk.Tk()
        self.root = root
        root.title("✨ Prompt Improved")
        root.configure(bg=self.BG)
        root.resizable(False, False)
        root.attributes("-topmost", True)          # always on top

        # ── Position: bottom-right corner ──
        root.update_idletasks()
        w, h = 440, 520
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{sw - w - 24}+{sh - h - 60}")

        pad = dict(padx=14, pady=6)

        # Title
        tk.Label(root, text="✨ Prompt Improved",
                 bg=self.BG, fg=self.TEXT_MAIN,
                 font=self.FONT_TITLE).pack(anchor="w", padx=14, pady=(14, 4))

        # ── Original section ──
        tk.Label(root, text="Original",
                 bg=self.BG, fg=self.TEXT_DIM,
                 font=self.FONT_LABEL).pack(anchor="w", **pad)

        orig_frame = tk.Frame(root, bg=self.CARD_ORIG,
                              bd=0, relief="flat")
        orig_frame.pack(fill="x", padx=14, pady=(0, 8))

        orig_box = tk.Text(orig_frame, wrap="word", height=5,
                           bg=self.CARD_ORIG, fg=self.TEXT_MAIN,
                           font=self.FONT_BODY, relief="flat",
                           bd=8, cursor="arrow", state="normal")
        orig_box.insert("1.0", self.original)
        orig_box.configure(state="disabled")
        orig_box.pack(fill="x")

        # ── Improved section ──
        tk.Label(root, text="Improved",
                 bg=self.BG, fg=self.TEXT_DIM,
                 font=self.FONT_LABEL).pack(anchor="w", **pad)

        impr_frame = tk.Frame(root, bg=self.CARD_IMPR,
                              bd=0, relief="flat")
        impr_frame.pack(fill="x", padx=14, pady=(0, 12))

        impr_scroll = tk.Scrollbar(impr_frame, orient="vertical")
        impr_box = tk.Text(impr_frame, wrap="word", height=10,
                           bg=self.CARD_IMPR, fg=self.TEXT_MAIN,
                           font=self.FONT_BODY, relief="flat",
                           bd=8, cursor="arrow",
                           yscrollcommand=impr_scroll.set)
        impr_scroll.config(command=impr_box.yview)
        impr_scroll.pack(side="right", fill="y")
        impr_box.insert("1.0", self.improved)
        impr_box.configure(state="disabled")
        impr_box.pack(fill="x", side="left", expand=True)

        # ── Buttons ──
        btn_frame = tk.Frame(root, bg=self.BG)
        btn_frame.pack(fill="x", padx=14, pady=(0, 14))

        def make_btn(parent, text, color, cmd):
            b = tk.Button(parent, text=text, command=cmd,
                          bg=color, fg="white",
                          font=("Segoe UI", 10, "bold"),
                          relief="flat", bd=0,
                          activebackground=color,
                          activeforeground="white",
                          cursor="hand2", padx=10, pady=8)
            b.bind("<Enter>", lambda e: b.configure(bg=self._darken(color)))
            b.bind("<Leave>", lambda e: b.configure(bg=color))
            b.pack(side="left", expand=True, fill="x", padx=4)
            return b

        self.copy_btn = make_btn(btn_frame, "Copy",    self.BTN_COPY,    self._on_copy)
        make_btn(btn_frame,                 "Replace",  self.BTN_REPLACE, self._on_replace)
        make_btn(btn_frame,                 "✕ Close",  self.BTN_CLOSE,   root.destroy)

        root.mainloop()

    # ── Button actions ────────────────────────────────────────────────────────
    def _on_copy(self):
        pyperclip.copy(self.improved)
        self.copy_btn.configure(text="Copied ✓")
        self.root.after(900, self.root.destroy)

    def _on_replace(self):
        """Copy improved text to clipboard (paste manually if needed)."""
        pyperclip.copy(self.improved)
        self.copy_btn.configure(text="Copied — Ctrl+V to paste ✓")
        self.root.after(1200, self.root.destroy)

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _darken(hex_color: str) -> str:
        """Return a slightly darker shade of the given hex colour."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        factor = 0.80
        return "#{:02x}{:02x}{:02x}".format(
            int(r * factor), int(g * factor), int(b * factor))


# ── Loading popup (shown while API call is in progress) ──────────────────────
class LoadingPopup:
    BG = "#1e1e1e"

    def __init__(self, original: str):
        self.root = tk.Tk()
        self.root.title("Prompt Improver")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        w, h = 440, 140
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{sw - w - 24}+{sh - h - 60}")

        tk.Label(self.root, text="⏳  Improving your prompt…",
                 bg=self.BG, fg="#ffffff",
                 font=("Segoe UI", 12, "bold")).pack(padx=16, pady=(18, 6), anchor="w")

        preview = original[:120] + ("…" if len(original) > 120 else "")
        tk.Label(self.root, text=preview,
                 bg=self.BG, fg="#999999",
                 font=("Segoe UI", 10),
                 wraplength=400, justify="left").pack(padx=16, anchor="w")

        self.root.update()

    def close(self):
        try:
            self.root.destroy()
        except Exception:
            pass


# ── Hotkey handlers ───────────────────────────────────────────────────────────
def on_copy():
    global captured_text
    time.sleep(0.15)                    # let OS finish writing to clipboard
    captured_text = pyperclip.paste()
    if captured_text.strip():
        print(f"[Captured] {len(captured_text)} chars — press Ctrl+Shift+Y to improve.")


def on_improve():
    global captured_text
    if not captured_text.strip():
        print("[!] Nothing captured. Select text → Ctrl+C → Ctrl+Shift+Y.")
        return

    original = captured_text           # snapshot before reset
    captured_text = ""                 # prevent double-trigger

    def _run():
        loader = LoadingPopup(original)

        try:
            improved = improve_prompt(original)
        except Exception as exc:
            loader.close()
            print(f"[Error] {exc}")
            return

        loader.close()

        # Save to file
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("\n--- Original ---\n")
            f.write(original.strip() + "\n")
            f.write("--- Improved ---\n")
            f.write(improved + "\n")

        PromptPopup(original, improved)   # blocks until user closes

    threading.Thread(target=_run, daemon=True).start()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    keyboard.add_hotkey("ctrl+c",       on_copy,    suppress=False)
    keyboard.add_hotkey("ctrl+shift+y", on_improve, suppress=True)

    print("=" * 56)
    print("  Prompt Improver  —  running")
    print("=" * 56)
    print("  Step 1 : Select text  →  Ctrl+C")
    print("  Step 2 : Ctrl+Shift+Y  →  popup appears")
    print("  Quit   : Ctrl+Shift+Q")
    print("=" * 56)

    keyboard.wait("ctrl+shift+q")
    print("\nBye!")


if __name__ == "__main__":
    main()