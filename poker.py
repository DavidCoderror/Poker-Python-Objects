# -------------------------------------------------------------# -------------------------------------------------------------
# Imports
import random


# -------------------------------------------------------------# -------------------------------------------------------------
# Card Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Card:
    def __init__(self, value, suit, img):  # Initialization (What does a card holds)
        self.value = value
        self.suit = suit
        self.img = img

    def __str__(self):  # To print the object when called ----> print(Card)
        return f"{self.value}{self.suit}{self.img}"  # To Show the card


# -------------------------------------------------------------# -------------------------------------------------------------
# Deck Class
# -------------------------------------------------------------# -------------------------------------------------------------
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

        random.shuffle(self.cardDeck)


    def customDeck(self, customDeck):
        self.cardDeck = []
        for value, suit, img in customDeck:
            self.cardDeck.append(Card(value, suit, img))


# -------------------------------------------------------------# -------------------------------------------------------------
# Player Class
# -------------------------------------------------------------# -------------------------------------------------------------

class Player:
    def __init__(self, name):  # A player holds a deck
        self.playerDeck = []
        self.playerName = name
        self.playerDeckValue = 0
        self.deckStatsData = {
            'HighPair': 0, 'HighThree': 0, 'HighFour': 0,
            'LowPair': 0, 'LowThree': 0,
            'LowCard': 0, 'HighCardType': 0, 'LowCardType': 0,
            'FlushType': "", 'HighestCardInStraight': 0
        }

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to PLAYER deck
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)  # We get a new card
        self.playerDeck.sort(key=lambda card: card.value)  # We sort the new Card


# -------------------------------------------------------------# -------------------------------------------------------------
# Table Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Table:
    def __init__(self):
        self.tableDeck = []

    def setupTable(self, MainDeck):  # Create 3 cards in deck

        try:
            while len(self.tableDeck) < 3:  # Create the 3 Starting Cards
                self.receiveCard(MainDeck)
        except:
            print("Table Setup has encountered an issue")

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to Table deck
        newCard = MainDeck.cardDeck.pop()
        self.tableDeck.append(newCard)


