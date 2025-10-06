import os
import google.generativeai as genai

# Replace with your actual Gemini API key if it's not in env vars
os.environ["GEMINI_API_KEY"] = "AIzaSyAf-uI66ynbbnshVTyE8xO2eXjmIgZedQ4"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\n🔍 Available Gemini models supporting text generation:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name, "-", m.supported_generation_methods)
