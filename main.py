import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot online 😎"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

ticket_users = {}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')
    print('Bot está online e pronto!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.bot:
        return
    
    if message.guild and hasattr(message.channel, 'name'):
        channel_name = message.channel.name.lower()
        
        if 'ticket' in channel_name:
            channel_id = message.channel.id
            user_id = message.author.id
            
            if channel_id not in ticket_users:
                ticket_users[channel_id] = set()
            
            if user_id not in ticket_users[channel_id]:
                ticket_users[channel_id].add(user_id)
                mensagem_boas_vindas = (
                    f'Olá {message.author.mention}, isso é uma mensagem automática\n\n'
                    'Digite **"script"** para o script seja mandado automaticamente\n'
                    'Digite **"aura"** para que o link das auras seja mandado automaticamente\n'
                    'Entre no meu Discord digite **"discord"**\n'
                    'Se quiser mais suporte digite **"suporte"**'
                )
                await message.channel.send(mensagem_boas_vindas)
    
    conteudo = message.content.lower()
    
    if conteudo == 'script':
        await message.channel.send('script 👇 `loadstring(game:HttpGet("https://pastebin.com/raw/B8h0DqhR"))()`')
    
    elif conteudo == 'aura':
        resposta_aura = (
            'aura 1 👉 https://www.roblox.com/game-pass/1612964554/Unlock-Script-Aura-1\n'
            'aura 2 (opcional mas recomendado) 👉 https://www.roblox.com/game-pass/1614434301/Aura-2\n'
            'aura 3 (opcional mas recomendado) 👉 https://www.roblox.com/game-pass/1613270490/Aura-3\n'
        )
        await message.channel.send(resposta_aura)
    
    elif conteudo == 'discord':
        await message.channel.send('https://discord.gg/BYSFmv9JKg')
    
    elif conteudo == 'suporte':
        if message.guild:
            adm_role = discord.utils.get(message.guild.roles, name='ADM')
            if adm_role:
                await message.channel.send(f'{adm_role.mention} {message.author.mention} precisa de suporte! Por favor, aguarde que um administrador irá te atender em breve.')
            else:
                await message.channel.send(f'{message.author.mention} Seu pedido de suporte foi registrado! Por favor, aguarde que um administrador irá te atender em breve.')
        else:
            await message.channel.send(f'{message.author.mention} O comando de suporte só funciona em servidores!')
    
    if message.content.startswith('!oi'):
        await message.channel.send(f'Olá {message.author.mention}! 👋')
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! Latência: {round(bot.latency * 1000)}ms')

@bot.command(name='ajuda')
async def ajuda(ctx):
    embed = discord.Embed(
        title="Comandos do Bot",
        description="Lista de comandos disponíveis",
        color=discord.Color.blue()
    )
    embed.add_field(name="!ping", value="Mostra a latência do bot", inline=False)
    embed.add_field(name="!oi", value="Bot responde com uma saudação", inline=False)
    embed.add_field(name="!ajuda", value="Mostra esta mensagem", inline=False)
    await ctx.send(embed=embed)

def main():
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("ERRO: Token do Discord não encontrado!")
        print("Por favor, adicione DISCORD_BOT_TOKEN nas Secrets do Replit")
        print("ou configure a variável de ambiente DISCORD_BOT_TOKEN")
        return
    
    keep_alive()
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("ERRO: Token inválido! Verifique seu token do Discord.")
    except Exception as e:
        print(f"ERRO ao iniciar o bot: {e}")

if __name__ == "__main__":
    main()