# -------------------------------------------------------------# -------------------------------------------------------------
# Game Class
# -------------------------------------------------------------# -------------------------------------------------------------
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

    # -------------------------------------------------------------# # -------------------------------------------------------------#
    # -------------------------------------------------------------------- We check the winner!# ------------------------------------------------------------- #
    # -------------------------------------------------------------# # -------------------------------------------------------------#

    def checkWinner(self):
        self.checkDeckValues()  # Check Decks
        player1 = self.players[0]
        player2 = self.players[1]

        # Player 1 Wins
        if player1.playerDeckValue < player2.playerDeckValue:
            print("Victory Royale : " + player1.playerName + " : " + str(
                player1.playerDeckValue) + " - Other Dude : " + str(player2.playerDeckValue))

        # Player 1 Loses
        elif player1.playerDeckValue > player2.playerDeckValue:
            print("Victory Royale : " + player2.playerName + " : " + str(
                player2.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

        # Player 1 = Player 2 - No-One Wins
        else:
            print("Tie : " + player2.playerName + " : " + str(
                player2.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

    def checkDeckValues(self):  # Checks Values of Deck of players (Scores from 1-10) 1 = Highest 10 = Lowest

        for player in self.players:

            deck = player.playerDeck + self.table.tableDeck
            deck.sort(key=lambda card: card.value)  # We sort the new Card

            if self.royalFlushCheck(deck, player):  # 1 Royal Flush - WORKS
                player.playerDeckValue = 1
                pass

            elif self.straightFlushCheck(deck, player):  # 2 Straight Flush - WORKS
                player.playerDeckValue = 2
                pass

            elif self.countCards(deck, player, 4):  # 3 Four of a kind - WORKS
                player.playerDeckValue = 3
                pass

            elif self.fullHouse(deck, player):  # 4 Full House - WORKS
                player.playerDeckValue = 4
                pass

            elif self.flushCheck(deck, player):  # 5 Flush - WORKS
                player.playerDeckValue = 5
                pass

            elif self.staightCheck(deck, player):  # 6 Straight - WORKS
                player.playerDeckValue = 6
                pass

            elif self.countCards(deck, player, 3):  # 7 Three of a kind - WORKS
                player.playerDeckValue = 7
                pass

            elif self.countDoublePair(deck, player):  # 8 Two Pairs - WORKS
                player.playerDeckValue = 8
                pass

            elif self.countCards(deck, player, 2):  # 9 One Pair - WORKS
                player.playerDeckValue = 9
                pass

            else:  # 10 High-card
                player.playerDeckValue = 10

    def countCards(self, deck, player, number):  # pairs, Three, four
        values = [card.value for card in deck]
        for value in values:
            count = values.count(value)
            if count == number:

                # Section to grab deck details
                if count == 2:
                    player.deckStatsData["HighPair"] = value
                elif count == 3:
                    player.deckStatsData["HighThree"] = value
                elif count == 4:
                    player.deckStatsData["HighFour"] = value

                return True
        return False

    def countDoublePair(self, deck, player):  # Double Pair
        countOfPairs = 0
        values = [card.value for card in deck]
        cardsChecked = []

        pairList = []

        for value in values:
            count = values.count(value)

            if value not in cardsChecked:  # Check if card already in deck
                if count == 2:
                    pairList.append(value)
                    countOfPairs += 1
                cardsChecked.append(value)  # Add to list to get marked that we checked

        # Section to grab deck details
        pairListSize = len(pairList)

        if pairListSize == 2:  # Just 2 pairs
            player.deckStatsData["LowPair"] = pairList[0]
            player.deckStatsData["HighPair"] = pairList[1]

        elif pairListSize == 3:  # Contains 3 pairs
            player.deckStatsData["LowPair"] = pairList[1]
            player.deckStatsData["HighPair"] = pairList[2]

        return countOfPairs == 2

    def flushCheck(self, deck, player):  # Check Flushes
        suits = [card.suit for card in deck]  # List of Suits

        for suit in suits:  # For suits in Suit
            player.deckStatsData["FlushType"] = suit
            if suits.count(suit) >= 5:  # We just look to see if there are 5 or more of the same type

                return True
        return False

    def staightCheck(self, deck, player):  # Check if deck contains straight
        values = [card.value for card in deck]
        values = sorted(set(values))

        straightCount = 1
        previousValue = 0

        straightList = []

        countAces = values.count(14)
        if countAces >= 1:
            values.append(1)
            values.sort()  # We sort the new Card

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
                    player.deckStatsData["HighestCardInStraight"] = value

                    return True


        return False

    def fullHouse(self, deck, player):
        countOfPairs = 0
        countOfThrees = 0

        values = [card.value for card in deck]
        cardsChecked = []

        for value in values:
            count = values.count(value)

            if value not in cardsChecked:  # Check if card already in deck
                if count == 2:
                    countOfPairs += 1
                    cardsChecked.append(value)  # Add to list to get marked that we checked

                if count == 3:
                    countOfThrees += 1
                    cardsChecked.append(value)  # Add to list to get marked that we checked

        if countOfPairs >= 1 and countOfThrees == 1:
            return True

        elif countOfThrees == 2:
            return True

        else:
            return False

    def straightFlushCheck(self, deck, player):  # Check if deck contains straight which is also a flush

        if self.flushCheck(deck, player) is not True:  # Check if there is a flush
            return False

        # Make Local List System
        hearts = []
        diamonds = []
        spades = []
        clubs = []

        for card in deck:
            if card.suit == "♡":
                hearts.append(card.value)
            elif card.suit == "♢":
                diamonds.append(card.value)
            elif card.suit == "♠":
                spades.append(card.value)
            else:
                clubs.append(card.value)

        listOfSuits = [hearts, diamonds, spades, clubs]

        for suits in listOfSuits:
            values = suits
            values = sorted(set(values))

            straightCount = 1
            previousValue = 0

            countAces = values.count(14)
            if countAces >= 1:
                values.append(1)
                values.sort()  # We sort the new Card

            for value in values:
                if previousValue == 0:
                    previousValue = value
                else:
                    if previousValue + 1 == value:
                        straightCount += 1
                    else:
                        straightCount = 1
                    previousValue = value

                    if straightCount == 5:
                        return True
        return False

    def royalFlushCheck(self, deck, player):

        if self.flushCheck(deck, player) is not True:  # Check if there is a flush
            return False

        if self.staightCheck(deck, player) is not True:  # Check if there is a straight
            return False

        # Make Local List
        hearts = []
        diamonds = []
        spades = []
        clubs = []

        neededValues = {10, 11, 12, 13, 14}

        for card in deck:
            if card.suit == "♡":
                hearts.append(card.value)
            elif card.suit == "♢":
                diamonds.append(card.value)
            elif card.suit == "♠":
                spades.append(card.value)
            else:
                clubs.append(card.value)

        listOfSuits = [hearts, diamonds, spades, clubs]

        for suits in listOfSuits:
            values = suits
            values = sorted(set(values))

            if neededValues.issubset(values):
                return True

        return False

    # -------------------------------------------------------------#  -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------------- Extra # -------------------------------------------------------------# -------------------------------------------------------------
    # -------------------------------------------------------------# -------------------------------------------------------------# -------------------------------------------------------------

    def askPlayerToContinue(self):
        acceptableAnswer = True
        while acceptableAnswer:
            answer = int(input("Do you want to Continue (1) or Fold(2)? : "))

            if answer == 1:
                return 1
            if answer == 2:
                return 2


# -------------------------------------------------------------# -------------------------------------------------------------
# -------------------------------------------------------------# -------------------------------------------------------------
# -------------------------------------------------------------# -------------------------------------------------------------

# MAIN

# Player List
# = Player("Computer")
Human = Player("David")
TestPlayer = Player("TEST")

# PlayerList = [Computer, Human]
PlayerList = [TestPlayer, Human]

# Game Class
Poker = Game(PlayerList)

# Force player cards
TestPlayer.playerDeck = [
    Card(9, "♡", "🂪"),
    Card(10, "♠", "🂫")
]

# Force table cards
Poker.table.tableDeck = [
    Card(11, "♠", "🂬"),
    Card(11, "♡", "🂮"),
    Card(11, "♠", "🂾"),
    Card(4, "♣", "🃄"),
    Card(9, "♡", "🂩")
]

Poker.startGame()
