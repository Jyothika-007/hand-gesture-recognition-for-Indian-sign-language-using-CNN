import numpy as np
import cv2
import os
import operator
from string import ascii_uppercase, digits
import tkinter as tk
from PIL import Image, ImageTk
from spellchecker import SpellChecker
from tensorflow.keras.models import model_from_json
import time

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

class Application:
    def __init__(self):
        self.symbol_start_time = None
        self.last_symbol = None
        self.prediction_start_time = None

        classes = list(digits) + list(ascii_uppercase)

        self.spell = SpellChecker()
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None

        # Load model
        with open("newproject/model_new_1.json", "r") as file:
            self.loaded_model = model_from_json(file.read())
        self.loaded_model.load_weights("newproject/model_new_1.h5")

        print("Loaded main model from disk")

        # ---------- Window ----------
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x770")
        self.root.configure(bg="#f9f0ff")  # light purple background

        # ---------- UI Layout ----------
        # Webcam
        self.panel = tk.Label(self.root, bg="white", relief="ridge", borderwidth=5)
        self.panel.place(x=20, y=50, width=580, height=480)

        # ROI Preview (Grayscale output)
        self.panel2 = tk.Label(self.root, bg="white", relief="ridge", borderwidth=5)
        self.panel2.place(x=620, y=50, width=250, height=250)

        # Suggestions label under ROI
        self.T4 = tk.Label(self.root, text="Suggestions :", fg="#6A0DAD",
                           font=("Courier", 16, "bold"), bg="#f9f0ff")
        self.T4.place(x=620, y=310)

        # Suggestion buttons stacked below grayscale ROI
        self.bt1 = tk.Button(self.root, command=self.action1,
                             bg="#d8bfff", fg="black", font=("Courier", 14), width=12)
        self.bt1.place(x=620, y=350)

        self.bt2 = tk.Button(self.root, command=self.action2,
                             bg="#d8bfff", fg="black", font=("Courier", 14), width=12)
        self.bt2.place(x=620, y=390)

        self.bt3 = tk.Button(self.root, command=self.action3,
                             bg="#d8bfff", fg="black", font=("Courier", 14), width=12)
        self.bt3.place(x=620, y=430)

        # Clear sentence button
        self.clear_btn = tk.Button(self.root, text="Clear Sentence", command=self.clear_sentence,
                                   bg="#ffccff", fg="black", font=("Courier", 14), width=14)
        self.clear_btn.place(x=620, y=470)

        # Title
        self.T = tk.Label(self.root, text="Sign Language To Text Conversion",
                          font=("Courier", 22, "bold"), bg="#f9f0ff", fg="#6A0DAD")
        self.T.place(x=80, y=5)

        # Character
        self.T1 = tk.Label(self.root, text="Character :", font=("Courier", 18, "bold"),
                           bg="#f9f0ff", fg="#6A0DAD")
        self.T1.place(x=20, y=550)
        self.panel3 = tk.Label(self.root, font=("Courier", 18), bg="white", relief="ridge", borderwidth=2)
        self.panel3.place(x=200, y=550, width=100, height=30)

        # Word entry
        self.T2 = tk.Label(self.root, text="Word :", font=("Courier", 18, "bold"),
                           bg="#f9f0ff", fg="#6A0DAD")
        self.T2.place(x=20, y=600)
        self.panel4 = tk.Entry(self.root, font=("Courier", 18), width=15, bg="white")
        self.panel4.place(x=200, y=600)
        self.panel4.focus_set()
        self.panel4.icursor(tk.END)

        # Sentence
        self.T3 = tk.Label(self.root, text="Sentence :", font=("Courier", 18, "bold"),
                           bg="#f9f0ff", fg="#6A0DAD")
        self.T3.place(x=20, y=650)
        # ---------- Sentence Box with Scrollbar ----------
        self.panel5_frame = tk.Frame(self.root, bg="#E6E6FA")
        self.panel5_frame.place(x=200, y=650, width=650, height=50)

        # Text widget for sentence
        self.panel5 = tk.Text(self.panel5_frame, font=("Courier", 18), bg="#EEE8F9", fg="#4B0082",
                      height=1, wrap="none")
        self.panel5.pack(side="top", fill="both", expand=True)

        # Horizontal scrollbar
        self.sentence_scroll = tk.Scrollbar(self.panel5_frame, orient="horizontal", command=self.panel5.xview)
        self.sentence_scroll.pack(side="bottom", fill="x")
        self.panel5.config(xscrollcommand=self.sentence_scroll.set)


        # Info label
        self.info_label = tk.Label(self.root, text="Ready", font=("Courier", 15),
                                   bg="#f9f0ff", fg="#6A0DAD")
        self.info_label.place(x=20, y=710)

        # Timer label
        self.timer_label = tk.Label(self.root, text="", font=("Courier", 16, "bold"),
                            bg="#f9f0ff", fg="#FF4500")
        self.timer_label.place(x=350, y=550)

        
        # ---------- Variables ----------
        self.str = ""  # sentence
        self.current_symbol = " "

        # Key bindings
        self.root.bind("<space>", self.space_pressed)
        self.root.bind("<Delete>", self.delete_last_character)

        self.video_loop()

    # ---------- Functions ----------
    def space_pressed(self, event):
        current_word = self.panel4.get().strip()
        if current_word:
            self.str += " " + current_word
            self.panel4.delete(0, tk.END)
            self.panel5.delete("1.0", tk.END)  # Clear old content
            self.panel5.insert(tk.END, self.str)  # Insert new sentence

    def delete_last_character(self, event):
        current_text = self.panel4.get()
        if current_text:
            self.panel4.delete(len(current_text) - 1, tk.END)

    def clear_sentence(self):
        self.str = ""
        self.panel5.delete("1.0", tk.END)


    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5 * frame.shape[1])
            y1, x2, y2 = 10, frame.shape[1] - 10, int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            roi = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
            _, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)

            # Show recognized character
            self.panel3.config(text=self.current_symbol, font=("Courier", 18))

            # Sentence label
            self.panel5.delete("1.0", tk.END)
            self.panel5.insert(tk.END, self.str)


            # Suggestions
            current_word = self.panel4.get().strip()
            predicts = []
            if current_word:
                candidates = self.spell.candidates(current_word)
                if candidates:
                    predicts = sorted(list(candidates))

            self.bt1.config(text=predicts[0] if len(predicts) > 0 else "")
            self.bt2.config(text=predicts[1] if len(predicts) > 1 else "")
            self.bt3.config(text=predicts[2] if len(predicts) > 2 else "")

        self.root.after(5, self.video_loop)

    def predict(self, test_image):
        # Preprocess image (same as training)
        test_image = cv2.resize(test_image, (128, 128))
        test_image = test_image.astype("float32") / 255.0
        test_image = test_image.reshape(1, 128, 128, 1)

        # Classes should match training order
        classes = sorted(os.listdir('dataSet/datasetimg/trainingData'))  # 0-9, a-z

        # Prediction
        result = self.loaded_model.predict(test_image)
        prediction = {cls: result[0][i] for i, cls in enumerate(classes)}
        prediction = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
        predicted_class = prediction[0][0]
        max_prob = prediction[0][1]

        current_time = time.time()
        CONFIDENCE_THRESHOLD = 0.8

        if max_prob >= CONFIDENCE_THRESHOLD:
            self.current_symbol = predicted_class

            # Show timer only if symbol is not blank (0)
            if self.current_symbol != '0':
                if self.current_symbol == self.last_symbol:
                    elapsed = current_time - self.prediction_start_time
                    remaining = max(0, 1.5 - elapsed)
                    self.timer_label.config(text=f"{remaining:.1f}s")

                    if elapsed >= 1.5:
                        self.panel4.insert(tk.END, self.current_symbol)
                        self.panel4.icursor(tk.END)
                        self.last_symbol = None
                        self.prediction_start_time = None
                        self.timer_label.config(text="")
                else:
                    self.last_symbol = self.current_symbol
                    self.prediction_start_time = current_time
                    self.timer_label.config(text="1.5s")  # reset timer
            else:
                # If blank page, just show it without inserting
                self.timer_label.config(text="")
                self.last_symbol = None
                self.prediction_start_time = None

        else:
            # Low confidence or blank
            self.current_symbol = ''
            self.last_symbol = None
            self.prediction_start_time = None
            self.timer_label.config(text="")



    def action1(self): self.add_suggestion(0)
    def action2(self): self.add_suggestion(1)
    def action3(self): self.add_suggestion(2)

    def add_suggestion(self, index):
        current_word = self.panel4.get().strip()
        predicts = []
        if current_word:
            candidates = self.spell.candidates(current_word)
            if candidates:
                predicts = sorted(list(candidates))

        if len(predicts) > index:
            self.str += " " + predicts[index]
            self.panel4.delete(0, tk.END)
            self.panel5.delete("1.0", tk.END)
            self.panel5.insert(tk.END, self.str)

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

print("Starting Application...")
(Application()).root.mainloop()
