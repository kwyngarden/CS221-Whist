from generate_hands import HandGenerator

import util
import random


def monte_carlo_utilities(game_state, player, max_simulations=2000):
    legal_cards = util.get_legal_cards(player.cards, game_state.trick.suit_led)
    utilities = {card: 0.0 for card in legal_cards}
    simulations_per_card = max_simulations / len(legal_cards)
    hand_generator = HandGenerator(max_hands=simulations_per_card)
    hand_assignments = hand_generator.generate_hands(game_state, player)

    for card in legal_cards:
        for i in xrange(len(hand_assignments)):
            hands = {player_name : list(hand_assignments[i][player_name]) for player_name in hand_assignments[i]}
            utilities[card] += monte_carlo_simulate(game_state, player, card, hands)

    # Normalize to probabilities and return
    for card in legal_cards:
        utilities[card] = float(utilities[card]) / simulations_per_card
    return utilities

def monte_carlo_simulate(game_state, player, chosen_card, hands):
    utility = 0
    player_names = [p.name for p in game_state.players]
    # TODO: this is cheating
    # hands = {player.name: list(player.cards) for player in game_state.players}
    
    played = dict({card: game_state.trick.played[card].name for card in game_state.trick.played})
    played[chosen_card] = player.name
    if not hands[player.name]:
        print 'Got empty hand for chosen card %s' % chosen_card
    # print 'Player hand: %s; trying to remove %s' % (hands[player.name], chosen_card)
    hands[player.name].remove(chosen_card)
    suit_led = game_state.trick.suit_led or chosen_card.suit
    for player_name in game_state.trick.left_to_play:
        if player_name != player.name:
            card_to_play = random.choice(util.get_legal_cards(hands[player_name], suit_led))
            played[card_to_play] = player_name
            hands[player_name].remove(card_to_play)
    winning_card = util.strongest_card([card for card in played], suit_led, game_state.trump)
    winning_player = played[winning_card]
    if game_state.are_partners(player.name, winning_player):
        utility += 1
    else:
        utility -= 1
    first_to_play = util.index_of_player_with_name(game_state, winning_player)

    # TODO bugtest
    while hands[game_state.players[first_to_play].name]:
        first_player_name = game_state.players[first_to_play].name
        lead_card = random.choice(hands[first_player_name])
        played = {lead_card: first_player_name}
        hands[first_player_name].remove(lead_card)
        suit_led = lead_card.suit

        for player_name in player_names:
            if player_name != first_player_name:
                card_to_play = random.choice(util.get_legal_cards(hands[player_name], suit_led))
                played[card_to_play] = player_name
                hands[player_name].remove(card_to_play)
        
        winning_card = util.strongest_card([card for card in played], suit_led, game_state.trump)
        winning_player = played[winning_card]
        if game_state.are_partners(player.name, winning_player):
            utility += 1
        else:
            utility -= 1
        first_to_play = util.index_of_player_with_name(game_state, winning_player)

    return utility