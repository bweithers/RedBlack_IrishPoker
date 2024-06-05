from random import shuffle
from statistics import mean, stdev
BLACK = 1
RED = -1

deck = [RED]*26 + [BLACK]*26

def redblack():
    shuffle(deck)
    count, correct = 0,0
    for card in deck:
        guess = RED if count >= 0 else BLACK
        correct += 1 if guess == card else 0
        # print(f'count: {count}, card: {card}, guess: {guess}', end=' ; ')
        count += card
    return correct



out = [redblack() for _ in range(1000000)]

import matplotlib.pyplot as plt

plt.hist(out, bins=21, range=(20,40))
plt.title("Red/Black Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")


mean_value = mean(out)
std_dev_value = stdev(out)

# Add text annotations
plt.text(mean_value, plt.ylim()[1]*0.9, f'Mean: {mean_value:.2f}', color='r', ha='center')
plt.text(mean_value + std_dev_value, plt.ylim()[1]*0.7, f'1 Sigma Hi: {mean_value + std_dev_value:.2f}', color='b', ha='left')
plt.text(mean_value - std_dev_value, plt.ylim()[1]*0.6, f'1 Sigma Lo: {mean_value - std_dev_value:.2f}', color='b', ha='right')




plt.axvline(mean_value, color='r', linestyle='dashed', linewidth=1)
plt.axvline(mean_value + std_dev_value, color='b', linestyle='dashed', linewidth=1)
plt.axvline(mean_value - std_dev_value, color='b', linestyle='dashed', linewidth=1)


# plt.show()
plt.savefig('redblack.png')