# -------------------------------------------------------------# -------------------------------------------------------------
# Imports
import random # Shuffle les cartes
from collections import Counter # Coumpter nombre d'un carte specifique  dans un mains

# -------------------------------------------------------------# -------------------------------------------------------------
# Card Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Card:
    def __init__(self, value, suit, img):
        self.value = value # VAleur D'un carte
        self.suit = suit # Type du carte
        self.img = img # Image pour representer la carte

    def __str__(self):
        return f"{self.value}{self.suit}{self.img}"

# -------------------------------------------------------------# -------------------------------------------------------------
# Deck Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Deck:
    def __init__(self):
        self.cardDeck = []
        self.createDeck()

    """""
    _______________________________________________________________________

    Methode: createDeck
    _______________________________________________________________________

    1. Creer une nouvelle deck pour la debut de la jeu. 
    2. On shuffle pour randomizer.    
    """""
    def createDeck(self):
        cardValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        cardSuit = ["D", "H", "S", "C"]
        cardImage = ["🃂", "🃃", "🃄", "🃅", "🂦", '🂧', "🂨", '🂩', "🂪", "🂫", "🂬", "🂮", "🂾"]

        for suit in cardSuit:
            for value in cardValues:
                self.cardDeck.append(Card(value, suit, cardImage[value - 2]))

        random.shuffle(self.cardDeck)
        
    """""
    _______________________________________________________________________

    Methode: customDeck
    _______________________________________________________________________

    Pour faire un custom deck pourla testage
    
    """""
    def customDeck(self, customDeck):
        self.cardDeck = []
        for value, suit, img in customDeck:
            self.cardDeck.append(Card(value, suit, img))

# -------------------------------------------------------------# -------------------------------------------------------------
# Player Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Player:
    def __init__(self, name):
        self.playerName = name # Nom du Joueur
        self.playerDeck = [] # Main du Joueur
        self.playerDeckValue = 0 # Niveau de force de la main du joueurs
        self.playerDeckStatsData = {
            'HighCard': 0, 'HighPair': 0, 'HighThree': 0, 'HighFour': 0,
            'LowCard': 0, 'LowPair': 0, 'LowThree': 0,
            'FlushType': "N/A", 'HighestCardInStraight': 0, 'FlushValues': [],
            'FiveHighestCards': [], 'HandValue': 0
        }
        self.playerCurrency = Currency()
        self.currentRoundBet = 0

    """""
    _______________________________________________________________________

    Methode: receiveCard
    _______________________________________________________________________

    Utiliser pour chercher une nouvelle carte pour le main du joueur.
    
    """""
    def receiveCard(self, MainDeck):
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)
        self.playerDeck.sort(key=lambda card: card.value)

    """""
    _______________________________________________________________________

    Methode: grabFiveHighestCards
    _______________________________________________________________________

    Utiliser pour chercher les 5 plus grand cartes du mains du joueurs en ordre DESC
    
    """""
    def grabFiveHighestCards(self, deck):
        reversedDeck = sorted(deck, key=lambda card: card.value, reverse=True)
        self.playerDeckStatsData['FiveHighestCards'] = [card.value for card in reversedDeck[:5]]

    """""
    _______________________________________________________________________

    Methode: resetData
    _______________________________________________________________________

    Utiliser pour faire un bon reset de tous les donne d'un joueurs
    au debut d'une nouvvelle jeux de poker!

    """""
    def resetData(self):
        self.playerDeckStatsData = {
            'HighCard': 0, 'HighPair': 0, 'HighThree': 0, 'HighFour': 0,
            'LowCard': 0, 'LowPair': 0, 'LowThree': 0,
            'FlushType': "N/A", 'HighestCardInStraight': 0, 'FlushValues': [],
            'FiveHighestCards': [], 'HandValue': 0
        }

# -------------------------------------------------------------# -------------------------------------------------------------
# Currency Class
# -------------------------------------------------------------# -------------------------------------------------------------

class Currency:
    def __init__(self):
        self.currency = 0
        
    """""
    _______________________________________________________________________

    addCurrency : Ajouter L'argent au object
    removeCurrency : Enelver L'argent du object
    resetCurrency : Reset L'argent de l'object
    getCurrency : Chercher L'argent de l'object
    setCurrency: Set L'argent de l'object

    _______________________________________________________________________

    Utiliser pour ajouter de l'argent
    """""

    def addCurrency(self, currencyBeingAdded):
        self.currency += currencyBeingAdded

    def removeCurrency(self, currencyBeingRemoved):
        self.currency -= currencyBeingRemoved

    def resetCurrency(self):
        self.currency = 0

    def getCurrency(self):
        return self.currency

    def setCurrency(self, amount):
        self.currency = amount

# -------------------------------------------------------------# -------------------------------------------------------------
# Table Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Table:
    def __init__(self):
        self.tableDeck = []
    """""
    _______________________________________________________________________

    Methode: receiveCard
    _______________________________________________________________________

    Utiliser pour ajouter un carte du deck au table
    """""
    def setupTable(self, MainDeck):
        try:
            while len(self.tableDeck) < 3:
                self.receiveCard(MainDeck)
        except:
            print("Table Setup has encountered an issue")

    
    """""
    _______________________________________________________________________

    Methode: receiveCard
    _______________________________________________________________________

    Utiliser pour ajouter un carte du deck au table
    """""
    def receiveCard(self, MainDeck):
        newCard = MainDeck.cardDeck.pop()
        self.tableDeck.append(newCard)

