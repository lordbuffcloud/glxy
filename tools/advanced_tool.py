import requests
import os

class AdvancedAI:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_url = 'https://api.openai.com/v1/completions'
        self.groq_url = 'https://api.groq.com/calculate'  # Hypothetical

    def generate_openai_text(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "text-davinci-003",  # Example OpenAI model
            "prompt": prompt,
            "max_tokens": 100
        }
        response = requests.post(self.openai_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['text']
        else:
            return "Error in OpenAI text generation."

    def perform_groq_calculation(self, calculation_request):
        headers = {
            'Authorization': f'Bearer {self.groq_key}',
            'Content-Type': 'application/json'
        }
        data = {
            "calculation": calculation_request
        }
        response = requests.post(self.groq_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['result']
        else:
            return "Error in Groq calculation."
