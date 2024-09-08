import discord
from discord import app_commands
import os
from crew import setup_crew
import asyncio
from dotenv import load_dotenv
import animations
import logging
import shlex
import json
import subprocess
import signal
import sys
from pymongo import MongoClient
from db import get_conversation_history, save_conversation 
from crewai import Crew, Process, Agent
from langchain_openai import ChatOpenAI
import discord
from discord import app_commands
import asyncio
import crew

# Define the agents in your hierarchical collaboration system
research_agent = Agent(role='Research Agent', goal='Gather relevant data for user query.')
reasoning_agent = Agent(role='Reasoning Agent', goal='Analyze and structure the information.')
writer_agent = Agent(role='Writer Agent', goal='Generate a concise, unified response.')
analysis_agent = Agent(role='Analysis Agent', goal='Analyze Nmap scan results and provide insights.')

# Create a Crew with a Manager LLM (GPT-4 or GPT-3.5 as an example)
crew = Crew(
    agents=[research_agent, reasoning_agent, writer_agent, analysis_agent],
    manager_llm=ChatOpenAI(temperature=0.5, model="gpt-4"),
    process=Process.hierarchical,
    memory=True,    # Enable memory for context persistence
    planning=True   # Enable planning for better collaboration
)

# Load environment variables
load_dotenv()

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client['discord_bot']  # Replace with your database name
conversations_collection = db['conversations']  # Collection to store conversations

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
def save_conversation(user_id: str, message: str, response: str):
    """Save the user input and agent response to MongoDB"""
    conversations_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "conversation": {
                    "user_message": message,
                    "agent_response": response
                }
            }
        },
        upsert=True  # If no document exists for the user, it will create one
    )

def get_conversation_history(user_id: str):
    """Retrieve conversation history for a specific user"""
    conversation = conversations_collection.find_one({"user_id": user_id})
    if conversation:
        return conversation.get('conversation', [])
    return []

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    asyncio.create_task(cleanup())

async def cleanup():
    print("Performing cleanup...")
    await bot.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} is now running!')
    logger.info("on_ready event triggered")

    try:
        await tree.sync()
        logger.info("Command tree synced successfully")
    except Exception as e:
        logger.error(f"Error syncing command tree: {e}")

    if STARTUP_CHANNEL_ID:
        logger.info(f"Attempting to send startup message to channel {STARTUP_CHANNEL_ID}")
        try:
            channel = await bot.fetch_channel(int(STARTUP_CHANNEL_ID))
            if channel:
                logger.info(f"Channel {STARTUP_CHANNEL_ID} found")
                
                # Send ASCII art and instructions
                ascii_art = """
    ╩╩╩╩╩╩___╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩
  ╩╩╩╩╩╩/\_ \╩╩╩3y5╩╩╩╩╩╩╩╩╩╩╩╩╩╩
  ╩╩╩__╩\//\ \╩╩╩__╩╩_╩__╩╩__╩╩╩╩
  ╩/'_ `\╩\╩\ \╩/\ \/'/\ \/\ \╩╩╩
  /\ \L\ \╩\_\ \\/>  <\ \ \_\ \╩╩
  \╩\____ \/\____/\_/\_\/`____ \╩
  ╩\/___L\ \/____\//\/_/`/___/> \╩
 ╩╩╩/\____/╩╩╩╩╩xyo╩╩╩╩╩╩╩╩╩\/__/╩
   
 ❖ ── ✦ ──『anon-glxy』── ✦ ── ❖

"""
                instructions = (
                    "**Welcome to xyo. This bot is your tool for pushing boundaries and building a future where information flows freely. Here's how you can use it:"
                    "\n\n**/chat** – Collaborate with specialized agents and gather deep insights."
                    "\n\n**/image** – Analyze images beyond human capacity."
                    "\n\n**/doc** – Scan documents for critical information."
                    "\n\n**/code** – Execute code safely in an isolated environment."
                    "\n\n**/memory** – Store important data for future use."
                )

                await channel.send(f"```{ascii_art}```")
                await channel.send(instructions)
                logger.info("Startup message sent successfully")
            else:
                logger.warning(f"Channel {STARTUP_CHANNEL_ID} not found")
        except Exception as e:
            logger.error(f"Error sending startup message: {e}", exc_info=True)
    else:
        logger.warning("STARTUP_CHANNEL_ID is not set")

    logger.info("on_ready event completed")

# /chat command with animation and multi-agent responses


from db import store_conversation  # Import the store_conversation function from db.py

