import random

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
    def show(self):
        print(self.rank, self.suit)

class Deck:
    def __init__(self):
        self.stack = self.construct() # constructs shuffled deck
        # self.size = len(self.stack)  # starts as full deck of cards
        # self.used_stack = []

    def construct(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['H', 'S', 'C', 'D']  # hearts, spades, clubs, diamonds
        stack = []
        for rank in ranks:
            for suit in suits:
                stack.append(Card(rank, suit))
        random.shuffle(stack)
        return stack

    def draw(self):
        # self.size -= 1 # removing card from deck
        return self.stack.pop(0)

class Dealer:
    def __init__(self):
        self.hand = []
        self.bust = False
    def deal(self, card):
        self.hand.append(card)
    def initial_show(self):
        self.hand[0].show() # only shows first card
    def show(self):
        for card in self.hand:
            card.show()

class Player(Dealer): # inherits the deal, show and sum methods
    def __init__(self, bet, funds):
        self.bet = bet
        self.funds = funds
        super().__init__()


class Table:
    def __init__(self):
        print("Welcome to Blackjack!")
        self.dealer = Dealer()
        self.deck = Deck()
        self.players = self.find_players()
        self.dealer_show = False

    # prompts user to input players, their funds and their bets
    def find_players(self):
        players = []
        more_players = True
        while (more_players):
            if input("Would you like to add a player? Y / N ").upper() == "Y":
                funds = int(input("How many funds do you have? "))
                bet = int(input("How much would you like to bet? "))
                bet, funds = get_valid_bet(bet, funds)
                players.append(Player(bet, funds))
            elif len(players) == 0:
                print("You need at least one player.")
            else: # we have at least one player and the user does not want anymore
                more_players = False

        print("Players and bets are set.\n")
        return players

    # displays bets and hands of each player
    def show(self):
        print("Current table dealings:")
        for i in range(len(self.players)):
            curr_player = self.players[i]
            print(f"Player {i + 1}, funds {curr_player.funds}, betting {curr_player.bet}")
            curr_player.show()
            if curr_player.bust:
                print("Busted!")
        print("Dealer")
        if self.dealer_show:
            self.dealer.show()
        else:
            self.dealer.initial_show()


    def deal(self):
        # first round of dealing
        # everyone is dealt 2 cards, one at a time
        # deals each player 2 cards
        for i in range(2):
            for person in self.players + [self.dealer]:
                person.deal(self.deck.draw())

        print("Initial cards have been dealt. \n")

    # NOTE: is there a way to combine dealer/player play to use the same functions?
    def players_play(self):
        print("\nCommencing hit/stay gameplay")
        # hit or stay
        # players go first, dealer goes last
        # if player hits, they recieve another card
        # if they stay, we move onto the next player
        # player can continue to hit until they are satified or until they bust (go over 21)
        for i in range(len(self.players)):
            print(f"Player {i + 1}:")
            curr_player = self.players[i]
            while bust_check(curr_player.hand) and input("Hit or Stay? H / S ").upper() == "H":
                curr_player.deal(self.deck.draw())
                curr_player.show()
            if not (bust_check(curr_player.hand)):
                curr_player.bust = True
                print("Bust!")

        self.dealer_show = True # dealer can now show all cards

    def dealer_play(self):
        print("Dealer:")
        while bust_check(self.dealer.hand) and best_sum(self.dealer.hand) < 17:
            self.dealer.deal(self.deck.draw())

        self.dealer.show()

        if not(bust_check(self.dealer.hand)):
            self.dealer.bust = True
            print("Bust!")

        print("Hit/stay gameplay complete\n")



    # fix me: find best sums for each non-busted players, and determine losses/ gains for each player
    def results(self):
        if self.dealer.bust: dealer_sum = 0
        else: dealer_sum = best_sum(self.dealer.hand)


        for i in range(len(self.players)):
            curr_player = self.players[i]
            curr_player_sum = best_sum(curr_player.hand)
            if not (curr_player.bust) and curr_player_sum > dealer_sum:
                curr_player.funds += curr_player.bet
                print(f"Player {i + 1}: wins {curr_player.bet}, new balance : {curr_player.funds}")
            elif curr_player_sum == dealer_sum:
                print(f"Player {i + 1}: no gains or losses, balance : {curr_player.funds}")
            else:
                curr_player.funds -= curr_player.bet
                print(f"Player {i + 1}: loses {curr_player.bet}, new balance : {curr_player.funds}")

    def clear(self):
        self.deck = Deck()
        for player in self.players: # clears hands, and resets bust state
            player.hand = []
            player.bust = False

        self.dealer.hand = []
        self.dealer.bust = False
        self.dealer_show = False

    def fund_checks(self):
        for i in range(len(self.players)):
            curr_player = self.players[i]
            if curr_player.funds < curr_player.bet:
                print(f"Player {i + 1} you no longer have enough funds for another game (bet : {curr_player.bet}, funds : {curr_player.funds}).")
                curr_player.bet, curr_player.funds = get_valid_bet(curr_player.bet, curr_player.funds)

    def update_bets(self):
        for i in range(len(self.players)):
            if len(self.players) == 1 or input(f"Player {i + 1} : new bet? Y / N ").upper() == "Y":
                curr_player = self.players[i]
                print(f"You are currently betting {curr_player.bet}. You have {curr_player.funds} funds.")
                bet = int(input("How much would you like to bet? "))
                bet, funds = get_valid_bet(bet, curr_player.funds)
                curr_player.bet = bet
                curr_player.funds = funds





def card_value(card):
    rankToVal = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
    return rankToVal[card.rank]

# returns true if player has not busted, otherwise false
def bust_check(hand):
    sum, ace_count = partial_sum(hand)
    if sum > 21 :
        return False
    if ace_count > 0:
        room = 21 - sum
        if ace_count > room: # having all aces set to 1
            return False
    return True

# determines hand sum excluding aces, as well as the quantity of aces in the hand
def partial_sum(hand):
    sum = 0
    ace_count = 0
    for card in hand:
        if card.rank != 'A':
            sum += card_value(card)
        else:
            ace_count += 1
    return sum, ace_count

# fix me : determines optimal sum when aces are in the hand
def best_ace_sum(sum, ace_count): # ouputs values can include 1,2,3,4 to 11,12,13,14
    if ace_count == 0: return 0
    if sum > 10 or (sum == 10 and ace_count > 1): # cannot have any 11s without busting
        return ace_count
    return 11 + ace_count - 1 # sum is less or eq to 10, and theres more than one ace

# returns optimal sum of hand
def best_sum(hand):
    non_ace_sum, ace_count = partial_sum(hand)
    ace_sum = best_ace_sum(non_ace_sum, ace_count)

    return non_ace_sum + ace_sum

def get_valid_bet(bet, funds):
    if funds == 0:
        funds = int(input("How many funds do you want to add? "))
    while bet > funds:
        print("Insufficient funds.")
        action = input("New bet? B   Add funds? F\n").upper()
        if action == "B":
            bet = int(input("How much would you like to bet? "))
        elif action == "F":
            funds += int(input("How many funds do you want to add? "))
        else:
            print("Invalid response")
    return bet, funds



# Improvements: add GUI


def play(game):
    game.deal()  # each person is dealt two cards
    game.show() # displays dealings before hit/stay play
    game.players_play() # player hit/stay gameplay
    game.dealer_play() # dealer hit/stay gameplay
    game.results() # displays results
    if input("Would you like to play again? Y / N ").upper() == "Y":
        game.clear()
        if input("Would any players like to place new bets? Y / N ").upper() == "Y":
            game.update_bets()
        else:
            game.fund_checks()
        play(game)
    else:
        print("Thanks for playing!")


game = Table()
play(game)















