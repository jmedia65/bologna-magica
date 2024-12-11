import random
import json
import os

def load_deck():
    """Load the deck data from JSON file"""
    base_path = os.path.dirname(os.path.dirname(__file__)) # go up one level from /webapp
    json_path = os.path.join(base_path, "data" "/tarot_cards.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def shuffle_deck(deck):
    """Shuffle the deck"""
    random.shuffle(deck)

def get_card(deck):
    """Pick a card from the deck"""
    num = random.randint(0, len(deck) - 1)  # the minus 1 fixes the zero indexed array out-of-range error
    card = deck[num]
    del (deck[num])  # so we don't get the same card twice if we're calling this multiple times for the same hand
    rev = random.randint(-1, 1)  # is card reversed? zero (false) or 1 (true)
    drawn = (card, rev)  # tuple of card dictionary + 1 or zero for reversal
    return drawn

def get_deck():
    """Return a fresh copy of the deck"""
    return load_deck()