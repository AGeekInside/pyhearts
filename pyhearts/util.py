import json

class mem:
    debug_mode = True;
    debug_level = 10;

def hand_points(work_hand):
    '''returns the point value of a given hand'''
    debug_level = 1

    work_points = 0

    for card in work_hand:
        work_points += card_point_value(card)

    return work_points


def find_holder(card,hands):
    '''returns the holder of a given cards'''
    holder = -1
    for player_num, hand in enumerate(hands):
        if card in hand:
            holder = player_num
    return holder


def find_starter(game_state):
    '''returns the player that has the two of clubs'''

    starter_player = find_holder('clubs_2',game_state.hands)
    if starter_player < 0:
        starter_player = find_holder('clubs_3',game_state.hands)
    if starter_player < 0:
        starter_player = find_holder('clubs_4',game_state.hands)

    return starter_player


def card_suit(card):
    return card.split('_')[0]


def card_value(card):
    return int(card.split('_')[1])


def card_point_value(card):
    '''returns the value of a given card.'''
    if card == 'spades_12':
        return 13
    if card_suit(card) == 'hearts':
        return 1
    if card == 'diamonds_11':
        return -10

    return 0


def check_moon(scores):
    nonMoonScore = False
    for score in scores:
        if score not in[26,0,16,-10]:
            return scores

    non_zero = 0
    for score in scores:
        if not score == 0:
            non_zero += 1

    if non_zero < 2:
        return scores

    for player, score in enumerate(scores):
#         print 'someone shot the moon!'
        if score > 0:
            scores[player] = 0
        else:
            if score == -10:
                scores[player] = 16
            else:
                scores[player] = 26

    return scores


def game_winner(scores):
    lowest_score = 200
    winner = -1

    for counter,score in enumerate(scores):
        if score < lowest_score:
            lowest_score = score
            winner = counter

    return winner


def debug_out(workStr,level):
#     caller_name = inspect.stack()[1][3]
#     caller_name = ''
    if(mem.debug_mode):
        if(level<mem.debug_level):
#             print '['+caller_name+'] - '+str(workStr)
            print str(workStr)


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

def return_game_info(state):

    state_str = state.json_str()

    print state_str

    out_str = ""

    winner = game_winner(state.scores)

    out_str += str(winner)+'\t'

    for score in state.scores:
        out_str += str(score)+'\t'
    out_str += '\n'
    return out_str


def hand_results(work_hand):
    '''returns the index of the player that won the hand'''
    debug_level = 100

    winning_player = 0
    debug_out('work_hand = '+str(work_hand),debug_level)

    lead_suit = card_suit(work_hand[0])
    lead_value = card_value(work_hand[0])

    debug_out('lead_suit = '+lead_suit,debug_level)
    debug_out('lead_value = '+str(lead_value),debug_level)

    for player, card in enumerate(work_hand[1:]):
        work_suit = card_suit(card)
        work_value = card_value(card)
        if work_suit == lead_suit:
            if work_value > lead_value:
                lead_value = work_value
                winning_player = player+1

    debug_out('winning_player = '+str(winning_player),debug_level)
    return winning_player


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


def win_percent(num_games, game_wins):
    '''returns the percentage of wins'''

    total_games = num_games

    win_percents = game_wins[:]

    for i in range(0,len(win_percents)):
        win_percents[i] = round((1.0*(game_wins[i]))/(total_games*1.0),2)

    return win_percents


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

