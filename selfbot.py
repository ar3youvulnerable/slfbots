import discord
from discord import Client, Status
from discord.ext import commands
from colorama import Fore, Back, Style
from datetime import datetime, timezone
import random
import asyncio
import os
import sys

try:
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("Enter your Discord token: ")
except (EOFError, RuntimeError):
    print(f"{Fore.RED}Error: Cannot read input. Please provide token as command line argument.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Usage: gothboiself.exe YOUR_TOKEN_HERE{Style.RESET_ALL}")
    sys.exit(1)
prefix = "s"

autodel_active = False
autodel_channel = None
autodel_target = None

client = commands.Bot(command_prefix=prefix, self_bot=True)

def display_logo():
    logo = '''                                                                                                       
  /$$$$$$  /$$                           /$$                
 /$$__  $$| $$                          | $$                
| $$  \__/| $$        /$$$$$$   /$$$$$$ | $$   /$$  /$$$$$$ 
|  $$$$$$ | $$       /$$__  $$ /$$__  $$| $$  /$$/ /$$__  $$
 \____  $$| $$      | $$$$$$$$| $$$$$$$$| $$$$$$/ | $$  \ $$
 /$$  \ $$| $$      | $$_____/| $$_____/| $$_  $$ | $$  | $$
|  $$$$$$/| $$$$$$$$|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$/
 \______/ |________/ \_______/ \_______/|__/  \__/ \______/ 
                                                            
                                                            
                                                                                                                                                    
                                                                                                                    
                                                                                                                    
                                                                                                                    
                               
                               
       Welcome Master
 '''
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + logo)

def display_commands():
    commands_display = f"""
{Fore.MAGENTA}SUPAH POWERZ {Style.RESET_ALL}
{Fore.CYAN}scom      {Fore.WHITE}| {Fore.CYAN}sclear     {Fore.WHITE}| 

{Fore.CYAN}sspam    {Fore.WHITE}| {Fore.CYAN}sping

{Fore.CYAN}scheck    {Fore.WHITE}| {Fore.CYAN}spack 
 
{Fore.CYAN}sstop      {Fore.WHITE}|        {Fore.CYAN}sdelete 
"""
    print(commands_display)

@client.event
async def on_ready():
    display_logo()
    display_commands()
    day = datetime.now(timezone.utc) - client.user.created_at
    print(f"{Fore.GREEN}Logged in\nUser : {client.user}\nID : {client.user.id}\nCreation Date : {client.user.created_at} ({day.days})\nBadges : ")
    for badg in client.user.public_flags.all():
        print(badg)
    await client.change_presence(status=discord.Status.invisible)

@client.command()
async def com(ctx):
    await ctx.message.delete()
    commands_list = """```   
       Supah Powers (Prefix: s)

 scom         sspam             scheck  
sclear                                sping     
 spack          sstop             sdelete    

```"""

    await ctx.send(commands_list)

@client.command()
async def clear(ctx, limit=100):
    await ctx.message.delete()
    channel = await client.fetch_channel(ctx.channel.id)
    number = 0
    async for message in channel.history(): 
        if int(number) == int(limit):
            pass
        else:
                if message.author.id == client.user.id: 
                    await message.delete()
                    number += 1
                    print(f"{Fore.GREEN}{message.content} Deleted [{number}]{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Done[{number} messages Deleted]{Style.RESET_ALL}")

@client.command()
async def spam(ctx, amount: int, *, message):
    await ctx.message.delete()
    for i in range(amount):
        await ctx.send(message)
        print(f"{Fore.GREEN}Spam message {i+1}/{amount} sent{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Done[{amount} spam messages sent]{Style.RESET_ALL}")

@client.command()
async def ping(ctx, amount: int, *, target):
    await ctx.message.delete()
    if ctx.author.id != client.user.id:
        return
  
    if not ctx.message.mentions:
        await ctx.send("*mention mo boss*", delete_after=3)
        return
    
    target_member = ctx.message.mentions[0]
    
    for i in range(amount):
        ghost_message = await ctx.send(target_member.mention)
        await ghost_message.delete()
        print(f"{Fore.GREEN}Ghost ping {i+1}/{amount} sent & deleted{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Done[{amount} ghost pings completed]{Style.RESET_ALL}")

