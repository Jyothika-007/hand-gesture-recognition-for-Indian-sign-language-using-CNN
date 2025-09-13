import os
import numpy as np
import cv2
import random

minValue = 70

def func(path):
    frame = cv2.imread(path)
    if frame is None:
        print(f"❌ Could not read: {path}")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)

    th3 = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    ret, res = cv2.threshold(
        th3, minValue, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    return res

# Paths
main_folder = r"dataSet/datasetimg/owndataset"
train_folder = r"dataSet/datasetimg/trainingData"
val_folder = r"dataSet/datasetimg/validatingData"
test_folder = r"dataSet/datasetimg/testingData"

# Create output folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Collect all image file paths with their relative folder paths
all_images = []
for root, dirs, files in os.walk(main_folder):
    for filename in files:
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(root, main_folder)
            all_images.append((file_path, relative_path, filename))

# Shuffle the list to randomize the split
random.shuffle(all_images)

# Calculate split indices for 70% train, 15% validation, 15% test
train_split = int(0.7 * len(all_images))
val_split = int(0.85 * len(all_images))

train_images = all_images[:train_split]
val_images = all_images[train_split:val_split]
test_images = all_images[val_split:]

def process_and_save(images, base_output_folder):
    count = 0
    for file_path, relative_path, filename in images:
        result = func(file_path)
        if result is not None:
            save_dir = os.path.join(base_output_folder, relative_path)
            os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, filename)
            cv2.imwrite(save_path, result)
            count += 1
            print(f"✅ Saved: {save_path}")
    return count

print("Processing and saving TRAINING images...")
train_count = process_and_save(train_images, train_folder)

print("\nProcessing and saving VALIDATION images...")
val_count = process_and_save(val_images, val_folder)

print("\nProcessing and saving TESTING images...")
test_count = process_and_save(test_images, test_folder)

print(f"\n🎯 Done! Processed and saved {train_count} training images, {val_count} validation images, and {test_count} testing images.")
