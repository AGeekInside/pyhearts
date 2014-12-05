#!/usr/bin/env python

import ConfigParser
import random
import sys

import players
import util

import json

class HeartsGamesInfo(object):
    '''Stores info on all hearts game played.'''
    num_players = -1
    num_games = -1
    player_names = []
    players = []
    games = []
    debugLevel = 100
    debugMode = True

    def _parse_config(self, config_filename):
        '''parses the configuration file given on the command line.'''
        config = ConfigParser.ConfigParser()

        config.read(config_filename)

        self.num_games = int(config.get("game", "num_games"))
        self.num_players = int(config.get("game", "num_players"))
        self.player_types = config.get("game", "player_types").split(" ")
        self.player_file = config.get("game", "player_file")
        self.new_players = config.get("game", "new_players")
        self.game_outfile = open(config.get("game", "game_outfile"),'w')
        self.trick_outfile = open(config.get("game", "trick_outfile"),'w')
        self.seed = config.get("game", "seed")

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

            work_str = json.dumps({'game' :[{'scores' : self.scores},
                                            {'players' : player_names}]})

            return work_str

    def play_tricks(players, game_state):
        '''plays out the trick for a given hand.  Returns the game state.'''
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
        self.trick_outfile.write(out_str+'\n')

        trick_scores = util.check_moon(trick_scores)
        out_str = '\t'
        for score in trick_scores:
            out_str += str(score)+'\t'
        self.trick_outfile.write(out_str+'\n')

        for i,score in enumerate(trick_scores):
            game_state.scores[i] += score

        util.debug_out('game_state.scores = '+str(game_state.scores),debug_level)

        self.trick_outfile.write(str(util.return_game_info(game_state)))

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
            self.trick_outfile.write('hand = '+str(hand_count)+'\n')
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

    def play_games(self, players, num_games):
        '''plays the given games an returns the results'''
        print 'Playing',num_games,'game(s) with',len(players),'players.'
        game_results = []

        self.game_wins = [0] * len(players)

        for game_num in range(0,num_games):
            result = play_game(players)
            game_results.append(result)

    #         print 'game['+str(game_num)+'] - '+str(result.scores)
            self.trick_outfile.write('\nGame '+str(game_num)+'\n')
            self.game_outfile.write(str(game_num)+'\t'+str(util.return_game_info(result)))
            self.game_wins[util.game_winner(result.scores)] += 1
            if ((game_num+1) % 250) == 0:
                percent_wins = win_percent(game_num+1, self.game_wins)
                print str(game_num)+'\t'+str(percent_wins)

    #     print str(self.game_wins)

    #     return game_results


def main(argv):
    '''main funciton to run hearts games'''

    games_info = HeartsGamesInfo()

    if len(argv)>0:
        games_info._parse_config(argv[0])
    else:
        print 'No config file given.'
        sys.exit(0)

#     random.seed(self.seed)


    # if self.new_players:
    #     players = create_players(int(self.num_players),
    #                              self.player_types,
    #                              self.player_names)
    # else:
    #     players = load_players(self.player_file)

    # play_games(players, self.num_games)

if __name__ == "__main__":
    main(sys.argv[1:])
