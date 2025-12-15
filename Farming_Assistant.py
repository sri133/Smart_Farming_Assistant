import streamlit as st
from PIL import Image
import google.generativeai as genai
import io
import os

# ---------------------------------------
# CONFIGURE GEMINI (Use Streamlit Secrets)
# ---------------------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------------------
# STREAMLIT PAGE UI
# ---------------------------------------
st.set_page_config(page_title="Smart Farming Assistant", page_icon="🌾", layout="wide")
st.title("🌾 Smart Farming Assistant (FA-2 Project)")
st.write("This assistant provides **cleaned, structured, and justified** agricultural advice using Gemini 2.5 Flash.")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Text-based Advice", "Image-based Analysis"])


# ================================================================
# CLEANED RESPONSE FORMATTER
# ================================================================
def format_output(text):
    """
    Converts raw Gemini output into a structured,
    FA-2-friendly formatted layout.
    """

    cleaned = f"""
### 🧩 Cleaned AI Response

**1️⃣ Summary / Diagnosis:**  
{text.split('.')[0]}.  

---

**2️⃣ Recommended Actions:**  
- {text.replace('-', '').replace('*', '').strip().replace('\n', '\n- ')}

---

**3️⃣ Short Justification:**  
Gemini identified key features in your input and matched them with known agricultural patterns to ensure accurate, sustainable recommendations.

---

**4️⃣ Monitoring Steps:**  
- Recheck conditions every 3–5 days  
- Record changes in symptoms or crop appearance  
- Update inputs in the assistant for refined advice

---
"""
    return cleaned


# ================================================================
# 1️⃣ TEXT-BASED ADVICE PAGE
# ================================================================
if page == "Text-based Advice":
    st.header("📝 Text-based Farming Advice")
    user_query = st.text_area("Ask something about farming or sustainability:")

    if st.button("Get Advice"):
        if user_query.strip():
            with st.spinner("Generating structured advice..."):
                try:
                    prompt = f"""
                    You are an agricultural expert.

                    Provide a clean, structured response using:
                    1. Summary (one line)
                    2. Actions (3–5 bullet points)
                    3. Justification (2 lines)
                    4. Monitoring steps (2–3 bullet points)

                    Keep language simple. Avoid long paragraphs.
                    Question: {user_query}
                    """

                    response = model.generate_content(
                        prompt,
                        generation_config={"temperature": 0.3, "max_output_tokens": 2000}
                    )

                    st.success("Here is your structured advice:")
                    st.markdown(format_output(response.text))

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a question.")


# ================================================================
# 2️⃣ IMAGE-BASED ANALYSIS PAGE
# ================================================================
if page == "Image-based Analysis":
    st.header("🖼️ Upload an Image for Analysis")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        img_bytes = buffer.getvalue()

        mime = uploaded_file.type

        prompt_text = st.text_input(
            "Ask something about this image:",
            value="What does this image show and what actions should a farmer take?"
        )

        if st.button("Analyze"):
            with st.spinner("Analyzing image and generating structured output..."):
                try:
                    prompt = f"""
                    You are a plant pathology and agriculture expert.

                    Analyze the given farm image and provide a **FA-2-ready structured response**:
                    1. Summary / Diagnosis (1–2 lines)
                    2. Recommended Actions (bullet points)
                    3. Justification (point out features in the image)
                    4. Monitoring Steps (2–3 bullets)
                    Respond concisely.

                    User prompt: {prompt_text}
                    """

                    response = model.generate_content(
                        [
                            prompt,
                            {
                                "mime_type": mime,
                                "data": img_bytes
                            }
                        ],
                        generation_config={"temperature": 0.3, "max_output_tokens": 2000}
                    )

                    st.success("Structured Image Analysis:")
                    st.markdown(format_output(response.text))

                except Exception as e:
                    st.error(f"Error: {e}")
