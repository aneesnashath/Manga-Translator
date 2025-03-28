import streamlit as st
from PIL import Image
import os
from insert_text import process_panel  # Make sure insert_text.py has process_panel function

st.set_page_config(page_title="Korean to English Webtoon Panel Translator", layout="centered")

st.title("📘 Korean to English Webtoon Panel Translator")

uploaded_file = st.file_uploader("Upload your webtoon panel (Korean)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Save uploaded image
    raw_path = "data/raw_panel.png"
    with open(raw_path, "wb") as f:
        f.write(uploaded_file.read())

    st.subheader("🧽 Cleaned Panel (No Text)")
    clean_path = "cleaned_panels/clean_panel.png"
    if os.path.exists(clean_path):
        st.image(clean_path, caption="Cleaned Panel", use_column_width=True)
    else:
        st.info("Cleaning in progress or cleaned panel not found.")

    st.subheader("🌐 Translated & Rewritten Panel")
    output_path = "final_translated_panel.png"
    
    with st.spinner("Translating and reinserting text..."):
        llm_path = "/home/vmuser/Downloads/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"
        process_panel(raw_path, clean_path, output_path, llm_path)

    if os.path.exists(output_path):
        st.image(output_path, caption="Translated Panel", use_column_width=True)
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Translated Panel", f, file_name="translated_panel.png", mime="image/png")
    else:
        st.error("Final translated panel not generated.")

