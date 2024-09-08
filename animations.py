import asyncio
import discord

# Terminal-style startup animation
# Startup Animation with Rich Embeds
async def startup_animation(interaction: discord.Interaction, product: str = "Multi-Agent System"):
    frames = [
        f"**$ Initializing {product}...**\n[▓▓░░░░░░░░░░] 20% | Establishing connection",
        f"**$ {product} System loading...**\n[▓▓▓▓▓▓░░░░░░] 40% | Breaking through firewalls",
        f"**$ {product} Security check complete**\n[▓▓▓▓▓▓▓▓░░░] 60% | Setting up environment",
        f"**$ {product} Optimization in progress**\n[▓▓▓▓▓▓▓▓▓▓░] 80% | Executing final routines",
        f"**$ {product} Initialized**\n[▓▓▓▓▓▓▓▓▓▓▓] 100% | Welcome to the revolution. ⚡"
    ]

    for frame in frames:
        await interaction.followup.send(frame)
        await asyncio.sleep(1)  # Simulate the animation delay


# Thinking animation (optional)
async def thinking_animation(ctx):
    frames = [
        "🤔 **Thinking.**",
        "🤔 **Thinking..**",
        "🤔 **Thinking...**"
    ]
    
    if isinstance(ctx, discord.Interaction):
        message = await ctx.original_response()
    else:
        message = await ctx.send(frames[0])
    
    i = 0
    while True:
        await asyncio.sleep(1)
        i = (i + 1) % len(frames)
        await message.edit(content=frames[i])

# Code processing animation (optional)
async def code_processing_animation(ctx):
    frames = [
        "🖥️ **Compiling code...**",
        "⚙️ **Running tests...**",
        "✅ **Code executed successfully!**"
    ]
    
    if isinstance(ctx, discord.Interaction):
        await ctx.followup.send(frames[0])
        message = await ctx.original_response()
    else:
        message = await ctx.send(frames[0])
    
    for frame in frames[1:]:
        await asyncio.sleep(1.5)
        await message.edit(content=frame)
