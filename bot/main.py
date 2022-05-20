import discord
from discord.ext import commands, tasks
import datetime

from sqlitedict import SqliteDict


def save(key, value, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as base_dict:
            base_dict[key] = value
            base_dict.commit()
    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)


def load(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as base_dict:
            value = base_dict[key]
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


"""
from replit import db
import os

from flask import Flask
from threading import Thread
app = Flask('')
 
@app.route('/')
def home():
  return "Монитор активен."
 
def run():
  app.run(host='0.0.0.0',port=8080)
 
def keep_alive():
  t = Thread(target=run)
  t.start()
"""

def get_workers_list(mark_list: dict, data: list):
    sort_list = []
    for string in data:
        args = [val.strip().lower() for val in string[1].split(' ')[:2]]
        value = 0
        if string[0] in mark_list.keys():
            value = mark_list.get(string[0]) * int(string[2])
        sort_list.append([value, int(string[2]), string[0], *args])
    sort_list = sorted(sort_list, key=lambda val: (val[0], val[1]))
    mine = []
    port = []
    for element in sort_list[:]:
        if element[3] == 'к':
            if len(port) != 5:
                port.append(element[2])
                sort_list.remove(element)
                if len(element) == 5:
                    sort_list.append(element)
        elif len(mine) != 4:
            mine.append(element[2])
            sort_list.remove(element)
            if len(element) == 5:
                sort_list.append(element)
        if len(mine) + len(port) == 9:
            break
    if len(mine) + len(port) != 9:
        for element in sort_list:
            if element[4] == 'к':
                if len(port) != 5:
                    port.append(element[2])
            elif len(mine) != 4:
                mine.append(element[2])
    return [mine, port]

class Distributor(commands.Cog):
    def __init__(self, bot_object):
        self.bot = bot_object
        self.num_arr = ["<:Numero1:976535090500890714>", "<:Numero2:976535090144358450>", "<:Numero3:976535090253418546>", "<:Numero4:976535090043699242>", "<:Numero5:976535090471526430>", "<:Numero6:976535090496700446>", "<:Numero7:976535090274385950>", "<:Numero8:976535090400210944>", "<:Numero9:976535090320519168>", "<:Numero10:976535090534440960>"]

    async def access(self, context: commands.Context, check_channel=False):
        if check_channel:
            if context.channel.id != load("channel_id"):
                return False
        if int(context.author.display_name.split('|')[0].strip()) >= 4:
            return True
        await context.message.delete(delay=5)
        await context.reply(":x: Доступ запрещён! :x:", delete_after=5)
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(load("channel_id"))
        mess_history = await channel.history().flatten()
        for record in mess_history:
            print(record.id, record.author.name)
        print(load("day_message_id"), datetime.datetime.strptime(load("alarm_time"), "%d.%m.%y %H:%M"))
        if load("channel_id") and load("week_message_id") and load("day_message_id"):
            alarm_time = datetime.datetime.strptime(load("alarm_time"), "%d.%m.%y %H:%M")
            if alarm_time > datetime.datetime.now() + datetime.timedelta(hours=3):
                self.check.start()
        '''
        try:
            with open("data.json", "r") as save_file:
                file_data = load(save_file)
                self.channel_id = file_data.get("channel_id")
                self.week_message_id = file_data.get("week_message_id")
                self.day_message_id = file_data.get("day_message_id")
                time = file_data.get("alarm_time")
                channel = self.bot.get_channel(self.channel_id)
                mess_history = await channel.history().flatten()
                for record in mess_history:
                    print(record.id, record.author.name)
                #mess = await channel.fetch_message(id=self.day_message_id)
                #print(mess.content)
                #print(time)
                self.alarm_time = datetime.datetime.strptime(time, "%d.%m.%y %H:%M")
                if self.channel_id and self.week_message_id and self.day_message_id and self.alarm_time > datetime.datetime.now() + datetime.timedelta(hours=3):
                    self.check.start()
        except FileNotFoundError:
            pass
        '''
        #db["channel_id"] = self.channel_id
        #db["week_message_id"] = self.week_message_id
        #db["day_message_id"] = self.day_message_id
        #db["alarm_time"] = self.alarm_time.strftime("%d.%m.%y %H:%M")

        """
        channel = self.bot.get_channel(self.channel_id)
        week_message = await channel.fetch_message(id=self.week_message_id)
        plus_list = dict()
        num_dict = {":zero:": 0, ":one:": 1, ":two:": 2, ":three:": 3, ":four:": 4, ":five:": 5, ":six:": 6,
                    ":seven:": 7, ":eight:": 8, ":nine:": 9}
        week_strings = week_message.content.split('\n')
        for string in week_strings[2:]:
            params = string.split(' ')
            count = 0
            for num in params[1].replace("::", ": :").split(' '):
                count = count * 10 + int(num_dict.get(num))
            plus_list[params[0].replace("<@!", "<@")] = count
        day_message = await channel.fetch_message(id=973257138535293000)
        embed = day_message.embeds[0]
        for index in range(2):
            field_value = embed.fields[index].value.split("\n")
            for val in field_value:
                if val != "Свободно":
                    val = val.replace("<@!", "<@")
                    if val in plus_list.keys():
                        plus_list[val] = plus_list.get(val) + 1
                    else:
                        plus_list[val] = 1
        text = week_strings[0] + "\n" + week_strings[1]
        reverse_num_dict = {v: k for k, v in num_dict.items()}
        for (key, val) in plus_list.items():
            text += "\n" + key + " " + ''.join([reverse_num_dict.get(int(number)) for number in str(val)])
        await week_message.edit(content=text)
        """

    @commands.command()
    async def change_car(self, ctx, pos: int, name, fuel):
        if not await self.access(ctx):
            return
        if len(load("cars")) >= pos:
            rang = load("cars")[pos-1][1]
            await self.del_car(ctx, pos)
            await self.add_car(ctx, name, rang, fuel)
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass

    @commands.command()
    async def reset_car(self, ctx, pos: int):
        if not await self.access(ctx):
            return
        if len(load("cars")) >= pos:
            arr = load("cars")
            fuel_id = load("fuel_id")
            car_id = load("car_id")
            if fuel_id is None or car_id is None:
                fuel_id = car_id = 0
            if fuel_id and car_id:
                try:
                    fuel_mess = await ctx.channel.fetch_message(id=fuel_id)
                    car_mess = await ctx.channel.fetch_message(id=car_id)
                    fuel_strings = fuel_mess.content.split('\n')
                    car_strings = car_mess.content.split('\n')
                    part = f"\t{self.num_arr[pos - 1]} **{arr[pos - 1][0]}** - "
                    new_pos = fuel_strings.index(f"{part}{arr[pos - 1][2]}")
                    car_strings[new_pos] = f"{part}Свободно"
                    car_strings = '\n'.join(car_strings)
                    await car_mess.edit(content=car_strings)
                except discord.NotFound:
                    pass
        await ctx.message.delete()

    @commands.command()
    async def del_car(self, ctx, pos: int):
        if not await self.access(ctx):
            return
        arr = load("cars")
        if arr is None:
            arr = []
        if 0 < pos <= len(arr):
            save("cars", load("cars").pop(pos - 1))
            fuel_id = load("fuel_id")
            car_id = load("car_id")
            if fuel_id is None or car_id is None:
                fuel_id = car_id = 0
            if fuel_id and car_id:
                try:
                    fuel_mess = await ctx.channel.fetch_message(id=fuel_id)
                    car_mess = await ctx.channel.fetch_message(id=car_id)
                    fuel_strings = fuel_mess.content.split('\n')
                    car_strings = car_mess.content.split('\n')
                    for i, string in reversed(list(enumerate(fuel_strings))):
                        if string.count(":"):
                            replace_part = string[1:string.find('>', 1) + 1]
                            num = self.num_arr.index(replace_part)
                            if num == pos - 1:
                                fuel_strings[i] = car_strings[i] = ""
                                if i == len(fuel_strings) - 1:
                                    if not fuel_strings[i-1].count(":"):
                                        fuel_strings[i - 1] = car_strings[i - 1] = ""
                                elif not fuel_strings[i-1].count(":") and not fuel_strings[i+1].count(":"):
                                    fuel_strings[i - 1] = car_strings[i - 1] = ""
                                break
                            elif num >= pos:
                                new_part = self.num_arr[num - 1]
                                fuel_strings[i] = fuel_strings[i].replace(replace_part, new_part)
                                car_strings[i] = car_strings[i].replace(replace_part, new_part)
                    fuel_strings = '\n'.join([string for string in fuel_strings if string != ''])
                    car_strings = '\n'.join([string for string in car_strings if string != ''])
                    await fuel_mess.edit(content=fuel_strings)
                    await car_mess.edit(content=car_strings)
                except discord.NotFound:
                    pass
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass
    
    @commands.command()
    async def add_car(self, ctx, name, rang: int, fuel):
        if not await self.access(ctx):
            return
        arr = load("cars"])
        if arr is None:
            arr = []
        if len(arr) == 10:
            await ctx.message.delete()
            return
        arr.append([name, rang, fuel])
        arr = sorted(arr, key=lambda val: (val[1]), reverse=True)
        save("cars", arr)
        fuel_id = load("fuel_id")
        car_id = load("car_id")
        if fuel_id is None or car_id is None:
            fuel_id = car_id = 0
        if fuel_id and car_id:
            try:
                fuel_mess = await ctx.channel.fetch_message(id=fuel_id)
                car_mess = await ctx.channel.fetch_message(id=car_id)
                fuel_strings = fuel_mess.content.split('\n')
                car_strings = car_mess.content.split('\n')
                pos = 0
                new_pos = arr.index([name, rang, fuel])
                if new_pos:
                    pos = fuel_strings.index(f"\t{self.num_arr[new_pos - 1]} **{arr[new_pos - 1][0]}** - {arr[new_pos - 1][2]}") + 1
                part = f"\t{self.num_arr[new_pos]} **{name}**"
                if f"__{rang}-й ранг__" in fuel_strings:
                    fuel_strings.insert(pos, f"{part} - {fuel}")
                    car_strings.insert(pos, f"{part} - Свободно")
                    pos += 1
                else:
                    fuel_strings[pos:pos] = [f"__{rang}-й ранг__", f"{part} - {fuel}"]
                    car_strings[pos:pos] = [f"__{rang}-й ранг__", f"{part} - Свободно"]
                    pos += 2
                for i in range(pos, len(fuel_strings)):
                    if fuel_strings[i].count(":"):
                        replace_part = fuel_strings[i][1:fuel_strings[i].find('>', 1) + 1]
                        num = self.num_arr.index(replace_part)
                        new_part = self.num_arr[num + 1]
                        fuel_strings[i] = fuel_strings[i].replace(replace_part, new_part)
                        car_strings[i] = car_strings[i].replace(replace_part, new_part)
                fuel_strings = '\n'.join(fuel_strings)
                car_strings = '\n'.join(car_strings)
                await fuel_mess.edit(content=fuel_strings)
                await car_mess.edit(content=car_strings)
            except discord.NotFound:
                pass
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass

    @commands.command()
    async def car(self, ctx, *args):
        fuel_id = load("fuel_id")
        car_id = load("car_id")
        if fuel_id is None or car_id is None:
            fuel_id = car_id = 0
        if not len(args):
            await ctx.message.delete()
            return
        if len(args) == 2:
            if args[0] != "admin" or int(args[1]) != 582:
                await ctx.message.delete()
                return
            if not await self.access(ctx):
                return
            if fuel_id:
                try:
                    mess = await ctx.channel.fetch_message(id=fuel_id)
                    await mess.delete()
                except discord.NotFound:
                    pass
            if car_id:
                try:
                    mess = await ctx.channel.fetch_message(id=car_id)
                    await mess.delete()
                except discord.NotFound:
                    pass
            arr = load("cars")
            if arr is None:
                arr = []
            fuel_text = car_text = ""
            rang = 0
            for i in range(len(arr)):
                if rang != arr[i][1]:
                    rang = arr[i][1]
                    fuel_text += f"__{rang}-й ранг__\n"
                    car_text += f"__{rang}-й ранг__\n"
                part = f"\t{self.num_arr[i]} **{arr[i][0]}**"
                fuel_text += f"{part} - {arr[i][2]}\n"
                car_text += f"{part} - Свободно\n"
            await ctx.send(file=discord.File('1.gif'))
            fuel_id = await ctx.send(fuel_text)
            save("fuel_id", fuel_id.id)
            await ctx.send(file=discord.File('2.gif'))
            car_id = await ctx.send(car_text)
            save("car_id", car_id.id)
        elif car_id:
            arr = load("cars")
            if arr is None:
                await ctx.message.delete()
                return
            car_mess = await ctx.channel.fetch_message(id=car_id)
            text = car_mess.content
            author_id = str(ctx.message.author.mention).replace("<@!", "<@")
            old_text = text.split('\n')
            text = text.replace(author_id, 'Свободно')
            text = text.split('\n')
            try:
                pos = text.index(f"\t{self.num_arr[int(args[0]) - 1]} **{arr[int(args[0]) - 1][0]}** - Свободно")
            except ValueError:
                await ctx.reply(":x: Транспорт занят! :x:", delete_after=5)
                await ctx.message.delete(delay=5)
                return
            if text[pos] == old_text[pos]:
                text[pos] = text[pos].replace('Свободно', author_id)
            text = '\n'.join(text)
            await car_mess.edit(content=text)
        await ctx.message.delete()
      
    @commands.command()
    async def init(self, ctx):  # !init
        await ctx.message.delete()
        if not await self.access(ctx):
            return
        save("channel_id", ctx.channel.id)

    @commands.command()
    async def test(self, ctx):
        await ctx.message.delete(delay=5)
        await ctx.reply(load("channel_id"), delete_after=5)

    @commands.command()
    async def week(self, ctx, week_date=''):  # !week 02.05.22
        if not await self.access(ctx, True):
            return
        if week_date == '':
            await ctx.message.delete(delay=5)
            await ctx.reply(":x: Ошибка количества аргументов [ДД.ММ.ГГ]! :x:", delete_after=5)
            return
        await ctx.message.delete()
        start_date = datetime.datetime.strptime(week_date, '%d.%m.%y')
        end_date = start_date + datetime.timedelta(days=7 - start_date.isoweekday())
        #text = f"{discord.utils.get(ctx.channel.guild.roles, name='🐅 Участник Delight FamQ').mention}\n"
        text = f">>> :white_check_mark: " \
               f":white_check_mark: :white_check_mark: *Выполнено* [**{start_date.strftime('%d.%m.%y')}** - **" \
               f"{end_date.strftime('%d.%m.%y')}**]: :white_check_mark: :white_check_mark: :white_check_mark:\n"
        if not load("week_message_id") is None:
            week_message = await ctx.channel.fetch_message(id=load("week_message_id"))
            await ctx.channel.purge(after=week_message)
        mess = await ctx.send(text)
        save("week_message_id", mess.id)
        
    @commands.command()
    async def change_dt(self, ctx, *args):  # !change_dt 30.05.22 14:30 30.05.22 15:30
        if not await self.access(ctx, True):
            return
        if len(args) != 4:
            await ctx.message.delete(delay=5)
            await ctx.reply(":x: Ошибка количества аргументов '[Дата Ш] [Время Ш] [Дата К] [Время К]'! :x:\n"
                            "Пример: !set_dt 30.04.22 14:30 30.04.22 15:30", delete_after=5)
            return
        min_datetime = min(datetime.datetime.strptime(args[0] + " " + args[1], '%d.%m.%y %H:%M'),
                           datetime.datetime.strptime(args[2] + " " + args[3], '%d.%m.%y %H:%M'))
        diff = (min_datetime - datetime.datetime.now() - datetime.timedelta(hours=3)).total_seconds()

        if diff <= 3600:
            await ctx.message.delete(delay=5)
            await ctx.reply("x: Ошибка даты / времени! :x:", delete_after=5)
            return

        await ctx.message.delete()
        save("alarm_time", min_datetime.strftime("%d.%m.%y %H:%M"))
        day_message = await ctx.channel.fetch_message(id=load("day_message_id"))
        embed = day_message.embeds[0]
        embed.description = f'>>> Шахта *[Ш]*: **{args[0]} {args[1]}**\nКабельщик *[К]*: **{args[2]} {args[3]}**'
        await day_message.edit(embed=embed)

    @commands.command()
    async def set_dt(self, ctx, *args):  # !set_dt 30.05.22 14:30 30.05.22 15:30
        if not await self.access(ctx, True):
            return
        try:
            week_message = await ctx.channel.fetch_message(id=load("week_message_id"))
            plus_list = dict()
            num_dict = {":zero:": 0, ":one:": 1, ":two:": 2, ":three:": 3, ":four:": 4, ":five:": 5, ":six:": 6,
                        ":seven:": 7, ":eight:": 8, ":nine:": 9}
            week_strings = week_message.content.split('\n')
            for string in week_strings[2:]:
                params = string.split(' ')
                count = 0
                for num in params[1].replace("::", ": :").split(' '):
                    count = count * 10 + int(num_dict.get(num))
                plus_list[params[0].replace("<@!", "<@")] = count
            day_message = await ctx.fetch_message(id=load("day_message_id"))
            embed = day_message.embeds[0]
            for index in range(2):
                field_value = embed.fields[index].value.split("\n")
                for val in field_value:
                    if val != "Свободно":
                        val = val.replace("<@!", "<@")
                        if val in plus_list.keys():
                            plus_list[val] = plus_list.get(val) + 1
                        else:
                            plus_list[val] = 1
            text = week_strings[0] + "\n" + week_strings[1]
            reverse_num_dict = {v: k for k, v in num_dict.items()}
            for (key, val) in plus_list.items():
                text += "\n" + key + " " + ''.join([reverse_num_dict.get(int(number)) for number in str(val)])
            await week_message.edit(content=text)
            await ctx.channel.purge(after=week_message, before=ctx.message)
        except discord.NotFound:
            pass
        if len(args) != 4:
            await ctx.message.delete(delay=5)
            await ctx.reply(":x: Ошибка количества аргументов '[Дата Ш] [Время Ш] [Дата К] [Время К]'! :x:\n"
                            "Пример: !set_dt 30.04.22 14:30 30.04.22 15:30", delete_after=5)
            return

        min_datetime = min(datetime.datetime.strptime(args[0] + " " + args[1], '%d.%m.%y %H:%M'),
                           datetime.datetime.strptime(args[2] + " " + args[3], '%d.%m.%y %H:%M'))
        diff = (min_datetime - datetime.datetime.now() - datetime.timedelta(hours=3)).total_seconds()

        if diff <= 3600:
            await ctx.message.delete(delay=5)
            await ctx.reply("x: Ошибка даты / времени! :x:", delete_after=5)
            return

        await ctx.message.delete()
        load("alarm_time", min_datetime.strftime("%d.%m.%y %H:%M"))
        embed = discord.Embed(
            title='Текущие контракты:',
            description=f'>>> Шахта *[Ш]*: **{args[0]} {args[1]}**\nКабельщик *[К]*: **{args[2]} {args[3]}**',
            color=discord.colour.Color.red()
        )
        embed.add_field(name='Шахта', value=f'Свободно\nСвободно\nСвободно\nСвободно', inline=True)
        embed.add_field(name='Кабельщик', value='Свободно\nСвободно\nСвободно\nСвободно\nСвободно', inline=True)
        embed.set_thumbnail(url='https://i.imgur.com/vwhyGVM.jpeg')
        mess = \
            await ctx.send(f"{discord.utils.get(ctx.channel.guild.roles, name='🐅 Участник Delight FamQ').mention}",
                           embed=embed)
        save("day_message_id", mess.id)
        if not self.check.is_running():
            self.check.start()

    async def edit_fields(self, ctx, block, aim: str, person: str):
        if not await self.access(ctx, True) or person is None:
            await ctx.message.delete()
            return
        if 0 <= block <= 1:
            day_message = await ctx.fetch_message(id=load("day_message_id"))
            embed = day_message.embeds[0]
            field_name = embed.fields[block].name
            field_value = embed.fields[block].value
            field_value = field_value.replace(aim, person, 1)
            embed.set_field_at(index=block, name=field_name, value=field_value)
            await day_message.edit(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def change(self, ctx, block: int = 0, aim: discord.Member = None, person: discord.Member = None):
        if aim is None:
            await ctx.message.delete()
            return
        await self.edit_fields(ctx, block, str(aim.mention).replace("<@!", "<@"),
                               str(person.mention).replace("<@!", "<@"))

    @commands.command()
    async def delete(self, ctx, block: int = 0, person: discord.Member = None):
        await self.edit_fields(ctx, block, str(person.mention).replace("<@!", "<@"), "Свободно")

    @commands.command()
    async def add(self, ctx, block: int = 0, person: discord.Member = None):
        await self.edit_fields(ctx, block, "Свободно", str(person.mention).replace("<@!", "<@"))

    @tasks.loop(minutes=1)
    async def check(self):
        if 0 <= (datetime.datetime.strptime(load("alarm_time"), "%d.%m.%y %H:%M") - datetime.datetime.now() - datetime.timedelta(hours=3)).total_seconds() <= 3600:
            try:
                channel = self.bot.get_channel(load("channel_id"))
                week_message = await channel.fetch_message(id=load("week_message_id"))
                plus_list = dict()
                num_dict = {":one:": 1, ":two:": 2, ":three:": 3, ":four:": 4, ":five:": 5, ":six:": 6, ":seven:": 7,
                            ":eight:": 8, ":nine:": 9}
                for string in week_message.content.split('\n')[2:]:
                    params = string.split(' ')
                    count = 0
                    for num in params[1].replace("::", ": :").split(' '):
                        count = count * 10 + int(num_dict.get(num))
                    plus_list[params[0].replace("<@!", "<@")] = count
                day_message = await channel.fetch_message(id=load("day_message_id"))
                embed = day_message.embeds[0]
                embed.clear_fields()
                listing = []
                async for mess in channel.history(after=day_message, limit=200):
                    person = await channel.guild.fetch_member(member_id=mess.author.id)
                    listing.append([mess.author.mention, mess.content, int(person.display_name.split('|')[0].strip())])
                    if listing[-1][-1] > 3:
                        listing[-1][-1] = 3
                workers = get_workers_list(plus_list, listing)
                embed.add_field(name='Шахта', value='\n'.join(value for value in workers[0]) +
                                                    ('\n' if len(workers[0]) != 4 else '') + '\n'
                                .join("Свободно" for i in range(4 - len(workers[0]))), inline=True)
                embed.add_field(name='Кабельщик', value='\n'.join(value for value in workers[1]) +
                                                        ('\n' if len(workers[1]) != 5 else '') + '\n'
                                .join("Свободно" for i in range(5 - len(workers[1]))), inline=True)
                await day_message.delete()
                day_message = await channel.send(embed=embed)
                save("day_message_id", day_message.id)
                save("alarm_time", (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%d.%m.%y %H:%M"))
            except discord.NotFound:
                pass
            self.check.cancel()

bot = commands.Bot(command_prefix='!')
bot.add_cog(Distributor(bot))
#keep_alive()
#bot.run(os.environ['TOKEN'])
bot.run('OTY5MTkyNDk4ODU1NTQ2OTgw.Ymp02g.YlGkvYwUyXWKDSRgoSunlzS8cqY')