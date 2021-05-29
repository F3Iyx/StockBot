import time
import datetime
from selenium import webdriver
from Amazon import Amazon
from beep import *
import platform
import os

platform = platform.system()
if 'Windows' in platform:
    clear = lambda: os.system('cls')
if 'Linux' in platform:
    clear = lambda: os.system('clear')
clear()

# Piepton wird vorbereitet
beepInit()

def searchFile(file):
    # öffnet das Dokument
    file = open(file, "r")

    # definiert die Variablen für die verschiedenen Läden
    global amazonLinks
    amazonLinks = []
    global nbbLinks
    nbbLinks = []
    global maxPrice
    global sleepTime

    # checkt alle Links
    currentLine = ''
    while 'This is the end of the file' not in currentLine:
        currentLine = str(file.readline())
        if currentLine[:1] != '#':
            if 'amazon' in currentLine:
                amazonLinks.append(currentLine)
            if 'nbb' in currentLine:
                nbbLinks.append(currentLine)
            if 'maxPrice[' in currentLine:
                currentLine = currentLine.lstrip('maxPrice[€]â‚¬= ')
                try:
                    currentLine = currentLine.replace(',', '.')
                except Exception:
                    time.sleep(0)
                maxPrice = float(currentLine)
                x = str(datetime.datetime.now())
                print('\033[2;37m' + x + '\033[2;33m' + " Your configured maximum price is " + str(maxPrice) + '€')
            if 'sleep-time[seconds]' in currentLine:
                currentLine = currentLine.lstrip('sleep-time[seconds]= ')
                try:
                    currentLine = currentLine.replace(',', '.')
                except Exception:
                    time.sleep(0)
                sleepTime = float(currentLine)
                x = str(datetime.datetime.now())
                print('\033[2;37m' + x + '\033[2;33m' + " Your configured sleep-time between reloads is " +
                      str(sleepTime) + ' seconds')

    # schließt das Dokument
    file.close()

#Durchsuchung des Textdokuments
searchFile('links.txt')

# Ein Webdriver-Fenster wird je nach OS mit einem bestimmten Treiber geöffnet
if 'Linux' in platform:
    browser = webdriver.Firefox(executable_path="./geckodriver")
elif 'Windows' in platform:
    browser = webdriver.Firefox(executable_path="./geckodriver.exe")
else:
    browser = webdriver.Firefox(executable_path="./geckodriver")
    x = str(datetime.datetime.now())
    print('\033[2;37m' + x + '\033[2;31m' + " An error occurred while checking your OS. There might be some problems")

# Die verschiedenen Website-Klassen werden initialisiert
amazon = Amazon(browser)

# Die exit-Variable für den Kreislauf wird eingestellt
global transactionPossible
# noinspection PyRedeclaration
transactionPossible = False

# Die Schleife prüft alle Links nacheinander
while transactionPossible is False:
    for i in amazonLinks:
        amazon.check(browser, i, maxPrice)
        time.sleep(sleepTime)
