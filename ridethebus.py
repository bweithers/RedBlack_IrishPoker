from random import shuffle, random
from statistics import mean, stdev
import matplotlib.pyplot as plt

deck = []
class Card:
    def __init__(self, suit, value, face):
        self.suit = suit
        self.value = value
        self.face = face
    def __repr__(self):
        return f"{self.face} of {self.suit}"

    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
    
def get_card() -> Card:
    # cards += 1
    if not deck:
        makeDeck()
    return deck.pop()

def driver():
    attempts = 0
    while True:
        attempts += 1
        # print(f'\nattempt: {attempts}')
        c1 = get_card()
        if not rb(c1):
            continue
        c2 = get_card()
        if not hilo(c1,c2):
            continue
        c3 = get_card()
        if not inout(c1,c2,c3):
            continue
        c4 = get_card()
        if suit(c4):
            break
    return attempts

def makeDeck():
    for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
        for value in range(1, 14):
            if value == 1:
                face = "Ace"
            elif value == 11:
                face = "Jack"
            elif value == 12:
                face = "Queen"
            elif value == 13:
                face = "King"
            else:
                face = str(value)
            deck.append(Card(suit, value, face))

    shuffle(deck)
    
def __main__():
    # print('start')
    makeDeck()
    scores = []
    for _ in range(100000):
        x = driver()
        scores.append(x) 
    # print('done')
    graphit(scores)

def rb(c1: Card) -> bool:
    # guessing algo
    guess = None
    if random() > 0.5:
        guess = "red"
    else:
        guess = "black"  
    
    # print(f'RB: {guess} vs {c1.suit}')
    # logic
    if guess == "red" and c1.suit in ("Hearts", "Diamonds"):
        return True
    if guess == "black" and c1.suit in ("Spades", "Clubs"):
        return True
    return False

def hilo(c1: Card, c2: Card) -> bool:
    # guessing algo
    guess = None
    if random() > 0.5:
        guess = "higher"
    else:
        guess = "lower"
    
    # print(f'HILO: {guess} vs {c1.value} , {c2.value}')
    # logic
    if guess == "higher":
        return c1.value < c2.value
    elif guess == "lower":
        return c1.value > c2.value

    return False

def inout(c1: Card, c2: Card, c3: Card) -> bool:
    guess = None
    if random() > 0.5:
        guess = "inside"
    else:
        guess = "outside"

    # logic
    bounds = sorted([c1,c2])
    # print(f'INOUT: {guess} vs {bounds}, {c3}')
    if guess == "inside":
        return c3 > bounds[0] and c3 < bounds[1]
    elif guess == "outside":
        return c3 < bounds[0] or c3 > bounds[1]
    return False

def suit(c4: Card) -> bool:
    guess = None
    if random() < 0.25:
        guess = "Clubs"
    elif random() < 0.5:
        guess = "Spades"
    elif random() < 0.75:
        guess = "Hearts"
    else:
        guess = "Diamonds"
    # print(f'SUIT: {guess} vs {c4.suit}')
    return guess == c4.suit

def graphit(scores):
    plt.hist(scores, bins=20, range=(0,100))
    plt.title("Irish Poker Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig('irishpoker.png')

__main__()