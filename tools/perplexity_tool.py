import requests
import os

class PerplexityTool:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")

    def perform_research(self, query):
        url = "https://api.perplexity.ai/v1/search"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "query": query,
            "num_results": 5
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            results = response.json()
            if "results" in results:
                return "\n".join([f"{i+1}: {item['title']} - {item['snippet']}" for i, item in enumerate(results["results"])])
            else:
                return "No results found."
        except requests.RequestException as e:
            return f"Error during research: {str(e)}"
