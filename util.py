from card import suits


def get_valid_number(min_num, max_num, message, indent=0):
    valid_nums = set()
    i = min_num
    while i <= max_num:
        valid_nums.add(i)
        i += 1
    
    tab_string = '\t' * indent
    while True:
        try:
            choice = int(raw_input(message))
            if choice not in valid_nums:
                message = tab_string + "That wasn't a valid option number. Try again: "
            else:
                return choice
        except ValueError:
            message = tab_string + "That wasn't a number. Try again: "
    return 0

def get_player_with_name(game_state, player_name):
    for i in xrange(len(game_state.players)):
        if game_state.players[i].name == player_name:
            return game_state.players[i]
    return None

def index_of_player_with_name(game_state, player_name):
    for i in xrange(len(game_state.players)):
        if game_state.players[i].name == player_name:
            return i
    return -1

def get_legal_cards(cards, suit_led):
    if not suit_led:
        return cards
    suited = cards_by_suit(cards)
    if suited[suit_led]:
        return suited[suit_led]
    # If no cards of the led suit, all plays are legal
    return get_card_list(suited)

def strongest_card(cards, suit_led, trump):
    if not cards:
        return None
    trumps = [card for card in cards if card.suit == trump]
    if trumps:
        return max(trumps)
    follows = [card for card in cards if card.suit == suit_led]
    if follows:
        return max(follows)
    return max(cards)

def weakest_card(cards, trump):
    nontrump = [card for card in cards if card.suit != trump]
    if nontrump:
        return min(nontrump)
    return min(cards)

def strongest_legal_play(cards, suit_led, trump):
    if not suit_led:
        # Can play any suit, so choose strongest card
        return max(cards)

    legal_cards = get_legal_cards(cards, suit_led)
    suited = cards_by_suit(legal_cards)
    if suited[trump]:
        return max(suited[trump])
    elif suited[suit_led]:
        return max(suited[suit_led])
    else:
        # If can't play trump or the suit led, the strongest play is to choose
        # weakest remaining card and preserve stronger ones
        return min(get_card_list(suited))

def get_card_list(suited_map):
    return [card for suited_cards in suited_map.values() for card in suited_cards]
    
def cards_by_suit(cards):
    suited_cards = {}
    for suit in suits:
        suited_cards[suit] = [card for card in cards if card.suit == suit]
        suited_cards[suit].sort()
    return suited_cards

def print_hands(game_state):
    for player in game_state.players:
        print '----- %s Hand -----' % player.name
        print_cards(player.cards)

def print_cards(cards, num_tabs=0):
    split_cards = cards_by_suit(cards)
    tab_str = '\t' * num_tabs
    for suit in suits:
        suited_cards = split_cards[suit]
        if suited_cards:
            print (tab_str + suit + ':').ljust(12) + ' '.join([card.rank for card in suited_cards])
        else:
            print (tab_str + suit + ':').ljust(12) + '-'
    print
