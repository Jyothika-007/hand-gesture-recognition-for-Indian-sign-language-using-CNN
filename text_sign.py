import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class TextToSignApp:
    def __init__(self, root, sign_image_folder="dataSet/sign_images"):
        self.root = root
        self.root.title("Creative Text to Sign Converter")
        self.root.geometry("1000x350")
        self.root.configure(bg="#E6E6FA")   # Light lavender (white-purple)

        self.sign_image_folder = sign_image_folder
        self.images = []
        self.image_labels = []

        # Title
        tk.Label(self.root, text="Text → Sign Language",
                 font=("Courier", 24, "bold"),
                 fg="white", bg="#9370DB"   # Medium purple header
                 ).pack(fill="x")

        # Input box
        self.text_entry = tk.Entry(self.root, font=("Courier", 20), bg="white", fg="#4B0082")  # Indigo text
        self.text_entry.place(x=20, y=60, width=600)

        # Show button
        tk.Button(self.root, text="Show Signs 🎯",
                  font=("Courier", 18),
                  bg="#8A2BE2", fg="white",   # BlueViolet button
                  activebackground="#BA55D3", activeforeground="white",
                  command=self.text_to_sign).place(x=640, y=55)

        # Frame for images
        self.canvas = tk.Canvas(self.root, height=150,
                                bg="#D8BFD8",  # Thistle (light purple)
                                highlightthickness=0)
        self.canvas.place(x=20, y=120, width=950, height=150)

        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview,
                                     bg="#E6E6FA", troughcolor="#D8BFD8")
        self.scroll_x.place(x=20, y=270, width=950)
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.sign_frame = tk.Frame(self.canvas, bg="#EEE8F9")  # Very light purple
        self.canvas.create_window((0, 0), window=self.sign_frame, anchor="nw")

    def text_to_sign(self):
        """Clear old images and display new ones with animation."""
        for widget in self.sign_frame.winfo_children():
            widget.destroy()

        self.images.clear()
        text = self.text_entry.get().upper()

        # Prepare image sequence
        for char in text:
            if char == " ":
                # Add spacer image for space
                spacer = Image.new("RGB", (50, 100), color="#EEE8F9")
                self.images.append(ImageTk.PhotoImage(spacer))
            else:
                img_path = os.path.join(self.sign_image_folder, f"{char}.jpg")
                if os.path.exists(img_path):
                    img = Image.open(img_path).resize((100, 100))
                    # Add rounded border
                    img = self.add_border(img, border_color=(186, 85, 211), border_width=4)  # Orchid purple border
                    self.images.append(ImageTk.PhotoImage(img))

        # Animate appearance
        self.animate_images(0)

    def animate_images(self, index):
        if index < len(self.images):
            label = tk.Label(self.sign_frame, image=self.images[index], bg="#EEE8F9")
            label.pack(side="left", padx=5)
            self.sign_frame.update_idletasks()

            # Adjust scroll region
            total_width = sum(img.width() for img in self.images) + (len(self.images) * 10)
            self.canvas.config(scrollregion=(0, 0, total_width, 100))

            # Schedule next image to appear
            self.root.after(200, lambda: self.animate_images(index + 1))

    def add_border(self, img, border_color=(255, 255, 255), border_width=5):
        """Add a colored border to the image."""
        w, h = img.size
        bordered = Image.new("RGB", (w + border_width*2, h + border_width*2), border_color)
        bordered.paste(img, (border_width, border_width))
        return bordered

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSignApp(root)
    root.mainloop()
