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

# -------------------------------
# LANGUAGE SELECTION
# -------------------------------
language = st.sidebar.selectbox("Select Language / மொழி தேர்வு:", ["English", "Tamil"])

# -------------------------------
# TEXT DICTIONARY
# -------------------------------
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
    "Useful Websites / பயனுள்ள இணையதளங்கள்"
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
        "nav": ["நிலை", "ரசாயனங்கள்", "பயிர் பரிந்துரை", "விவசாய செயல்பாடுகள்", "வணிகக் கருத்துகள்", "படப் பகுப்பு"],
        "placeholders": {
            "Land": "நிலத் தயாரிப்பு, மண் மேலாண்மை, நீர்ப்பாசனம் பற்றி கேளுங்கள்:",
            "Chemical": "சிறுதானியங்கள், பூச்சிக்கொல்லிகள் மற்றும் பாதுகாப்பான பயன்பாடு பற்றி கேளுங்கள்:",
            "Crop Suggestion": "எந்த பயிர்களை வளர்க்கலாம், சுழற்சி, விளைவு மேம்படுத்தல் பற்றி கேளுங்கள்:",
            "Farming Activity": "செயல்பாடுகள், சிறந்த பழக்கவழக்கங்கள் அல்லது தொழில்நுட்பங்கள் பற்றி கேளுங்கள்:",
            "Farming Business Idea": "விவசாயத்தை சார்ந்த வணிகக் கருத்துக்கள் மற்றும் நன்மைகள், தீமைகள் பற்றி கேளுங்கள்:",
            "Image": "இந்த படத்தைப் பற்றிப் கேளுங்கள்:"
        },
        "buttons": {
            "get_advice": "உதவி பெறுங்கள்",
            "analyze_image": "படத்தை பகுப்பாய்வு செய்"
        },
        "messages": {
            "type_question": "தயவு செய்து ஒரு கேள்வியை உள்ளிடுங்கள்.",
            "loading": "உதவி உருவாக்கப்படுகிறது...",
            "loading_image": "படத்தை பகுப்பாய்வு செய்கிறது..."
        }
    }
}

txt = text_dict[language]


# -------------------------------
# USEFUL WEBSITES PAGE
# -------------------------------
if page == "Useful Websites / பயனுள்ள இணையதளங்கள்":
    st.header("🔗 Useful Websites for Farmers / விவசாயிகளுக்கான பயனுள்ள இணையதளங்கள்")
    
    websites = [
        {
            "url": "https://www.tnagrisnet.tn.gov.in/esevai/",
            "title_en": "TN Agri E-Services",
            "title_ta": "தமிழ்நாடு விவசாய E-சேவைகள்",
            "desc_en": "Official Tamil Nadu government portal for agricultural services like scheme status, certificates, soil test, farmer records.",
            "desc_ta": "தமிழ்நாட்டுத் தமிழக அரசின் விவசாய சேவைகள்: திட்ட நிலை, சான்றிதழ்கள், மண் பரிசோதனை, விவசாயி பதிவுகள்."
        },
        {
            "url": "https://play.google.com/store/apps/details?id=agri.tnagri&hl=en_IN",
            "title_en": "TNAgrI (Mobile App)",
            "title_ta": "TNAgrI (மொபைல் செயலி)",
            "desc_en": "Mobile app for Tamil Nadu agriculture services; access schemes, weather updates, notifications and farmer info.",
            "desc_ta": "தமிழ்நாடு விவசாய சேவைகளுக்கான செயலி; திட்ட தகவல், வானிலை, அறிவிப்புகள் மற்றும் விவசாயி தகவல்."
        },
        {
            "url": "http://www.agritech.tnau.ac.in/",
            "title_en": "TNAU Agritech",
            "title_ta": "TNAU Agritech",
            "desc_en": "Tamil Nadu Agricultural University’s Agritech portal with scientific crop tips, technologies, and educational resources.",
            "desc_ta": "தமிழ்நாடு வேளாண்மை பல்கலைக்கழகத்தின் Agritech தளம்; விஞ்ஞானப் பயிர் அறிவுரைகள் மற்றும் தொழில்நுட்பங்கள்."
        },
        {
            "url": "https://tnhorticulture.tn.gov.in/",
            "title_en": "TN Horticulture Department",
            "title_ta": "தமிழ்நாடு விளைவுப் பகுதிகள் துறை",
            "desc_en": "Official site for Tamil Nadu horticulture — plant protection, nursery info, garden programs and schemes.",
            "desc_ta": "தமிழ்நாடு விளைவுப் பிரிவு அதிகார இணையதளம்; பிளாக் பாதுகாப்பு, நர்சரி தகவல், தோட்டத்திட்டங்கள்."
        },
        {
            "url": "https://enam.gov.in/web/stakeholders-Involved/farmers",
            "title_en": "eNAM (National Agriculture Market)",
            "title_ta": "eNAM (தேசிய விவசாய சந்தை)",
            "desc_en": "Portal connecting farmers, traders, and markets for transparent pricing and mandi operations.",
            "desc_ta": "விவசாயிகள், வர்த்தகர்கள் மற்றும் சந்தைகள் இடையே நேரடி விலையில் பரிவர்த்தனை செய்ய உதவும் தளம்."
        },
        {
            "url": "https://kisansarathi.in/",
            "title_en": "Kisan Sarathi",
            "title_ta": "கிசான் சாரதி",
            "desc_en": "AI-based farmer advisory portal offering crop plans, weather forecasts, and customized guidance.",
            "desc_ta": "பயிர் திட்டம், வானிலை முன்னறிவு மற்றும் தனிப்பயன் அறிவுரைகள் வழங்கும் விவசாயி உதவி தளம்."
        },
        {
            "url": "https://pmkisan.gov.in/",
            "title_en": "PM-Kisan Scheme",
            "title_ta": "பிஎம்-கிசான் திட்டம்",
            "desc_en": "Government of India income support scheme for farmers; registration, beneficiary status, payment info.",
            "desc_ta": "இந்திய அரசின் விவசாயிகளுக்கான வருமான உதவி திட்டம்; பதிவு, பயனாளி நிலை, பணம் விவரம்."
        },
        {
            "url": "https://agrimachinery.nic.in/index/index",
            "title_en": "Agricultural Machinery Portal",
            "title_ta": "வேளாண் இயந்திரங்கள் போர்டல்",
            "desc_en": "Central government’s portal on farm machinery — schemes, subsidies, and equipment info.",
            "desc_ta": "மத்திய அரசின் வேளாண் இயந்திர தகவல் தளம்; திட்டம், சலுகை, உபகரண விவரம்."
        }
    ]

    for site in websites:
        st.markdown(f"### 🔗 [{site['title_en']} / {site['title_ta']}]({site['url']})")
        if language == "Tamil":
            st.write(site["desc_ta"])
        else:
            st.write(site["desc_en"])

