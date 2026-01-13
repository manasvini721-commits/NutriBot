import os
import google.generativeai as genai

# Configure Gemini ONLY from environment / secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("\n🔍 Available Gemini models supporting text generation:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name, "-", m.supported_generation_methods)

