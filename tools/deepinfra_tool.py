import requests
import os
import base64
from io import BytesIO
from PIL import Image
class DeepInfraTool:
    def __init__(self):
        self.api_key = os.getenv("DEEPINFRA_API_KEY")
        self.text_model_url = 'https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3-8B-Instruct'
        self.image_model_url = 'https://api.deepinfra.com/v1/inference/stabilityai/stable-diffusion-2-1'

    def generate_text(self, prompt):
        """
        Generate text based on the prompt using the DeepInfra text generation model.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        body = {
            "input": prompt,
            "stop": ["<|end_of_text|>"]
        }
        response = requests.post(self.text_model_url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()['results'][0]['generated_text']
        else:
            return f"Error in text generation: {response.status_code} {response.text}"

    def generate_image(self, prompt):
        """
        Generate an image based on the given prompt using the DeepInfra image generation model (Stable Diffusion).
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        body = {
            "prompt": prompt  # Image prompt for generation
        }
        response = requests.post(self.image_model_url, headers=headers, json=body)
        if response.status_code == 200:
            # Get the Base64-encoded image string
            base64_image = response.json().get('images')[0]
            
            # Decode the Base64 string
            image_data = base64.b64decode(base64_image.split(',')[1])
            
            # Open the image using PIL and save it locally
            image = Image.open(BytesIO(image_data))
            file_path = f"generated_image.png"
            image.save(file_path)

            return file_path  # Return the path to the saved image file
        else:
            return f"Error in image generation: {response.status_code} {response.text}"