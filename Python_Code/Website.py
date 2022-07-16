#General Imports
import numpy as np
import time
import sys 

#BrowserControl Imports

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

sys.path.insert(1,'../Credentials')
import google

#Chess API imports
import requests
import json

class BrowerControl:
    PATH = "/Users/harmandeepdubb/Documents/Chess Board Project/MECH423ProjectChessBoard/Python_Code/Selenium_Setup/geckodriver"
    
    profile = webdriver.FirefoxProfile(
        "/Users/harmandeepdubb/Library/Application Support/Firefox/Profiles/zxgi3khf.default-release")

        # s14duu3r.default

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX


    def __init__(self) -> None:
        pass

    def inputMove(self, gameURL) -> None:
        driver = webdriver.Firefox(firefox_profile=self.profile,
                                    executable_path=self.PATH,
                                    desired_capabilities=self.desired)

        driver.get("https://www.chess.com/home")

        if (driver.current_url == "https://www.chess.com/login"):
            #First time login route
            driver.get("https://www.chess.com/login/google")
            userBox = driver.find_element(By.NAME, "identifier")
            
            time.sleep(2)

            userBox.send_keys(google.username)
            userBox.send_keys(Keys.RETURN)
        
        driver.get(gameURL)

        boardInfo = driver.execute_script('''
            function coords(elem){
                var n = elem.getBoundingClientRect()
                return {top:n.top, left:n.left, width:n.width, height:n.height}
            }
            var pieces = []
            for (var i = 1; i < 9; i++){
                if (i > 6 || i < 3){
                    pieces.push(Array.from((new Array(8)).keys()).map(function(x){
                    var square = document.querySelector(`.piece.square-${x+1}${i}`)
                    return {...coords(square), piece:square.getAttribute('class').split(' ')[1]}
                    }));
                }
                else{
                    pieces.push(Array.from((new Array(8)).keys()).map(function(x){
                    var arr = pieces[pieces.length-1]
                    return {left:arr[x].left, top:arr[x].top - arr[x].height, 
                        width:arr[x].width, height:arr[x].height, piece:null}
                    }));
                }
            }
            return pieces
            ''')[::-1]


        pixelWidth = boardInfo[0][0]['width']

        time.sleep(2)

        pieceLayout = createOffsetMap(pixelWidth)

        click_square(pieceLayout[1][6], pixelWidth, driver)


def click_square(pieceOffset,width, driver):
   elem = driver.execute_script('''return document.querySelector('chess-board')''')
   ac = ActionChains(driver)
# Horizontal translation before verticle translation
# Reset the position to be at 0 0 
   ac.move_to_element(elem).move_by_offset(int(-3.5*width) + pieceOffset["right"], int(-3.5*width) + pieceOffset["down"]).click().perform()

   print("Preformed the context Click")
#    ac.move_to_element(elem).move_by_offset(square['left']+int(square['width']/2), square['top']+int(square['width']/2)).context_click().perform()

def createOffsetMap(pixelWidth):
    rightOffset = 0 
    downOffset = 0 
    pieceLayout = []
    pieceRow = []

    for i in range(7):
        for j in range(7):
            pieceDictionary = {
                "right": rightOffset*pixelWidth,
                "down": downOffset*pixelWidth
            }

            pieceRow.append(pieceDictionary)
            
            rightOffset = rightOffset + 1

        print(pieceRow)
        pieceLayout.append(pieceRow.copy())
        pieceRow.clear()

        rightOffset = 0
        downOffset = downOffset + 1

    
    print(pieceLayout)

    return pieceLayout





class chessAPI: 
    chessBoardSideLength = 8
    chessBoardSquares = 8*8

    username = ""
    opponent = ""
    jsonGameData = {}
    gameURL = ""
    playerColor = ""
    


    def __init__(self, username = "harmandeepdubb", opponent= "max_bian") -> None:

        # Reece = chessmaestro979
        self.username = username
        self.opponent = opponent

        self.jsonGameData = self.requestGameInfo()
        self.gameURL = self.getGameURL()
        self.playerColor = self.getPlayerColor()

        
    def requestGameInfo(self) -> None:
        URL = "https://api.chess.com/pub/player/" + (self.username) + "/games"

        r = requests.get(URL)

        jsonGamesData = r.json()

        games = jsonGamesData["games"]

        for game in games: 
            if (self.opponent in game["white"] or self.opponent in game["black"]):
                return game


    def getGameURL(self) -> str:
        return self.jsonGameData["url"]

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

    def getGameURL(self) -> str:
        return self.jsonGameData["url"]

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

bc = BrowerControl()

bc.inputMove(chAPI.gameURL)


