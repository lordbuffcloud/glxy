import asyncio
import discord

async def startup_animation(ctx, product):
    frames = [
        f"Initializing {product}...",
        f"Initializing {product}....",
        f"Initializing {product}.....",
        f"{product} Initialized!"
    ]
    
    if isinstance(ctx, discord.Interaction):
        await ctx.followup.send(frames[0])
        message = await ctx.original_response()
    else:
        message = await ctx.send(frames[0])
    
    for frame in frames[1:]:
        await asyncio.sleep(1)
        await message.edit(content=frame)

async def thinking_animation(ctx):
    frames = [
        "Thinking.",
        "Thinking..",
        "Thinking...",
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