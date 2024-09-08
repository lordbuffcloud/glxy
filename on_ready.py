@bot.event
async def on_ready():
    logger.info(f'{bot.user} is now running!')
    logger.info("on_ready event triggered")

    if STARTUP_CHANNEL_ID:
        logger.info(f"Attempting to send startup message to channel {STARTUP_CHANNEL_ID}")
        try:
            channel = await bot.fetch_channel(int(STARTUP_CHANNEL_ID))
            if channel:
                logger.info(f"Channel {STARTUP_CHANNEL_ID} found")

                # Step 1: Send cryptic ASCII art
                ascii_art = """
    ╩╩╩╩╩╩╩___╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩
  ╩╩╩╩╩╩/\_ \╩╩╩3y5╩╩╩╩╩╩╩╩╩╩╩╩╩╩
  ╩╩╩__╩\//\ \╩╩╩__╩╩_╩__╩╩__╩╩╩╩
  ╩/'_ `\╩\╩\ \╩/\ \/'/\ \/\ \╩╩╩
  /\ \L\ \╩\_\ \\/>  <\ \ \_\ \╩╩
  \╩\____ \/\____/\_/\_\/`____ \╩
  ╩\/___L\ \/____\//\/_/`/___/> \╩
 ╩╩╩/\____/╩╩╩╩╩xyo╩╩╩╩╩╩╩╩╩\/__/╩
   
 ❖ ── ✦ ──『anon-glxy』── ✦ ── ❖

"""

                await channel.send(f"```{ascii_art}```")
                logger.info("ASCII art sent successfully")

                # Step 2: Send cryptic instructions
                instructions = (
    "**Welcome to the system. Here's how you can use this bot to get things done efficiently:**"
    "\n\n**/chat** – Ask your question, and the agents will collaborate to provide you with detailed answers."
    "\n\n**/image** – Upload an image for AI processing and analysis. The bot will extract the details you need."
    "\n\n**/doc** – Submit a document, and the AI will parse and summarize the key points."
    "\n\n**/code** – Run your code in a safe, isolated environment. Designed for quick and reliable execution."
    "\n\n**/memory** – Store and retrieve information for future use. The bot keeps track of what's important."
    "\n\n**These commands are here to streamline your tasks and give you quick, actionable insights.**"
)

                await channel.send(instructions)
                logger.info(f"Instructions sent to channel {STARTUP_CHANNEL_ID}")
            else:
                logger.warning(f"Channel with ID {STARTUP_CHANNEL_ID} not found")
        except Exception as e:
            logger.error(f"Error sending startup message: {e}", exc_info=True)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    