import requests
import os

class DeepInfraTool:
    def __init__(self):
        self.api_key = os.getenv("DEEPINFRA_API_KEY")
        self.text_model_url = 'https://api.deepinfra.com/v1/openai/chat/completions'

    def generate_text(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        body = {
            "model": "mattshumer/Reflection-Llama-3.1-70B",  # Change to Reflection-Llama
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.text_model_url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: Unable to process your request. Please try again. [Code: {response.status_code}]"

