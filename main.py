import random
import pathlib

card_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11
    }

class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.value = card_values[rank]
        self.suit = suit
    def __str__(self): 
        return f"{self.rank} of {self.suit}"

class Deck():
    def get_cards(self): # get deck from txt file
        self.cards = []
        file = open(pathlib.Path("") / "deck.txt")
        for line in file: # add each line to deck as a card
            try:
                rank = line.split(" of ")[0].strip()
                suit = line.split(" of ")[1].strip()
                self.cards.append(Card(rank, suit))
            except: raise Exception("Invalid deck data") # raise an exception if there is an error
        random.shuffle(self.cards)
    def __init__(self):
        self.get_cards()
    def draw_top_card(self): # draw card and remove it from the deck
        return self.cards.pop(0)

class Hand():
    def __init__(self):
        self.cards = []
    def __str__(self):
        card_strings = []
        for card in self.cards:
            card_strings.append(str(card))
        return ", ".join(card_strings)
    
    def show_first(self): # used when the dealer's second card is face down
        return self.cards[0]
    def add_card(self, card):
        self.cards.append(card)

    def total_value(self):
        # count total points of all cards in hand
        total = 0
        ace_count = 0
        for card in self.cards:
            total += card.value
            if card.value == 11: ace_count += 1

        # aces can be either 1 or 11, which we need to account for if the total would otherwise be more than 21
        # if there are still aces left and there's still too many points, make one ace 1 instead of 11
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
    
        return total

def main():
    print("Welcome to Blackjack!\n")

    # basic game loop
    deck = Deck()
    dealer_hand = Hand()
    hand = Hand()

    # two cards for both parties
    for i in range(2): hand.add_card(deck.draw_top_card())
    for i in range(2): dealer_hand.add_card(deck.draw_top_card())

    # show drawn cards
    print(f"Dealer's hand: {dealer_hand.show_first()}")
    print(f"Your hand: {hand}")

    # player turn
    while True:
        print()
        decision = input("Hit or stand? (h/s) ")
        if decision == "h":
            if deck.cards == []: deck.get_cards() # if ran out of cards, restock
            hand.add_card(deck.draw_top_card())
            print(f"Your hand: {hand}")
            if hand.total_value() > 21: # busting loses you the game instantly
                print("Bust! You lost!")
                quit()
        elif decision == "s": break
        else: print("Invalid input, type h or s")
    print()
    
    # dealer reveals second card
    print(f"Dealer hand: {dealer_hand}")

    # dealer draws new cards until their value is over 16
    while dealer_hand.total_value() <= 16:
        if deck.cards == []: deck.get_cards() # if ran out of cards, restock
        print(f"Dealer draws a {deck.cards[0]}.")
        dealer_hand.add_card(deck.draw_top_card())

    # print final hand scores
    print()
    print(f"Dealer's hand value: {dealer_hand.total_value()}")
    print(f"Your hand value: {hand.total_value()}")

    # calculate who wins
    if dealer_hand.total_value() > 21: # dealer bust
        print("Dealer busts! You win!")
    elif dealer_hand.total_value() < hand.total_value(): # player win
        print("You have a better hand than the dealer! You win!")
    elif dealer_hand.total_value() == hand.total_value(): # tie
        print("Tie!")
    else: # any other scenario is a loss
        print("You lost!")

    quit()

if __name__ == "__main__":
    main()