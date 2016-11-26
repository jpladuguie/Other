#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, send_from_directory
import sqlite3, time

# Web server name.
app = Flask(__name__)

# Allow access to team images.
@app.route('/TeamImages/<path:path>')
def send_js(path):
    # Return the image.
    return send_from_directory('TeamImages', path)

# Search for a players.
@app.route('/searchForPlayers')
def searchForPlayers():
    # Start timer to measure time taken to search for players.
    startTime = time.time()
    
    # Get search string from HTTP request.
    SearchString = request.args.get('SearchString')

    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Create a string to store the json data.
    json = '[  '
    
    # Search database until player with correct PlayerId is found.
    for row in curs.execute("SELECT PlayerId, Name, RegionCode FROM Players WHERE Name LIKE '% " + SearchString + "%' COLLATE NOACCENTS or Name LIKE '" + SearchString + "%' COLLATE NOACCENTS ORDER BY OverallRating DESC LIMIT 8"):
        # Create a string to store the player as json.
        json += ' { '
        for i in range(len(curs.description)):
            # Add attribute name to data.
            json += '"' + curs.description[i][0] + '": '
            # Add attribute value to data. Parse integers and floats to strings.
            if type(row[i]) == int or type(row[i]) == float:
                json += '"' + str(row[i]) + '", '
            # Unicode cannot be converted with str() so it can be parsed as it is.
            else:
                json += '"' + row[i] + '", '
        
        # Parse the string so it is correct json.
        json = json[:-2] + ' }, '

    json = json[:-2] + ' ]'
    
    # Output time taken to complete search.
    endTime = time.time()
    print("Search completed in " + str(endTime - startTime) + " seconds.")

    return json

# Returns a player data for a given PlayerId.
@app.route('/getPlayer')
def getPlayer():
    # Get PlayerId from HTTP request.
    PlayerId = request.args.get('PlayerId')
    
    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Search database until player with correct PlayerId is found.
    curs.execute("SELECT * FROM Players WHERE PlayerId='" + PlayerId + "'")
    player = curs.fetchone()
    
    # Close database.
    conn.close()
    
    if player is None:
        return "Invalid PlayerId. No player found."
    else:
    
        # Create string to store json data.
        json = '{ '
    
        # Loop through each attribute.
        for i in range(len(curs.description)):
            # Add attribute name to data.
            json += '"' + curs.description[i][0] + '": '
            # Add attribute value to data. Parse integers and floats to strings.
            if type(player[i]) == int or type(player[i]) == float:
                json += '"' + str(player[i]) + '", '
            # Unicode cannot be converted with str() so it can be parsed as it is.
            else:
                json += '"' + player[i] + '", '

        # Parse data so that it is correct json.
        json = json[:-2] + ' }'

        # Return the json data.
        return json

# Returns a certain number of player sorted by a value. It return PlayerId, Name, RegionCode,
# Team, TeamId and the value being sorted.
@app.route('/getPlayers')
def getPlayers():
    # Get the attribute to sort the players by, the startPosition and the endPosition from
    # From the HTTP request. The start and end positions are based on where the players are
    # In the data. For example, if StartPositon = 0 and EndPosition = 9 it will return
    # The top ten players.
    SortValue = request.args.get('SortValue')
    StartPosition = request.args.get('StartPosition')
    EndPosition = request.args.get('EndPosition')
    
    # Set up Players database.
    conn=sqlite3.connect('Footballers.db')
    curs=conn.cursor()
    
    # Create a string to store the json data.
    json = '[  '
    
    # Gets the correct number of player attributes sorted by the given value.
    data = curs.execute("SELECT PlayerId, Name, RegionCode, Team, TeamId, " + SortValue + " FROM Players WHERE Minutes>200 ORDER BY " + SortValue + " DESC LIMIT " + EndPosition)
    data = data.fetchall()
    
    # Select only the required number of players.
    for i in range(int(StartPosition), int(EndPosition)):
        
        # Try getting another player. If the player is out of range, (i.e. the last player has
        # been reached), break out of the loop and return the data.
        try:
            # Get the player from data.
            player = data[i]
        
            # Create a string to store the player as json.
            json += ' { '
            for j in range(len(curs.description)):
                # Add attribute name to data.
                json += '"' + curs.description[j][0] + '": '
                # Add attribute value to data. Parse integers and floats to strings.
                if type(player[j]) == int or type(player[j]) == float:
                    json += '"' + str(player[j]) + '", '
                # Unicode cannot be converted with str() so it can be parsed as it is.
                else:
                    json += '"' + player[j] + '", '
        except:
            break
        
        # Parse the string so it is correct json.
        json = json[:-2] + ' }, '

    json = json[:-2] + ' ]'
    
    # Close the database.
    conn.close()
    
    # Return the data.
    return json


# Run the server.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
