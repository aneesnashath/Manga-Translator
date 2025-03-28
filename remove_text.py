import cv2
import easyocr
import numpy as np

# Load original image
img_path = "/home/vmuser/Desktop/translator/manga_env/data/raw_panel.png"  
image = cv2.imread(img_path)

# Make a copy for masking
mask = np.zeros(image.shape[:2], dtype=np.uint8)

# Load OCR and detect text
reader = easyocr.Reader(['ko'], gpu=True)
results = reader.readtext(image)

# Draw white rectangles (text areas) on the mask
for (bbox, text, prob) in results:
    pts = np.array(bbox, dtype=np.int32)
    cv2.fillPoly(mask, [pts], 255)

# Inpaint using Telea algorithm
inpainted = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

# Save and show result
cv2.imwrite("clean_panel.png", inpainted)
print("✅ Saved as clean_panel.png")