# -------------------------------------------------------------# -------------------------------------------------------------
# Game Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Game:
    
    def __init__(self, playerNames):
        self.deck = Deck() # Deck de carte
        self.table = Table() # Table actif
        self.players = playerNames # Nom des Joueurs
        self.round = 0 # Ronde actif
        self.currentTurn = 0 # Active turn
        self.playerFolded = False # Si Un joueur a arreter le jeu
        self.pot = Currency() # L'argent du jeu
        self.pot.resetCurrency() # Reset L'argent
        self.currentBet = 0 # Le bet sera 0
        self.lastPot = 0 # Pot sera 0
        self.gameOver = False # Jeu Fini
    
    # -------------------------------------------------------------# ------------------------------------------------------------- 
    # -------------------------------------------------------------# ------------------------------------------------------------- Turns
    # -------------------------------------------------------------# ------------------------------------------------------------- 

    """""
    _______________________________________________________________________

    ***** Section *****
      
    Turn Management

    Ici c'est pour pour les turns des joueurs
    _______________________________________________________________________

    Methode: nextTurn
    _______________________________________________________________________

    Utiliser pour chercher le joeuur qui doit joueuer 
    """""
    def getCurrentPlayer(self): # Chercher le joueur present
        return self.players[self.currentTurn]

    """""
    _______________________________________________________________________

    Methode: nextTurn
    _______________________________________________________________________

    Utiliser pour changer le turn du joeueur actif

    """""
    def nextTurn(self): #Changer le turn du joueur actif
        self.currentTurn = (self.currentTurn + 1) % len(self.players)

    # -------------------------------------------------------------# ------------------------------------------------------------- 
    # -------------------------------------------------------------# ------------------------------------------------------------- Game Setup
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    ***** Section *****
      
    Game Setup

    Ici on setup le jeu qaund il commence, systeme de rondes
    _______________________________________________________________________

    Methode: startGameSession
    _______________________________________________________________________

    Quand le joueur veut commencer a jouer au poker du site , ce fonction est la
    pour setup le jeu elle meme et donner l'argent au joueur

    returns status du joeur qui a faite l'action.
    """""   
    def startGameSession(self): # Pour quand les joueurs rentre dans jeux initiallement
        for player in self.players:
            player.playerCurrency.setCurrency(100)
        self.newWholeRound()

    """""
    _______________________________________________________________________

    Methode: newWholeRound
    _______________________________________________________________________

    Quand le jeu est fini, mais les joueurs veut continuer ave cleur pots

    1. Reset Round
    2. Reset Joueurs
    3. Reste Table
    4. Reset Cartes
    5. Reset Etat du Jeu

    """""
    def newWholeRound(self): # Setup pour le nouvelle jeux
        self.deck = Deck()
        self.round = 0
        self.playerFolded = False
        self.table.tableDeck = []
        self.pot.resetCurrency()
        self.currentBet = 0
        self.currentTurn = 0
        self.gameOver = False

        for player in self.players:
            player.playerDeck = []
            player.receiveCard(self.deck)
            player.receiveCard(self.deck)
            player.resetData()
            player.playerDeckValue = 0
        
        for _ in range(5):
            self.table.receiveCard(self.deck)
    
    """""
    _______________________________________________________________________

    Methode: progressRound
    _______________________________________________________________________

    Le system ronde, pour quoi faire quand il y aune nouvelle ronde?

    Donc a chaque etape du jeux:
    1. Ecrit le satus et le nom de la ronde commedans le vrai jeu
    2. Les bet du joeuurs
    3. Cherche le nouvelle state de sjoeuurs pour le front-end
    4. L enumero de la ronde
    5. Determine si le jeu est fini ou non.

    """""
    def progressRound(self): # Changer le ronde durant le jeux
        if self.gameOver:
            return {"status": "error", "message": "Game already finished"}

        # PRE-FLOP
        if self.round == 0:
            self.resetBettingRound()
            self.currentTurn = 1
            state = self.getStateForPlayer(1)
            self.round = 1
            return {"status": "preflop", "state": state}

        # FLOP
        elif self.round == 1:
            self.resetBettingRound()
            self.currentTurn = 1
            state = self.getStateForPlayer(1)
            self.round = 2
            return {"status": "flop", "state": state}

        # TURN
        elif self.round == 2:
            self.resetBettingRound()
            self.currentTurn = 1
            state = self.getStateForPlayer(1)
            self.round = 3
            return {"status": "turn", "state": state}

        # RIVER
        elif self.round == 3:
            self.resetBettingRound()
            self.currentTurn = 1
            state = self.getStateForPlayer(1)
            self.round = 4
            return {"status": "river", "state": state}

        # SHOWDOWN
        elif self.round == 4:
            self.checkDeckValues()
            final_state = self.getFinalState()
            winner_name = final_state["winner"]
            pot_amount = self.pot.getCurrency()
            self.lastPot = pot_amount

            if winner_name != "Tie!":
                for player in self.players:
                    if player.playerName == winner_name:
                        player.playerCurrency.addCurrency(pot_amount)
            else:
                split = pot_amount // len(self.players)
                for player in self.players:
                    player.playerCurrency.addCurrency(split)

            self.gameOver = True
            return {
                "status": "showdown",
                "state": final_state,
                "pot_won": pot_amount
            }

    """""
    _______________________________________________________________________

    Methode: aiVisibleDeck
    _______________________________________________________________________

    Utiliser pour faire le ronde claire  pour l'ordinateur dans le backend

    """""
    def aiVisibleDeck(self, playerIndex): # Utiliser pour faire le ronde claire  pour l'ordinateur dans le backend

        visibleCount = 0
        if self.round == 0:   # preflop
            visibleCount = 0
        elif self.round == 1: # flop
            visibleCount = 3
        elif self.round == 2: # turn
            visibleCount = 4
        elif self.round >= 3: # river
            visibleCount = 5

        player = self.players[playerIndex]
        return player.playerDeck + self.table.tableDeck[:visibleCount]    

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Betting
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    ***** Section *****
      
    System de Betting

    Utilisation du class Currency et Joueurs pour creer un experience realsitique
    pour les jouuerus
    _______________________________________________________________________

    Methode: bet
    _______________________________________________________________________

    Quand le joueur veut faire un bet, son bet  augmenter le bet  feaut
    et non le defaut qu'ont force.

    1. Verfie si jeu est deja fini
    2. Verfie si c'est le tourne du joueur
    3. Largent se fait ajouter au pot
    4. L'argent sera enlever au joueur

    returns status du joeur qui a faite l'action.
    """""    
    def bet(self, playerIndex, amount): # Action Bet, ajouter un valeur defaut l'argent au pot!

        # Si Jeu est deja fini
        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}

        #Si c'est pas le tourne du joeur encore
        if playerIndex != self.currentTurn:
            return {"status": "error",
                    "message": f"Ce n'est pas votre tour de jouer! C'est le tour de {self.players[self.currentTurn].playerName}."}

        player = self.players[playerIndex]
        if amount > player.playerCurrency.currency:
            amount = player.playerCurrency.currency

        player.playerCurrency.removeCurrency(amount)
        self.pot.addCurrency(amount)
        player.currentRoundBet = amount

        self.currentBet = amount
        self.nextTurn()

        if self.bettingRoundComplete():
            return self.progressRound()  # auto-progress and return new state

        return {"status": "bet_placed", "player": player.playerName, "amount": amount, "pot": self.pot.getCurrency()}

    """""
    _______________________________________________________________________

    Methode: raise_bet
    _______________________________________________________________________

    Quand le joueur veut faire un raise_bet, son bet  augmenter le bet totale custom
    et non le defaut qu'ont force.

    1. Verfie si jeu est deja fini
    2. Verfie si c'est le tourne du joueur
    3. Largent se fait ajouter au pot
    4. L'argent sera enlever au joueur

    returns status du joeur qui a faite l'action.
    """""
    def raise_bet(self, playerIndex, raiseAmount): # Action Raise_Bet pour fair un valeur custom

        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}

        if playerIndex != self.currentTurn:
            return {"status": "error",
                    "message": f"Ce n'est pas votre tour de jouer! C'est le tour de {self.players[self.currentTurn].playerName}."}

        player = self.players[playerIndex]
        newBet = self.currentBet + raiseAmount
        to_pay = newBet - player.currentRoundBet

        if to_pay > player.playerCurrency.currency:
            to_pay = player.playerCurrency.currency
            newBet = player.currentRoundBet + to_pay

        player.playerCurrency.removeCurrency(to_pay)
        self.pot.addCurrency(to_pay)
        player.currentRoundBet += to_pay
        self.currentBet = newBet
        self.nextTurn()

        if self.bettingRoundComplete():
            return self.progressRound()  # auto-progress and return new state

        return {"status": "raise", "player": player.playerName, "raise_amount": raiseAmount, "total_bet": newBet, "pot": self.pot.getCurrency()}
    
    """""
    _______________________________________________________________________

    Methode: call
    _______________________________________________________________________

    Quand le joueur veut faire un call, son bet va macther celle qui est demander exacte

    1. Verfie si jeu est deja fini
    2. Verfie si c'est le tourne du joueur
    3. L'argent se fait ajouter au pot
    4. L'argent sera enlever au joueur

    returns status du joeur qui a faite l'action.
    """""
    def call(self, playerIndex): # Action Call, pour accepter le bet

        # Si Deja Fini
        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}

        # Si Pas son tourne
        if playerIndex != self.currentTurn:
            return {"status": "error",
                    "message": f"Ce n'est pas votre tour de jouer! C'est le tour de {self.players[self.currentTurn].playerName}."}

        player = self.players[playerIndex]
        to_call = self.currentBet - player.currentRoundBet

        # Ajoute L'argent au totale
        if to_call < 0:
            to_call = 0
        if to_call > player.playerCurrency.currency:
            to_call = player.playerCurrency.currency

        #Enleve L'argent
        player.playerCurrency.removeCurrency(to_call)
        self.pot.addCurrency(to_call)
        player.currentRoundBet += to_call
        self.nextTurn()

        if self.bettingRoundComplete():
            return self.progressRound()  # auto-progress and return new state

        return {"status": "call", "player": player.playerName, "amount": to_call, "pot": self.pot.getCurrency()}

    """""
    _______________________________________________________________________

    Methode: fold
    _______________________________________________________________________

    Quand le joueur veut faire un fold, le jeux va s'arreter

    1. Verfie si jeu est deja fini
    2. Verfie si c'est le tourne du joueur
    3. Largent se fait ajouter au pot
    4. L'argent sera enlever au joueur

    returns status du joeur qui a faite l'action.
    """""
    def fold(self, playerIndex): # Action Fold, Arreter le jeux car cartes ne sont pas assez bonnes

        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}

        self.playerFolded = True
        winnerIndex = 0 if playerIndex == 1 else 1
        self.players[winnerIndex].playerCurrency.addCurrency(self.pot.getCurrency())
        self.pot.resetCurrency()
        return {"status": "player_folded", "foldedPlayer": self.players[playerIndex].playerName,
                "winner": self.players[winnerIndex].playerName, "pot": self.players[winnerIndex].playerCurrency.getCurrency()}

    """""
    _______________________________________________________________________

    Methode: check
    _______________________________________________________________________

    Quand le joueur veut faire un check, il va simpleemnt allez au prochain tourne.

    returns status du joeur qui a faite l'action.
    """""
    def check(self, playerIndex): # Action Check, bet rien et continue car cartes sont okay mais pas super

        player = self.players[playerIndex]

        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}


        if playerIndex != self.currentTurn:
            return {"status": "error", "message": f"Ce n'est pas votre tour de jouer! C'est le tour de {self.players[self.currentTurn].playerName}."}

        if player.currentRoundBet < self.currentBet:
            return {"status": "error", "message": "Action doit être suivre, relancer, ou tout miser."}

        self.nextTurn()

        # Auto-progress if all matched
        if self.bettingRoundComplete():
            return self.progressRound()

        return {"status": "check", "player": player.playerName, "pot": self.pot.getCurrency()}

    """""
    _______________________________________________________________________

    Methode: all_in
    _______________________________________________________________________

    Quand le joueur veut faire un all-in, on va prendre l'argent complete du joueur.
    Et puis on le met dnas le pot.

    returns l'action faite.
    """""
    def all_in(self, playerIndex): # Action All in, le joeuur met tous son argent dans le pot
        player = self.players[playerIndex]

        if self.round >= 4:
            return {"status": "error", "message": "Partie déjà terminée"}

        if playerIndex != self.currentTurn:
            return {"status": "error",
                    "message": f"Ce n'est pas votre tour de jouer! C'est le tour de {self.players[self.currentTurn].playerName}."}

        # Full stack as raise amount
        raiseAmount = player.playerCurrency.getCurrency()
        result = self.raise_bet(playerIndex, raiseAmount)
        return result

    """""
    _______________________________________________________________________

    Methode: callAllIn
    _______________________________________________________________________

    Quand les joueurs call un all-in, le jeux va continuer jusqua au showdown
    pour montrer tous les cartes sur la tables.

    returns le dernier ronde.
    """""
    def callAllIn(self): # Action call All in, si il y a simpleemnt plus d'argent, il va matcher son All in
        result = None
        while self.round != 4:
            result = self.progressRound()
        return result

    """""
    _______________________________________________________________________

    Methode: resetBettingRound
    _______________________________________________________________________

    Utilser quand onchange les ronde, on reset le montant que les joueurs bet a 0.
    On prend player.currentRoundBet et le metre a 0.

    returns action
    """""
    def resetBettingRound(self): # Ici on reset le pot, bet des joueurs....
        self.currentBet = 0
        for player in self.players:
            player.currentRoundBet = 0

    """""
    _______________________________________________________________________

    Methode: bettingRoundComplete
    _______________________________________________________________________

    Pour allez au prochain ronde, il verfie que tous les joeuurs on fait leur actions

    returns Bool, true si tous les joeurs ont fite un action, else si doit attendre encore
    """""
    def bettingRoundComplete(self): # Determiner si tous le monde a joueur
        for player in self.players:
            if player.currentRoundBet != self.currentBet:
                return False
        return True

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Front-End
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    ***** Section *****
      
    Front-End

    Creer pour le front-end, Utiliser dans le fornt-end
    _______________________________________________________________________

    Methode: getStateForPlayer
    _______________________________________________________________________

    Utiliser pour le front end pour les cartes. Methode creer pour le formatage

    returns Nicely formated JSON Package pour front-end
    """""
    def cardToDict(self, card): # UI pour les cartes
        return {"value": card.value, "suit": card.suit, "img": card.img}
    
    """""
    _______________________________________________________________________

    Methode: getStateForPlayer
    _______________________________________________________________________

    Utiliser pour le front end pour le joueur. Montre qui a gagner durant le ronde.

    returns Nicley formated JSON Package pour front-end
    """""
    def getStateForPlayer(self, playerIndex): # Front-End pour les joueur
        player = self.players[playerIndex]
        opponent = self.players[0] if playerIndex == 1 else self.players[1]
        return {
            "round": self.round,
            "table": [self.cardToDict(card) for card in self.table.tableDeck],
            "your_cards": [self.cardToDict(card) for card in player.playerDeck],
            "handValue": player.playerDeckStatsData["HandValue"],
            "your_currency": player.playerCurrency.currency,
            "opponent_currency": opponent.playerCurrency.currency,
            "opponent_cards": ["🂠", "🂠"],
            "player_chance": self.estimateWinProbability(playerIndex),
            "pot": self.pot.getCurrency()
        }

    """""
    _______________________________________________________________________

    Methode: getFinalState
    _______________________________________________________________________

    Utiliser pour le front end au fin du ronde. Montre qui a gagner

    returns Nicley formated JSON Package pour front-end
    """""
    def getFinalState(self): # Front-End pour les joueurs au fin
        player1 = self.players[0]
        player2 = self.players[1]
        winnerData = self.checkWinner()
        return {
            "round": self.round,
            "table": [self.cardToDict(card) for card in self.table.tableDeck],
            "player1_cards": [self.cardToDict(card) for card in player1.playerDeck],
            "player2_cards": [self.cardToDict(card) for card in player2.playerDeck],
            "player1_handValue": player1.playerDeckStatsData["HandValue"],
            "player2_handValue": player2.playerDeckStatsData["HandValue"],
            "player1_currency": player1.playerCurrency.currency,
            "player2_currency": player2.playerCurrency.currency,
            "winner": winnerData['winner'],
            "reason": winnerData['reason'],
        }

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Ordinateur et Pourcentage
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    Methode: aiAction
    _______________________________________________________________________

    Determination de ce que l'ordinateur devrai faire

    returns action de l'ordinateur.
    """""
    def aiAction(self, playerIndex): # Determiner l'action de l'ordinateur
        player = self.players[playerIndex]

        # only pass revealed table cards for AI evaluation
        visible_table_cards = self.table.tableDeck[:self.round + 2]  # e.g., flop = 3 cards, turn = 4
        self.checkDeckValuesVisible(self.players[playerIndex], visible_table_cards)
        strength = self.players[playerIndex].playerDeckValue

        to_call = self.currentBet - player.currentRoundBet

        # Pretty good hand
        if strength <= 4:  # Full house or better
            if player.playerCurrency.getCurrency() > 0:
                return self.all_in(playerIndex)
            else:
                return self.call(playerIndex)

        # Decent hand
        elif strength <= 7:
            if to_call == 0:
                return self.bet(playerIndex, 10)
            else:
                return self.call(playerIndex)

        # Meh hand
        elif strength <= 9:
            if to_call == 0:
                return self.check(playerIndex)
            else:
                return self.call(playerIndex)

        # Trash hand
        else:
            if to_call == 0:
                return self.check(playerIndex)
            else:
                return self.call(playerIndex)
    
    """""
    _______________________________________________________________________

    Methode: estimateWinProbability
    _______________________________________________________________________

    - Methode Majeure
    On detemrine le probailite (0% - 100%) d'un main et retourne un reccomendation en utilise le stategie Monto Carlo

    1. En utilisant les cartes de notre joueurs:
        - Construit un main virtuel qui represent le joueur
        - Une autre main virtuel qui represent l'ordinateur.
        - Creer un table virtuel
        - Ajout des cartes au tab les mains jusaqua tous les cartes est representer comme au SHowdown
        - Utilise notre methode checkDeckValues pour evauluer les mains virtuels            
        - Repete ceci dependant de la variable simulations dans le parametre a defaut de 5000
        - Garde nombre fois que le joeuur gagne contre l'ordinateur

    2. Retrouve le pourcentage de montent de fois que les joueurs a gagner par diviser sur le montent de fois 
       le simulations a courru

    3.En utilisant le pourcenatge, on peut creer des recomendation de ce que le joeuur devrai faire prochaine

    returns pourcentage et reccomandation de ce que le joeuur devrait faire
    """""
    def estimateWinProbability(self, playerIndex, simulations=5000): # Pourcentage de gagner la ronde
        player = self.players[playerIndex]
        wins = 0

        # Known cards: player's hand + table
        known_cards = player.playerDeck + self.table.tableDeck
        known_set = {(c.value, c.suit) for c in known_cards}

        # Build remaining deck
        full_deck = [(v, s) for v in range(2, 15) for s in ["♢", "♡", "♠", "♣"]]
        remaining_deck = [c for c in full_deck if c not in known_set]

        for _ in range(simulations):
            random.shuffle(remaining_deck)

            # Deal random opponent hand (2 cards)
            opp_hand = [Card(*remaining_deck[0], ''), Card(*remaining_deck[1], '')]

            # Complete table if needed
            table_needed = 5 - len(self.table.tableDeck)
            table_cards = self.table.tableDeck.copy() + [Card(*remaining_deck[i + 2], '') for i in range(table_needed)]

            # Evaluate hands
            temp_player = player.playerDeck + table_cards
            temp_opponent = opp_hand + table_cards

            # Temporary stats containers
            temp_player_stats = Player("temp")
            temp_player_stats.playerDeck = temp_player
            temp_opponent_stats = Player("temp")
            temp_opponent_stats.playerDeck = temp_opponent

            # Evaluate hand values
            temp_game = Game([temp_player_stats, temp_opponent_stats])
            temp_game.table.tableDeck = []
            temp_game.checkDeckValues()

            if temp_player_stats.playerDeckValue < temp_opponent_stats.playerDeckValue:
                wins += 1

        probability = wins / simulations
        probability = max(probability, 0.05)
        probability = round(probability, 2)
        probabilityMessage = round(probability * 100)

        # Section de recomendation
        if probability >= 0.8:
            message = "Avec une probabilité de {}%, vous devriez miser ALL-IN. Ta main est vraiment bonne!".format(probabilityMessage)
        elif probability >= 0.4:
            message = "Avec une probabilité de {}%, vous pouvez miser un raise. Ta main est bonne!".format(probabilityMessage)
        elif probability >= 0.2:
            message = "Avec une probabilité de {}%, vous devriez checker! ".format(probabilityMessage)
        else:
            message = "Avec une probabilité de {}%, vous devriez checker ou coucher. Ne pas jouer avec confiance!".format(probabilityMessage)
        print(message)
        return {"win": probability, "Action": message}

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Gagnan
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    Methode: checkWinner
    _______________________________________________________________________

    Activer au fin de la ronde pour determiner le gagnant

    Il existe trois possibiite:
    Cas 1: Joueurs Gagne
    Cas 2: Ordinateur Gagne
    Cas 3: Egailite

    1. Compare le niveau de force des main de chaque joueurs (Pair vs Highcard) pour retouver vite le gaggant
    2. Au cas que le sjoueur on le me meme niveau de force (Pair vs Pair), on doit comparer les statistique specfique
       comme marquer dansles regles specfique:

       1- RoyalFlush : Egaliter
       2- StraightFlush: Qui a un straight plus haut de la meme type
       3- Quads: Comapre qui a le Quad plus haute, else durant l'evaluationon prend note des 5 plus grand carte, donc on doit comparer les cartes qui reste apres le Quads si
       4- FullHouse: Qui a un Triple plus haut, si non qui a le pair est plus Haute
       5- Flush: En ordres des 5 carte du meme type, qui a le main de flush plus haute
       6- Straight: Qui a un straight plus haut
       7- Brelan :  Comapre qui a le Quad plus haute, durant l'evaluation prend note des 5 plus grand carte, donc on doit comparer les cartes qui reste apres le Brelan
       8- Deux Pair:  Comkpare le Pair plus haut, puis compare le pair plus bas, else durant l'evaluation prend note des 5 plus grand carte, donc on doit comparer les cartes qui reste apres les deux paires
       9- Pair: Comaprer les pairs, else durant l'evaluation prend note des 5 plus grand carte, donc on doit comparer les cartes qui reste apres les deux paires
       10- HighCard: else durant l'evaluation prend note des 5 plus grand carte, donc on doit comparer les cartes qui reste apres highcard

    returns dictionnaire, utiliser dans Final Game State pour montrer le gagant au joueurs eyt aussi reason pour expliquer pouruqoi

    """""
    def checkWinner(self): # Comparerles mains des joueurs pour determiner qui a gagner 
        self.checkDeckValues()  # Check Decks
        player1 = self.players[0]
        player2 = self.players[1]

        result = {"winner": "?", "reason": "Erreur: Les cartes des joueurs n'ont pas pu être vérifiées"}

        hand_names = {
            1: "Quinte Flush Royal",
            2: "Quinte Flush",
            3: "Carré",
            4: "Full House",
            5: "Flush",
            6: "Quinte",
            7: "Brelan",
            8: "Deux Paires",
            9: "Une Paire",
            10: "Carte Haute"
        }

        # Player 1 Wins
        if player1.playerDeckValue < player2.playerDeckValue:
            result = {"winner": player1.playerName, "reason": f"La combinaison : {hand_names[player1.playerDeckValue]} bat la combinaison : {hand_names[player2.playerDeckValue]}"}
            pass

        # Player 2 Wins
        elif player1.playerDeckValue > player2.playerDeckValue:
            result = {"winner": player2.playerName, "reason": f"La combinaison : {hand_names[player2.playerDeckValue]} bat la combinaison : {hand_names[player1.playerDeckValue]}"}

            pass

        # IF hand is the same
        else:
            # 1. Straight Flush or Straight
            if player1.playerDeckValue == 2 or player1.playerDeckValue == 6:
                if player1.playerDeckStatsData['HighestCardInStraight'] > player2.playerDeckStatsData['HighestCardInStraight']:
                    result = {"winner": player1.playerName,
                              "reason": f"Meilleur Quinte! Carte forte de la quinte : {player1.playerDeckStatsData['HighestCardInStraight']}"}
                    pass
                elif player1.playerDeckStatsData['HighestCardInStraight'] < player2.playerDeckStatsData[
                    'HighestCardInStraight']:
                    result = {"winner": player2.playerName,
                              "reason": f"Meilleure Quinte! Carte forte de la quinte : {player2.playerDeckStatsData['HighestCardInStraight']}"}
                    pass

            # 2. Four of a kind
            elif player1.playerDeckValue == 3:
                if player1.playerDeckStatsData['HighFour'] > player2.playerDeckStatsData['HighFour']:
                    result = {"winner": player1.playerName,
                              "reason": f"Carré de {player1.playerDeckStatsData['HighFour']}s bat le carré de {player2.playerDeckStatsData['HighFour']}s"}
                    pass
                elif player1.playerDeckStatsData['HighFour'] < player2.playerDeckStatsData['HighFour']:
                    result = {"winner": player2.playerName,
                              "reason": f"Carré de {player2.playerDeckStatsData['HighFour']}s bat le carré de {player1.playerDeckStatsData['HighFour']}s"}
                    pass
                else:
                    kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighFour']] * 4)
                    if kicker_winner == "Tie":
                        result = {"winner": "Égalité!", "reason": "Carré pareil, cinquième carte de puissance identique"}
                    else:
                        result = {"winner": kicker_winner, "reason": "Carré pareil, cinquième carte plus forte"}

            # 3. Full House
            elif player1.playerDeckValue == 4:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player1.playerName,
                              "reason": f"Full House : Brelan de {player1.playerDeckStatsData['HighThree']}s bat Full House: Brelan de {player2.playerDeckStatsData['HighThree']}"}
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player2.playerName,
                              "reason": f"Full House : Brelan de {player2.playerDeckStatsData['HighThree']}s bat Full House : Brelan de {player1.playerDeckStatsData['HighThree']}"}
                    pass
                else:
                    if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                        result = {"winner": player1.playerName,
                                  "reason": f"Full House : Paire de {player1.playerDeckStatsData['HighPair']}s bat Full House : Paire de {player2.playerDeckStatsData['HighPair']}"}
                        pass
                    elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                        result = {"winner": player2.playerName,
                                  "reason": f"Full House : Paire de {player2.playerDeckStatsData['HighPair']}s bat Full House : Paire de {player1.playerDeckStatsData['HighPair']}"}
                        pass

            # 4. Flush
            elif player1.playerDeckValue == 5:
                if player1.playerDeckStatsData['FlushValues'] > player2.playerDeckStatsData['FlushValues']:
                    result = {"winner": player1.playerName,
                              "reason": f"Flush : Carte la plus forte : {player1.playerDeckStatsData['FlushValues'][0]}"}
                    pass
                elif player1.playerDeckStatsData['FlushValues'] < player2.playerDeckStatsData['FlushValues']:
                    result = {"winner": player2.playerName,
                              "reason": f"Flush : Carte la plus forte : {player2.playerDeckStatsData['FlushValues'][0]}"}
                    pass

            # 5. Three of a kind
            elif player1.playerDeckValue == 7:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player1.playerName,
                              "reason": f"Brelan de {player1.playerDeckStatsData['HighThree']}s bat {player2.playerDeckStatsData['HighThree']}"}
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player2.playerName,
                              "reason": f"Brelan de {player2.playerDeckStatsData['HighThree']}s bat {player1.playerDeckStatsData['HighThree']}"}
                    pass
                else:
                    kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighThree']] * 3)
                    if kicker_winner == "Tie":
                        result = {"winner": "Égalité!", "reason": "Brelan pareil, 5 cartes les plus fortes identiques"}
                    else:
                        result = {"winner": kicker_winner, "reason": f"Brelan pareil, deux prochaines cartes les plus fortes décident du gagnant: {kicker_winner}"}

            # 6. Two Pair
            elif player1.playerDeckValue == 8:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player1.playerName, "reason": f"Paire de {player1.playerDeckStatsData['HighPair']}s bat la paire plus faible : Paire de {player2.playerDeckStatsData['HighPair']}s"}
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player2.playerName, "reason": f"Paire de {player2.playerDeckStatsData['HighPair']}s bat la paire plus faible : Paire de {player1.playerDeckStatsData['HighPair']}s"}
                    pass
                else:
                    if player1.playerDeckStatsData['LowPair'] > player2.playerDeckStatsData['LowPair']:
                        result = {"winner": player1.playerName, "reason": f"Paire forte identique, deuxième paire : Paire de {player1.playerDeckStatsData['HighPair']}s bat la paire plus faible : Paire de {player2.playerDeckStatsData['HighPair']}s"}
                        pass
                    elif player1.playerDeckStatsData['LowPair'] < player2.playerDeckStatsData['LowPair']:
                        result = {"winner": player2.playerName, "reason": f"Paire forte identique, deuxième paire : Paire de {player2.playerDeckStatsData['HighPair']}s bat la paire plus faible : Paire de {player1.playerDeckStatsData['HighPair']}s"}
                        pass
                    else:
                        kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighPair']] * 2 + [player1.playerDeckStatsData['LowPair']] * 2)
                        if kicker_winner == "Tie":
                            result = {"winner": "Égalité!", "reason": "Deux paires identiques, cinquième carte pareillement identique"}
                        else:
                            result = {"winner": kicker_winner, "reason": f"Deux paires identiques, cinquième carte hors combinaison à souligné le gagnant"}

            # 7. Pair
            elif player1.playerDeckValue == 9:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player1.playerName,
                              "reason": f"Paire de {player1.playerDeckStatsData['HighPair']}s bat Paire de {player2.playerDeckStatsData['HighPair']}s"}
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player2.playerName,
                              "reason": f"Paire de {player2.playerDeckStatsData['HighPair']}s bat Paire de {player1.playerDeckStatsData['HighPair']}s"}
                    pass
                else:
                    kicker_winner = self.compareKickers( player1,player2,[player1.playerDeckStatsData['HighPair']] * 2)
                    if kicker_winner == "Tie":
                        result = {"winner": "Égalité!", "reason": "Paire identique, trois meilleures cartes de valeur identique"}
                    else:
                        result = {"winner": kicker_winner, "reason": f"Paire identique, {kicker_winner} avait les trois meilleures cartes hors combinaison"}

            # 8. HighCard
            else:

                kicker_winner = self.compareKickers(player1, player2, [])
                if kicker_winner == "Tie":
                    result = {"winner": "Égalité!",
                              "reason": f"Carte Haute identique! Cinq cartes fortes hors combinaison identiques : {player1.playerDeckStatsData['FiveHighestCards']}"}
                else:
                    result = {"winner": kicker_winner, "reason": f" {kicker_winner} avait les cinq meilleures cartes hors combinaison"}

        return result

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Evaulateur
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    ***** Section *****
      
    Evaluation du mains

    Determination du force du main
    
    _______________________________________________________________________

    Methode: checkDeckValues
    _______________________________________________________________________

    - Methode Majeure
    - On detemrine le force d'un main 

    1. Sort notre mains apr valeur Descendant
    2. Notez la valeur plus haut (HighCard), le valeur qui suivre au bas du HighCard (LowCard)
    3. Verifier Chaque Mains possible d eplus gros au patit pour detemriner sa force (1 = Plus Grand, 10, Plus faible)

    returns Rien, tous sera notez dans le profil du joueur directement

    """""
    def checkDeckValues(self):  # Checks Values of Deck of players (Scores from 1-10) 1 = Highest 10 = Lowest
        

        for player in self.players:

            deck = player.playerDeck + self.table.tableDeck
            deck.sort(key=lambda card: card.value)  # We sort the new Card

            # Grab five highest cards
            player.grabFiveHighestCards(deck)

            # High Card and LowCard
            sorted_values = sorted([card.value for card in deck])
            player.playerDeckStatsData["LowCard"] = sorted_values[0]
            player.playerDeckStatsData["HighCard"] = sorted_values[-1]

            if self.royalFlushCheck(deck, player):  # 1 Royal Flush - WORKS
                player.playerDeckValue = 1
                player.playerDeckStatsData["HandValue"] = 1
                pass

            elif self.straightFlushCheck(deck, player):  # 2 Straight Flush - WORKS
                player.playerDeckValue = 2
                player.playerDeckStatsData["HandValue"] = 2

                pass

            elif self.countCards(deck, player, 4):  # 3 Four of a kind - WORKS
                player.playerDeckValue = 3
                player.playerDeckStatsData["HandValue"] = 3
                pass

            elif self.fullHouse(deck, player):  # 4 Full House - WORKS
                player.playerDeckValue = 4
                player.playerDeckStatsData["HandValue"] = 4
                pass

            elif self.flushCheck(deck, player):  # 5 Flush - WORKS
                player.playerDeckValue = 5
                player.playerDeckStatsData["HandValue"] = 5
                pass

            elif self.staightCheck(deck, player):  # 6 Straight - WORKS
                player.playerDeckValue = 6
                player.playerDeckStatsData["HandValue"] = 6
                pass

            elif self.countCards(deck, player, 3):  # 7 Three of a kind - WORKS
                player.playerDeckValue = 7
                player.playerDeckStatsData["HandValue"] = 7

                pass

            elif self.countDoublePair(deck, player):  # 8 Two Pairs - WORKS
                player.playerDeckValue = 8
                player.playerDeckStatsData["HandValue"] = 8

                pass

            elif self.countCards(deck, player, 2):  # 9 One Pair - WORKS
                player.playerDeckValue = 9
                player.playerDeckStatsData["HandValue"] = 9

                pass

            else:  # 10 High-card
                player.playerDeckValue = 10
                player.playerDeckStatsData["HandValue"] = 10
    
    """""
    _______________________________________________________________________

    Methode: checkDeckValuesVisible
    _______________________________________________________________________

    - Methode Majeure
    - On detemrine le force d'un main, difference est ceci est utilsier pour le Site 

    1. Sort notre mains apr valeur Descendant
    2. Notez la valeur plus haut (HighCard), le valeur qui suivre au bas du HighCard (LowCard)
    3. Verifier Chaque Mains possible d eplus gros au patit pour detemriner sa force (1 = Plus Grand, 10, Plus faible)

    returns Rien, tous sera notez dans le profil du joueur directement
    """""
    def checkDeckValuesVisible(self, player, visibleTableCards): # Check the deck values but of front-end visual
        """
        Evaluate a player's hand strength using only currently revealed table cards.
        :param player: Player object
        :param visibleTableCards: list of Card objects currently revealed on table
        """
        # Combine player's own cards with visible table cards
        deck = player.playerDeck + visibleTableCards
        deck.sort(key=lambda card: card.value)

        # Grab five highest cards (even if fewer than 5 revealed, pick what we have)
        player.grabFiveHighestCards(deck)

        # High Card and Low Card
        sorted_values = sorted([card.value for card in deck])
        player.playerDeckStatsData["LowCard"] = sorted_values[0]
        player.playerDeckStatsData["HighCard"] = sorted_values[-1]

        # Reset stats for this visible evaluation
        player.playerDeckStatsData["FlushValues"] = []
        player.playerDeckStatsData["FlushType"] = "N/A"
        player.playerDeckStatsData["HighestCardInStraight"] = 0
        player.playerDeckStatsData["HandValue"] = 10  # default = High Card
        player.playerDeckValue = 10

        # Evaluate hand rankings in order (same as original checkDeckValues)
        if self.royalFlushCheck(deck, player):
            player.playerDeckValue = 1
            player.playerDeckStatsData["HandValue"] = 1
        elif self.straightFlushCheck(deck, player):
            player.playerDeckValue = 2
            player.playerDeckStatsData["HandValue"] = 2
        elif self.countCards(deck, player, 4):
            player.playerDeckValue = 3
            player.playerDeckStatsData["HandValue"] = 3
        elif self.fullHouse(deck, player):
            player.playerDeckValue = 4
            player.playerDeckStatsData["HandValue"] = 4
        elif self.flushCheck(deck, player):
            player.playerDeckValue = 5
            player.playerDeckStatsData["HandValue"] = 5
        elif self.staightCheck(deck, player):
            player.playerDeckValue = 6
            player.playerDeckStatsData["HandValue"] = 6
        elif self.countCards(deck, player, 3):
            player.playerDeckValue = 7
            player.playerDeckStatsData["HandValue"] = 7
        elif self.countDoublePair(deck, player):
            player.playerDeckValue = 8
            player.playerDeckStatsData["HandValue"] = 8
        elif self.countCards(deck, player, 2):
            player.playerDeckValue = 9
            player.playerDeckStatsData["HandValue"] = 9
        else:
            player.playerDeckValue = 10
            player.playerDeckStatsData["HandValue"] = 10

    # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# ------------------------------------------------------------- Details du deck
    # -------------------------------------------------------------# -------------------------------------------------------------

    """""
    _______________________________________________________________________

    ***** Section *****
    
    Details du deck

    Ici est le section qui determine le niveau de force d'un mains.
    Les evaluateur utilise ces methodes pour determiner le force d'un mains

    - Cherche les details specfique de chauqe mains en cas d'un Tie
    _______________________________________________________________________

    Methode: countCards
    _______________________________________________________________________

    Verifie le deck pour si un Pair/Brelan/Quad est present dans le mains! Tu dois specifer dans les parametres ce que tu recherche!

    1. Parcous le liste par chaque valeur
    2. Verfiier le montant de fois un valeur ce retrouve dans un liste
    3. Cas 1 : Pair, On note le valeur pour l'evaluation plus tard
    4. Cas 2:  Brelan,  On note le carte pour l'evaluation plus tard
    5. Cas 3:  Quad,  On note le carte pour l'evaluation plus tard

    returns Bool, True si valeur specifier retrouver, else non

    """""
    def countCards(self, deck, player, number):  # pairs, Three, four
        values = [card.value for card in deck]
        cardChecked = False

        count = Counter(values)

        #Comptez nombre de du valuer dans le mains
        for value in values:
            if count[value] == number:

                # Cas 1: Pair
                if number == 2:
                    player.playerDeckStatsData["HighPair"] = value
                    cardChecked = True
                # Cas 2: Brelan
                elif number == 3:
                    player.playerDeckStatsData["HighThree"] = value
                    cardChecked = True
                #Cas 3: Quad
                elif number == 4:
                    player.playerDeckStatsData["HighFour"] = value
                    cardChecked = True

        return cardChecked
    
    """""
    _______________________________________________________________________

    Methode: countDoublePair
    _______________________________________________________________________

    Verifie le deck pour le nombre de Double Pair present!

    1. Parcous le liste par chaque valeur, incremnt un counter
    2. Verfiier qu'ont compte pas le meme valeur plusieur fois
    3. Verifer longeur de notre lists de pair
    4. Cas 1: 2 Pairs, notez pair bas et pair haut index 0 et 1
    5. Cas 2: 3 Pairs, notez pair bas et pair haut index 1 et 2

    returns Bool, True si Deux ou pluspair present, else non

    """""
    def countDoublePair(self, deck, player):  # Double Pair
        countOfPairs = 0
        values = [card.value for card in deck]
        cardsChecked = []

        pairList = []

        # Regarde chaque carte pour retrouver le nombre de pair present
        for value in values:
            count = values.count(value)

            if value not in cardsChecked:  # Check if card already in deck
                if count == 2:
                    pairList.append(value)
                    countOfPairs += 1
                cardsChecked.append(value)  # Add to list to get marked that we checked

        # Section to grab deck details
        pairListSize = len(pairList)

        # Cas 1: 2 Pairs
        if pairListSize == 2:  
            player.playerDeckStatsData["LowPair"] = pairList[0]
            player.playerDeckStatsData["HighPair"] = pairList[1]

        # Cas 1: 3 Pairs
        elif pairListSize == 3:  # Contains 3 pairs
            player.playerDeckStatsData["LowPair"] = pairList[1]
            player.playerDeckStatsData["HighPair"] = pairList[2]

        return countOfPairs >= 2
    
    """""
    _______________________________________________________________________

    Methode: flushCheck
    _______________________________________________________________________

    Verifie le deck si il contient un 5 cartes du meme type!

    1. On cherche tous les cartes et ajoute leur type dans un list
    2. On utilise Len pour ocmpter le type de cartes present
    3. Si oui, on sort et cherche le valeur du meme type qui est le plus haut!

    returns Bool, True si il existe un Full House, else Non

    """""
    def flushCheck(self, deck, player):  # Check Flushes
        suits = {}

        # Group cards by suit
        for card in deck:
            suits.setdefault(card.suit, []).append(card.value)

        for suit, values in suits.items():
            if len(values) >= 5:  # We only look for the suit that has 5 or more items in them
                values.sort(reverse=True)  # Highest to lowest now
                player.playerDeckStatsData["FlushValues"] = values[:5]  # We put the 5 highest values in the list
                player.playerDeckStatsData["FlushType"] = suit  # We mark the suit npw
                return True

        return False
    
    """""
    _______________________________________________________________________

    Methode: staightCheck
    _______________________________________________________________________

    Verfie le deck si il contient un combinaison de un pair et un brelan ou deux brelean!

    1. Chercher unqiuement les valeurs des cartes de notres mains
    2. Creer unliste pour guarder compte des 5 valeurs
    3. On assure que A compte comme valeur 1 et 14 comme dans le sregles
    4. Regarde dan snotre lists pour 5 valeur consecutif de + 1
    5. Prend en compte le carte plus haute dna sle straight

    returns Bool, True si il existe un Straight, else Non

    """""
    def staightCheck(self, deck, player):  # Check si un deck contains un straight
        values = [card.value for card in deck]
        values = sorted(set(values))

        straightCount = 1
        previousValue = 0

        straightList = []

        # Le carte A compte comme le 1 et 14 dans un straight
        countAces = values.count(14)
        if countAces >= 1:
            values.append(1)
            values.sort()  # We sort the new Card

        # Voir si 5 cartes a un value plus grand de 1, si non resetnotre counter
        for value in values:
            if previousValue == 0:
                previousValue = value
            else:
                if previousValue + 1 == value:
                    straightCount += 1
                    straightList.append(value)
                else:
                    straightCount = 1
                    straightList.clear()

                straightList.append(value)
                previousValue = value

                if straightCount == 5:
                    player.playerDeckStatsData["HighestCardInStraight"] = value

                    return True

        return False

    """""
    _______________________________________________________________________

    Methode: fullHouse
    _______________________________________________________________________

    Verifie le deck si il contient un combinaison de un pair et un brelan ou deux brelean!

    1. Chercher unqiuement les valeurs des cartes de notres mains
    2. Creer deux listes et fait un rehereche pour retrouver le nombre de pairs et de brelan present
    3. Cas 1: Triple + Pair, Chercher le pair le plus grand et notez pour compairson plus tard
    4. Cas 2: Deux Triples, Chercher le triple le plus grand et notez pour compairson plus tard

    returns Bool, True si il existe un Full House, else Non

    """""
    def fullHouse(self, deck, player): # Check si un full house est present

        # Chercher les valeur de chaque carte,
        values = [card.value for card in deck]
        uniqueValues = set(values)

        triples = []
        pairs = []

        # Trouver tous les pairs et triples dans le main du joueur
        for value in uniqueValues:
            count = values.count(value)

            if count >= 3:
                triples.append(value)
            elif count == 2:
                pairs.append(value)

        # Case 1: 1 triple + 1 pair
        if len(triples) == 1 and len(pairs) >= 1:
            player.playerDeckStatsData["HighThree"] = triples[0]
            player.playerDeckStatsData["HighPair"] = max(pairs)
            return True

        # Case 2: 2 triples
        elif len(triples) == 2:
            triples.sort()
            player.playerDeckStatsData["HighThree"] = triples[1]
            player.playerDeckStatsData["HighPair"] = triples[0]
            return True

        return False

    """""
    _______________________________________________________________________

    Methode: straightFlushCheck
    _______________________________________________________________________

    Checks the deck to see if the cards arein the right order to be an Straight Flush

    1. Check if there is an flush 
    2. Define the values needed and create local lists
    3. Sort each card in their own lists by type (Hearts, Spades....)
    4. On sort nos lists et regarde si il y a 5 cartes consecutifs de +1

    returns Bool, True si il existe un Straight FLush, else Non

    """""
    def straightFlushCheck(self, deck, player): # Check si un straight flush est present 

        if self.flushCheck(deck, player) is not True:  # Check if there is a flush
            return False

        hearts = []
        diamonds = []
        spades = []
        clubs = []

        # Sort nos cartes par type ( Coeurs, Spades...)
        for card in deck:
            if card.suit == "H":
                hearts.append(card.value)
            elif card.suit == "D":
                diamonds.append(card.value)
            elif card.suit == "S":
                spades.append(card.value)
            else:
                clubs.append(card.value)

        # List organiser
        listOfSuits = [hearts, diamonds, spades, clubs]

        # On regarde si il contient un staright dans nos lists
        for suits in listOfSuits:
            # Chercher les valeur unique
            values = suits
            values = sorted(set(values))

            straightCount = 1
            previousValue = 0

            # Le carte A compte comme le 1 et 14 dans un straight
            countAces = values.count(14)
            if countAces >= 1:
                values.append(1)
                values.sort()  

            # Voir si 5 cartes a un value plus grand de 1, si non resetnotre counter
            for value in values:
                if previousValue == 0:
                    previousValue = value
                else:
                    if previousValue + 1 == value:
                        straightCount += 1
                    else:
                        straightCount = 1
                    previousValue = value

                    # Straight retrouver!
                    if straightCount == 5:
                        player.playerDeckStatsData["HighestCardInStraight"] = value
                        return True
        return False

    """""
    _______________________________________________________________________

    Methode: royalFlushCheck
    _______________________________________________________________________

    Checks the deck to see if the cards arein the right order to be an Royal FLush

    1. Check si il ia un flush present 
    2. Define the values needed and create lcoal lists
    3. Sort each card in their own lists by type (Hearts, Spades....)
    4. On sort nos lists et regarde si il contient les valeur specifier

    Returns Bool, True si il existe un Royale FLush, else Non

    """""
    def royalFlushCheck(self, deck, player): # Check si un Royale Flush est present

        if self.flushCheck(deck, player) is not True:  # Check if there is a flush
            return False

        if self.staightCheck(deck, player) is not True:  # Check if there is a straight
            return False

        # Make Local List
        hearts = []
        diamonds = []
        spades = []
        clubs = []

        # Nos Valeur que nous recherchons
        neededValues = {10, 11, 12, 13, 14}

        # Sort les cartes dans leur propres list
        for card in deck:
            if card.suit == "H":
                hearts.append(card.value)
            elif card.suit == "D":
                diamonds.append(card.value)
            elif card.suit == "S":
                spades.append(card.value)
            else:
                clubs.append(card.value)
        listOfSuits = [hearts, diamonds, spades, clubs]

        # Compare chaque list pour voir si il contient notre valeur que nous avons specifier
        for suits in listOfSuits:
            values = suits
            values = sorted(set(values))

            if neededValues.issubset(values):  # If royal flush is same as our hand
                return True

        return False

    """""
    _______________________________________________________________________

    Methode: compareKickers
    _______________________________________________________________________
     
    Allows us to compare the remaining cards in a deck if both players end up having an equal hand. Essentially our tie-braker.
    1. Check si il ia un flush present ou straight, royale flush is a combination of both
    2. Cherche nos 5 carte d evaleur plus haute
    3. On sorte nos cartes par valeur
    4. On compare nos cartes en facon descendant
    5. If all cards are the same, its an Tie

    Returns String, Nom du Joueur or Tie!

    """""
    def compareKickers(self, player1, player2, mainCards): # Comparer les reste des carte sen cas d'egalite

        # mainCards = list of values forming the main hand (e.g., [9,9,9,9])
        p1_Deck = [v for v in player1.playerDeckStatsData['FiveHighestCards'] if v not in mainCards]
        p2_Deck = [v for v in player2.playerDeckStatsData['FiveHighestCards'] if v not in mainCards]

        # Sort remaining cards descending
        p1_Deck.sort(reverse=True)
        p2_Deck.sort(reverse=True)

        # Compare our Cards
        for player1Card, player2Card in zip(p1_Deck, p2_Deck):
            if player1Card > player2Card:
                return player1.playerName
            elif player1Card < player2Card:
                return player2.playerName
        return "Tie" 

"""""
_______________________________________________________________________

MAIN
_______________________________________________________________________
"""""
Computer = Player("Computer")
Human = Player("David")
PlayerList = [Computer, Human]

Poker = Game(PlayerList)

Poker.startGameSession()  # Deal pre-flop and give 100 chips each

human = 1
computer = 0