@client.command()
async def check(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    await ctx.message.delete()
    info_text = f"""
```
USERNAME: {member.name}
USER ID: {member.id}
DISPLAY NAME: {member.display_name}
ACCOUNT CREATED: {member.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
```
"""
    await ctx.send(info_text)


roasting_active = False

@client.command()
async def pack(ctx, *, target):
    global roasting_active, target_user_id, target_channel_id
    await ctx.message.delete()

    if not ctx.message.mentions:
        await ctx.send("*ay need pala eh mention *", delete_after=3)
        return

    target_member = ctx.message.mentions[0]
    target_user_id = target_member.id
    target_channel_id = ctx.channel.id

# To input roast pls use:

# f"roast message", 

# to add roasts.
    roasts = [
    
    f"example roast",
    
    f"roast 2",
   
    f"final roast"

          ]

    roasting_active = True
    roast_count = 0

    while roasting_active:
        try:
            def check(msg):
                return msg.author.id == target_user_id and msg.channel.id == target_channel_id

            # Wait up to 1 second before retrying
            user_message = await asyncio.wait_for(client.wait_for("message", check=check), timeout=1.0)

            roast = random.choice(roasts)
            await user_message.reply(roast)
            roast_count += 1
            print(f"{Fore.GREEN}Roast {roast_count} sent{Style.RESET_ALL}")
            await asyncio.sleep(0.02)

        except asyncio.TimeoutError:
            # Just loop again and check if roasting_active is still True
            continue
        except Exception as e:
            print(f"Error in pack loop: {e}")
            break

    print(f"{Fore.CYAN}Roasting stopped after {roast_count} roasts{Style.RESET_ALL}")   

    print(f"{Fore.CYAN}Roasting stopped after {roast_count} roasts{Style.RESET_ALL}")
    

auto_reaction_active = False
auto_reactions = {}  # Must be initialized

auto_reaction_ active = False

@client.command()
async def react(ctx, *args):
    global auto_reaction_active
    await ctx.message.delete()
    if len(args) < 2:
        return
    # Extract emojis (non-digit, not a mention)
    emojis = [arg for arg in args if not arg.isdigit() and not arg.startswith('<@')]
    # Extract user IDs from mentions or raw IDs
    users = []
    for arg in args:
        if arg.isdigit():
            users.append(int(arg))
        elif arg.startswith('<@'):
            # Remove <@! (for nicked mentions) or <@ and trailing >
            uid = ''.join(filter(str.isdigit, arg))
            if uid:
                users.append(int(uid))
    
# Assign emojis to each user
    for uid in users:
        auto_reactions[uid] = emojis
    auto_reaction_active = True

 
@client.command()
async def stop(ctx):
    global roasting_active, auto_reaction_active, autodel_active, autodel_channel, autodel_target, auto_reaction_target
    global autodel_target_id, auto_reaction_target_id
    await ctx.message.delete()
    auto_reaction_active = False
    roasting_active = False
    autodel_active = False
    autodel_channel = None
    autodel_target = None
    autodel_target_id = None
    await ctx.send("```Stopping...```", delete_after=1)
    print(f"{Fore.YELLOW}Roasting, auto-reaction, and auto-delete stopped by user{Style.RESET_ALL}")

@client.command()
async def delete(ctx, member: discord.Member = None):
    global autodel_active, autodel_channel, autodel_target, autodel_target_id
    await ctx.message.delete()
    
    if member:
        autodel_active = True
        autodel_channel = ctx.channel
        autodel_target = member
        autodel_target_id = member.id
        await ctx.send(f"mawawala message ni {member.mention} parang magic", delete_after=2)
        print(f"{Fore.GREEN}Auto delete activated for {member} in {ctx.channel.name}{Style.RESET_ALL}")
    else:
        autodel_active = False
        autodel_channel = None
        autodel_target = None
        autodel_target_id = None
        await ctx.send("*auto delete deactivated*", delete_after=2)
        print(f"{Fore.YELLOW}Auto delete deactivated{Style.RESET_ALL}")

@client.event
async def on_message(message):
    global autodel_active, autodel_channel, autodel_target, autodel_target_id
    global auto_reaction_active, auto_reaction_emoji, auto_reaction_target, auto_reaction_target_id

    if autodel_active and autodel_channel and message.channel == autodel_channel and autodel_target_id is not None and message.author.id == autodel_target_id:
        try:
            await message.delete()
            print(f"{Fore.GREEN}Auto-deleted message from {message.author}: {message.content[:50]}{Style.RESET_ALL}")
        except discord.Forbidden:
            print(f"{Fore.RED}Cannot delete message: Missing permissions{Style.RESET_ALL}")
            autodel_active = False
            autodel_channel = None
            autodel_target = None
            autodel_target_id = None
        except Exception as e:
            print(f"{Fore.RED}Error deleting message: {e}{Style.RESET_ALL}")
            
    await client.process_commands(message)

@client.event
async def on_message(message):
    await client.process_commands(message)
    if auto_reaction_active and message.author.id in auto_reactions:
        # React with all emojis concurrently
        await asyncio.gather(
            *(message.add_reaction(emoji) for emoji in auto_reactions[message.author.id]),
            return_exceptions=True
        )

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        print(f"{Fore.RED}Pls provide a number to delete\nExample : {prefix}clear 100 {Style.RESET_ALL}")

try:
    if not token:
        print(f"{Fore.RED}Error: No token provided. Please provide a token via command line argument or when prompted.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Usage: python gothboiself.py YOUR_TOKEN_HERE{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}Starting bot...{Style.RESET_ALL}")
    client.run(token)
except discord.LoginFailure:
    print(f"{Fore.RED}Error: Invalid token provided. Please check your token and try again.{Style.RESET_ALL}")
    sys.exit(1)
except Exception as e:
    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

    sys.exit(1)
