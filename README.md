# Hand Gesture Recognition for Indian Sign Language

This project focuses on recognizing **static Indian Sign Language (ISL) hand gestures (A–Z, 0–9)** using a **Convolutional Neural Network (CNN)**.  
It enables **real-time Sign-to-Text** conversion via webcam and also supports **Text-to-Sign translation**, making communication easier for the hearing-impaired community.

---

## ✨ Features
- 📷 Real-time hand gesture recognition using a webcam  
- 🔤 Recognizes alphabets (A–Z) and numbers (0–9)  
- 🧠 Deep learning model (CNN) trained on a custom dataset  
- 🖼 Dataset preprocessing for better accuracy  
- 🖥 Interactive **GUI with Tkinter**  
- 🔄 Two-way translation:  
  - Sign → Text  
  - Text → Sign (via images/gestures)

---

## 🛠 Tech Stack
- **Programming Language**: Python  
- **Deep Learning**: TensorFlow / Keras  
- **Computer Vision**: OpenCV  
- **GUI**: Tkinter  

---

## 🚀 How to Run

1. **Clone this repository**  
```bash
git clone https://github.com/Jyothika-007/hand-gesture-recognition-for-Indian-sign-language-using-CNN.git
cd hand-gesture-recognition-for-Indian-sign-language-using-CNN
```
2. **Install dependencies**  
3. **Collect dataset**  
4. **Create folders**  
5. **Preprocess and split the dataset**  
6. **Train the model**  
7. **Run the GUI**  

```bash
pip install -r requirements.txt
python DataCollection.py
python foldercreation.py
python preprocess_split.py
python model.py
python gui.py
- **Sign-to-Text**: Show a gesture in front of the webcam → converts it to text.  
- **Text-to-Sign**: Type text → shows corresponding gesture images.
```
