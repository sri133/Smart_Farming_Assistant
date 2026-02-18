import streamlit as st
from PIL import Image, ImageOps
import io
import google.generativeai as genai

# ---------------------------------------
# CONFIGURE GEMINI
# ---------------------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="Cronus", page_icon="🌾", layout="wide")
st.title("🌾 Cronus - Smart Farming Assistant for Tamil Nadu Farmers")
st.write("Ask anything about farming, crops, land, chemicals, or business ideas and get AI-powered advice.")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select a Page:", ["Land", "Chemical", "Crop Suggestion", "Farming Activity", "Farming Business Idea", "Image Analysis"])

# ------------------------------------------------
# Function to call AI directly
# ------------------------------------------------
def get_ai_response(user_query):
    try:
        response = model.generate_content(
            user_query,
            generation_config={"temperature": 0.3, "max_output_tokens": 2000}
        )
        return response.text
    except Exception as e:
        return f"Error generating AI response: {e}"

# ------------------------------------------------
# TEXT-BASED PAGES
# ------------------------------------------------
text_pages = {
    "Land": "Ask about land preparation, soil management, or irrigation:",
    "Chemical": "Ask about fertilizers, pesticides, and safe usage:",
    "Crop Suggestion": "Ask about which crops to grow, rotations, or yield optimization:",
    "Farming Activity": "Ask for activity tips, best practices, or techniques:",
    "Farming Business Idea": "Ask about farming-related business ideas with pros and cons:"
}

if page in text_pages:
    st.header(f"📝 {page}")
    query = st.text_area(text_pages[page])
    if st.button("Get Advice", key=page):
        if query.strip():
            with st.spinner(f"Generating {page.lower()} advice..."):
                st.markdown(get_ai_response(query))
        else:
            st.warning("Please type a question.")

# ------------------------------------------------
# IMAGE ANALYSIS PAGE
# ------------------------------------------------
if page == "Image Analysis":
    st.header("🖼️ Image-Based Plant Analysis")
    uploaded_file = st.file_uploader("Upload an image of the plant:", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image)  # fix rotation
        image.thumbnail((1024, 1024))  # optional: reduce size
        st.image(image, caption="Uploaded Image", use_container_width=True)

        prompt_text = st.text_input(
            "Ask a question about this image:",
            value="What does this image show and what actions should be taken?"
        )

        if st.button("Analyze Image", key="image_analysis"):
            if prompt_text.strip():
                with st.spinner("Analyzing image..."):
                    try:
                        buffer = io.BytesIO()
                        image.save(buffer, format=image.format)
                        img_bytes = buffer.getvalue()
                        mime = uploaded_file.type

                        # AI multi-modal input (text + image)
                        analysis_prompt = f"""
You are an agriculture and plant health expert.

Analyze the given plant image and respond clearly and responsibly.
Include:
- Probable diagnosis / issue
- 3–5 practical recommended actions
- Short justification based on visible features
- Monitoring steps

Question: {prompt_text}
"""
                        response = model.generate_content(
                            [
                                analysis_prompt,
                                {"mime_type": mime, "data": img_bytes}
                            ],
                            generation_config={"temperature": 0.3, "max_output_tokens": 2000}
                        )

                        st.success("AI Image Analysis Result:")
                        st.markdown(response.text + "\n\n*Disclaimer: This is an AI-generated probable diagnosis. Please consult a professional for confirmation.*")

                    except Exception as e:
                        st.error(f"Error generating image analysis: {e}")
            else:
                st.warning("Please type a question about the image.")
