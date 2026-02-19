import streamlit as st
from PIL import Image, ImageOps
import io
import google.generativeai as genai
import time

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="Cronus", page_icon="🌾", layout="wide")

# ---------------------------------------
# LOAD MODEL (Cached)
# ---------------------------------------
@st.cache_resource
def load_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-2.5-flash")

model = load_model()

# ---------------------------------------
# LANGUAGE SELECTION
# ---------------------------------------
language = st.sidebar.selectbox("Select Language / மொழி தேர்வு:", ["English", "Tamil"])

# ---------------------------------------
# TEXT DICTIONARY
# ---------------------------------------
text_dict = {
    "English": {
        "title": "🌾 Cronus - Smart Farming Assistant for Tamil Nadu Farmers",
        "desc": "Ask anything about farming, crops, land, chemicals, or business ideas and get AI-powered advice.",
        "nav": [
            "Land",
            "Chemical",
            "Crop Suggestion",
            "Farming Activity",
            "Farming Business Idea",
            "Image Analysis",
            "Useful Websites"
        ],
        "placeholders": {
            "Land": "Ask about land preparation, soil management, or irrigation:",
            "Chemical": "Ask about fertilizers, pesticides, and safe usage:",
            "Crop Suggestion": "Ask about which crops to grow, rotations, or yield optimization:",
            "Farming Activity": "Ask for activity tips, best practices, or techniques:",
            "Farming Business Idea": "Ask about farming-related business ideas with pros and cons:",
            "Image": "Ask a question about this image:"
        },
        "buttons": {
            "get_advice": "Get Advice",
            "analyze_image": "Analyze Image"
        },
        "messages": {
            "type_question": "Please type a question.",
            "loading": "Generating advice...",
            "loading_image": "Analyzing image..."
        }
    },
    "Tamil": {
        "title": "🌾 கிரோனஸ் - தமிழ்நாடு விவசாயிகளுக்கான புத்திசாலி உதவியாளர்",
        "desc": "விவசாயம், பயிர்கள், நிலம், ரசாயனங்கள் அல்லது வணிகக் கருத்துக்கள் குறித்து கேளுங்கள், AI மூலம் பதில் பெறுங்கள்.",
        "nav": [
            "நிலை",
            "ரசாயனங்கள்",
            "பயிர் பரிந்துரை",
            "விவசாய செயல்பாடுகள்",
            "வணிகக் கருத்துகள்",
            "படப் பகுப்பு",
            "பயனுள்ள இணையதளங்கள்"
        ],
        "placeholders": {
            "Land": "நிலத் தயாரிப்பு, மண் மேலாண்மை, நீர்ப்பாசனம் பற்றி கேளுங்கள்:",
            "Chemical": "உரங்கள், பூச்சிக்கொல்லிகள் மற்றும் பாதுகாப்பான பயன்பாடு பற்றி கேளுங்கள்:",
            "Crop Suggestion": "எந்த பயிர்களை வளர்க்கலாம், சுழற்சி பற்றி கேளுங்கள்:",
            "Farming Activity": "சிறந்த தொழில்நுட்பங்கள் பற்றி கேளுங்கள்:",
            "Farming Business Idea": "விவசாய வணிகக் கருத்துக்கள் பற்றி கேளுங்கள்:",
            "Image": "இந்த படத்தைப் பற்றிக் கேளுங்கள்:"
        },
        "buttons": {
            "get_advice": "உதவி பெறுங்கள்",
            "analyze_image": "படத்தை பகுப்பாய்வு செய்"
        },
        "messages": {
            "type_question": "தயவு செய்து ஒரு கேள்வியை உள்ளிடுங்கள்.",
            "loading": "உதவி உருவாக்கப்படுகிறது...",
            "loading_image": "படம் பகுப்பாய்வு செய்யப்படுகிறது..."
        }
    }
}

txt = text_dict[language]

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title(txt["title"])
st.write(txt["desc"])

# ---------------------------------------
# NAVIGATION
# ---------------------------------------
page = st.sidebar.radio("Navigation / துவக்கம்:", txt["nav"])

