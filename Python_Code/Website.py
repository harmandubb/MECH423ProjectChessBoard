from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

import sys 

sys.path.insert(1,'../Credentials')

import google



PATH = "/Users/harmandeepdubb/Documents/Chess Board Project/MECH423ProjectChessBoard/Python_Code/Selenium_Setup/geckodriver"


profile = webdriver.FirefoxProfile(
    "/Users/harmandeepdubb/Library/Application Support/Firefox/Profiles/zxgi3khf.default-release")

    # s14duu3r.default

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX


driver = webdriver.Firefox(firefox_profile=profile,
                            executable_path=PATH,
                            desired_capabilities=desired)

driver.get("https://www.chess.com/home")

if (driver.current_url == "https://www.chess.com/login"):
    #First time login route
    driver.get("https://www.chess.com/login/google")
    userBox = driver.find_element(By.NAME, "identifier")
    
    time.sleep(2)

    userBox.send_keys(google.username)
    userBox.send_keys(Keys.RETURN)

gameBox = driver.find_element(By.CLASS_NAME, "daily-game-grid-item-bottom")    
gameBox.click()

#now we are in the game state
dailyGameURL = driver.current_url

print("Type is: {}".format(type(dailyGameURL)))

print(dailyGameURL)

IDIndex = dailyGameURL.rfind("/")

gameID = dailyGameURL[IDIndex+1:len(dailyGameURL)-1]

print(gameID)

