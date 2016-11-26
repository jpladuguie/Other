#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, json, sqlite3, time, pycountry
from datetime import datetime
from scipy.stats import norm


# Given a country name, generates a two character country code.
def getCountryCode(countryName):
    # Get country code data.
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
    
    # Add additional countries which are left out of the default data.
    countries['England'] = 'GB-ENG'
    countries['Wales'] = 'GB-WLS'
    countries['Scotland'] = 'GB-SCT'
    countries['Northern Ireland'] = 'GB-NIR'
    countries['Republic of Ireland'] = 'IE'
    countries['Congo DR'] = 'CD'
    countries['Côte d’Ivoire'] = 'CI'
    countries['Korea Republic'] = 'KR'
    countries['Venezuela'] = 'VE'
    countries['Curaçao'] = 'CW'
    
    # Use the dictionary to look up the code and return it.
    countryCode = countries.get(countryName.encode("utf-8"), "")
    return countryCode


# Generate a percentage from two values to prevent a divide by zero error.
def getPercentage(x, y):
    if y == 0.0:
        return 0.0
    else:
        return float((x / y) * 100.0)


# Given a date of birth, returns an age.
def getAge(dateOfBirth):
    dateOfBirth = dateOfBirth[:-9]
    date = datetime.strptime(dateOfBirth, '%Y-%m-%d')
    return ((datetime.today() - date).days/365)

# Generate ratings for attacking, defending, passing and statistics based on player statistics.
# Uses the inverse normal distribution to normalise the values.
def getRatings(player):
    # Get attributes.
    ShotSuccess = getPercentage(player["ShotsOnGoal"], player["Shots"])
    PassSuccess = getPercentage(player["PassesCompleted"], player["Passes"])
    
    # Weighted attacking rating.
    AttackingRating = (((float(player["Goals"]) * 5.0) + (float(player["Assists"]) * 3.0) + float(player["Shots"])) / float(player["Games"])) + (ShotSuccess / 75.0)

    # Weighted defending rating.
    DefendingRating = (((float(player["TacklesWon"]) * 5.0) + (float(player["LastManTackle"]) * 3.0) + (float(player["Interceptions"]) * 1.5) + (float(player["BlockedShots"]) * 10.0)) / float(player["Games"])) + (float(player["DefenderCleanSheets"]) * 5.0) + (PassSuccess / 20.0)
    
    # Weighted passing rating.
    PassingRating = (((float(player["Assists"]) * 3.0) + float(player["Crosses"]) + (float(player["Passes"]) * 0.1)) / float(player["Games"])) + (PassSuccess / 75.0)
    
    # Weighted discipline rating.
    DisciplineRating = ((player["RedCards"] * 5.0) + player["YellowCards"] + (float(player["Fouls"])) / (float(player["Games"])))
    
    # Return the ratings as a dictionary.
    return {"AttackingRating": AttackingRating, "DefendingRating": DefendingRating, "PassingRating": PassingRating, "DisciplineRating": DisciplineRating}


# Get data from API. If argument is left empty, statistics for all players will be fetched.
# Otherwise, the personal information of a specific player provided by the PlayerId will be fetched.
def getData(PlayerId=""):
    # Start timer to measure time taken to get data.
    startTime = time.time()
    
    # Set HTTP headers for request.
    headers = {
        'Host': 'api.fantasydata.net',
        'Ocp-Apim-Subscription-Key': '5a2b7b21c3524a15a7ab1721bb43d7b8',
    }
    
    # Get all player data or a specific player's data depending on whether the PlayerId has been provided.
    if PlayerId == "":
        path = "/soccer/v2/json/PlayerSeasonStats/73?"
    else:
        path = "/soccer/v2/json/Player/" + str(PlayerId) + "?"
    
    try:
        # API url.
        conn = httplib.HTTPSConnection('api.fantasydata.net')
        # Create the request.
        conn.request("GET", path, "{body}", headers)
        # Get the response and save it to the data variable.
        response = conn.getresponse()
        data = response.read()
        # Convert the data string to json to be parsed correctly.
        players = json.loads(data)
        # Close the connection once the data has been received.
        conn.close()
        
        endTime = time.time()
        print("Data received in " + str(endTime - startTime) + " seconds.")
    
        # Return the data.
        return players
    # Catch any erros in getting the data.
    except Exception as e:
        print("Error, unable to load data from API.".format(e.errno, e.strerror))
        return false

