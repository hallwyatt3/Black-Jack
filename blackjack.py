'''
A very simple BlackJack game. Written by Wyatt Hall. Thank you for coming out to the show tonight. I love all of you.
'''
print('Hello World')


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return (f'{self.rank} of {self.suit}')

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        return "this is the Deck class"

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        n = self.deck.pop()
        return n


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces            
    
    def what_card_value(self, card):
        return(values[card.rank])
        
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
                self.aces += 1
    
    def adjust_for_ace(self):
        if self.value > 21:
            if self.aces > 0:
                self.value -= 10
                self.aces -= 1
                
    def show_all_card(self, name):
        for i in self.cards:
            print(i)
        print(f'\nTotal value of {name} hand: {self.value}')
        
    def show_one(self):
        print(self.cards[0])
        print('*This card is flipped*')
        print('\n')


class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

# and now a list of the functions that will be used for the game

def take_bet(chips):
    
    bet = int(input('How much would you like to bet?  '))
    
    try:
        bet
    except:
        print('Sorry that is not an integer. Please try again.')
    else:
        if chips.total < bet:
            print('Sorry! You do not have enough chips!')
        else:
            chips.bet = bet
            print('Bet placed')
            return int(bet)

def hit(deck,hand):
    
    new_card = deck.deal()
    hand.add_card(new_card)
    if hand.value > 21:
        if hand.aces > 0:
            hand.value -= 10


def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    answer = input('Would you like to hit or stand? Type \'hit\' or \'stand\'\n')
    if answer == 'hit':
        print('\nYou chose to hit.\n')
        hit(deck, hand)
        hand.show_all_card(name = 'player')
        if hand.value > 21:
            pass
        else:     
            hit_or_stand(deck, hand)
    else:
        playing = False


def show_some(player,dealer):
    
    print('\nPlayer cards: \n')
    player.show_all_card(name = 'player')
    print('\nDealer cards: \n')
    dealer.show_one()
    
def show_all(player,dealer):
    
    player.show_all_card(name = 'player')
    dealer.show_all_card(name = 'dealer')


def player_busts(chips):
    print("Sorry, you busted!")
    chips.lose_bet()
    print(f'Account: $ {chips.total}')

def player_wins(chips):
    print('Congrats! You win!')
    chips.win_bet()
    print(f'Account: $ {chips.total}')
    

def dealer_busts(chips):
    print('Congrats! You win because the dealer busted!')
    chips.win_bet()
    print(f'Account: $ {chips.total}')
    
def dealer_wins(chips):
    print('Sorry, you lose!')
    chips.lose_bet()
    print(f'Account: $ {chips.total}')
    
def push():
    print('Tie!')


# and now for the final push, the actual game itself:

player_chips = Chips()

def run_game(): 
    global playing
    
    
    while True:
        playing = True
        # Print an opening statement
        print('Thanks for choosing to play Black Jack! Let\'s begin')

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        random.shuffle(deck.deck)
        hand_player = Hand()
        hand_computer = Hand()
        hand_player.add_card(deck.deal())
        hand_player.add_card(deck.deal())
        hand_computer.add_card(deck.deal())
        hand_computer.add_card(deck.deal())   

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_some(hand_player, hand_computer)

        while playing:  # recall this variable from our hit_or_stand function


                # Prompt for Player to Hit or Stand
            hit_or_stand(deck, hand_player)

                # Show cards (but keep one dealer card hidden)
            show_some(hand_player, hand_computer)

                # If player's hand exceeds 21, run player_busts() and break out of loop
            if hand_player.value > 21:
                player_busts(player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
            if hand_computer.value < 17:
                hit(deck, hand_computer)

            # Show all cards
            show_all(hand_player, hand_computer)
            # Run different winning scenarios
            if hand_computer.value > 21:
                dealer_busts(player_chips)
            elif hand_player.value >21:
                pass
            elif hand_player.value > hand_computer.value:
                player_wins(player_chips) 
            elif hand_player.value == hand_computer.value:
                push()
            else:
                dealer_wins(player_chips)

        # Inform Player of their chips total 
        print(f'Your total chips: {player_chips.total}')
        # Ask to play again
        play_again = input('\n\nWould you like to play again? Type Y or N')

        if play_again == 'Y':
            run_game()
        break
        
run_game()