# -------------------------------
# PAGE TITLE & DESCRIPTION
# -------------------------------
st.title(txt["title"])
st.write(txt["desc"])

# -------------------------------
# PAGE NAVIGATION
# -------------------------------
page = st.sidebar.radio("Navigation / துவக்கம்:", txt["nav"])

# -------------------------------
# FUNCTION TO CALL AI
# -------------------------------
def get_ai_response(user_query, language):
    try:
        if language == "Tamil":
            user_query = f"உங்கள் பதில் தமிழ் மொழியில் அளிக்கவும்: {user_query}"
        response = model.generate_content(
            user_query,
            generation_config={"temperature": 0.3, "max_output_tokens": 2000}
        )
        return response.text
    except Exception as e:
        return f"Error generating AI response: {e}"

# -------------------------------
# TEXT-BASED PAGES
# -------------------------------
text_pages_map = {
    txt["nav"][0]: "Land",
    txt["nav"][1]: "Chemical",
    txt["nav"][2]: "Crop Suggestion",
    txt["nav"][3]: "Farming Activity",
    txt["nav"][4]: "Farming Business Idea"
}

if page in txt["nav"][:-1]:  # all except last
    key_name = text_pages_map[page]
    st.header(f"📝 {page}")
    query = st.text_area(txt["placeholders"][key_name])
    if st.button(txt["buttons"]["get_advice"], key=key_name):
        if query.strip():
            with st.spinner(txt["messages"]["loading"]):
                st.markdown(get_ai_response(query, language))
        else:
            st.warning(txt["messages"]["type_question"])

# -------------------------------
# IMAGE ANALYSIS PAGE
# -------------------------------
if page == txt["nav"][-1]:
    st.header("🖼️ Image-Based Plant Analysis / படப் பகுப்பு")
    uploaded_file = st.file_uploader("Upload an image / படத்தை பதிவேற்றவும்:", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image)
        image.thumbnail((1024, 1024))
        st.image(image, caption="Uploaded Image / பதிவேற்றப்பட்ட படம்", use_container_width=True)

        prompt_text = st.text_input(txt["placeholders"]["Image"])
        if st.button(txt["buttons"]["analyze_image"], key="image_analysis"):
            if prompt_text.strip():
                with st.spinner(txt["messages"]["loading_image"]):
                    try:
                        buffer = io.BytesIO()
                        image.save(buffer, format=image.format)
                        img_bytes = buffer.getvalue()
                        mime = uploaded_file.type

                        analysis_prompt = prompt_text
                        if language == "Tamil":
                            analysis_prompt = f"உங்கள் பதில் தமிழ் மொழியில் அளிக்கவும்: {prompt_text}"

                        response = model.generate_content(
                            [
                                analysis_prompt,
                                {"mime_type": mime, "data": img_bytes}
                            ],
                            generation_config={"temperature": 0.3, "max_output_tokens": 2000}
                        )

                        st.success("AI Image Analysis Result / AI பட பகுப்பு முடிவு:")
                        st.markdown(response.text + "\n\n*Disclaimer: This is an AI-generated probable diagnosis. Please consult a professional for confirmation.*")

                    except Exception as e:
                        st.error(f"Error generating image analysis: {e}")
            else:
                st.warning(txt["messages"]["type_question"])

