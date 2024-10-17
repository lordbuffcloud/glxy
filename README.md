# GLXY - Agent Framework

![GLXY Logo](.glxy_logo.png)

**GLXY** is a powerful AI agent framework that integrates seamlessly into your workflows. It features a command-line interface for full control, helping you automate tasks, manage data, and boost productivity.

GLXY is proprietary and serves as the backbone of **King Digital Solutions**. Want GLXY in your apps or life? Head to [glxy.api](https://glxy.api) (coming soon).

## 🚀 Features

- **AI Text Embedding & Vector RAG**: Extract meaning and perform retrieval-augmented generation (RAG) with embeddings.
- **System Message Interchangeability**: Easily switch system messages for different conversation styles.
- **Video Translation to System Messages**: Convert video content into actionable system messages.
- **Automatic Text to Hosted Article**: Turn text into hosted articles instantly.
- **Multi-Model LLM Queries**: Use GPT-01, Claude 3.5, and local LLMs (via LM Studio) for top-tier responses.
- **Interchangeable API Integration**: Swap between AI models and APIs as needed.
- **Text to Hosted Website**: Transform text into websites, hosted and ready.
- **PC File Manipulation**: Use agent swarms to clean data, create JSONs, and more.
- **Automated Cybersecurity**: Red and blue team operations for security tasks.
- **Advanced Memory & Storage**: Store user data, including options for data brokers.
- **Constant Updates**: Features are added daily to keep GLXY at the forefront of automation.

## 💻 Command-Line Interface

GLXY comes with a simple command-line interface for easy task deployment.

### Command Help

- **Get Context**: Retrieve current AI context.
  ```bash
  glxy -h 
  ### provides link to this page
  ```
- **Create Embed**: Generate embeddings from text or file.
  ```bash
  glxy -f  <prompt_name> <file_or_text>
  ### Uses an extensive library of crowd sourced carefully engineered prompts
  ### This command alone is endless features as each gives the agents detailed instructions with the large library of tools to complete virtually any task.
    **For example**: glxy -f article <a bunch of text to make an article>
    ###This instructs the agents to craft an article by:
    - Using perplexity.ai / duckduck go api to research topic
    - Read system.md a system message that explains to the agents industry standard on online articles
    - Generates images 
    - Uses coding enviorment to create the file
    - Hosts to web and provides message in discord of successful (or unsuccessful) deployment

  ```
- **Extract Text from File**: Extract text from a file.
  ```bash
  glxy -tf <prompt> <youtube link>
  ### Transcribes video and then uses engineered prompt with transcription
  ```
- **Load Pattern**: Load a specific pattern.
  ```bash
  glx -file <file>
  ### Uploads file to directory. 
    - I use this to for instance upload an excel document and the use glxy -c to extract add data using code execution tool.
    - Use cases are endless.
  ```
- **Commands added everyday**: 
  ```bash
  ### Ill build a command for a customer test it with discord for interactionand then run the api or make an app :D
  ```


## 📞 Contact

Questions? Reach me at [GLXY.API](https://glxy.api).

---


