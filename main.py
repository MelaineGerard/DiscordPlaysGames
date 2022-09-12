import os

from ahk import AHK
from ahk.window import Window
from dotenv import load_dotenv
import discord


# Run the user key
def handle_commands(key):
    win.activate()
    if key == "a":
        ahk.key_press(os.getenv("A_KEY"))
    elif key == "b":
        ahk.key_press(os.getenv("B_KEY"))
    elif key == "x":
        ahk.key_press(os.getenv("X_KEY"))
    elif key == "y":
        ahk.key_press(os.getenv("Y_KEY"))
    elif key == "haut":
        ahk.key_press(os.getenv("UP_KEY"))
    elif key == "bas":
        ahk.key_press(os.getenv("DOWN_KEY"))
    elif key == "gauche":
        ahk.key_press(os.getenv("LEFT_KEY"))
    elif key == "droite":
        ahk.key_press(os.getenv("RIGHT_KEY"))
    elif key == "start":
        ahk.key_press(os.getenv("START_KEY"))
    elif key == "select":
        ahk.key_press(os.getenv("SELECT_KEY"))


class DiscordBot(discord.Client):
    async def on_ready(self):
        print('Connected as', self.user)

    async def on_message(self, message):
        # Ignore message if it comes from the bot
        if message.author == self.user:
            return

        # check if we are in the right channel
        if str(message.channel.id) != os.getenv('CHANNEL'):
            print("channel not found !")
            return

        key = message.content.lower()
        handle_commands(key)


if __name__ == "__main__":
    load_dotenv()
    ahk = AHK()
    wins = list(ahk.windows())
    win = None

    # Check in the wins list if the emulator is inside
    for window in wins:
        if str(window.title.lower()).find(f'{os.getenv("EMULATOR")}') != -1:
            win = Window(ahk, ahk_id=window.id)

    if win is not None:
        print("Starting Discord Plays Game...")
        intents = discord.Intents.default()
        intents.message_content = True
        client = DiscordBot(intents=intents)
        client.run(os.getenv('TOKEN'))
    else:
        print("Couldn't find the emulator !")
