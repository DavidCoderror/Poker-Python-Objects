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

    def sortDeck(self):
        self.cardDeck.sort(self)


# -------------------------------------------------------------# -------------------------------------------------------------
# Player Class
class Player:
    def __init__(self, name):  # A player holds a deck
        self.playerDeck = []
        self.playerName = name

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to PLAYER deck
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)  # We get a new card
        self.playerDeck.sort(key=lambda card: card.value)  # We sort the new Card


# -------------------------------------------------------------# -------------------------------------------------------------
# Table Class
class Table:
    def __init__(self):
        self.tableDeck = []

    def setupTable(self, MainDeck):  # Create 3 cards in deck

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
        self.fold = False

        for name in playerNames:
            self.players.append(name)

    def startGame(self):
        for player in self.players:  # Players Get their 2 initial Cards
            player.receiveCard(self.deck)
            player.receiveCard(self.deck)

        self.table.setupTable(self.deck)  # Table gets their Cards
        self.currentState()

        startPlayerResponse = self.askPlayerToContinue()

        if startPlayerResponse == 2:
            print("Folded!!")
            pass
        else:
            # -------------------------------------------------------------------- Start of Actual Game
            while self.round < 3 and self.fold is not True:  # Round System
                self.roundCounter()  # Round UI ----- Round 1
                self.table.receiveCard(self.deck)
                self.currentState()
                playerResponse = self.askPlayerToContinue()

                if playerResponse == 1:
                    pass
                elif playerResponse == 2:
                    print("Folded!!")
                    break
            # -------------------------------------------------------------------- End of Actual Game

    def currentState(self):  # We Show The Cards
        print("--------Table------")  # Table UI
        for card in self.table.tableDeck:
            print(card)

        print("------Players------")  # Players UI
        for player in self.players:
            print(player.playerName)

            for card in player.playerDeck:
                print(card)

    def roundCounter(self):  # Round Console UI
        self.round += 1
        print("**************")
        print(f"Round : {self.round}")
        print("**************")

    def winner(self):  # Determines who won
        for player in self.players:
            deck = player.playerDeck

            # 1 Royal Flush
            # if (True):
            # royalFlushCheck(deck)

            # 2 Straight Flush
            # elif (True):
            # straightFlushCheck(deck)

            # 3 Four of a kind
            # elif (True):
            # self.countCards(deck,4)

            # 4 Full House
            # elif (True):
            # self.countCards(deck,2) and self.countCards(deck,3)

            # 5 Flush
            # elif (True):
            # flushCheck(deck)

            # 6 Straight
            # elif (True):
            # self.staightCheck(deck)

            # 7 Three of a kind
            # elif (True):
            # self.countCards(deck,3)

            # 8 Two Pairs
            # elif (True):
            # self.countDoublePair(deck)

            # 9 One Pair
            # if (True) :
            # self.countCards(deck,2)

            # 10 Highcard
            # else:
            # pass

    def askPlayerToContinue(self):
        acceptableAnswer = True
        while acceptableAnswer:
            answer = int(input("Do you want to Continue (1) or Fold(2)? : "))

            if answer == 1:
                return 1
            elif answer == 2:
                return 2
            else:
                acceptableAnswer = False

    def putTableAndPlayerCardsTogheter(self):
        for player in self.players:
            for tableCard in self.table.tableDeck:
                player.playerDeck.append(tableCard)  # Gets the table Cards added
                player.playerDeck.sort(key=lambda card: card.value)  # We sort the new Card

    # -------------------------------------------------------------------- Deck Check!
    def countCards(self, deck, number):  # pairs,Three, four
        for card in deck:
            countOfCard = deck.count(card.value)

            if countOfCard == number:
                return True

    def countDoublePair(self, deck):  # Double Pair
        countOfPairs = 0
        cardsChecked = []

        for card in deck:
            if cardsChecked.count(card.value) == 0:  # To make we don't count twice the same card
                countOfCard = deck.count(card.value)  # Check count of card and store it in var

                if countOfCard == 2:  # Check amount
                    countOfPairs += 1  # Add to the counter

            cardsChecked.append(card.value)  # Add the card to the list that we already checked

        if countOfPairs == 2:
            return True

    def flushCheck(self, deck):  # Check Flushes
        for card in deck:
            countOfCard = deck.count(card.suit)

            if countOfCard == 5:
                return True

    def staightCheck(self, deck):  # Check if deck contains straight
        count = 1
        previousCardValue = 0
        for card in deck:
            if previousCardValue == 0:  # Move past from  first card
                previousCardValue = card.value
            else:
                if card.value == previousCardValue:  # if card is same value
                    pass

                elif card.value == previousCardValue + 1:  # if card is one higher than next
                    count += 1
                    previousCardValue = card.value
                    if count == 5:  # If there are 5 cards in a row higher than 1
                        return True

                else:  # if not higher than 1, reset count variable
                    count = 1
                    previousCardValue = card.value

    def straightFlushCheck(self, deck):  # Check if deck contains straight which is also a flush
        count = 1
        previousCardValue = 0
        previousCardValueSuit = 0

        for card in deck:
            if previousCardValue == 0:  # Move past from  first card
                previousCardValue = card.value
                previousCardValueSuit = card.suit
            else:
                if card.value == previousCardValue:  # if card is same value
                    pass

                elif card.value == previousCardValue + 1 and card.suit == previousCardValueSuit:  # if card is one higher than next one and same suit
                    count += 1
                    previousCardValue = card.value
                    previousCardValueSuit = card.suit

                    if count == 5:  # If there are 5 cards in a row higher than 1
                        return True
                else:  # if not higher than 1, reset count variable
                    count = 1
                    previousCardValue = card.value
                    previousCardValueSuit = card.suit

        return False

    def royalFlushCheck(self, deck):
        count = 0
        cardSuit = ""

        if self.flushCheck(deck):  # Check to see if there is a flush to begin with
            return False

        elif self.staightCheck(deck):  # Check to se if there is a straight to begin with
            return False

        else:
            for card in deck:
                if card.value == 10:
                    count += 1
                    cardSuit = card.suit  # Make this the standard

                if card.value == 11:
                    if cardSuit is not card.suit:
                        return False
                    count += 1

                if card.value == 12:
                    if cardSuit is not card.suit:
                        return False
                    count += 1

                if card.value == 13:
                    if cardSuit is not card.suit:
                        return False
                    count += 1

                if card.value == 14:
                    if cardSuit is not card.suit:
                        return False
                    count += 1

# -------------------------------------------------------------# -------------------------------------------------------------


# MAIN

# Player List
Computer = Player("Computer")
Human = Player("David")
PlayerList = [Computer, Human]

# Game Class
Poker = Game(PlayerList)
Poker.startGame()
