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
    # rev = random.randint(-1, 1)  # is card reversed? zero (false) or 1 (true)
    rev = random.randint(0, 1)
    drawn = (card, rev)  # tuple of card dictionary + 1 or zero for reversal
    return drawn

def get_deck():
    """Return a fresh copy of the deck"""
    return load_deck()

def get_love_reading(card_tuple, question_type):
    """Get love-specific reading based on card and question type"""
    card, rev = card_tuple
    
     # Map question types to interpretations for Major Arcana vs Minor Arcana
    love_readings_major = {
        'future': {
            'upright': 'Nel futuro della tua relazione si prospetta un periodo di {message}. {desc}',
            'reversed': '{rdesc}'
        },
        'feelings': {
            'upright': 'I sentimenti attuali mostrano {desc}',
            'reversed': 'C\'è qualche difficoltà: {rdesc}'
        },
        'return': {
            'upright': 'Per quanto riguarda un possibile ritorno: {desc}',
            'reversed': 'Riguardo al ritorno, attenzione: {rdesc}'
        },
        'crisis': {
            'upright': 'La situazione attuale indica: {desc}',
            'reversed': 'In questo momento di crisi: {rdesc}'
        },
        'angels': {
            'upright': 'Gli Angeli del Cuore suggeriscono: {desc}',
            'reversed': 'Gli Angeli consigliano cautela: {rdesc}'
        },
        'advice': {
            'upright': 'Il consiglio delle carte: {desc}',
            'reversed': 'Un avvertimento importante: {rdesc}'
        },
        'newmeet': {
            'upright': 'Per i nuovi incontri: {desc}',
            'reversed': 'Riguardo ai nuovi incontri, attenzione: {rdesc}'
        }
    }

    love_readings_minor = {
        'future': {
            'upright': '{desc}',
            'reversed': '{rdesc}'
        },
        'feelings': {
            'upright': 'I sentimenti attuali mostrano: {desc}',
            'reversed': 'C\'è qualche difficoltà: {rdesc}'
        },
        'return': {
            'upright': 'Per quanto riguarda un possibile ritorno: {desc}',
            'reversed': 'Riguardo al ritorno: {rdesc}'
        },
        'crisis': {
            'upright': 'La situazione attuale indica: {desc}',
            'reversed': 'In questo momento di crisi: {rdesc}'
        },
        'angels': {
            'upright': 'Il messaggio spirituale indica: {desc}',
            'reversed': 'Un avvertimento spirituale: {rdesc}'
        },
        'advice': {
            'upright': 'Il consiglio delle carte: {desc}',
            'reversed': 'Un avvertimento importante: {rdesc}'
        },
        'newmeet': {
            'upright': 'Per i nuovi incontri: {desc}',
            'reversed': 'Riguardo ai nuovi incontri: {rdesc}'
        }
    }
    
    # Choose template based on card type
    readings = love_readings_major if card['cardtype'] == 'major' else love_readings_minor
    reading_template = readings[question_type]['reversed' if rev else 'upright']
    
    # Format the template with the card's values
    # For Major Arcana, include message; for Minor Arcana, just use desc/rdesc
    if card['cardtype'] == 'major':
        reading = reading_template.format(
            message=card['message'],
            desc=card['desc'],
            rdesc=card['rdesc']
        )
    else:
        reading = reading_template.format(
            desc=card['desc'],
            rdesc=card['rdesc']
        )
    
    return reading 

# Tarocchi Si o No
def get_yesno_reading(card_tuple):
    """Get yes/no response based on card and orientation"""
    card, rev = card_tuple
    
    # Define naturally positive cards (you can adjust this list)
    positive_cards = [
        "Il Mago", "L'Imperatrice", "Il Papa", "Il Carro", 
        "La Ruota della Fortuna", "La Forza", "Il Sole", 
        "Il Mondo"
    ]
    
    # Define naturally negative cards (you can adjust this list)
    negative_cards = [
        "La Torre", "Il Diavolo", "La Morte", "La Luna"
    ]
    
    # Basic algorithm:
    # 1. If card is naturally positive:
    #    - Upright = Yes
    #    - Reversed = No
    # 2. If card is naturally negative:
    #    - Upright = No
    #    - Reversed = Yes
    # 3. If card is neutral:
    #    - Upright = Yes
    #    - Reversed = No
    
    if card['name'] in positive_cards:
        response = "NO" if rev else "SI"
    elif card['name'] in negative_cards:
        response = "SI" if rev else "NO"
    else:
        response = "NO" if rev else "SI"
        
    return response


 
       