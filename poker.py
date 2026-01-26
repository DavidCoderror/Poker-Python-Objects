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
        self.cardDeck.sort()


# -------------------------------------------------------------# -------------------------------------------------------------
# Player Class
class Player:
    def __init__(self, name):  # A player holds a deck
        self.playerDeck = []
        self.playerName = name
        self.playerDeckValue = 0

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
# Game Class
class Game:  # The actual Game and Rounds
    def __init__(self, playerNames):
        self.deck = Deck()
        self.table = Table()
        self.players = []
        self.round = 0
        self.fold = False

        for name in playerNames:  # Add players to the list
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
            while self.round < 2 and self.fold is not True:  # Round System
                self.roundCounter()  # Round UI ----- Round 1
                self.table.receiveCard(self.deck)
                self.currentState()
                playerResponse = self.askPlayerToContinue()

                if playerResponse == 1:
                    pass
                elif playerResponse == 2:
                    print("Folded!!")
                    break
        self.checkWinner()
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

    # -------------------------------------------------------------------- We check the winner!
    def checkWinner(self):
        self.checkDeckValues()  # Check Decks
        player1 = self.players[0]
        player2 = self.players[1]

        # Player 1 < Player 2 - Human Higher
        if player1.playerDeckValue > player2.playerDeckValue:
            print("Victory Royale : " + player1.playerName + " : " + str(
                player1.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

        # Player 1 > Player 2 - Bot Higher
        elif player1.playerDeckValue < player2.playerDeckValue:
            print("Victory Royale : " + player2.playerName + " : " + str(
                player2.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

        # Player 1 = Player 2 - No-One Wins
        else:
            print("Tie")
        # -------------------------------------------------------------------- Deck Check!

    def checkDeckValues(self):  # Checks Values of Deck of players (Scores from 1-10) 1 = Highest 10 = Lowest

        for player in self.players:

            deck = player.playerDeck + self.table.tableDeck
            deck.sort(key=lambda card: card.value)  # We sort the new Card

            if self.royalFlushCheck(deck):  # 1 Royal Flush
                player.playerDeckValue = 1

            elif self.straightFlushCheck(deck):  # 2 Straight Flush
                player.playerDeckValue = 2

            elif self.countCards(deck, 4):  # 3 Four of a kind
                player.playerDeckValue = 3

            elif self.countCards(deck, 2) and self.countCards(deck, 3):  # 4 Full House
                player.playerDeckValue = 4

            elif self.flushCheck(deck):  # 5 Flush
                player.playerDeckValue = 5

            elif self.staightCheck(deck):  # 6 Straight
                player.playerDeckValue = 6

            elif self.countCards(deck, 3):  # 7 Three of a kind
                player.playerDeckValue = 7

            elif self.countDoublePair(deck):  # 8 Two Pairs
                player.playerDeckValue = 8

            elif self.countCards(deck, 2):  # 9 One Pair
                player.playerDeckValue = 9

            else:  # 10 High-card
                player.playerDeckValue = 10

    def countCards(self, deck, number):  # pairs,Three, four
        values = [card.value for card in deck]

        for value in values:
            count = values.count(value)
            if count == number:
                return True
        return False

    def countDoublePair(self, deck):  # Double Pair
        countOfPairs = 0
        values = [card.value for card in deck]
        cardsChecked = []

        for value in values:
            count = values.count(value)

            if value not in cardsChecked:  # Check if card already in deck
                if count == 2:
                    countOfPairs += 1
                    cardsChecked.append(value)  # Add to list to get marked that we checked

        return countOfPairs == 2



    def flushCheck(self, deck):  # Check Flushes
        suits = [card.suit for card in deck]  # List of Suits

        for suit in suits:  # For suits in Suit
            if suits.count(suit) >= 5:
                return True
        return False


    def staightCheck(self, deck):  # Check if deck contains straight
        count = 1
        previousCardValue = 0
        functionDeck = deck

        aDetected = 0
        aSuit = ""
        for card in functionDeck:  # Ace counts as both value 1 and 14
            if card.value == 14:
                aDetected = 1
                aSuit = card.suit

        if aDetected == 1:
            addNewAce = Card(1, aSuit, "🂾")
            functionDeck.append(addNewAce)
            functionDeck.sort(key=lambda card: card.value)

        for card in functionDeck:
            if previousCardValue == 0:  # Move past from  first card
                previousCardValue = card.value
            else:
                if card.value == previousCardValue:  # if card is same value
                    pass

                elif card.value == previousCardValue + 1:  # if card is one higher than next
                    count += 1
                    previousCardValue = card.value
                    if count == 5:  # If there are 5 cards in a row higher than 1
                        functionDeck.remove(functionDeck[0])
                        return True

                else:  # if not higher than 1, reset count variable
                    count = 1
                    previousCardValue = card.value

        functionDeck.remove(functionDeck[0])
        return False

    def straightFlushCheck(self, deck):  # Check if deck contains straight which is also a flush
        count = 1
        previousCardValue = 0
        previousCardValueSuit = ""

        functionDeck = deck

        aDetected = 0
        aSuit = ""
        for card in functionDeck:  # Ace counts as both value 1 and 14
            if card.value == 14:
                aDetected = 1
                aSuit = card.suit

        if aDetected == 1:
            addNewAce = Card(1, aSuit, "🂾")
            functionDeck.append(addNewAce)
            functionDeck.sort(key=lambda card: card.value)

        for card in functionDeck:  # Straight Check
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

        functionDeck.remove(functionDeck[0])
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
                    if cardSuit == card.suit:
                        count += 1

                if card.value == 12:
                    if cardSuit is not card.suit:
                        if cardSuit == card.suit:
                            count += 1

                if card.value == 13:
                    if cardSuit is not card.suit:
                        if cardSuit == card.suit:
                            count += 1

                if card.value == 14:
                    if cardSuit == card.suit:
                        count += 1

        if count == 5:
            return True
        else:
            return False

    # -------------------------------------------------------------------- Extra

    def askPlayerToContinue(self):
        acceptableAnswer = True
        while acceptableAnswer:
            answer = int(input("Do you want to Continue (1) or Fold(2)? : "))

            if answer == 1:
                return 1
            if answer == 2:
                return 2


# -------------------------------------------------------------# -------------------------------------------------------------

# MAIN

# Player List
Computer = Player("Computer")
Human = Player("David")
PlayerList = [Computer, Human]

# Game Class
Poker = Game(PlayerList)
Poker.startGame()
