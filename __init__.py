from flask import Flask
import sys
import os

if getattr(sys, 'frozen', False):
    templateFolder = os.path.join(sys._MEIPASS, 'templates')
    entryFile = os.path.join(sys._MEIPASS,'entries.txt')
    app = Flask(__name__, template_folder=templateFolder)
else:
    entryFile = 'entries.txt'
    app = Flask(__name__)

cardDefs = set()
with open(entryFile,'r',encoding='utf-8') as f:
    cardDefs = set(f.readlines())

class Game(object):
    def __init__(self):
        self.run = False
        self.players = dict()
        self.cards = dict()
        self.lastcard = dict()
        self.cardPool = set(cardDefs)
        self.settings = {
            'quantity':3,
            'extraCards':set()
        }

game = Game()
    