# ---------------------------------------
# AI FUNCTION
# ---------------------------------------
SYSTEM_PROMPT = """
You are Cronus, a smart farming assistant for Tamil Nadu farmers.
Provide safe, practical, agriculture-related advice.
Do not give harmful, illegal, or unsafe instructions.
Structure answers clearly with:
1. Explanation
2. Steps
3. Safety tips
4. Tamil Nadu relevance
"""

def get_ai_response(user_query):
    try:
        if language == "Tamil":
            user_query = f"உங்கள் பதில் தமிழ் மொழியில் அளிக்கவும்:\n{user_query}"

        response = model.generate_content(
            [SYSTEM_PROMPT, user_query],
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1500
            }
        )
        return response.text
    except Exception:
        return "AI service is temporarily unavailable. Please try again."

# ---------------------------------------
# TEXT PAGES
# ---------------------------------------
text_pages_map = {
    txt["nav"][0]: "Land",
    txt["nav"][1]: "Chemical",
    txt["nav"][2]: "Crop Suggestion",
    txt["nav"][3]: "Farming Activity",
    txt["nav"][4]: "Farming Business Idea"
}

if page in txt["nav"][:5]:
    key_name = text_pages_map[page]
    st.header(f"📝 {page}")
    query = st.text_area(txt["placeholders"][key_name])

    if st.button(txt["buttons"]["get_advice"]):
        if query.strip():
            with st.spinner(txt["messages"]["loading"]):
                st.markdown(get_ai_response(query))
        else:
            st.warning(txt["messages"]["type_question"])

# ---------------------------------------
# IMAGE ANALYSIS
# ---------------------------------------
if page == txt["nav"][5]:
    st.header("🖼️ Image Analysis")
    uploaded_file = st.file_uploader("Upload image:", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image)
        image.thumbnail((1024, 1024))
        st.image(image, use_container_width=True)

        prompt_text = st.text_input(txt["placeholders"]["Image"])

        if st.button(txt["buttons"]["analyze_image"]):
            if prompt_text.strip():
                with st.spinner(txt["messages"]["loading_image"]):
                    try:
                        buffer = io.BytesIO()
                        image.save(buffer, format="PNG")
                        img_bytes = buffer.getvalue()

                        if language == "Tamil":
                            prompt_text = f"உங்கள் பதில் தமிழ் மொழியில் அளிக்கவும்:\n{prompt_text}"

                        response = model.generate_content(
                            [
                                SYSTEM_PROMPT,
                                prompt_text,
                                {"mime_type": "image/png", "data": img_bytes}
                            ],
                            generation_config={
                                "temperature": 0.3,
                                "max_output_tokens": 1500
                            }
                        )

                        st.success("AI Analysis Result:")
                        st.markdown(response.text)
                        st.info("Disclaimer: This is AI-generated guidance. Consult experts for confirmation.")

                    except Exception:
                        st.error("Error generating image analysis.")
            else:
                st.warning(txt["messages"]["type_question"])

# ---------------------------------------
# USEFUL WEBSITES PAGE
# ---------------------------------------
if page == txt["nav"][6]:
    st.header("🔗 Useful Websites")

    websites = [
        ("TN Agri E-Services", "https://www.tnagrisnet.tn.gov.in/esevai/",
         "Government agricultural services, scheme status, soil testing."),
        ("TNAgrI App", "https://play.google.com/store/apps/details?id=agri.tnagri&hl=en_IN",
         "Tamil Nadu agriculture mobile app with scheme & weather updates."),
        ("TNAU Agritech", "http://www.agritech.tnau.ac.in/",
         "Scientific crop practices and university-backed guidance."),
        ("TN Horticulture", "https://tnhorticulture.tn.gov.in/",
         "Horticulture schemes and plant protection info."),
        ("eNAM", "https://enam.gov.in/web/stakeholders-Involved/farmers",
         "National agriculture market for mandi pricing."),
        ("Kisan Sarathi", "https://kisansarathi.in/",
         "AI advisory with crop planning & forecasts."),
        ("PM-Kisan", "https://pmkisan.gov.in/",
         "Farmer income support scheme portal."),
        ("Agri Machinery Portal", "https://agrimachinery.nic.in/index/index",
         "Farm machinery schemes and subsidy information.")
    ]

    for name, url, desc in websites:
        st.markdown(f"### 🔗 [{name}]({url})")
        st.write(desc)
        st.markdown("---")

