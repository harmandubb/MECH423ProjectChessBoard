import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import numpy as np

import time

import sys 

sys.path.insert(1,'../Credentials')

import google


# PATH = "/Users/harmandeepdubb/Documents/Chess Board Project/MECH423ProjectChessBoard/Python_Code/Selenium_Setup/geckodriver"


# profile = webdriver.FirefoxProfile(
#     "/Users/harmandeepdubb/Library/Application Support/Firefox/Profiles/zxgi3khf.default-release")

#     # s14duu3r.default

# profile.set_preference("dom.webdriver.enabled", False)
# profile.set_preference('useAutomationExtension', False)
# profile.update_preferences()
# desired = DesiredCapabilities.FIREFOX


# driver = webdriver.Firefox(firefox_profile=profile,
#                             executable_path=PATH,
#                             desired_capabilities=desired)

# driver.get("https://www.chess.com/home")

# if (driver.current_url == "https://www.chess.com/login"):
#     #First time login route
#     driver.get("https://www.chess.com/login/google")
#     userBox = driver.find_element(By.NAME, "identifier")
    
#     time.sleep(2)

#     userBox.send_keys(google.username)
#     userBox.send_keys(Keys.RETURN)

# gameBox = driver.find_element(By.CLASS_NAME, "daily-game-grid-item-bottom")    
# gameBox.click()

# #now we are in the game state
# dailyGameURL = driver.current_url

# print(dailyGameURL)

# IDIndex = dailyGameURL.rfind("/")

# gameID = dailyGameURL[IDIndex+1:len(dailyGameURL)-1]

# print(gameID)

# # I need to know whos turn it is inorder to choose what needs to occur next. 

import requests
import json

class chessAPI: 
    chessBoardSideLength = 8
    chessBoardSquares = 8*8

    username = ""
    opponent = ""
    jasonGameData = {}
    

    def __init__(self, username = "harmandeepdubb", opponent= "chessmaestro979") -> None:
        self.username = username
        self.opponent = opponent

        URL = "https://api.chess.com/pub/player/" + (self.username) + "/games"

        r = requests.get(URL)

        jsonGamesData = r.json()

        games = jsonGamesData["games"]

        for game in games: 
            if (self.opponent in game["white"] or self.opponent in game["black"]):
                self.jsonGameData = game
                break
    

    def requestGameInfo(self, GameID= None) -> json:
        URL = "https://api.chess.com/pub/player/" + (self.username) + "/games"

        r = requests.get(URL)

        return r.json()

    def findOpponentGame(self, jsonGamesData) -> json:
        # print(json.dumps(jsonGamesData, indent=4))
        # print(json.dumps(jsonGamesData["games"], indent=4))

        # Assume only one game match is happening right now
        games = jsonGamesData["games"]


        for game in games: 
            if (self.opponent in game["white"] or self.opponent in game["black"]):
                # print(game)
                return game

    def getPlayerColor(self) -> str:
        print(json.dumps(self.jsonGameData, indent=4))

        playerColor = ""

        if(self.username in self.jsonGameData["white"]):
            playerColor = "white"
        elif(self.username in self.jsonGameData["black"]):
            playerColor = "black"

        print(playerColor)
        return playerColor

    def getCurrentToMove(self) -> str:
        return self.jsonGameData["turn"]

    def getBoardState(self) -> str:
        fen = self.jsonGameData["fen"]

        print(fen)

        board = np.zeros([8,8])

        row = 0
        col = 0

        # need to decode the string in order to get the general board set up 
        for val in fen:
            if val.isdigit():
                num = int(val)
                col = col + num
            elif (val == "/"):
                row = row + 1
                col = 0
            elif (val == " "):
                return board
            else: 
                board[row,col] = 1
                col = col + 1
            
        

chAPI = chessAPI()

playerColor = chAPI.getPlayerColor()
board = chAPI.getBoardState()


