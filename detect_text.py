import easyocr
from googletrans import Translator
import cv2
import matplotlib.pyplot as plt

# Step 1: Load image
image_path = "/home/vmuser/Desktop/translator/manga_env/data/raw_panel.png"  
image = cv2.imread(image_path)

# Step 2: Initialize EasyOCR for Korean + Chinese (in case some panels use both)
reader = easyocr.Reader(['ko'], gpu=True)
results = reader.readtext(image)

# Step 3: Initialize Google Translator
translator = Translator()

# Step 4: Translate and display results
for (bbox, text, prob) in results:
    # Translate text to English
    try:
        translation = translator.translate(text, src='auto', dest='en').text
    except Exception as e:
        translation = "[Translation Error]"

    print(f"🔸 Original: {text}")
    print(f"➡️  Translated: {translation}")
    print("-" * 40)

