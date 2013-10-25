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
