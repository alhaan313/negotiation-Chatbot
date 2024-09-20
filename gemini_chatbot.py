import google.generativeai as genai
import os

api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text