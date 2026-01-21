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
class Player:
    def __init__(self):  # A player holds a deck
        self.playerDeck = []

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to PLAYER deck
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)


# -------------------------------------------------------------# -------------------------------------------------------------
# Create the deck
deck = Deck()

# Print all cards
# for card in deck.cardDeck:
# print(card)  # Uses the __str__ we defined in Card

computer = Player()
computer.receiveCard(deck)
computer.receiveCard(deck)

for card in computer.playerDeck:
    print(card)
