import tkinter as tk
from tkinter import ttk
import threading
import json
import requests

# --- Initialize main window ---
chatbot_frame = tk.Tk()
chatbot_frame.geometry('400x600')
chatbot_frame.title('Chatbot Guru')
chatbot_frame.configure(bg="#171970")

# --- Global variables ---
chat_history = []

# --- Functions ---
def append_to_chat(message):
    chat_display.config(state="normal")
    chat_display.insert(tk.END, message + "\n")
    chat_display.config(state="disabled")
    chat_display.see(tk.END)

def send_message():
    user_message = user_input.get().strip()
    if not user_message:
        return

    append_to_chat(f"You: {user_message}")
    user_input.delete(0, tk.END)
    loading_label.config(text="Thinking...")

    thread = threading.Thread(target=get_bot_response, args=(user_message,))
    thread.start()

def get_bot_response(user_message):
    try:
        chat_history.append({"role": "user", "parts": [{"text": user_message}]})

        # --- Replace with your actual Gemini API key ---
        api_key = "AIzaSyDIfuvL8H8N7S9hYwsQYFQsnBSqHeVc1w8"
        #api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

        model = "gemini-2.5-flash"  # or another model from the docs
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        payload = {"contents": chat_history}
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()
        bot_text = "I'm sorry, I couldn't generate a response."
        if result and 'candidates' in result and len(result['candidates']) > 0:
            bot_text = result['candidates'][0]['content']['parts'][0]['text']

        chat_history.append({"role": "model", "parts": [{"text": bot_text}]})
        chatbot_frame.after(0, lambda: append_to_chat(f"Bot: {bot_text}"))

    except requests.exceptions.RequestException as e:
        chatbot_frame.after(0, lambda: append_to_chat("Bot: API request failed. Check your internet or API key."))
        print(f"API Error: {e}")
    except Exception as e:
        chatbot_frame.after(0, lambda: append_to_chat("Bot: Unexpected error occurred."))
        print(f"Unexpected Error: {e}")
    finally:
        chatbot_frame.after(0, lambda: loading_label.config(text=""))

def on_enter_pressed(event):
    send_message()

# --- UI Layout ---
chatbot_label = ttk.Label(chatbot_frame, text="Chatbot Guru", font=("Helvetica", 14, "bold"))
chatbot_label.pack(pady=10)

chat_display = tk.Text(chatbot_frame, height=20, state="disabled", borderwidth=1, relief="solid")
chat_display.pack(fill="both", expand=True, padx=5, pady=5)

input_frame = ttk.Frame(chatbot_frame)
input_frame.pack(fill="x", padx=5, pady=5)

user_input = ttk.Entry(input_frame)
user_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
user_input.bind("<Return>", on_enter_pressed)

send_button = ttk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side="right")

loading_label = ttk.Label(input_frame, text="", foreground="blue")
loading_label.pack(side="right", padx=5)

# --- Initial greeting ---
append_to_chat("Bot: Hello! I'm your online teacher. How can I help you today?")

# --- Start the chatbot ---
chatbot_frame.mainloop()