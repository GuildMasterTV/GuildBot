# Gets PC WR of Specified Game and Category
def world_record(message):
    response = requests.get("https://www.speedrun.com/api/v1/games/" + message[1].lower() + "/categories")
    json_data = json.loads(response.text)
    category = json_data["data"]  # List of all the Categories

    for i in range(len(category)):  # Finds Category ID for User Specified Category
        if category[i]["name"].lower() == message[2].lower():
            gameID = category[i]["id"]
            response = requests.get("https://www.speedrun.com/api/v1/categories/" + gameID + "/records")  # Records for Game

    json_data = json.loads(response.text)
    record = json_data["data"][0]["runs"][0]["run"]["weblink"]  # First Place Run

    # Converting Seconds to hh:mm:ss
    run_time = json_data["data"][0]["runs"][0]["run"]["times"]["primary_t"]
    hours = math.floor(int(run_time) / 3600)
    minutes = str(math.floor(((int(run_time) / 3600) - math.floor(int(run_time) / 3600)) * 60))
    minutes = minutes.rjust(2, "0")  # Adds 0 to left if minutes is 1 digit
    seconds = round(((int(run_time) / 60) - math.floor(int(run_time) / 60)) * 60)

    # Getting Name of WR Holder
    name = json_data["data"][0]["runs"][0]["run"]["players"][0]["uri"]
    response = requests.get(name)
    json_data = json.loads(response.text)
    name = json_data["data"]["names"]["international"]

    print("WR: " + str(hours) + ":" + minutes + ":" + str(seconds) + " by " + name)
    return record


def miner():
    randomNum = random.randint(1, 100)
    if randomNum <= 10:  # Trash
        luck = 0
        stones = 0
        return luck, stones
    if randomNum <= 70:  # Common
        luck = 1
        stones = random.randint(1, 40)
        return luck, stones
    if randomNum <= 90:  # Uncommon
        luck = 2
        stones = random.randint(41, 100)
        return luck, stones
    if randomNum <= 99:  # Super Rare
        luck = 3
        stones = random.randint(101, 400)
        return luck, stones
    if randomNum == 100:  # Legendary
        luck = 4
        stones = random.randint(401, 1000)
        return luck, stones

@client.event
async def on_message(message):  # When Someone Types Something
    if message.author == client.user:  # So it doesn't respond to itself potentially
        return

    if message.content.startswith("$wr"):  # $wr (Game Abbreviation) (Category)
        msg = message.content.split()  # Converts Users Message into Array Separated by Spaces
        await message.channel.send(world_record(msg))

    if message.content.startswith(">mine"):
        foundID = False
        stats = miner()
        with open("Texts/MiningStats.txt", "r") as filestream:
            data = filestream.readlines()
            index = 1
            current_time = time.localtime()
            timeNow = datetime.datetime.now()
            offset = timeNow - datetime.timedelta(0, 7200)  # 2 Hour delay between commands
            for line in data[1:]:
                currentline = line.split(",")
                if message.author.id == int(currentline[0]):
                    print(":YEP:")
                    foundID = True
                    if offset > datetime.datetime.strptime(currentline[7][:19], "%Y-%m-%d %H:%M:%S"):  # Converts to dateTime Obj
                        currentline[7] = time.strftime("%Y-%m-%d %H:%M:%S\n", current_time)  # Converts Time Obj to Str

                        if stats[0] == 0:
                            currentline[1] = str(int(currentline[1]) + 1)
                            await message.channel.send("Mined **Trash!** Better luck next time.")
                        elif stats[0] == 1:
                            currentline[2] = str(int(currentline[2]) + 1)
                            currentline[6] = str(int(currentline[6]) + stats[1])
                            await message.channel.send("Mined **" + str(stats[1]) + "** Stone")
                        elif stats[0] == 2:
                            currentline[3] = str(int(currentline[3]) + 1)
                            currentline[6] = str(int(currentline[6]) + stats[1])
                            await message.channel.send("** :small_blue_diamond: Mined an uncommon jewel! :small_blue_diamond: (" + str(stats[1]) + ")**")
                        elif stats[0] == 3:
                            currentline[4] = str(int(currentline[4]) + 1)
                            currentline[6] = str(int(currentline[6]) + stats[1])
                            await message.channel.send("Mined Trash! Better luck next time.")
                        elif stats[0] == 4:
                            currentline[5] = str(int(currentline[5]) + 1)
                            currentline[6] = str(int(currentline[6]) + stats[1])
                            await message.channel.send("Mined Trash! Better luck next time.")

                        joined_string = ",".join(currentline)
                        data[index] = joined_string
                    else:
                        difference = datetime.datetime.strptime(currentline[7][:19], "%Y-%m-%d %H:%M:%S") - offset
                        difference = str(difference)
                        await message.channel.send("You're mining too fast! Please Wait **1 hour " + difference[2:3] + " minutes and " + difference[5:6] + " seconds**")
                else:
                    index += 1

            if not foundID:
                data.append(str(message.author.id) + ',1,0,0,0,0,0,' + time.strftime("%Y-%m-%d %H:%M:%S\n", current_time))
                await message.channel.send("Caught Trash! Better luck next time.")

        with open("Texts/MiningStats.txt", "w") as filestream2:
            filestream2.writelines(data)

    if message.content.startswith("yeet"):
        if message.author.id == 227499228413427712:
            await message.channel.send("Gamer")
        else:
            await message.channel.send("Not a Gamer")