# Imports
import random


# -------------------------------------------------------------# -------------------------------------------------------------
# Card Class
class Card:
    def __init__(self, value, suit, img):  # Initialization (What does a card holds)
        self.value = value
        self.suit = suit
        self.img = img

    def __str__(self):  # To print the object when called ----> print(Card)
        return f"{self.value}{self.suit}{self.img}"  # To Show the card


# -------------------------------------------------------------# -------------------------------------------------------------
# Deck Class
class Deck:
    def __init__(self):  # A Deck holds Cards
        self.cardDeck = []
        self.createDeck()  # Call function when initialized

    def createDeck(self):  # Creating the Main Deck
        cardValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # There are 14 Values
        cardSuit = ["♢", "♡", "♠", "♣"]  # There Are Four Suits
        cardImage = ["🃂", "🃃", "🃄", "🃅", "🂦", '🂧', "🂨", '🂩', "🂪", "🂫", "🂬", "🂮", "🂾"]  # There are 14 Images

        for suit in cardSuit:
            for value in cardValues:
                self.cardDeck.append(Card(value, suit, cardImage[value - 2]))

        self.shuffle()  # Shuffle the deck

    def shuffle(self):  # Shuffles the Deck for us (Randomizes it)
        random.shuffle(self.cardDeck)


# -------------------------------------------------------------# -------------------------------------------------------------
# Player Class
class Player:
    def __init__(self, name):  # A player holds a deck
        self.playerDeck = []
        self.playerName = name

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to PLAYER deck
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)


# -------------------------------------------------------------# -------------------------------------------------------------
# Table Class
class Table:
    def __init__(self):
        self.tableDeck = []

    def setupTable(self, MainDeck):

        try:
            while len(self.tableDeck) < 3:  # Create the 3 Starting Cards
                self.receiveCard(MainDeck)
        except:
            print("Tabel Setup has encountered an issue")

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to Table deck
        newCard = MainDeck.cardDeck.pop()
        self.tableDeck.append(newCard)


# -------------------------------------------------------------# -------------------------------------------------------------
class Game:  # The actual Game and Rounds
    def __init__(self, playerNames):
        self.deck = Deck()
        self.table = Table()
        self.players = []
        self.round = 0

        for name in playerNames:
            self.players.append(name)

    def startGame(self):
        for player in self.players:  # Players Get their 2 intial Cards
            player.receiveCard(self.deck)
            player.receiveCard(self.deck)

        self.table.setupTable(self.deck)  # Table gets their Cards
        self.currentState()

        self.roundCounter()  # Round UI ----- Round 1
        self.table.receiveCard(self.deck)
        self.currentState()

        self.roundCounter()  # Round UI ----- Round 2
        self.table.receiveCard(self.deck)
        self.currentState()

        self.roundCounter()  # Round UI ----- Round 3
        self.table.receiveCard(self.deck)
        self.currentState()


    def currentState(self):  # We Show The Cards
        print("--------Table------")  # Table UI
        for card in self.table.tableDeck:
            print(card)

        print("------Players------")  # Players UI
        for player in self.players:
            print(player.playerName)

            for card in player.playerDeck:
                print(card)

    def roundCounter(self): # Round Console UI
        self.round += 1
        print("**************")
        print(f"Round : {self.round}")
        print("**************")


# -------------------------------------------------------------# -------------------------------------------------------------
# MAIN

computer = Player("Computer")
Human = Player("David")

PlayerList = [computer, Human]
Poker = Game(PlayerList)

Poker.startGame()
