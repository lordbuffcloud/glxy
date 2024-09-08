# GLXY Discord Bot

GLXY is an intelligent multi-agent Discord bot designed to handle various tasks including general conversation, web research, document analysis, and code execution.

## Features

- General conversation using AI agents
- Web research capabilities using Perplexity API
- Document analysis and RAG (Retrieval-Augmented Generation)
- Code execution and generation
- Memory storage and retrieval

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lordbuffcloud/glxy.git
   ```

2. Navigate to the project directory:
   ```
   cd glxy
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the root directory and add your Discord bot token and other necessary API keys:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   DEEPINFRA_API_KEY=your_deepinfra_api_key
   ```

## Usage

1. Run the bot:
   ```
   python bot.py
   ```

2. Invite the bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.

3. Use the following commands in your Discord server:
   - `/chat [message]`: Interact with the multi-agent system
   - `/memory [operation] [key] [value]`: Store or retrieve information from the bot's memory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [crewAI](https://github.com/joaomdmoura/crewAI)
- [DeepInfra](https://deepinfra.com/)
