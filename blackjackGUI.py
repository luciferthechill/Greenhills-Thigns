try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
#various globsls
inPlay = False
outcome = "Hit or stand?"
playerScore = 0
dealerScore = 0
#global cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
#front cards from jfitz.com
#card front
cardSize = (73, 98)
cardCenter = (36.5, 49)
cardImages = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
#card back
cardBackSize = (71, 96)
cardBackCenter = (35.5, 48)
cardBack = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")
#card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)
    def __str__(self):
        return self.suit + self.rank
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank
    def draw(self, canvas, pos):
        cardLoc = (cardCenter[0] + cardSize[0] * RANKS.index(self.rank),
                    cardCenter[1] + cardSize[1] * SUITS.index(self.suit))
        canvas.draw_image(cardImages, cardLoc, cardSize, [pos[0] + cardCenter[0], pos[1] + cardCenter[1]], cardSize)
#hand class
class Hand:
    def __init__(self):
        self.cards = []
    def __str__(self):
        result = ""
        for card in self.cards:
            result += " " + card.__str__()
        return "Hand contains" + result
    def addCard(self, card):
        self.cards.append(card)
    def getValue(self):
        #scoring
        value = 0
        containsAce = False
        for card in self.cards:
            rank = card.getRank()
            value += VALUES[rank]
            if(rank == 'A'):
                containsAce = True
        #ace handling
        if(value <= 11 and containsAce):
            value += 10
        return value
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 80
#deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
    def shuffle(self):
        random.shuffle(self.cards)
    def dealCard(self):
        return self.cards.pop(0)
    def __str__(self):
        result = ""
        for card in self.cards:
            result += " " + card.__str__()
        return "Deck contains" + result
#######################################
####            Buttons            ####
#######################################
#deal function
def deal():
    global outcome, inPlay, deck, playerHand, dealerHand, deck, dealerScore
    if(inPlay == True):
        outcome = "Player lost because of re-deal! New deal?"
        dealerScore += 1
        inPlay = False
    else:
        deck = Deck()
        outcome
        deck.shuffle()
        playerHand = Hand()
        dealerHand = Hand()
        playerHand.addCard(deck.dealCard())
        playerHand.addCard(deck.dealCard())
        dealerHand.addCard(deck.dealCard())
        dealerHand.addCard(deck.dealCard())
        print ("Player: {}".format(playerHand))
        print ("Dealer: {}".format(dealerHand))
        inPlay = True
#hit function
def hit():
    global outcome, inPlay, dealerScore
    if inPlay:
        if playerHand.getValue() <= 21:
            playerHand.addCard(deck.dealCard())

        print ("Player hand {}".format(playerHand))

        if playerHand.getValue() > 21:
            outcome = "You have busted. New deal?"
            inPlay = False
            dealerScore += 1
            print ("You have busted")
#stand function
def stand():
    global outcome, playerScore, dealerScore, inPlay
    if inPlay:
        inPlay = False

        while dealerHand.getValue() < 17:
            dealerHand.addCard(deck.dealCard())

        print ("Dealer: {}".format(dealerHand))

        if dealerHand.getValue() > 21:
            outcome = "Dealer busted. Congratulations!"
            print ("Dealer is busted. Player wins.")
            playerScore += 1
        else:
            if dealerHand.getValue() >= playerHand.getValue() or playerHand.getValue() > 21:
                print ("Dealer wins")
                outcome = "Dealer wins. New deal?"
                dealerScore += 1
            else:
                print ("Player wins. New deal?")
                outcome = "Player wins"
                playerScore += 1
#drawing function
def draw(canvas):
    global outcome, inPlay, cardBack, cardLoc, playerScore, dealerScore
    canvas.draw_text("Blackjack", [220, 50], 50 ,"White")
    playerHand.draw(canvas, [100, 300])
    dealerHand.draw(canvas, [100, 150])
    canvas.draw_text(outcome, [10, 100], 30 ,"White")
    canvas.draw_text("Dealer: %s" % dealerScore, [10, 150], 20 ,"Gray")
    canvas.draw_text("Player: %s" % playerScore, [10, 300], 20 ,"Gray")
    if inPlay:
        canvas.draw_image(cardBack, cardBackCenter, cardBackSize, (136,199), cardBackSize)
        outcome = "Game in progress..."
#game window
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Black")
#buttons
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
#start
deal()
frame.start()
