# Smart_Farming_Assistant
🌾 Smart Farming Assistant (FA-2 Project)
📌 Overview

Smart Farming Assistant is a Streamlit-based AI application designed to provide clean, structured, and responsible agricultural guidance.
It supports both text-based farming queries and image-based crop/plant analysis, making it suitable for school-level projects and evaluations.

The app uses Google Gemini AI to generate expert-like responses while clearly stating uncertainty and promoting safe, sustainable practices.

🎯 Project Objectives

Assist farmers/students with basic agricultural decision-making

Demonstrate responsible use of AI in agriculture

Provide structured, easy-to-understand responses

Avoid unsafe or strong chemical recommendations

Suitable for FA-2 academic evaluation

🧠 Key Features
📝 Text-based Farming Advice

Ask questions about:

Crop health

Soil management

Sustainability

Farming best practices

AI responses are structured into:

Summary / Diagnosis

Recommended Actions

Justification

Monitoring Steps

Uses simple, school-appropriate language

🖼️ Image-based Crop Analysis

Upload plant or crop images (jpg, jpeg, png)

AI provides a probable diagnosis, not absolute claims

Includes:

Visible symptom-based reasoning

Safe and practical action steps

Monitoring guidance with time references

Automatically adds a professional disclaimer

🧠 How It Works

User selects a mode from the sidebar:

Text-based Advice

Image-based Analysis

The query or image is sent to Google Gemini AI

The response is formatted to ensure:

Safety

Clarity

Structured output

Responsible AI usage

🛠️ Tech Stack

Python

Streamlit

Google Gemini API

Pillow (PIL)

🔐 Environment Variables

The app uses Streamlit Secrets for API key management.

GEMINI_API_KEY = "your_google_gemini_api_key"


⚠️ Never commit API keys to GitHub.

🚀 Deployment

This app is already deployed using Streamlit Cloud and connected directly to this GitHub repository.

Any push to the main branch automatically updates the live app.

⚠️ Disclaimer

This application provides AI-generated probable agricultural advice only.
It is not a substitute for professional agricultural consultation.

📚 Academic Use

Suitable for school FA-2 / internal assessments

Demonstrates:

Responsible AI usage

Explainable outputs

Ethical AI deployment

🔮 Future Improvements

Crop-specific recommendations

Weather-based insights

Regional language support

Downloadable reports
