class Deck:
    """object to hold the deck of cards"""

    suits = ["0", "1", "2", "3"]
    suit_names = ["spades", "hearts", "clubs", "diamonds"]


def makeDeck():
    # jack is 11, queen is 12, king is 13, Ace is 14
    deck = []
    for suit in "sdhc":
        for value in range(2, 15):
            deck.append(suit + str(value))
    return deck