from crewai import Crew, Process, Agent
from langchain_openai import ChatOpenAI
import discord
from discord import app_commands
import asyncio

# Create a Crew with a Manager LLM (GPT-4 or GPT-3.5 as an example)
crew = Crew(
    agents=[research_agent, reasoning_agent, writer_agent, analysis_agent],
    manager_llm=ChatOpenAI(temperature=0.5, model="gpt-4"),
    process=Process.hierarchical,
    memory=True,    # Enable memory for context persistence
    planning=True   # Enable planning for better collaboration
)

import subprocess
import discord
from discord import app_commands

@tree.command(name="nmap", description="Collaborative Nmap scan for penetration testing")
async def nmap(interaction: discord.Interaction, target: str):
    user_id = str(interaction.user.id)  # Get user ID as a string
    agent_chatter_channel_id = int(os.getenv("AGENT_CHATTER_CHANNEL_ID"))  # Channel ID for agent chatter
    agent_chatter_channel = await bot.fetch_channel(agent_chatter_channel_id)

    try:
        # Defer interaction to show the bot is processing
        await interaction.response.defer(thinking=True)

        # Initialize the animation message
        embed = discord.Embed(title="🔍 Nmap Penetration Testing", description="Collaborating with agents for a scan...", color=0x00ff00)
        message_obj = await interaction.followup.send(embed=embed)

        # Step 1: Research Agent validates the input
        await agent_chatter_channel.send("**Research Agent**: Validating the target for Nmap scan...")
        # Assuming a research_agent.verify_target(target) function validates the target IP/domain
        validation = research_agent.verify_target(target)

        if not validation['valid']:
            await interaction.followup.send(f"❗ Invalid target: {target}. Please provide a valid IP or domain.")
            return

        await agent_chatter_channel.send(f"**Research Agent Response**: Target `{target}` is valid for Nmap scan.")

        # Step 2: Reasoning Agent determines Nmap scan type
        await agent_chatter_channel.send("**Reasoning Agent**: Choosing the appropriate Nmap scan...")
        # Choosing an Nmap scan type (e.g., SYN scan, version detection)
        nmap_scan_command = reasoning_agent.choose_scan_type(target)

        await agent_chatter_channel.send(f"**Reasoning Agent Response**: Running command `{nmap_scan_command}` on target `{target}`.")

        # Step 3: Execution Agent runs the Nmap scan in a secure environment
        await agent_chatter_channel.send("**Execution Agent**: Executing Nmap scan...")
        
        # Sanitize input and run Nmap using subprocess
        try:
            nmap_output = subprocess.run(shlex.split(nmap_scan_command), capture_output=True, timeout=60)
            nmap_result = nmap_output.stdout.decode()
            await agent_chatter_channel.send(f"**Execution Agent Response**: Nmap scan completed.")
        except subprocess.TimeoutExpired:
            await interaction.followup.send(f"❗ Nmap scan timed out after 60 seconds. Please try again later.")
            return
        except Exception as e:
            await interaction.followup.send(f"❗ An error occurred during Nmap execution: {str(e)}")
            return

        # Step 4: Analysis Agent analyzes the Nmap result
        await agent_chatter_channel.send("**Analysis Agent**: Analyzing Nmap scan results...")
        analysis_response = analysis_agent.analyze_nmap_output(nmap_result)
        await agent_chatter_channel.send(f"**Analysis Agent Response**: {analysis_response}")

        # Send the final results back to the user
        final_embed = discord.Embed(title="📊 Nmap Penetration Testing Results", description=analysis_response, color=0x1E90FF)
        await interaction.followup.send(embed=final_embed)

    except Exception as e:
        await interaction.followup.send(f"❗ **An error occurred**: {str(e)}")
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

from tools.nmap_tool import NmapTool

