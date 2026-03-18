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
            'FlushType': "N/A", 'HighestCardInStraight': 0, 'FlushValues': [],
            'FiveHighestCards': []
        }
        self.playerCurrency = Currency()

    def receiveCard(self, MainDeck):  # Grab a card from MAIN deck and add to PLAYER deck
        newCard = MainDeck.cardDeck.pop()
        self.playerDeck.append(newCard)  # We get a new card
        self.playerDeck.sort(key=lambda card: card.value)  # We sort the new Card

    def grabFiveHighestCards(self, deck):
        reversedDeck = sorted(deck, key=lambda card: card.value, reverse=True)  # Reverse the deck
        theFiveHighestCards = reversedDeck[:5]  # Grab First 5 cards
        self.playerDeckStatsData['FiveHighestCards'] = [card.value for card in theFiveHighestCards] # Store Data

    def resetData(self):
        self.playerDeckStatsData = {
            'HighCard': 0, 'HighPair': 0, 'HighThree': 0, 'HighFour': 0,
            'LowCard': 0, 'LowPair': 0, 'LowThree': 0,
            'FlushType': "N/A", 'HighestCardInStraight': 0, 'FlushValues': [],
            'FiveHighestCards': [], 'HandValue' : 0
        }

# -------------------------------------------------------------# -------------------------------------------------------------
# Currency Class
# -------------------------------------------------------------# -------------------------------------------------------------
class Currency:
    def __init__(self):
        self.currency = 0

    def addCurrency(self, currencyBeingAdded):  # Create 3 cards in deck
        self.currency += currencyBeingAdded

    def removeCurrency(self, currencyBeingRemoved):  # Grab a card from MAIN deck and add to Table deck=
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
        self.currentTurn = 0
        self.playerFolded = False
        self.pot = Currency()
        self.pot.resetCurrency()

        for player in playerNames:  # Add players to the list
            self.players.append(player)

    def newGameSession(self):  # Lets say to begin a long lien of matches
        for player in self.players:
            player.playerCurrency.setCurrency(100)
        self.startGame()  # Start the new round

    def startGame(self):  # Reset and Setups

        self.deck = Deck()
        self.round = 0
        self.playerFolded = False
        self.table.tableDeck = []
        self.pot.resetCurrency()
        self.currentBet = 0

        for player in self.players:
            player.playerDeck = []
            player.receiveCard(self.deck)
            player.receiveCard(self.deck)
            player.resetData()
            player.playerDeckValue = 0

        self.table.setupTable(self.deck)

    #-------------------------------------------------------------------------------------------#

    # Player places a bet
    def bet(self, playerIndex, amount):
        player = self.players[playerIndex]
        if amount > player.playerCurrency.currency:
            amount = player.playerCurrency.currency  # All-in if not enough

        player.playerCurrency.removeCurrency(amount)
        self.pot.addCurrency(amount)
        self.currentBet = amount  # Current bet for opponent to match

        return {
            "status": "bet_placed",
            "player": player.playerName,
            "amount": amount,
            "pot": self.pot.getCurrency()
        }

    # Player raises the current bet
    def raise_bet(self, playerIndex, raiseAmount):
        player = self.players[playerIndex]

        # Total amount to put in the pot
        totalBet = self.currentBet + raiseAmount

        if totalBet > player.playerCurrency.currency:
            totalBet = player.playerCurrency.currency  # all-in if not enough

        # Deduct currency from player and add to pot
        player.playerCurrency.removeCurrency(totalBet)
        self.pot.addCurrency(totalBet)

        # Update current bet
        self.currentBet = totalBet

        return {
            "status": "raise",
            "player": player.playerName,
            "raise_amount": raiseAmount,
            "total_bet": totalBet,
            "pot": self.pot.getCurrency()
        }

    # Player calls the current bet
    def call(self, playerIndex):
        player = self.players[playerIndex]
        to_call = self.currentBet
        if player.playerCurrency.currency < to_call:
            to_call = player.playerCurrency.currency  # All-in if not enough

        player.playerCurrency.removeCurrency(to_call)
        self.pot.addCurrency(to_call)

        return {
            "status": "call",
            "player": player.playerName,
            "amount": to_call,
            "pot": self.pot.getCurrency()
        }

    # Player folds
    def fold(self, playerIndex):
        self.playerFolded = True
        winnerIndex = 0 if playerIndex == 1 else 1
        self.players[winnerIndex].playerCurrency.addCurrency(self.pot.getCurrency())
        self.pot.resetCurrency()

        return {
                   "status": "player_folded",
                   "foldedPlayer": self.players[playerIndex].playerName,
                   "winner": self.players[winnerIndex].playerName,
                   "pot": self.players[winnerIndex].playerCurrency.getCurrency()
               }
    #------------------------------------------------------------------------------------#

    def cardToDict(self, card):
        return {
            "value": card.value,
            "suit": card.suit,
            "img": card.img
        }

    def getStateForPlayer(self, playerIndex):  # Grab the State

        player = self.players[playerIndex]
        opponent = self.players[0] if playerIndex == 1 else self.players[1]

        return {
            "round": self.round,
            "table": [self.cardToDict(card) for card in self.table.tableDeck],
            "your_cards": [self.cardToDict(card) for card in player.playerDeck],
            "handValue": player.playerDeckStatsData["HandValue"],
            "your_currency": player.playerCurrency.currency,

            "opponent_currency": opponent.playerCurrency.currency,
            "opponent_cards": ["🂠", "🂠"]  # hidden cards

        }

    def getFinalState(self):  # When Cards Revealed at the end

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
            "reason": winnerData['reason']
        }

    # -------------------------------------------------------------# # -------------------------------------------------------------#
    # -------------------------------------------------------------------- We check the winner!# ------------------------------------------------------------- #
    # -------------------------------------------------------------# # -------------------------------------------------------------#

    def checkWinner(self):
        self.checkDeckValues()  # Check Decks
        player1 = self.players[0]
        player2 = self.players[1]

        result = {"winner": "?", "reason": "Hand Not Checked"}

        hand_names = {
            1: "Royal Flush",
            2: "Straight Flush",
            3: "Four of a Kind",
            4: "Full House",
            5: "Flush",
            6: "Straight",
            7: "Three of a Kind",
            8: "Two Pair",
            9: "Pair",
            10: "High Card"
        }

        # Player 1 Wins
        if player1.playerDeckValue < player2.playerDeckValue:
            result = {"winner": player1.playerName, "reason": f"{hand_names[player1.playerDeckValue]} beats {hand_names[player2.playerDeckValue]}"}
            pass

        # Player 2 Wins
        elif player1.playerDeckValue > player2.playerDeckValue:
            result = {"winner": player2.playerName, "reason": f"{hand_names[player2.playerDeckValue]} beats {hand_names[player1.playerDeckValue]}"}

            pass

        # IF hand is the same
        else:
            # 1. Straight Flush or Straight
            if player1.playerDeckValue == 2 or player1.playerDeckValue == 6:
                if player1.playerDeckStatsData['HighestCardInStraight'] > player2.playerDeckStatsData['HighestCardInStraight']:
                    result = {"winner": player1.playerName,
                              "reason": f"Better Straight! Top card: {player1.playerDeckStatsData['HighestCardInStraight']}"}
                    pass
                elif player1.playerDeckStatsData['HighestCardInStraight'] < player2.playerDeckStatsData[
                    'HighestCardInStraight']:
                    result = {"winner": player2.playerName,
                              "reason": f"Better Straight! Top card: {player2.playerDeckStatsData['HighestCardInStraight']}"}
                    pass

            # 2. Four of a kind
            elif player1.playerDeckValue == 3:
                if player1.playerDeckStatsData['HighFour'] > player2.playerDeckStatsData['HighFour']:
                    result = {"winner": player1.playerName,
                              "reason": f"Four of a kind! {player1.playerDeckStatsData['HighFour']}s beat {player2.playerDeckStatsData['HighFour']}s"}
                    pass
                elif player1.playerDeckStatsData['HighFour'] < player2.playerDeckStatsData['HighFour']:
                    result = {"winner": player2.playerName,
                              "reason": f"Four of a kind! {player2.playerDeckStatsData['HighFour']}s beat {player1.playerDeckStatsData['HighFour']}s"}
                    pass
                else:
                    kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighFour']] * 4)
                    if kicker_winner == "Tie":
                        result = {"winner": "Tie!", "reason": "Same Quads, but better Kicker"}
                    else:
                        result = {"winner": kicker_winner, "reason": "Same Quads, but better kicker"}

            # 3. Full House
            elif player1.playerDeckValue == 4:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player1.playerName,
                              "reason": f"Full House! Triple {player1.playerDeckStatsData['HighThree']} beats {player2.playerDeckStatsData['HighThree']}"}
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player2.playerName,
                              "reason": f"Full House! Triple {player2.playerDeckStatsData['HighThree']} beats {player1.playerDeckStatsData['HighThree']}"}
                    pass
                else:
                    if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                        result = {"winner": player1.playerName,
                                  "reason": f"Full House tie, Pair {player1.playerDeckStatsData['HighPair']} wins"}
                        pass
                    elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                        result = {"winner": player2.playerName,
                                  "reason": f"Full House tie, Pair {player2.playerDeckStatsData['HighPair']} wins"}
                        pass

            # 4. Flush
            elif player1.playerDeckValue == 5:
                if player1.playerDeckStatsData['FlushValues'] > player2.playerDeckStatsData['FlushValues']:
                    result = {"winner": player1.playerName,
                              "reason": f"Flush! High card: {player1.playerDeckStatsData['FlushValues'][0]}"}
                    pass
                elif player1.playerDeckStatsData['FlushValues'] < player2.playerDeckStatsData['FlushValues']:
                    result = {"winner": player2.playerName,
                              "reason": f"Flush! High card: {player2.playerDeckStatsData['FlushValues'][0]}"}
                    pass

            # 5. Three of a kind
            elif player1.playerDeckValue == 7:
                if player1.playerDeckStatsData['HighThree'] > player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player1.playerName,
                              "reason": f"Triple {player1.playerDeckStatsData['HighThree']} beats {player2.playerDeckStatsData['HighThree']}"}
                    pass
                elif player1.playerDeckStatsData['HighThree'] < player2.playerDeckStatsData['HighThree']:
                    result = {"winner": player2.playerName,
                              "reason": f"Triple {player2.playerDeckStatsData['HighThree']} beats {player1.playerDeckStatsData['HighThree']}"}
                    pass
                else:
                    kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighThree']] * 3)
                    if kicker_winner == "Tie":
                        result = {"winner": "Tie!", "reason": "Same Three of a Kind, better kicker"}
                    else:
                        result = {"winner": kicker_winner, "reason": f"Triple tie, kicker wins: {kicker_winner}"}

            # 6. Two Pair
            elif player1.playerDeckValue == 8:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player1.playerName, "reason": "Better Two Pair, Higher Pair"}
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    result = {"winner": "Tie!", "reason": "Two Pair tie, kicker same"}
                    pass
                else:
                    if player1.playerDeckStatsData['LowPair'] > player2.playerDeckStatsData['LowPair']:
                        result = {"winner": player1.playerName, "reason": "Same High Pair, better Lower pair"}
                        pass
                    elif player1.playerDeckStatsData['LowPair'] < player2.playerDeckStatsData['LowPair']:
                        result = {"winner": player2.playerName, "reason": "Same High Pair, better Lower pair "}
                        pass
                    else:
                        kicker_winner = self.compareKickers(player1, player2, [player1.playerDeckStatsData['HighPair']] * 2 + [player1.playerDeckStatsData['LowPair']] * 2)
                        if kicker_winner == "Tie":
                            result = {"winner": "Tie!", "reason": "Same Two Pair, better kicker"}
                        else:
                            result = {"winner": kicker_winner, "reason": f"Two Pair tie, kicker wins: {kicker_winner}"}

            # 7. Pair
            elif player1.playerDeckValue == 9:
                if player1.playerDeckStatsData['HighPair'] > player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player1.playerName,
                              "reason": f"Pair {player1.playerDeckStatsData['HighPair']} beats {player2.playerDeckStatsData['HighPair']}"}
                    pass
                elif player1.playerDeckStatsData['HighPair'] < player2.playerDeckStatsData['HighPair']:
                    result = {"winner": player2.playerName,
                              "reason": f"Pair {player2.playerDeckStatsData['HighPair']} beats {player1.playerDeckStatsData['HighPair']}"}
                    pass
                else:
                    kicker_winner = self.compareKickers( player1,player2,[player1.playerDeckStatsData['HighPair']] * 2)
                    if kicker_winner == "Tie":
                        result = {"winner": "Tie!", "reason": "Same Pairs, better kicker"}
                    else:
                        result = {"winner": kicker_winner, "reason": f"Pair tie, kicker wins: {kicker_winner}"}

            # 8. HighCard
            else:

                kicker_winner = self.compareKickers(player1, player2, [])
                if kicker_winner == "Tie":
                    result = {"winner": "Tie!",
                              "reason": f"High Card tie! Top cards: {player1.playerDeckStatsData['FiveHighestCards']}"}
                else:
                    result = {"winner": kicker_winner, "reason": f"Top card wins: {kicker_winner}"}

        return result

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
            if len(values) >= 5:  # We only look for the suit that has 5 or more items in them
                values.sort(reverse=True)  # Highest to lowest now
                player.playerDeckStatsData["FlushValues"] = values[:5]  # We put the 5 highest values in the list
                player.playerDeckStatsData["FlushType"] = suit  # We mark the suit npw
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

    def compareKickers(self, player1, player2, mainCards):
        # mainCards = list of values forming the main hand (e.g., [9,9,9,9])
        p1_Deck = [v for v in player1.playerDeckStatsData['FiveHighestCards'] if v not in mainCards]
        p2_Deck = [v for v in player2.playerDeckStatsData['FiveHighestCards'] if v not in mainCards]

        # Compare remaining cards descending
        p1_Deck.sort(reverse=True)
        p2_Deck.sort(reverse=True)

        for player1Card, player2Card in zip(p1_Deck, p2_Deck):
            if player1Card > player2Card:
                return player1.playerName
            elif player1Card < player2Card:
                return player2.playerName
        return "Tie"

