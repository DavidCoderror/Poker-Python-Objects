# Imports
import random


# -------------------------------------------------------------
# Card Class
class Card:
    # Initialization (What does a card hold)
    def __init__(self, value, suit, img):
        self.value = value
        self.suit = suit
        self.img = img

    def __str__(self):
        return f"{self.value}{self.suit}" # To Show the card


# -------------------------------------------------------------
# Deck Class
class Deck:
    def __init__(self):
        self.cardDeck = []
        self.createDeck()

    def createDeck(self):
        cardValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # There are 14 Values
        cardSuit = ["♢", "♡", "♠", "♣"]  # There Are Four Suits
        cardImage = ["🃂", "🃃", "🃄", "🃅", "🂦", '🂧', "🂨", '🂩', "🂪", "🂫", "🂬", "🂮", "🂾"]  # There are 14 Images

        for suit in cardSuit:
            for value in cardValues:
                self.cardDeck.append(Card(value, suit, cardImage[value - 2]))


    def shuffle(self):  # Shuffles the deck for us
        random.shuffle(self.cardDeck)


# ------------------------------------------------------------- Test
# Create the deck
deck = Deck()

# Print all cards
for card in deck.cardDeck:
    print(card)  # uses the __str__ we defined in Card
