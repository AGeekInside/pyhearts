#!/usr/bin/env python

import ConfigParser
import random
import sys

import players
import util

import json

class mem:
    '''object to store program wide information.'''
    num_players = -1
    num_games = -1
    player_names = []
    players = []
    games = []
    debugLevel = 100
    debugMode = True
    

class GameState:
    '''used to store the state of games'''
    deck = []
    hands = []
    scores = []
    players = []
    played_tricks = []
    visible_cards = []
    hearts_broken = False
    led_suit = None

    def json_str(self):
        '''Returns a json str for the object.'''

        work_str = ''

        player_names = [player.name for player in self.players]

        work_str = json.dumps({'game' :[
                                       {'scores' : self.scores},
                                       {'players' : player_names}
                                     ]})

        return work_str


def _parse_config(config_filename):
    '''parses the configuration file given on the command line.'''
    config = ConfigParser.ConfigParser()
    
    config.read(config_filename)
    
    mem.num_games = int(config.get("game","num_games"))
    mem.num_players = int(config.get("game","num_players"))
    mem.player_types = config.get("game","player_types").split(" ")
    mem.player_file = config.get("game","player_file")
    mem.new_players = config.get("game","new_players")
    mem.game_outfile = open(config.get("game","game_outfile"),'w')
    mem.trick_outfile = open(config.get("game","trick_outfile"),'w')
    mem.seed = config.get("game","seed")


def create_player(player_type):
    '''create a player of the specified type'''
    debug_level = 1
    work_player = None
    
    util.debug_out( 'player_type '+player_type, debug_level)
    
    if player_type == 'random':
        work_player = players.RandomPlayer()
    else:
        if player_type == 'lowest':
            work_player = players.LowestPlayer()
        else:
            if player_type == 'highest':
                work_player = players.HighestPlayer()
            else:
                if player_type == 'hybrid':
                    work_player = players.HybridPlayer()
                else:
                    print player_type+' is not a valid player type.'
                    sys.exit(1)
    
    return work_player


def create_players(num_players,player_types,player_names):
    '''returns an array of new players of the specified type'''
    
    new_players = []
    
    for i in range(0,num_players):
        new_players.append(create_player(player_types[i]))
    
    return new_players    


def load_players(player_file):
    '''loads players that were stored into a json file'''
    
    return None


def deal_hand(deck, handSize=5):
    '''Deals out supplied deck to the hand array and returns it.'''
    hand = []
    for i in range(handSize):
        hand.append(deck.pop())
    return hand


def deal_cards(players,game_state):
    '''deals the cards to the players provided'''
    #jack is 11, queen is 12, king is 13, Ace is 14
    deck = []
    for suit in ['spades','hearts','diamonds','clubs']:
        for value in range(2,15):
            deck.append(suit+'_'+str(value))
            
    random.shuffle(deck)
    
    num_players = len(players)
    excess_cards = len(deck) % num_players
    hand_size = len(deck) / num_players
    
    hands = []
    
    for index in range(0,num_players):
        new_hand = deal_hand(deck,hand_size)
        hands.append(new_hand)
        players[index].hand = new_hand
    
    game_state.hands = hands 
    game_state.excess = deck


