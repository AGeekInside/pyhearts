import util
import random

class RandomPlayer:
    hand = []
    state = None
    name = 'Random'

    def _highest_value_card(self,cards):
        highest_value = 0
        highest_card = ""
        
        for card in cards:
            if util.card_value(card) > highest_value:
                highest_value = util.card_value(card)
                highest_card = card
                
        return highest_card

    
    def _lowest_value_card(self,cards):
        lowest_value = 200
        lowest_card = ""
        
        for card in cards:
            if util.card_value(card) < lowest_value:
                lowest_value = util.card_value(card)
                lowest_card = card
                
        return lowest_card

    
    def has_suit(self,suit):
        '''returns true if suit is in the hand'''
        for card in self.hand:
            if suit == util.card_suit(card):
                return True
        return False                

    def only_hearts(self):
        for card in self.hand:
            if not util.card_suit(card) == 'heart':
                return False
        
        return True

    def random_non_heart(self):
        '''returns a card from the hand that is not a heart'''
        temp_cards = []
        for card in self.hand:
            if not util.card_suit(card) == 'hearts':
                temp_cards.append(card)
        
        return random.choice(temp_cards)
        
    def random_card(self,suit=None,none_of=None):
        '''returns a random card (of the suit, if specified)'''
        debug_level = 100
        util.debug_out('none_of = '+str(none_of),debug_level)        
        work_card = None

        if none_of:
            work_cards = [i for i in self.hand if not i.startswith(none_of)]
            if len(work_cards) > 1:
                work_card = random.choice(work_cards)
            else:
                work_card = random.choice(self.hand)
            
        if suit:
            util.debug_out('suit - '+suit,debug_level)
            if self.has_suit(suit):
                util.debug_out('had suit',debug_level)
                suit_cards = [i for i in self.hand if i.startswith(suit)]
                util.debug_out('suit_cards = '+str(suit_cards),debug_level)
                work_card = random.choice(suit_cards)
            else:
                util.debug_out('did have suit',debug_level)
                work_card = random.choice(self.hand)                
        else:
            util.debug_out('no suit set',debug_level)
            work_card = random.choice(self.hand)
            
        util.debug_out('picked card '+work_card,debug_level)
        self.hand.remove(work_card)
        return work_card
        
    def logic(self,game_state):
        '''logic used by a player to discard a random card.'''
        debug_level = 100
        util.debug_out( 'hand '+str(self.hand), debug_level)
        
        work_card = None
        self.state = game_state
        
        if 'clubs_2' in self.hand:
            self.hand.remove('clubs_2')
            return 'clubs_2'
        
        hearts_broken = game_state.hearts_broken
        led_suit = game_state.led_suit
        
        util.debug_out( 'hearts_broken '+str(hearts_broken), debug_level)
#         util.debug_out( 'led_suit '+str(led_suit), debug_level)
        
        if led_suit:
            if self.has_suit(led_suit):
                util.debug_out('had '+led_suit,debug_level)
                work_card = self.random_card(led_suit)
            else:
                util.debug_out('did not have '+led_suit,debug_level)
                if hearts_broken:
                    work_card = random.choice(self.hand)
                else:
                    # hearts not broken
                    if self.only_hearts():
                        work_card = random.choice(self.hand)
                    else:
                        work_card = self.random_card(none_of='hearts')
        else:
            if hearts_broken:
                util.debug_out('no led_suit',debug_level)
                work_card = self.random_card()
            else:
                util.debug_out('no led_suit, no hearts working',debug_level)
                if self.only_hearts():
                    work_card = random.choice(self.hand)
                else:
                    work_card = self.random_card(none_of='hearts')
                
        return work_card


class LowestPlayer(RandomPlayer):
    '''a player who simply always picks the lowest value possible.'''

    def __init__(self):
        self.name = 'Lowest'
    
    def choose_card(self,cards):
        return self._lowest_value_card(cards)

    def determine_valid_cards(self,suit=None,none_of=None):
        '''returns a the lowest card (of the suit, if specified)'''
        debug_level = 100
        util.debug_out('none_of = '+str(none_of),debug_level)        
        work_card = None

        if none_of:
            work_cards = [i for i in self.hand if not i.startswith(none_of)]
            if len(work_cards) > 1:
                work_card = self.choose_card(work_cards)
            else:
                work_card = self.choose_card(self.hand)
            
        if suit:
            util.debug_out('suit - '+suit,debug_level)
            if self.has_suit(suit):
                util.debug_out('had suit',debug_level)
                suit_cards = [i for i in self.hand if i.startswith(suit)]
                util.debug_out('suit_cards = '+str(suit_cards),debug_level)
                work_card = self.choose_card(suit_cards)
            else:
                util.debug_out('did have suit',debug_level)
                work_card = self.choose_card(self.hand)                
        else:
            util.debug_out('no suit set',debug_level)
            work_card = self.choose_card(self.hand)
            
        util.debug_out('picked card '+work_card,debug_level)
        self.hand.remove(work_card)
        return work_card
        
    def logic(self,game_state):
        '''logic used to always pick the lowest value card'''
        debug_level = 100
        
        work_card = None
        
        if 'clubs_2' in self.hand:
            self.hand.remove('clubs_2')
            return 'clubs_2'
        
        hearts_broken = game_state.hearts_broken
        led_suit = game_state.led_suit
        
        util.debug_out( 'hearts_broken '+str(hearts_broken), debug_level)
#         util.debug_out( 'led_suit '+str(led_suit), debug_level)
        
        if led_suit:
            if self.has_suit(led_suit):
                util.debug_out('had '+led_suit,debug_level)
                work_card = self.determine_valid_cards(led_suit)
            else:
                util.debug_out('did not have '+led_suit,debug_level)
                work_card = self.determine_valid_cards()
        else:
            if hearts_broken:
                util.debug_out('no led_suit',debug_level)
                work_card = self.determine_valid_cards()
            else:
                util.debug_out('no led_suit, no hearts working',debug_level)
                work_card = self.determine_valid_cards(none_of='hearts')
                
        return work_card

class HighestPlayer(LowestPlayer):
    
    def __init__(self):
        super(self)
        self.name = 'Highest'

    def choose_card(self,cards):
        return self._highest_value_card(cards)
        
    
class HybridPlayer(HighestPlayer):

    def __init__(self):
        super(self)
        self.name = 'Hybrid'

    def choose_card(self,cards):
        if len(self.hand) > 1:
            return self._highest_value_card(cards)
        else:
            return self._lowest_value_card(cards)