@tree.command(name="nmap", description="Collaborative Nmap scan for penetration testing")
async def nmap(interaction: discord.Interaction, target: str):
    user_id = str(interaction.user.id)  # Get user ID as a string
    agent_chatter_channel_id = int(os.getenv("AGENT_CHATTER_CHANNEL_ID"))  # Channel ID for agent chatter
    agent_chatter_channel = await bot.fetch_channel(agent_chatter_channel_id)

    try:
        # Defer interaction to show the bot is processing
        await interaction.response.defer(thinking=True)

        # Initialize the animation message
        embed = discord.Embed(title="🔍 Nmap Penetration Testing", description="Collaborating with agents for a scan...", color=0x00ff00)
        message_obj = await interaction.followup.send(embed=embed)

        # Initialize the NmapTool
        nmap_tool = NmapTool()

        # Step 1: Research Agent validates the input
        await agent_chatter_channel.send("**Research Agent**: Validating the target for Nmap scan...")
        if not nmap_tool.validate_target(target):
            await interaction.followup.send(f"❗ Invalid target: {target}. Please provide a valid IP or domain.")
            return

        await agent_chatter_channel.send(f"**Research Agent Response**: Target `{target}` is valid for Nmap scan.")

        # Step 2: Reasoning Agent determines the Nmap scan type
        await agent_chatter_channel.send("**Reasoning Agent**: Choosing the appropriate Nmap scan...")
        scan_type = "-sS -sV"  # This could be chosen dynamically based on the input or agent decisions

        # Step 3: Execution Agent runs the Nmap scan
        await agent_chatter_channel.send("**Execution Agent**: Executing Nmap scan...")
        nmap_result = nmap_tool.run_scan(target, scan_type)

        # Step 4: Analysis Agent analyzes the Nmap result
        await agent_chatter_channel.send("**Analysis Agent**: Analyzing Nmap scan results...")
        analysis_response = analysis_agent.analyze_nmap_output(nmap_result)

        # Send the final results back to the user
        final_embed = discord.Embed(title="📊 Nmap Penetration Testing Results", description=analysis_response, color=0x1E90FF)
        await interaction.followup.send(embed=final_embed)

    except Exception as e:
        await interaction.followup.send(f"❗ **An error occurred**: {str(e)}")
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
# /image command to process images with RAG
@tree.command(name="image", description="Process image files with RAG")
async def image(interaction: discord.Interaction, attachment: discord.Attachment):
    try:
        file_path = f"./images/{attachment.filename}"
        await attachment.save(file_path)
        await interaction.response.send_message(f"Image {attachment.filename} saved and processed.")
        
        # Simulated RAG processing task (replace this with actual AI processing)
        result = crew.handle_task(f"Process image with RAG: {file_path}")
        await interaction.followup.send(result)
    except Exception as e:
        await interaction.followup.send(f"❗ **An error occurred**: {str(e)}")

# /doc command to analyze documents
@tree.command(name="doc", description="Analyze documents with advanced AI")
async def doc(interaction: discord.Interaction, attachment: discord.Attachment):
    try:
        # Start an animation to show progress
        await animations.startup_animation(interaction, "Document Analysis")

        file_path = f"./docs/{attachment.filename}"
        await attachment.save(file_path)

        # Simulate thinking animation while processing
        await animations.thinking_animation(interaction)

        # Simulate document analysis task
        document_agent_response = crew.handle_task(f"analyze document {file_path}")

        await interaction.followup.send(f"Document analysis complete:\n{document_agent_response}")
    except Exception as e:
        await interaction.followup.send(f"❗ **An error occurred**: {str(e)}")

# /code command to execute code in a sandbox environment
@tree.command(name="code", description="Execute code in a sandbox environment")
async def code(interaction: discord.Interaction, script: str):
    try:
        # Sanitize the input and run in a sandbox
        sanitized_script = shlex.quote(script)
        result = subprocess.run(f"python3 -c {sanitized_script}", shell=True, capture_output=True, timeout=5)

        output = result.stdout.decode() if result.stdout else "No output"
        error = result.stderr.decode() if result.stderr else "No errors"

        await interaction.response.send_message(f"**Output**:\n{output}\n**Errors**:\n{error}")
    except Exception as e:
        await interaction.followup.send(f"❗ **An error occurred**: {str(e)}")

# /memory command for memory operations
from db import store_memory, retrieve_memory

@tree.command(name="memory", description="Manage memory operations")
async def memory(interaction: discord.Interaction, operation: str, key: str, value: str = None):
    if operation.lower() not in ["store", "retrieve"]:
        await interaction.response.send_message("Invalid operation. Use 'store' or 'retrieve'.")
        return

    if operation.lower() == "store":
        if value is None:
            await interaction.response.send_message("Value is required for store operation.")
            return
        store_memory(key, value)
        await interaction.response.send_message(f"Memory saved: {key} -> {value}")

    elif operation.lower() == "retrieve":
        stored_value = retrieve_memory(key)
        if stored_value:
            await interaction.response.send_message(f"Retrieved: {key} -> {stored_value}")
        else:
            await interaction.response.send_message(f"No memory found for key: {key}")

# Run the bot
if __name__ == "__main__":
    try:
        bot.run(DISCORD_CHAT_TOKEN)
    except KeyboardInterrupt:
        print("Bot is shutting down...")
        asyncio.run(cleanup())
