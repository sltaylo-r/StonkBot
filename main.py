# https://rapidapi.com/apidojo/api/yahoo-finance1

from replit import db
import requests
import discord
import os

client = discord.Client()
my_secret = os.environ['TOKEN']
my_x_rapidapi_key = os.environ['x-rapidapi-key']
my_x_rapidapi_host = os.environ['x-rapidapi-host']

headers = {
    'x-rapidapi-key': my_x_rapidapi_key,
    'x-rapidapi-host': my_x_rapidapi_host
    }

# gets the price of a stock ticker
def getPrice(ticker):
  # api link for getting ticker data
  url = "https://realstonks.p.rapidapi.com/" + ticker
  
  # getting api response
  response = requests.request("GET", url, headers=headers)

  # formatting api response
  data = response.text.split(": ")

  # getting price from data
  price = data[1].split(", ")

  # returning price
  return price[0]



# gets the volume of a stock ticker
def getVolume(ticker):
  # api link for getting ticker data
  url = "https://realstonks.p.rapidapi.com/" + ticker
  
  # getting api response
  response = requests.request("GET", url, headers=headers)

  # formatting api response
  data = response.text.split(": ")

  # getting volume from data
  volume = data[4].split(", ")
  volume = volume[0].split("\"")

  # returning volume
  return volume[1]



# checks if an item exists in the database for a given user
def existsInDB(item, author):

  # if item exists in db return true
  if item in db[author]:
    return True

  # else return false
  return False



### LOGIN ###
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='use ?help for help'))



### ON MESSAGE ###
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # if message matches requirements for 
  if message.content.startswith('?'):
    # getting message contents
    message_contents = message.content.split()
    command = message_contents[0]

    # database keys
    keys = db.keys()



    ### HELP STUFF ###
    # if command matches the ?help command
    if(command == '?help'):
      print(str(message.author) + " requested help")
      await message.channel.send("```List of available commands:\n - '?price [ticker]' will fetch the price of a given stock\n - '?volume [ticker]' will fetch the volume of a stock\n - '?list' returns the items in your list and has the following modifiers:\n   - 'add [ticker]' will add a stock to your list\n   - 'remove [ticker]' will remove a stock from your list\n   - 'price [ticker]' will return the price of all tickers in your list\n   - 'volume [ticker]' will return the volume of all tickers in your list```")



    ### PRICE STUFF ###
    # if command matches the ?price command
    elif(command == '?price'):
      if(message_contents[1] != None):
        ticker = message_contents[1]
        # get price from data block
        price = getPrice(ticker)

        # print price to console and chat
        print(str(message.author) + " requested price for " + ticker)
        await message.channel.send("```" + ticker + ": " + price + "```")

      else:
        print(str(message.author) + " invalid command: \"" + message.content + "\"")
        await message.channel.send("```command not found, use '?help' for more information```")
      return



    ### VOLUME STUFF ###
    # if command matches the ?volume command
    elif(command == '?volume'):
      ticker = message_contents[1]
      # get volume from data block
      volume = getVolume(ticker)

      # print volume to console and chat
      print(str(message.author) + " requested volume for " + ticker)
      await message.channel.send("```" + ticker + " volume: " + volume + "```")
      return



    ### LIST STUFF ###
    # if command matches the ?list command
    elif(command == '?list'):
      # here we will handle user's ticker lists

      # checking if user is already in db
      if str(message.author) in keys:
        user_values = db[str(message.author)]

      # if they aren't in the db, add an entry for them
      else:
        db[str(message.author)] = user_values = [None]



      # '?list' will return the list items
      if(len(message_contents) < 2):
        # print values of list
        values = ""
        i = 1

        # update 'user_values'
        user_values = db[str(message.author)]

        # build string to print for user
        for value in user_values:
          values += str(i) + ". " + value + "\n"
          i = i + 1

        # print all values to user
        print(str(message.author) + " requested '?list'")
        await message.channel.send("```" + str(message.author) +  "'s tickers:\n" + values + "```")
        return



      # checking what the next command is
      command2 = message_contents[1]

      # checking if message_contents is long enough to have a ticker
      if(len(message_contents) > 2):
        ticker = message_contents[2]

        # if command2 is add
        if(command2 == 'add'):
          # check if they have reached the max number (10)
          if(len(db[str(message.author)]) > 9):
            print(str(message.author) + " has reached the max # of tickers")
            await message.channel.send("```oops - you have reached the maximum number of tickers (10), please remove a ticker before adding another one```")
            return

          # add 'ticker' to list
          if(existsInDB(ticker, str(message.author))):
            print("oops - " + ticker + " already in list")
            await message.channel.send("```oops - " + ticker + " already in list```")

          else:
            user_values.append(ticker)
            # if None is still in list, remove it
            if None in user_values:
              user_values.remove(None)

            db[str(message.author)] = user_values
            print("ticker " + ticker + " added to list")
            await message.channel.send("```ticker " + ticker + " added to list```")
          return



        # if command2 is remove
        elif(command2 == 'remove'):
          # remove 'ticker' from list

          if ticker in db[str(message.author)]:
            user_values.remove(ticker)
            print("ticker " + ticker + " removed from list")
            await message.channel.send("```ticker " + ticker + " removed from list```")

          else:
            print("oops - " + ticker + " not in list")
            await message.channel.send("```oops - " + ticker + " not in list```")
          return



      # if command2 is price
      elif(command2 == 'price'):
        # print values of list with the price
        values = ""
        i = 1

        # update 'user_values'
        user_values = db[str(message.author)]

        # build string to print for user
        for value in user_values:
          price = getPrice(value)
          values += str(i) + ". " + value + " - " + price + "\n"
          i = i + 1

        # print all values with prices to user
        print(str(message.author) + " requested ?list price")
        await message.channel.send("```" + str(message.author) +  "'s tickers with prices:\n" + values + "```")
        return



      # if command2 is volume
      elif(command2 == 'volume'):
        # print values of list with the volume
        values = ""
        i = 1

        # update 'user_values'
        user_values = db[str(message.author)]

        # build string to print for user
        for value in user_values:
          volume = getVolume(value)
          values += str(i) + ". " + value + " - " + volume + "\n"
          i = i + 1

        # print all values with volumes to user
        print(str(message.author) + " requested ?list volume")
        await message.channel.send("```" + str(message.author) +  "'s tickers with volume:\n" + values + "```")
        return



      # else print error
      else:
        # unknown command, print default reply
        print(str(message.author) + " invalid command: \"" + message.content + "\"")
        await message.channel.send("```command not found, please try ?help for more information```")
        return



client.run(my_secret)
