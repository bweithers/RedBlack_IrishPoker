from random import shuffle, random
from statistics import mean, stdev
import matplotlib.pyplot as plt
from datetime import datetime

DEBUG = False
SMART = False
LOGGING = True
LOGFILE = open('log.csv', 'a')
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
        if DEBUG:
            print(f'\nattempt: {attempts}')
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
    makeDeck()
    scores = []
    iterations = 10000 
    for _ in range(iterations):
        scores.append(driver())
    print(f'Random mode: {mean(scores)=:.2f}, {stdev(scores)=:.2f}')

    makeDeck()
    global SMART
    SMART = True
    scores = []
    for _ in range(iterations):
        scores.append(driver())
    print(f'SMART mode: {mean(scores)=:.2f}, {stdev(scores)=:.2f}')
    
    # graphit(scores)

def rb(c1: Card) -> bool:
    # guessing algo
    guess = None
    if random() > 0.5:
        guess = "red"
    else:
        guess = "black"  

    if SMART:
        guess = "red" if sum(map(lambda c: 1 if c.suit in ("Hearts", "Diamonds") else -1, deck + [c1])) > 0 else "black"  
    if DEBUG:
        print(f'RB: {guess} vs {c1.suit}')
    # logic
    if guess == "red":
        result = c1.suit in ("Hearts", "Diamonds")
    if guess == "black":
        result =  c1.suit in ("Spades", "Clubs")

    if LOGGING:
        log_step('rb', guess, result, sum(map(lambda c: 1 if c.suit in ("Hearts", "Diamonds") else -1, deck + [c1])))
    return result

def hilo(c1: Card, c2: Card) -> bool:
    # guessing algo
    guess = None
    if random() > 0.5:
        guess = "higher"
    else:
        guess = "lower"
    if SMART:
        guess = "higher" if sum(map(lambda c: 1 if c > c1 else -1, deck + [c2])) > 0 else "lower"

    if DEBUG:
        print(f'HILO: {guess} vs {c1.value} , {c2.value}')
    # logic
    if guess == "higher":
        result = c1.value < c2.value
    elif guess == "lower":
        result = c1.value > c2.value

    if LOGGING:
        log_step('hilo', guess, result, sum(map(lambda c: 1 if c > c1 else -1, deck + [c2])))
    return result

def inout(c1: Card, c2: Card, c3: Card) -> bool:
    guess = None
    if random() > 0.5:
        guess = "inside"
    else:
        guess = "outside"

    # logic
    bounds = sorted([c1,c2])

    if SMART:
        guess = "inside" if sum(map(lambda c: 1 if c > bounds[0] and c < bounds[1] else -1, deck + [c3])) > 0 else "outside"
    
    if DEBUG:
        print(f'INOUT: {guess} vs {bounds}, {c3}')
    if guess == "inside":
        result = c3 > bounds[0] and c3 < bounds[1]
    elif guess == "outside":
        result = c3 < bounds[0] or c3 > bounds[1]
    
    if LOGGING:
        log_step('inout', guess, result, sum(map(lambda c: 1 if c > bounds[0] and c < bounds[1] else -1, deck + [c3])))
    return result

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

    d = {"Clubs": 0, "Spades": 0, "Hearts": 0, "Diamonds": 0}
    for c in deck:
        d[c.suit] += 1

    if SMART:
        guess = sorted(d.items(), key=lambda x: -x[1])[0][0]
    if DEBUG:
        print(f'SUIT: {guess} vs {c4.suit}')
    result = guess == c4.suit

    if LOGGING:
        log_step('suit', guess, result, ':'.join(f'{d[k]}' for k in sorted(d)))
    return result

def log_step(step_name, guess, result, deck_status):
    LOGFILE.write(f'{SMART}, {step_name}, {deck_status}, {guess}, {result}\n')

def graphit(scores):
    plt.hist(scores, bins=20, range=(0,100))
    plt.title("Ride the Bus Distribution")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig('ridethebus_smart.png')

__main__()