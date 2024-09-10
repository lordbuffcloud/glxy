import requests
import os

class DeepInfraTool:
    def __init__(self):
        self.api_key = os.getenv("DEEPINFRA_API_KEY")
        self.text_model_url = 'https://api.deepinfra.com/v1/openai/chat/completions'
        self.image_model_url = 'https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-1-dev'

    def generate_text(self, prompt, task_type='chat'):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        model = self._get_model_for_task(task_type)
        
        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(self.text_model_url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: Unable to process your request. Please try again. [Code: {response.status_code}]"

    def generate_image(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        body = {
            "input": {
                "prompt": prompt
            }
        }
        
        response = requests.post(self.image_model_url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()['output']  # This should be the URL or base64 of the generated image
        else:
            return f"Error: Unable to generate image. Please try again. [Code: {response.status_code}]"

    def _get_model_for_task(self, task_type):
        if task_type == 'hard':
            return "meta-llama/Meta-Llama-3.1-405B-Instruct"
        elif task_type == 'easy':
            return "mistralai/Mistral-Nemo-Instruct-2407"
        elif task_type == 'chat':
            return "Sao10K/L3-70B-Euryale-v2.1"
        else:
            return "Sao10K/L3-70B-Euryale-v2.1"  # Default to chat model