"""def getData(PlayerId=""):
    # Start timer to measure time taken to get data.
    startTime = time.time()
    
    # Set HTTP headers for request.
    headers = {
    'Host': 'api.fantasydata.net',
    'Ocp-Apim-Subscription-Key': '5a2b7b21c3524a15a7ab1721bb43d7b8',
    }
    
    # Get all player data or a specific player's data depending on whether the PlayerId has been provided.
    if PlayerId == "":
        path = "/soccer/v2/json/PlayerSeasonStats/73?"
    else:
        path = "/soccer/v2/json/Player/" + str(PlayerId) + "?"
    
    try:
        conn = httplib2.Http()
        resp, resp_body = conn.request('http://api.fantasydata.net' + path, "GET", headers=headers, body=None)
        # Convert the data string to json to be parsed correctly.
        players = json.loads(resp_body.decode('utf8'))
        
    
        endTime = time.time()
        print("Data received in " + str(endTime - startTime) + " seconds.")
    
        # Return the data.
        return players
    # Catch any erros in getting the data.
    except Exception as e:
        print("Error, unable to load data from API.".format(e.errno, e.strerror))
        return false"""


# Given a set of data received from the API, it will save it to the database. Only statistical data needs
# To be updated, as personal information never changes. If the player isn't in the database, their personal
# Information is fetched and they are added to the database.
def saveData(players):
    # Start timer to measure time taken to save data.
    startTime = time.time()
    
    # Counters.
    numberUpdated = 0
    numberAdded = 0
    
    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Loop through every player.
    for playerStats in players:
        curs.execute("SELECT * FROM Players WHERE PlayerId='" + str(playerStats["PlayerId"]) + "'")
        player = curs.fetchone()
        
        if player is None:
            # If the player isn't in the database, get their personal information and insert a new entry.
            playerData = getData(playerStats["PlayerId"])
            ratings = getRatings(playerStats)
            # Insert the player as a new row into the table.
            curs.execute("""INSERT INTO Players values((?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))""", (playerStats["PlayerId"], playerStats["Name"], playerData["Nationality"], getCountryCode(playerData["Nationality"]), playerStats["Team"], playerStats["TeamId"], playerStats["Position"], playerData["Jersey"], playerData["Height"], playerData["Weight"], playerData["BirthDate"], getAge(playerData["BirthDate"]), playerData["PhotoUrl"], int(playerStats["Games"]), int(playerStats["Minutes"]), int(playerStats["Goals"]), int(playerStats["Assists"]), int(playerStats["YellowCards"]), int(playerStats["RedCards"]), getPercentage(playerStats["ShotsOnGoal"], playerStats["Shots"]), getPercentage(playerStats["PassesCompleted"], playerStats["Passes"]), getPercentage(playerStats["TacklesWon"], playerStats["Games"])/100.0, ratings["AttackingRating"], ratings["DefendingRating"], ratings["PassingRating"], ratings["DisciplineRating"], 0))
            numberAdded += 1
            print("Added: " + playerStats["Name"])
        
        else:
        # If the player is already in the database, update the data using the statistics from the data.
            ratings = getRatings(playerStats)
            curs.execute("UPDATE Players SET Games = ?, Minutes = ?, Goals = ?, Assists = ?, YellowCards = ?, RedCards = ?, ShotSuccess = ?, PassSuccess = ?, TacklesWon = ?, AttackingRating = ?, DefendingRating = ?, PassingRating = ?, DisciplineRating = ?, Age = ? WHERE PlayerId='" + str(playerStats["PlayerId"]) + "'", (int(playerStats["Games"]), int(playerStats["Minutes"]), int(playerStats["Goals"]), int(playerStats["Assists"]), int(playerStats["YellowCards"]),int( playerStats["RedCards"]), getPercentage(playerStats["ShotsOnGoal"], playerStats["Shots"]), getPercentage(playerStats["PassesCompleted"], playerStats["Passes"]), getPercentage(playerStats["TacklesWon"], playerStats["Games"])/100.0, ratings["AttackingRating"], ratings["DefendingRating"], ratings["PassingRating"], ratings["DisciplineRating"], getAge(player[10])))
            numberUpdated += 1

    # Remove any null values.
    curs.execute("UPDATE Players SET Jersey = ' ' WHERE Jersey IS NULL")
    curs.execute("UPDATE Players SET Height = ' ' WHERE Height IS NULL")
    curs.execute("UPDATE Players SET Weight = ' ' WHERE Weight IS NULL")
    
    # Close database.
    conn.commit()
    conn.close()
    
    endTime = time.time()
    print(str(numberAdded) + " players added and " + str(numberUpdated) + " players updated in " + str(endTime - startTime) + " seconds.")


