# -------------------------------------------------------------# -------------------------------------------------------------
# Imports
import random
from collections import Counter

# -------------------------------------------------------------# -------------------------------------------------------------


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
        self.playerName = name
        self.playerDeck = []
        self.playerDeckValue = 0
        self.playerDeckStatsData = {
            'HighCard': 0, 'HighPair': 0, 'HighThree': 0, 'HighFour': 0,  # Highs
            'LowCard': 0, 'LowPair': 0, 'LowThree': 0,  # lows
            'FlushType': "N/A", 'HighestCardInStraight': 0, 'FlushValues': []
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
            self.endMessage(1)
            pass

        # Player 1 Loses
        elif player1.playerDeckValue > player2.playerDeckValue:
            self.endMessage(2)
            pass

        else:
            # 1. Straight Flush or Straight
            if player1.playerDeckValue == 2 or player1.playerDeckValue == 6:
                if player1.playerDeckStatsData['HighestCardInStraight'] > player2.playerDeckStatsData['HighestCardInStraight']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighestCardInStraight'] < player2.playerDeckStatsData['HighestCardInStraight']:
                    self.endMessage(2)
                    pass

            # 2. Four of a kind
            elif player1.playerDeckValue == 3:
                if player1.playerDeckStatsData['HighFour'] > player2.playerDeckStatsData['HighFour']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighFour'] < player2.playerDeckStatsData['HighFour']:
                    self.endMessage(2)
                    pass
            # 3. Full House -- REWORK (NEED TO LOOK INTO)
            elif player1.playerDeckValue == 4:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    self.endMessage(2)
                    pass
                else:
                    if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                        self.endMessage(1)
                        pass
                    elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                        self.endMessage(2)
                        pass

            # 4. Flush -- REWORK (NEED TO LOOK INTO)
            elif player1.playerDeckValue == 5:
                if player1.playerDeckStatsData['FlushValues'] > player2.playerDeckStatsData['FlushValues']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['FlushValues'] < player2.playerDeckStatsData['FlushValues']:
                    self.endMessage(2)
                    pass

            # 5. Three of a kind
            elif player1.playerDeckValue == 7:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    self.endMessage(2)
                    pass

            # 6. Two Pair
            elif player1.playerDeckValue == 8:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    self.endMessage(2)
                    pass
                else:
                    if player1.playerDeckStatsData['LowPair'] > player2.playerDeckStatsData['LowPair']:
                        self.endMessage(1)
                        pass
                    elif player1.playerDeckStatsData['LowPair'] < player2.playerDeckStatsData['LowPair']:
                        self.endMessage(2)
                        pass

            # 7. Pair
            elif player1.playerDeckValue == 9:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    self.endMessage(2)
                    pass
                else:
                    if player1.playerDeckStatsData['HighCard'] > player2.playerDeckStatsData['HighCard']:
                        self.endMessage(1)
                        pass
                    elif player1.playerDeckStatsData['HighCard'] < player2.playerDeckStatsData['HighCard']:
                        self.endMessage(2)
                        pass
                    else:
                        if player1.playerDeckStatsData['LowCard'] > player2.playerDeckStatsData['LowCard']:
                            self.endMessage(1)
                            pass
                        elif player1.playerDeckStatsData['LowCard'] < player2.playerDeckStatsData['LowCard']:
                            self.endMessage(2)
                            pass

            # 8. HighCard
            elif player1.playerDeckValue == 10:
                if player1.playerDeckStatsData['HighCard'] > player2.playerDeckStatsData['HighCard']:
                    self.endMessage(1)
                    pass
                elif player1.playerDeckStatsData['HighCard'] < player2.playerDeckStatsData['HighCard']:
                    self.endMessage(2)
                    pass
                else:
                    if player1.playerDeckStatsData['LowCard'] > player2.playerDeckStatsData['LowCard']:
                        self.endMessage(1)
                        pass
                    elif player1.playerDeckStatsData['LowCard'] < player2.playerDeckStatsData['LowCard']:
                        self.endMessage(2)
                        pass

            # LAST RESORT: Player 1 = Player 2 - No-One Wins / It's a tie!
            else:
                self.endMessage(3)

    def checkDeckValues(self):  # Checks Values of Deck of players (Scores from 1-10) 1 = Highest 10 = Lowest

        for player in self.players:

            deck = player.playerDeck + self.table.tableDeck
            deck.sort(key=lambda card: card.value)  # We sort the new Card

            # High Card and LowCard
            sorted_values = sorted([card.value for card in deck])
            player.playerDeckStatsData["LowCard"] = sorted_values[0]
            player.playerDeckStatsData["HighCard"] = sorted_values[-1]

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
        cardChecked = False

        count = Counter(values)

        for value in values:
            if count[value] == number:

                # Section to grab deck details
                if number == 2:
                    player.playerDeckStatsData["HighPair"] = value
                    cardChecked = True

                elif number == 3:
                    player.playerDeckStatsData["HighThree"] = value
                    cardChecked = True

                elif number == 4:
                    player.playerDeckStatsData["HighFour"] = value
                    cardChecked = True


        return cardChecked

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
            player.playerDeckStatsData["LowPair"] = pairList[0]
            player.playerDeckStatsData["HighPair"] = pairList[1]

        elif pairListSize == 3:  # Contains 3 pairs
            player.playerDeckStatsData["LowPair"] = pairList[1]
            player.playerDeckStatsData["HighPair"] = pairList[2]

        return countOfPairs >= 2

    def flushCheck(self, deck, player):  # Check Flushes
        suits = {}

        # Group cards by suit
        for card in deck:
            suits.setdefault(card.suit, []).append(card.value)

        for suit, values in suits.items():
            if len(values) >= 5: # We only look for the suit that has 5 or more items in them
                values.sort(reverse=True) # Highest to lowest now
                player.playerDeckStatsData["FlushValues"] = values[:5] # We put the 5 highest values in the list
                player.playerDeckStatsData["FlushType"] = suit # We mark the suit npw
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
                    player.playerDeckStatsData["HighestCardInStraight"] = value

                    return True

        return False

    def fullHouse(self, deck, player):
        values = [card.value for card in deck]
        uniqueValues = set(values)

        triples = []
        pairs = []

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
                        player.playerDeckStatsData["HighestCardInStraight"] = value
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

            if neededValues.issubset(values):  # If royal flush is same as our hand
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

    def endMessage(self, number):
        player1 = self.players[0]
        player2 = self.players[1]

        if number == 1:  # Player 1 WINS
            print("Victory Royale : " + player1.playerName + " : " + str(
                player1.playerDeckValue) + " - Other Dude : " + str(player2.playerDeckValue))

        elif number == 2:  # Player 2 WINS
            print("Victory Royale : " + player2.playerName + " : " + str(
                player2.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

        elif number == 3:  # TIE
            print("Tie : " + player2.playerName + " : " + str(
                player2.playerDeckValue) + " - Other Dude : " + str(player1.playerDeckValue))

        else:
            print("endMessage Method Issue - Use Correct Number")


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
    Card(11, "♠", "🂬"),
    Card(11, "♡", "🂮"),
    Card(11, "♠", "🂾"),
    Card(9, "♣", "🃄"),
    Card(9, "♡", "🂩")
]

# Force table cards
#Poker.table.tableDeck = [
#    Card(11, "♠", "🂬"),
#    Card(11, "♡", "🂮"),
#    Card(11, "♠", "🂾"),
##
# #Card(9, "♡", "🂩")
#]

Poker.startGame()
