import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# ---------- Button Actions ----------
def open_sign_to_text():
    subprocess.Popen(["python", "newproject/sign_to_text.py"])

def open_text_to_sign():
    subprocess.Popen(["python", "newproject/text_sign.py"])


# ---------- Main Window ----------
root = tk.Tk()
root.title("Indian Sign Language Project")

# Set fixed 1920x1080 window
root.geometry("1920x1080")

# -------- Gradient Background (White → Purple) --------
canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Gradient: White (#FFFFFF) → Purple (#A020F0)
start_r, start_g, start_b = (255, 255, 255)
end_r, end_g, end_b = (160, 32, 240)

for i in range(1080):  # height = 1080
    r = int(start_r + (end_r - start_r) * (i / 1080))
    g = int(start_g + (end_g - start_g) * (i / 1080))
    b = int(start_b + (end_b - start_b) * (i / 1080))
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 1920, i, fill=color)

# -------- Overlay Frame --------
frame = tk.Frame(canvas, bg="white", bd=0, highlightthickness=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

# -------- Title --------
title = tk.Label(frame, text="🤟 Indian Sign Language 🤟",
                 font=("Helvetica", 32, "bold"), fg="#6A0DAD", bg="white")
title.pack(pady=20)

# -------- Collage Banner --------
collage_img = Image.open("collage_with_names.jpg")
collage_img = collage_img.resize((900, 350))   # banner size for 1080p
collage_photo = ImageTk.PhotoImage(collage_img)

collage_label = tk.Label(frame, image=collage_photo, bg="white")
collage_label.pack(pady=20)

# -------- Button Frame --------
btn_frame = tk.Frame(frame, bg="white")
btn_frame.pack(pady=40)

# Hover effects
def on_enter(e): e.widget.config(bg="#8A2BE2", fg="white")   # darker purple
def on_leave(e): e.widget.config(bg="#9370DB", fg="white")  # soft purple

# Buttons
btn1 = tk.Button(btn_frame, text="Sign → Text", font=("Arial", 18, "bold"),
                 bg="#9370DB", fg="white", width=20, relief="flat",
                 command=open_sign_to_text)
btn1.grid(row=0, column=0, padx=50, pady=20)
btn1.bind("<Enter>", on_enter)
btn1.bind("<Leave>", on_leave)

btn2 = tk.Button(btn_frame, text="Text → Sign", font=("Arial", 18, "bold"),
                 bg="#9370DB", fg="white", width=20, relief="flat",
                 command=open_text_to_sign)
btn2.grid(row=0, column=1, padx=50, pady=20)
btn2.bind("<Enter>", on_enter)
btn2.bind("<Leave>", on_leave)

# -------- Footer --------
footer = tk.Label(frame, text="Made with ❤️ for Indian Sign Language",
                  font=("Arial", 14), fg="#6A0DAD", bg="white")
footer.pack(pady=20)

root.mainloop()
