from colorama import Fore, init
from discord.ext import commands, tasks
import threading, os, random, pyfade

# Put "user_id" -> mention user
__MESSAGE__ = '''

'''

__TOKEN__   = 'XxXxXXxXxXXxXxXXxXxXXxXxX.XxXxX.XxXxXXxXxXXxXxXXxXxXXxXxXXxX'

class Worker(threading.Thread):
    def __init__(self, token: str):
        threading.Thread.__init__(self)
        self.client = commands.Bot(command_prefix= 'zap.', self_bot= True)
        self.token = token

        self.black_list = []
        self.wait_list  = []
        self.error      = 0 
        init()

        @tasks.loop(seconds= 1)
        async def update_gui():
            print(f'&> Waitlist: {Fore.CYAN}{len(self.wait_list)}{Fore.RESET} DM: {Fore.GREEN}{len(self.black_list) - len(self.wait_list) - self.error}{Fore.RESET} Blocked: {Fore.RED}{self.error}{Fore.RESET}    ', end= '\r')
    
        @tasks.loop(minutes= 1)
        async def dm_one():
            if len(self.wait_list) == 0:
                return
            
            ppl = random.choice(self.wait_list)
            self.wait_list.remove(ppl)

            try:
                user = await self.client.fetch_user(ppl)
                await user.send(__MESSAGE__.replace('user_id', f'<@{ppl}>'))
            except:
                self.error += 1
        
        @self.client.event
        async def on_ready():
            update_gui.start()
            dm_one.start()

        @self.client.event
        async def on_message(ctx):
            if not ctx.author.bot:
                self.add_user(ctx.author.id)

        @self.client.event
        async def on_raw_reaction_add(payload):
            if not payload.member.bot:
                self.add_user(payload.member.id)

        @self.client.event
        async def on_member_join(member):
            if not member.bot:
                self.add_user(member.id)

        # AttributeError: 'Member' object has no attribute 'member'
        @self.client.event
        async def on_member_update(before, after):
            if not after.bot:
                self.add_user(after.id)

        @self.client.event
        async def on_voice_state_update(member, before, after):
            if not member.bot:
                self.add_user(member.id)

    def add_user(self, user_id: str):
        if user_id != self.client.user.id and user_id not in self.black_list:
            self.black_list.append(user_id)
            self.wait_list.append(user_id)

    def run(self):
        self.client.run(self.token, bot= False)

if __name__ == '__main__':
    os.system('cls && title !ZAPP ~ github.com/its_vichy' if os.name == 'nt' else 'clear')
    print(pyfade.Fade.Horizontal(pyfade.Colors.red_to_purple, '''
    ┬ ╔═╗╔═╗╔═╗╔═╗
    │ ╔═╝╠═╣╠═╝╠═╝
    o ╚═╝╩ ╩╩  ╩
    '''))

    Worker(__TOKEN__).start()