#!/usr/bin/env python3

import os
import sys
import requests
import urllib.request
import shutil
from PyQt4 import QtGui, QtCore
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Subtype

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 400, 480)
        self.setWindowTitle("MTG random card fetcher")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

# This will show the File menu

        extractAction = QtGui.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Exit the program")
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extractAction)
        
        self.home()

        cardBack = QtGui.QLabel(self)
        cardBack.setGeometry(80, 55, 223, 311)
        pixmap = QtGui.QPixmap("cardback.png")
        cardBack.setPixmap(pixmap)
        cardBack.show()

    def home(self):

# The random button

        btn = QtGui.QPushButton("Random Card", self)
        btn.clicked.connect(self.fetch_card)
        btn.resize(btn.sizeHint())
        btn.move(140, 380)
        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, "Exit?",
                                            "Are you sure you want to exit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Application was closed by the user.")
            sys.exit()
        else:
            pass

# Get a random Magic the Gathering card from http://gatherer.wizards.com

    def fetch_card(self):
        res = requests.get('http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random')
        try:
            res.raise_for_status()
            multiUrl = res.url
            multiId = multiUrl.split('=')[-1] # Split the URL to get the digits at the end of the URL

            url = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + multiId + "&type=card"

            response = requests.get(url, stream=True)
            with open("card.jpg", "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            image = QtGui.QLabel(self)
            image.setGeometry(80, 55, 223, 311)
            pixmap = QtGui.QPixmap("card.jpg")
            image.setPixmap(pixmap)
            image.show()
            print(url)
            return url
            
        except Exception as exc:
            print('There was a problem: %s' % (exc))

def run():

    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
