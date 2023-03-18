# main.py
import random
import discord
from discord import Interaction
from discord.ext import commands
from countries import country_ids

REACTIONS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

TOKEN = ''
client = commands.Bot(
                        command_prefix="?",
                        intents=discord.Intents.all()
                        )
client.synced = False

game_on = False
flag_ids = country_ids
challenge = ""
answers = []
correct_answer = ""

# prints when the bot is online to console.
@client.event
async def on_ready():
    await client.wait_until_ready()
    if not client.synced:                                                                               # check if slash commands have been synced 
        await client.tree.sync()
        client.synced = True;
    print(f'{client.user} has connected to Discord!')

# check for challenge messages
@client.tree.command(name = 'guess', description='starts flag guessing game!')
async def guess(interaction: Interaction,):
    global game_on, answers, correct_answer, challenge
    
    if interaction.user != client.user:
        answers = []
        game_on = True
        country, flag_id = random.choice(list(flag_ids.items()))                                        # get country name and id
        correct_answer = country
        countries = list(flag_ids.keys())
        answers = [country]

        for i in range(3):
            picked_country = random.choice(countries)
            answers += [picked_country]
            countries.remove(picked_country)
        random.shuffle(answers)
        
        embed = discord.Embed(
            title = "Flag Guesser",
            description = "Who does this flag belong to? React to the emoji!",
        )

        embed.set_image(url = f"https://flagcdn.com/w1280/{flag_id.lower()}.png")
        embed.add_field(name=f":one:. {answers[0]}", value=f"‎", inline=False)
        embed.add_field(name=f":two:. {answers[1]}", value=f"‎", inline=False)
        embed.add_field(name=f":three:. {answers[2]}", value=f"‎", inline=False)
        embed.add_field(name=f":four:. {answers[3]}", value=f"‎", inline=False)
        embed.set_footer(text="Developed by Lectern Dev")

        sent_challenge = await interaction.response.send_message(embed=embed)
        challenge = await interaction.original_response()

        for reaction in REACTIONS:
            await challenge.add_reaction(reaction)                                                      # add reaction for answers

@client.event
async def on_raw_reaction_add(payload):
    global game_on, answers, correct_answer

    message_id = payload.message_id

    if message_id == challenge.id and payload.member != client.user:                                        # if challenge message and not self reacting

        if game_on and payload.emoji.name in REACTIONS: 
            indices = {}
            for reaction in REACTIONS:
                indices[reaction] = REACTIONS.index(reaction)                                               # get indices of reactions

            if indices[payload.emoji.name] == answers.index(correct_answer):                                # check answer
                embed = discord.Embed(
                    title = "Flag Guesser",
                    description = f"Correct! It was indeed `{correct_answer}`! Use `/guess` to play again.",
                )
            else:
                embed = discord.Embed(
                    title = "Flag Guesser",
                    description = f"Sorry! It was actually `{correct_answer}`! Use `/guess` to play again.",
                )
        
            answers = []
            game_on = False
            await challenge.channel.send(embed=embed)                                                       # send game over message

if __name__ == "__main__":
    client.run(TOKEN)