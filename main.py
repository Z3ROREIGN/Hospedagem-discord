import discord
from discord.ext import commands
import os
import shutil
import json

# Create a new bot instance
bot = commands.Bot(command_prefix='/')

# Load the bot configurations from bots.js
with open('bots.js', 'r') as f:
    bots_config = json.load(f)

# Store user permissions and bot limits
user_permissions = {}
user_bot_limits = {}

# Command to add a new bot
@bot.command(name='newBot')
async def new_bot(ctx):
    # Prompt the user to enter the bot token
    await ctx.send('Please enter the bot token:')
    token = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author)

    # Create a new bot instance
    new_bot = discord.Client()
    new_bot.run(token.content)

    # Start the new bot instance
    new_bot.loop.create_task(new_bot.start(token.content))

    # Add the new bot to the list of bots
    bots_config[token.content] = {
        'owner_id': ctx.author.id,
        'permissions': [],
        'bot_limit': 0
    }

    # Save the updated bot configurations to bots.js
    with open('bots.js', 'w') as f:
        json.dump(bots_config, f)

    await ctx.send('New bot created and started successfully!')

# Command to add code files
@bot.command(name='addcode')
async def add_code(ctx):
    # Prompt the user to upload the code files
    await ctx.send('Please upload the code files:')
    attachment = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author)

    # Save the code files to a directory
    os.makedirs('code_files', exist_ok=True)
    with open(os.path.join('code_files', attachment.filename), 'wb') as f:
        f.write(attachment.attachments[0].read())

    await ctx.send('Code files added successfully!')

# Command to commit code changes
@bot.command(name='commitcode')
async def commit_code(ctx):
    # Prompt the user to enter the commit message
    await ctx.send('Please enter the commit message:')
    commit_message = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author)

    # Commit the code changes
    os.system(f'git commit -m "{commit_message.content}"')
    os.system('git push')

    await ctx.send('Code changes committed successfully!')

# Command to delete code files
@bot.command(name='deletecode')
async def delete_code(ctx):
    # Prompt the user to select a code file to delete
    await ctx.send('Please select a code file to delete:')
    code_file = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author)

    # Delete the selected code file
    os.remove(os.path.join('code_files', code_file.content))

    await ctx.send('Code file deleted successfully!')

# Command to delete a bot
@bot.command(name='deletebot')
async def delete_bot(ctx):
    # Prompt the user to select a bot to delete
    await ctx.send('Please select a bot to delete:')
    bot_to_delete = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author)

    # Remove the selected bot from the list of bots
    del bots_config[bot_to_delete.content]

    # Save the updated bot configurations to bots.js
    with open('bots.js', 'w') as f:
        json.dump(bots_config, f)

    await ctx.send('Bot deleted successfully!')

# Command to grant permissions to a user
@bot.command(name='perm')
async def grant_permissions(ctx, user_id: int, bot_limit: int):
    # Check if the user is authorized to grant permissions
    if ctx.author.id != 1098745384848859258:
        await ctx.send('Only the authorized user can grant permissions.')
        return

    # Grant permissions to the specified user
    user_permissions[user_id] = True
    user_bot_limits[user_id] = bot_limit

    await ctx.send(f'Permissions granted to user {user_id} with a bot limit of {bot_limit}.')

# Command to remove permissions from a user
@bot.command(name='removeperm')
async def remove_permissions(ctx, user_id: int):
    # Check if the user is authorized to remove permissions
    if ctx.author.id != 1098745384848859258:
        await ctx.send('Only the authorized user can remove permissions.')
        return

    # Remove permissions from the specified user
    user_permissions[user_id] = False
    user_bot_limits[user_id] = 0

    await ctx.send(f'Permissions removed from user {user_id}.')

# Command to edit the bot limit for a user
@bot.command(name='editarquantia')
async def edit_bot_limit(ctx, user_id: int, bot_limit: int):
    # Check if the user is authorized to edit the bot limit
    if ctx.author.id != 1098745384848859258:
        await ctx.send('Only the authorized user can edit the bot limit.')
        return

    # Edit the bot limit for the specified user
    user_bot_limits[user_id] = bot_limit

    await ctx.send(f'Bot limit edited for user {user_id} to {bot_limit}.')

# Event to handle the bot startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run('MTQyODcwOTI2MTU4Mzg0MzM1OA.GSf3rR.IhOq-32l1kJGNN0egCxITdNoHlmggt6EMlgx5E')
