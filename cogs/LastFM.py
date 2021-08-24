import sys

import discord
from discord.ext import commands
import requests
import json
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('Texts/Secrets.txt', 'r') as filestream:
    data = filestream.readlines()
    API_KEY = data[1]
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=data[2][:-1], client_secret=data[3][:-1]))
filestream.close()
USER_AGENT = 'GuildMaster'


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def jprint(obj):  # Create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def nameCheck(discordid):
    with open('Texts/lastfmNames.txt') as filestream4:
        foundID = False
        names = filestream4.readlines()
        for line in names:
            currentline = line.split(',')
            if discordid == currentline[0]:
                foundID = True
                return currentline[1]
        if not foundID:
            return None
    filestream4.close()


def spotifyInfo(name, selection):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        if selection == 'url':
            return items[0]['images'][0]['url']
        if selection == 'genres':
            return ' - '.join(items[0]['genres'])
    else:
        if selection == 'url':
            return 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png'
        if selection == 'genres':
            return ""


def tupleSort(t):  # Sort Key for Tuples
    return int(t[1])


class LastFM(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['fmtopartist', 'fmtopartists', 'fmtopart'], pass_context=True)  # Commands
    async def fmta(self, ctx, *args):
        name = nameCheck(str(ctx.author.id))
        if name is not None:
            r = lastfm_get({'method': 'user.getTopArtists', 'user': name, 'limit': 100})
            artists = []
            artist1 = r.json()['topartists']['artist'][0]['name']
            for i in range(len(r.json()['topartists']['artist'])):
                artists.append(str(i + 1) + ". **" + r.json()['topartists']['artist'][i]['name'] + "** (" + r.json()['topartists']['artist'][i]['playcount'] + " plays)")
            desc0, desc1, desc2, desc3, desc4, desc5, desc6, desc7, desc8, desc9 = [], [], [], [], [], [], [], [], [], []
            for x in range(10):
                desc0.append(artists[x])
                desc1.append(artists[x + 10])
                desc2.append(artists[x + 20])
                desc3.append(artists[x + 30])
                desc4.append(artists[x + 40])
                desc5.append(artists[x + 50])
                desc6.append(artists[x + 60])
                desc7.append(artists[x + 70])
                desc8.append(artists[x + 80])
                desc9.append(artists[x + 90])
            desc0 = '\n'.join(desc0)
            desc1 = '\n'.join(desc1)
            desc2 = '\n'.join(desc2)
            desc3 = '\n'.join(desc3)
            desc4 = '\n'.join(desc4)
            desc5 = '\n'.join(desc5)
            desc6 = '\n'.join(desc6)
            desc7 = '\n'.join(desc7)
            desc8 = '\n'.join(desc8)
            desc9 = '\n'.join(desc9)

            artistList0 = discord.Embed(title='Top Artists', description=desc0, colour=discord.Colour.dark_theme())
            artistList1 = discord.Embed(title='Top Artists', description=desc1, colour=discord.Colour.dark_theme())
            artistList2 = discord.Embed(title='Top Artists', description=desc2, colour=discord.Colour.dark_theme())
            artistList3 = discord.Embed(title='Top Artists', description=desc3, colour=discord.Colour.dark_theme())
            artistList4 = discord.Embed(title='Top Artists', description=desc4, colour=discord.Colour.dark_theme())
            artistList5 = discord.Embed(title='Top Artists', description=desc5, colour=discord.Colour.dark_theme())
            artistList6 = discord.Embed(title='Top Artists', description=desc6, colour=discord.Colour.dark_theme())
            artistList7 = discord.Embed(title='Top Artists', description=desc7, colour=discord.Colour.dark_theme())
            artistList8 = discord.Embed(title='Top Artists', description=desc8, colour=discord.Colour.dark_theme())
            artistList9 = discord.Embed(title='Top Artists', description=desc9, colour=discord.Colour.dark_theme())

            self.client.fmta_pages = [artistList0, artistList1, artistList2, artistList3, artistList4, artistList5, artistList6, artistList7, artistList8, artistList9]
            buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
            current = 0
            embed = self.client.fmta_pages[current]
            embed.set_footer(text="Page " + str(current + 1) + "/" + str(len(self.client.fmta_pages)))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=spotifyInfo(artist1, 'url'))
            msg = await ctx.send(embed=self.client.fmta_pages[current])

            for button in buttons:
                await msg.add_reaction(button)

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    await msg.edit(embed=self.client.fmta_pages[current])
                else:
                    previous_page = current
                    if reaction.emoji == buttons[0]:
                        current = 0
                    elif reaction.emoji == buttons[1]:
                        if current > 0:
                            current -= 1
                    elif reaction.emoji == buttons[2]:
                        if current < len(self.client.fmta_pages) - 1:
                            current += 1
                    elif reaction.emoji == buttons[3]:
                        current = len(self.client.fmta_pages) - 1

                    for button in buttons:
                        await msg.remove_reaction(button, ctx.author)
                    if current != previous_page:
                        embed = self.client.fmta_pages[current]
                        embed.set_footer(text="Page " + str(current + 1) + "/" + str(len(self.client.fmta_pages)))
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.set_thumbnail(url=spotifyInfo(artist1, 'url'))
                        await msg.edit(embed=self.client.fmta_pages[current])
        else:
            await ctx.send("You're not logged in yet! Use `?fmlogin <yourname>` to set your LastFM name.")

    @commands.command(pass_context=True)
    async def fmlogin(self, ctx, message):
        foundID = False
        with open('Texts/lastfmNames.txt', 'r') as filestream2:
            names = filestream2.readlines()
            for line in names:
                currentline = line.split(',')
                if ctx.author.id == int(currentline[0]):
                    foundID = True
                    await ctx.send("You are already logged in!")
            if not foundID:
                names.append(str(ctx.author.id) + ',' + message + ',0,0' + '\n')
                with open('Texts/lastfmNames.txt', 'w') as filestream3:
                    filestream3.writelines(names)
                await ctx.send("Succesfully saved LastFM name as: " + message)
        filestream2.close()
        filestream3.close()

    @commands.command(pass_context=True, aliases=['wk', 'fmwhoknows', 'whoknows', 'Wk', 'Fmwk'])
    async def fmwk(self, ctx, *, message):  # Lists Artist Crowns
        with open('Texts/lastfmNames.txt', 'r') as filestream5:
            names = filestream5.readlines()
            plays = []
            totalPlays = 0
            for line in names:
                currentLine = line.split(',')
                user = currentLine[1]
                userID = currentLine[0]
                request = lastfm_get({'method': 'artist.getInfo', 'username': user, 'artist': message, 'autocorrect': 1})
                member = ctx.guild.get_member(int(userID))
                totalPlays += int(request.json()['artist']['stats']['userplaycount'])
                plays.append((member.display_name, request.json()['artist']['stats']['userplaycount'], userID))

        plays.sort(reverse=True, key=tupleSort)
        artist = request.json()['artist']['name']
        desc = []

        while int(plays[-1][1]) == 0:  # Removes all people with 0 plays
            for x in plays:
                if x[1] == '0':
                    plays.remove(x)

        if len(plays) != 0:
            for i in range(len(plays)):  # Makes Description string
                if i == 0:
                    desc.append(":crown: **" + plays[i][0] + "** - **" + plays[i][1] + "** plays")
                else:
                    desc.append(str(i + 1) + ". **" + plays[i][0] + "** - **" + plays[i][1] + "** plays")
            desc = '\n'.join(desc)
        else:
            desc = "No one has listened to " + artist

        with open('Texts/artists.txt', 'r') as filestream6:
            crown = 0
            remove = None
            crowns = filestream6.readlines()
            artistFound = False
            index = 0
            for line in crowns:
                cl = line.split(',')
                if artist == cl[0] and plays[0][2] == cl[1][:-1]:
                    artistFound = True
                elif artist == cl[0] and plays[0][2] != cl[1][:-1]:
                    artistFound = True
                    remove = cl[1][:-1]
                    crowns[index] = cl[0] + ',' + plays[0][2] + '\n'
                    crown = 1
                index += 1

            if not artistFound:
                crowns.append(artist + ',' + plays[0][2] + '\n')
                crown = 1

        with open('Texts/artists.txt', 'w') as filestream7:
            try:
                filestream7.writelines(crowns)
            except UnicodeEncodeError:
                uni = crowns.pop(-1)
                spl = uni.split(',')
                fixed = spl[0].encode('utf-8')
                ending = str(fixed) + "," + spl[1]
                filestream7.writelines(ending)

        ind = 0
        for el in names:
            li = el.split(',')
            if li[0] == plays[0][2]:
                names[ind] = li[0] + ',' + li[1] + ',' + str(int(li[2]) + crown) + ',0\n'
            elif li[0] == remove:
                names[ind] = li[0] + ',' + li[1] + ',' + str(int(li[2]) - crown) + ',0\n'
            ind += 1

        with open('Texts/lastfmNames.txt', 'w') as filestream8:
            filestream8.writelines(names)

        genre = spotifyInfo(artist, 'genres')
        artistE = discord.Embed(title="Who knows **" + artist + "**?", description=desc, colour=discord.Colour.dark_theme())
        artistE.set_footer(text=genre + '\n' + 'Total Plays: ' + str(totalPlays))
        artistE.set_thumbnail(url=spotifyInfo(artist, 'url'))

        filestream5.close()
        filestream6.close()
        filestream7.close()
        filestream8.close()

        await ctx.send(embed=artistE)

    @commands.command()
    async def cwlb(self, ctx):
        with open('Texts/lastfmNames.txt', 'r') as filestreamcwlb:
            cws = filestreamcwlb.readlines()
            leaderboard = []
            totalCrowns = 0
            for lines in cws:
                currentLine = lines.split(',')
                discID = currentLine[0]
                totalCrowns += int(currentLine[2])
                member = ctx.guild.get_member(int(discID))
                leaderboard.append((member.display_name, currentLine[2]))

        leaderboard.sort(reverse=True, key=tupleSort)
        desc = []
        for i in range(len(leaderboard)):
            desc.append(str(i + 1) + ". **" + leaderboard[i][0] + "** - **" + leaderboard[i][1] + "** Crowns")
        desc = '\n'.join(desc)
        lb = discord.Embed(title="Crown Leaderboard for " + str(ctx.guild), description=desc, colour=discord.Colour.dark_theme())
        lb.set_footer(text='Total Crowns: ' + str(totalCrowns))
        filestreamcwlb.close()

        await ctx.send(embed=lb)

    @commands.command()
    async def fmtest(self, ctx, message):
        r = lastfm_get({'method': 'artist.getInfo', 'username': 'GuildMasterTV', 'artist': message, 'autocorrect': 1})
        artist = r.json()['artist']['name']
        #print(r.json()['topartists']['artist'][0]['image'][1]['#text'])
        results = sp.search(q='artist:' + artist, type='artist')
        print(results)


def setup(client):  # Adds Cog
    client.add_cog(LastFM(client))