def play_tricks(players,game_state):
    '''plays out the trick for a given hand'''
    debug_level = 100
    
    starter_player = util.find_starter(game_state)
    util.debug_out( 'starter_player '+str(starter_player), debug_level+100)
    
    num_players = len(players)
    num_tricks = len(game_state.hands[0])
    
    util.debug_out('num_tricks '+str(num_tricks),debug_level+100)
    util.debug_out('num_players '+str(num_players),debug_level+100)
    
    trick_scores = [0]*len(players)

    game_state.players = players
    
    for trick in range(0,num_tricks):
        util.debug_out( '****** playing trick '+str(trick),debug_level+100)
        cards_played = []
        for player in range(0,num_players):
            current_player = (starter_player + player) % num_players
            util.debug_out( 'current_player '+str(current_player), debug_level)

            played_card = players[current_player].logic(game_state)
            util.debug_out( 'played_card '+str(played_card), debug_level)
            
            if util.card_suit(played_card) == 'hearts':
                game_state.hearts_broken = True
                
            cards_played.append(played_card)
            util.debug_out( str(sorted(players[current_player].hand)), debug_level+100)
            
            if not game_state.led_suit:
                game_state.led_suit = util.card_suit(played_card)
                
        util.debug_out('-==-=- after trick, starter_player = '+str(starter_player),debug_level)
        result = util.hand_results(cards_played)
        points = util.hand_points(cards_played)

        util.debug_out('cards_played = '+str(cards_played),debug_level)
        util.debug_out('result = '+str(result),debug_level)
        util.debug_out('points = '+str(points),debug_level)
        util.debug_out('starter_player = '+str(starter_player),debug_level)
        winning_player =  (int(starter_player) + int(result)) % num_players
        util.debug_out('winning_player = '+str(winning_player),debug_level)
        

        # TODO-- NEED TO ADD CHECK FOR SCORES
        trick_scores[winning_player] += points
        util.debug_out('trick_scores = '+str(trick_scores),debug_level)
        
        starter_player = winning_player
        util.debug_out( str(cards_played), debug_level)
        
#         hand_points = hand_value(cards_played)
        game_state.led_suit = None
    
#     if moon_shot(trick_scores):
    out_str = '\t'
    for score in trick_scores:
        out_str += str(score)+'\t'    
    mem.trick_outfile.write(out_str+'\n')

    trick_scores = util.check_moon(trick_scores)
    out_str = '\t'
    for score in trick_scores:
        out_str += str(score)+'\t'
    mem.trick_outfile.write(out_str+'\n')

    for i,score in enumerate(trick_scores):
        game_state.scores[i] += score

    util.debug_out('game_state.scores = '+str(game_state.scores),debug_level)
    
    mem.trick_outfile.write(str(util.return_game_info(game_state)))
    
    return game_state


def game_status(game_state):
    '''return if a given game is complete, based off game_state'''
    for score in game_state.scores:
        if score > 100:
            return True

    return False


def play_game(players):
    '''plays a game between the specified players and returns the results'''
    game_state = GameState()
    game_state.scores = [0] * len(players)
    game_done = False
    
    hand_count = 0
    
    while not game_done:
        mem.trick_outfile.write('hand = '+str(hand_count)+'\n')
        deal_cards(players,game_state)
        play_tricks(players,game_state)
        hand_count += 1
        game_done = game_status(game_state)

    return game_state


def win_percent(num_games, game_wins):
    '''returns the percentage of wins'''
    
    total_games = num_games
    
    win_percents = game_wins[:]

    for i in range(0,len(win_percents)):
        win_percents[i] = round((1.0*(game_wins[i]))/(total_games*1.0),2)

    return win_percents

def play_games(players,num_games):
    '''plays the given games an returns the results'''
    print 'Playing',num_games,'game(s) with',len(players),'players.'
    game_results = []
    
    mem.game_wins = [0] * len(players)
    
    for game_num in range(0,num_games):
        result = play_game(players)
        game_results.append(result)
        
#         print 'game['+str(game_num)+'] - '+str(result.scores)
        mem.trick_outfile.write('\nGame '+str(game_num)+'\n')
        mem.game_outfile.write(str(game_num)+'\t'+str(util.return_game_info(result)))
        mem.game_wins[util.game_winner(result.scores)] += 1
        if ((game_num+1) % 250) == 0:
            percent_wins = win_percent(game_num+1, mem.game_wins)
            print str(game_num)+'\t'+str(percent_wins)
    
#     print str(mem.game_wins)
    
#     return game_results


def main(argv):
    '''main funciton to run hearts games'''
    
    if len(argv)>0:
        _parse_config(argv[0])
    else:
        print 'No config file given.'
        sys.exit(0)
        
#     random.seed(mem.seed)
        
    if mem.new_players:
        players = create_players(int(mem.num_players),
                                 mem.player_types,
                                 mem.player_names)
    else:
        players = load_players(mem.player_file)
        
    play_games(players,mem.num_games)

if __name__ == "__main__":
    main(sys.argv[1:])  