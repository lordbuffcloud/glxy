"""
╩╩╩╩╩╩╩___╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩
╩╩╩╩╩╩/\_ \╩╩╩3y5╩╩╩╩╩╩╩╩╩╩╩╩╩╩
╩╩╩__╩\//\ \╩╩╩__╩╩_╩__╩╩__╩╩╩╩
╩/'_ `\╩\╩\ \╩/\ \/'/\ \/\ \╩╩╩
/\ \L\ \╩\_\ \\/>  <\ \ \_\ \╩╩
\╩\____ \/\____/\_/\_\/`____ \╩
╩\/___L\ \/____\//\/_/`/___/> \
╩╩╩/\____/╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩/\___/
╩╩╩\_/__/╩╩╩╩╩xyo╩╩╩╩╩╩╩╩╩\/__/╩
"""
 
          GLXY Discord App
Introduction
Welcome to GLXY, an intelligent, multi-agent Discord bot. GLXY can engage in general conversation, perform web research, analyze documents, and even generate or execute code! Whether you’re a casual user or a tech enthusiast, GLXY is designed to be your virtual assistant on Discord.

Key Features
💬 General conversation with AI agents.
🔍 Web research using the Perplexity API.
📄 Document analysis through RAG (Retrieval-Augmented Generation).
🖥️ Code generation and execution.
🧠 Memory storage and retrieval capabilities.
Installation
Prerequisites
Before installing GLXY, ensure that you have:

Python 3.7+ installed.
A Discord account and Developer Portal access to create your bot.
API keys for integrated services (e.g., Perplexity, DeepInfra).
Step-by-Step Guide
Clone the Repository
Open your terminal and run:

bash
Copy code
git clone https://github.com/lordbuffcloud/glxy.git
Navigate to the Project Directory

bash
Copy code
cd glxy
Create a Virtual Environment
This helps keep your project dependencies isolated:

bash
Copy code
python -m venv venv
Activate the Virtual Environment

On Windows:
bash
Copy code
.\venv\Scripts\activate
On macOS and Linux:
bash
Copy code
source venv/bin/activate
Install Dependencies Ensure all required packages are installed:

bash
Copy code
pip install -r requirements.txt
Create a .env File
This file will store your sensitive keys. In the root directory, create a .env file and add your bot token and API keys:

env
Copy code
DISCORD_TOKEN=your_discord_bot_token
DEEPINFRA_API_KEY=your_deepinfra_api_key
Usage
Run the Bot
Start your Discord bot by running the following command:

bash
Copy code
python bot.py
Invite the Bot to Your Server
Head to the Discord Developer Portal, generate an OAuth2 URL, and invite your bot using the generated link.

Interact with GLXY
In your Discord server, use the following commands:

/chat [message]: Engage in conversation with GLXY.
/memory [operation] [key] [value]: Store or retrieve information from GLXY’s memory.
Troubleshooting
Common Issues and Solutions
Bot Not Responding?

Ensure the bot is online by checking the Discord Developer Portal.
Verify your token in the .env file is correct and valid.
Dependencies Not Installing?

Check if you’re using the correct Python version (3.7 or higher).
Ensure the virtual environment is activated before running installation commands.
Commands Not Working?

Confirm the bot has the necessary permissions within your Discord server.
Check the bot logs for any error messages, which can be found in the terminal where you ran python bot.py.
Contributing
We love contributions! If you have ideas for new features or improvements, feel free to fork the project and submit a pull request. Please ensure your code follows the project's style and standards.

License
This project is licensed under the MIT License.

Acknowledgements
discord.py
crewAI
DeepInfra