# -------------------------------------------------------------# -------------------------------------------------------------
# -------------------------------------------------------------# -------------------------------------------------------------
# -------------------------------------------------------------# -------------------------------------------------------------
# MAIN - Test 5 Cards Hands

# Create Players
Computer = Player("Computer")
Human = Player("David")
PlayerList = [Computer, Human]

# Initialize Game
Poker = Game(PlayerList)

# Assign 5-card hands to Table
Poker.table.tableDeck = [

]

# Assign 5-card hands to players
Computer.playerDeck = [
    Card(2, "♠", "🂩"),
    Card(3, "♠", "🂪"),
    Card(3, "♠", "🂫"),
    Card(3, "♠", "🂬"),
    Card(11, "♠", "🂮"),
]

Human.playerDeck = [
    Card(2, "♢", "🃂"),
    Card(2, "♢", "🃃"),
    Card(2, "♢", "🃄"),
    Card(2, "♢", "🃅"),
    Card(6, "♢", "🂦"),
]

# Update Hand Values
Poker.checkDeckValues()

# Show Table
print("\n--- Table Cards ---")
for card in Poker.table.tableDeck:
    print(f"{card.value}{card.suit}{card.img}", end="  ")
print("\n")

# Show Player Hands
print("--- Player Hands ---")
for player in PlayerList:
    hand = "  ".join([f"{card.value}{card.suit}{card.img}" for card in player.playerDeck])
    print(f"{player.playerName}: {hand}")

# Check Winner
winner = Poker.checkWinner()
print("\n--- Winner ---")
print(f"Winner: {winner['winner']}")
print(f"Reason: {winner['reason']}")


# Betting System
Poker.newGameSession()


# Example Betting Round
print(Poker.bet(0, 20))  # Computer bets 20
print(Poker.call(1))     # Human calls 20

print("Pot:", Poker.pot.getCurrency())  # Pot should now be 40

print(Poker.bet(0, 10))       # Computer bets 10
print(Poker.raise_bet(1, 15)) # David raises 15 (total 25)
print(Poker.call(0))           # Computer calls 25

print("Pot after second round:", Poker.pot.getCurrency())
