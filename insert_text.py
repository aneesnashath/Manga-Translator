import cv2
import easyocr
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from llama_cpp import Llama
import os

def process_panel(raw_path, clean_path, output_path, llm_path):
    # === STEP 1: Load image with text ===
    raw_image = cv2.imread(raw_path)
    reader = easyocr.Reader(['ko'], gpu=True)
    results = reader.readtext(raw_image)

    # === STEP 2: Load cleaned panel ===
    image = cv2.imread(clean_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # === STEP 3: Load LLM ===
    llm = Llama(model_path=llm_path, n_ctx=2048, n_threads=8, n_gpu_layers=35)

    # === STEP 4: Font path ===
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # === STEP 5: Font fitting ===
    def fit_text(text, font_path, box_width, box_height, max_font_size=40, min_font_size=10):
        for font_size in range(max_font_size, min_font_size - 1, -1):
            font = ImageFont.truetype(font_path, font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            if text_width <= box_width and text_height <= box_height:
                return font
        return ImageFont.truetype(font_path, min_font_size)

    # === STEP 6: Prompt Template ===
    def get_translation(text):
        prompt = f"Translate the following Korean dialogue to natural conversational English for a comic panel:\n\n\"{text}\"\n\nEnglish:"
        output = llm(prompt, max_tokens=128, stop=["</s>", "\n"], echo=False)
        return output["choices"][0]["text"].strip()

    # === STEP 7: Translate + insert text ===
    for (bbox, text, prob) in results:
        if prob < 0.3 or not text.strip():
            continue

        try:
            translated = get_translation(text)
        except Exception as e:
            translated = "[error]"
            print(f"⚠️ Translation error for '{text}': {e}")

        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        box_width = bottom_right[0] - top_left[0]
        box_height = bottom_right[1] - top_left[1]

        font = fit_text(translated, font_path, box_width, box_height)
        draw.text(top_left, translated, font=font, fill=(0, 0, 0))

    # === STEP 8: Save result ===
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    pil_image.save(output_path)
    output_path = "/home/vmuser/Desktop/translator/manga_env/output_panels/final_translated_panel.png"

    print(f"✅ LLM Translated panel saved as {output_path}")
