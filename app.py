from flask import Flask,request,jsonify,redirect,render_template
from random import sample,shuffle

from defs import cardDefs

app = Flask(__name__)

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

@app.route('/', methods=["GET"])
def hello():
    addr = request.remote_addr
    playerName = None

    if addr in game.players:
        playerName = game.players[addr]

    return render_template('index.html',playerName = playerName, playerAddr = addr, game = game)
    

@app.route("/login", methods=["POST"])
def login():
    if game.run:
        return f'A game is already running.'

    playerName = request.form['user']
    if playerName.strip() != '': # None empty name
        addr = request.remote_addr
        if addr not in game.players:
            game.players.update({addr:playerName})
    else:
        pass
    return redirect('/',302)

@app.route("/settings", methods=["GET","POST"])
def settings():
    if game.run:
        return redirect('/',302)
    if request.method == "GET":
        return render_template('settings.html',game = game)
    elif request.method == "POST":
        game.settings['quantity'] = int(request.form['quantity'])
        
        userInput = request.form['extraCards'].split('\r')
        for i in userInput:
            if i.strip() != '':
                game.settings['extraCards'].add(i.strip())
        return redirect('/',302)
    

@app.route("/start", methods=["GET"])
def start():
    cardNumber = game.settings['quantity'] * len(game.players)
    if cardNumber > len(cardDefs):
        return f'Insufficient cards!'

    if len(game.settings['extraCards']) > cardNumber:
        selection = list(sample(game.settings['extraCards'],cardNumber))
    else: 
        selection = list(game.settings['extraCards'])
        selection.extend(sample(game.cardPool,cardNumber-len(selection)))
    
    shuffle(selection)

    for addr,_ in game.players.items():
        game.cards.update({addr:[]})
        for i in range(game.settings['quantity']):
            game.cards[addr].append(selection.pop())

    for addr,_ in game.lastcard.items():
        game.lastcard[addr] = None

    game.run = True
    
    return redirect('/',302)

@app.route("/pass", methods=["GET"])
def pass_():
    addr = request.remote_addr
    if len(game.cards[addr]) > 0:
        game.lastcard[addr] = game.cards[addr].pop()
    else:
        pass
    return redirect('/',302)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({'players':game.players, \
                    'cards':game.cards}), \
                    200

@app.route("/reset", methods=["GET"])
def reset():
    game.__init__()
    return redirect('/',302)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80',debug=True)

