import discord
from discord import app_commands
import os
from crew import setup_crew
import asyncio
from dotenv import load_dotenv
import animations
import shlex
import json
import subprocess   

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
DISCORD_CHAT_TOKEN = os.getenv("DISCORD_CHAT_TOKEN")
STARTUP_CHANNEL_ID = os.getenv("STARTUP_CHANNEL_ID")

# Initialize CrewAI with hierarchical agents
crew = setup_crew()

@bot.event
async def on_ready():
    # Send startup message when the bot goes online
    channel = bot.get_channel(int(STARTUP_CHANNEL_ID))
    
    if channel:
        # Send instructions in the style of Elon Musk
        instructions = (
            "**Hey, it's glxy-musk here.** Welcome to your AI assistant. Here’s how you can use this bot to do some really mind-blowing things."
            "\n\n**/chat** – Wanna talk to multiple specialized agents at once? This is your command. You ask something, and boom, the agents collaborate to deliver an answer. It’s like having a team of experts at your fingertips."
            "\n\n**/image** – Got an image you need processed? Upload it, and this bot will run some insane image analysis with AI. We’re talking next-level vision."
            "\n\n**/doc** – Throw in a document, and let the AI dissect it, process it, and give you the important stuff. No more skimming through endless pages."
            "\n\n**/code** – Enter your code, and this bot executes it in a sandbox. It’s basically a tiny developer running your scripts. Just be safe, okay? Don’t break the internet."
            "\n\n**/memory** – This one’s for when you need the bot to remember things. Store information here, and it’s ready for future reference. Think of it like a hard drive for your conversations."
            "\n\nSo, use these wisely, because they are powerful tools. Like I always say, we’re building the future, one command at a time. 🚀"
        )

        await channel.send(instructions)
        print(f"Instructions sent to channel {STARTUP_CHANNEL_ID}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    

# bot.py (Rich Embed Enhancements)

# Startup Animation with Rich Embeds
@tree.command(name="startup", description="Show startup animations with rich embeds")
async def startup(interaction: discord.Interaction, product: str):
    try:
        embed = discord.Embed(title="Initializing", description=f"Starting {product}...", color=0x00ff00)
        message = await interaction.response.send_message(embed=embed)
        
        for i in range(3):
            embed.description += "."
            await message.edit(embed=embed)
            await asyncio.sleep(1)
        
        embed.description = f"{product} Initialized!"
        await message.edit(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# Thinking Animation with Rich Embeds
async def thinking_animation(interaction: discord.Interaction):
    embed = discord.Embed(title="Thinking", description="Please wait while we process...", color=0x00ff00)
    message = await interaction.response.send_message(embed=embed)
    
    frames = ["Thinking.", "Thinking..", "Thinking..."]
    i = 0
    while True:
        embed.description = frames[i % len(frames)]
        await message.edit(embed=embed)
        await asyncio.sleep(1)
        i += 1

# Enhanced Multi-Agent Command: /chat
# bot.py (Enhance /chat Command for Deep Research)

@tree.command(name="chat", description="Chat with an intelligent multi-agent system for deep research")
async def chat(interaction: discord.Interaction, message: str):
    try:
        # Send an initial response
        await interaction.response.send_message("Processing your request...")

        # General agent for basic conversation
        general_agent_response = crew.handle_task("general", message)
        
        # Research agent for deep web research using Perplexity API
        web_research_agent_response = crew.handle_task("research", message)
        
        # Document agent for document analysis
        document_agent_response = crew.handle_task("document", message)
        
        # Code agent for code execution tasks
        code_agent_response = crew.handle_task("code", message)

        # Combine responses
        combined_response = (
            f"General Agent: {general_agent_response}\n"
            f"Research Agent: {web_research_agent_response}\n"
            f"Document Agent: {document_agent_response}\n"
            f"Code Agent: {code_agent_response}"
        )

        # Handling large responses
        if len(combined_response) > 2000:
            chunks = [combined_response[i:i + 2000] for i in range(0, len(combined_response), 2000)]
            for chunk in chunks:
                await interaction.followup.send(chunk)
        else:
            await interaction.followup.send(combined_response)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# bot.py (Enhanced /image and /doc Commands)

# Enhanced Image Command with RAG
@tree.command(name="image", description="Process image files with RAG")
async def image(interaction: discord.Interaction, attachment: discord.Attachment):
    try:
        file_path = f"./images/{attachment.filename}"
        await attachment.save(file_path)
        await interaction.response.send_message(f"Image {attachment.filename} saved and processed.")
        
        # Process image with RAG (handled by crew agent)
        result = crew.handle_task(f"Process image with RAG: {file_path}")
        await interaction.followup.send(result)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# Enhanced Document Command with RAG
@tree.command(name="doc", description="Process document files with RAG")
async def doc(interaction: discord.Interaction, attachment: discord.Attachment):
    try:
        file_path = f"./docs/{attachment.filename}"
        await attachment.save(file_path)
        await interaction.response.send_message(f"Document {attachment.filename} saved and processed.")
        
        # Process document with RAG (handled by crew agent)
        result = crew.handle_task(f"Process document with RAG: {file_path}")
        await interaction.followup.send(result)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# Command: /code
@tree.command(name="code", description="Execute code in a sandbox environment")
async def code(interaction: discord.Interaction, script: str):
    try:
        # Sanitize the input and run in a sandbox
        sanitized_script = shlex.quote(script)
        result = subprocess.run(f"python3 -c {sanitized_script}", shell=True, capture_output=True, timeout=5)
        
        output = result.stdout.decode() if result.stdout else "No output"
        error = result.stderr.decode() if result.stderr else "No errors"
        
        await interaction.response.send_message(f"Output:\n{output}\nErrors:\n{error}")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")
# Command: /memory
@tree.command(name="memory", description="Manage memory operations")
async def memory(interaction: discord.Interaction, operation: str, key: str, value: str = None):
    memory_file = "./memory/memory.json"
    
    if operation.lower() not in ["store", "retrieve"]:
        await interaction.response.send_message("Invalid operation. Use 'store' or 'retrieve'.")
        return

    try:
        with open(memory_file, 'r') as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        memory_data = {}

    if operation.lower() == "store":
        if value is None:
            await interaction.response.send_message("Value is required for store operation.")
            return
        memory_data[key] = value
        with open(memory_file, 'w') as f:
            json.dump(memory_data, f)
        await interaction.response.send_message(f"Memory saved: {key} -> {value}")
    
    elif operation.lower() == "retrieve":
        if key in memory_data:
            await interaction.response.send_message(f"Retrieved: {key} -> {memory_data[key]}")
        else:
            await interaction.response.send_message(f"No memory found for key: {key}")

# Command: /hi
@tree.command(name="hi", description="Engage in a conversation with memory")
async def hi(interaction: discord.Interaction):
    try:
        # Call the agent for a simple conversation using stored memory
        result = crew.handle_task("Engage in conversation using memory.")
        await interaction.response.send_message(result)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

# Startup actions
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await tree.sync()

    if STARTUP_CHANNEL_ID:
        channel = bot.get_channel(int(STARTUP_CHANNEL_ID))
        if channel:
            await channel.send("Hello! I'm ready to process your documents and images.")

if __name__ == "__main__":
    bot.run(DISCORD_CHAT_TOKEN)
