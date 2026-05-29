import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import webbrowser

# ---------- Functions ----------
def open_chat_guru():
    os.system("python chatbot.py")

def open_login_page():
    os.system("python loginReg.py")

def open_video_tutorial():
    video_link = "https://www.youtube.com/watch?v=2ePf9rue1Ao"
    webbrowser.open(video_link)


# ---------- Main Dashboard ----------
root = tk.Tk()
root.title("AI Learning Dashboard for Rural Empowerment")
root.geometry("900x600")

# ----- Load and Set Background Image -----
try:
    bg_image = Image.open("bg.jpeg")   # 👈 Put your image name here
    bg_image = bg_image.resize((1500, 900), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Background image not found. Using solid color.")
    root.config(bg="#ccf2ff")

# ----- Overlay Content on Top of Background -----
# Header
header = tk.Label(root, text="🌾 AI Learning Dashboard 🌾",
                  font=("Arial Rounded MT Bold", 26),
                  bg="#0066cc", fg="white", pady=10)
header.pack(fill="x")

# Transparent Frame (for buttons)
frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Buttons
btn_chat = tk.Button(frame, text="🗣️ Chat Guru", font=("Arial", 16, "bold"),
                     bg="#00b300", fg="white", width=20, height=2,
                     command=open_chat_guru)
btn_chat.grid(row=0, column=0, padx=20, pady=10)

btn_login = tk.Button(frame, text="🔐 Login Page", font=("Arial", 16, "bold"),
                      bg="#ff9933", fg="white", width=20, height=2,
                      command=open_login_page)
btn_login.grid(row=0, column=1, padx=20, pady=10)

btn_video = tk.Button(frame, text="🎥 Video Tutorial", font=("Arial", 16, "bold"),
                      bg="#0099cc", fg="white", width=20, height=2,
                      command=open_video_tutorial)
btn_video.grid(row=1, column=0, columnspan=2, pady=20)

# Footer
footer = tk.Label(root, text="Empowering Rural India with AI 🌱",
                  font=("Arial", 12, "italic"),
                  bg="#e6f3ff", fg="#004d99")
footer.pack(side="bottom", pady=10)

root.mainloop()