# Normalise all ratings between 1 and 100 based on the inverse normal distribution.
def normaliseRating(rating):
    # Start timer to measure time taken to normalise the ratings.
    startTime = time.time()
    
    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Get the maximum value to calculate probabilities for each player, giving a value between 0 and 1.
    maxValue = curs.execute("SELECT " + rating + " FROM Players ORDER BY " + rating + " DESC LIMIT 1").fetchone()[0]
    numberOfPlayers = curs.execute("SELECT Count(*) FROM Players").fetchall()[0][0]
    maxProb = 1.0 - (1.0 / float(numberOfPlayers))
    maxZ = norm.ppf(maxProb)
    sigma = (50.0 / maxZ)
    
    # Get the PlayerId and rating value for each player, sorted by value.
    data = curs.execute("SELECT PlayerId, " + rating + " FROM Players ORDER BY " + rating + " DESC")
    data = data.fetchall()
    
    # Initialise a counter variable.
    pos = 1
    
    # Loop through each player.
    for player in data:
        # Get a value between 0 and 1 depending on how high the value is.
        prob = 1.0 - (float(pos) / float(numberOfPlayers + 1.0))
        # Get the z value from the probablity using the inverse normal distribution.
        z = norm.ppf(prob)
        # Calculate the normalised value.
        value = int(50.0 + sigma * z)
        # Invert if DisciplineRating as a lower value is better.
        if rating == "DisciplineRating":
            value = 100 - value
        # Update the player with the new value.
        curs.execute("UPDATE Players SET " + rating + " = ? WHERE PlayerId = ?", (value, player[0]))
        # Increment the counter.
        pos += 1
    
    # Save the changes to the database.
    curs.close()
    conn.commit()

    endTime = time.time()
    print("Normalised " + rating + " in " + str(endTime - startTime) + " seconds.")

def getOverallRatings():
    # Start timer to measure time taken to normalise the ratings.
    startTime = time.time()
    
    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Get the PlayerId and rating value for each player, sorted by value.
    data = curs.execute("SELECT PlayerId, AttackingRating, DefendingRating, PassingRating FROM Players")
    data = data.fetchall()
    
    # Loop through each player.
    for player in data:
        # Get the rating as an average of AttackingRating, DefendingRating and PassingRating.
        rating = (player[1] + player[2] + player[3]) / 3.0
        # Update the player with the new value.
        curs.execute("UPDATE Players SET OverallRating = ? WHERE PlayerId = ?", (rating, player[0]))
    
    # Save the changes to the database.
    curs.close()
    conn.commit()

    endTime = time.time()
    print("Overall ratings generated in " + str(endTime - startTime) + " seconds.")


print("Beginning update.")
# Start the timer to measure total time taken.
startTime = time.time()
# Get the data from the API.
players = getData()
# Save the data to the database.
saveData(players)
# Normalise the ratings values.
normaliseRating("AttackingRating")
normaliseRating("DefendingRating")
normaliseRating("PassingRating")
normaliseRating("DisciplineRating")
getOverallRatings()
# End the timer and print the time taken.
endTime = time.time()
print("Total database updated in " + str(endTime - startTime) + " seconds.")

