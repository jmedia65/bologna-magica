# for the app routes
from webapp import app 
from flask import render_template, jsonify

# for the cards 
from webapp import cards
# and the shuffle
# import random

# home page
@app.route('/')
def index():
	return render_template("index.html")

# tarot study
@app.route('/tarot-study', strict_slashes=False)
def all_cards():
	return render_template("tarot_study.html")

# reading list
@app.route('/reading-list', strict_slashes=False)
def reading_list():
	return render_template("reading_list.html")


# One Card In-Between Route
@app.route('/one-card-tarot', strict_slashes=False)
def one_card_tarot():
    return render_template('one_card_tarot.html', 
                         title="Estrai Una Carta dei Tarocchi")

# Get One Card
@app.route('/one-card', strict_slashes=False)
def one_card():
	my_deck = cards.get_deck()
	my_card = cards.get_card(my_deck)
	if my_card[0]['cardtype'] == "major" :
		return render_template("one_card.html",
								name = my_card[0]['name'],
								title = my_card[0]['name'],
								rev = my_card[1],
								meaning = my_card[0]['desc'],
								message = my_card[0]['message'],
								reversed_meaning = my_card[0]['rdesc'],
								image = my_card[0]['image'],
								url = my_card[0]['url'],
								cardtype = my_card[0]['cardtype'])
	else:
		return render_template("one_card.html",
								name = my_card[0]['name'],
								title = my_card[0]['name'],
								rev = my_card[1],
								meaning = my_card[0]['desc'],
								reversed_meaning = my_card[0]['rdesc'],
								image = my_card[0]['image'],
								url = my_card[0]['url'],
								cardtype = my_card[0]['cardtype'])

# Three Cards In-Between Route
@app.route('/three-cards-tarot', strict_slashes=False)
def three_cards_tarot():
    return render_template('three_cards_tarot.html', 
                         title="Lettura dei Tarocchi: Passato, Presente e Futuro")

# get three cards
@app.route('/three-cards', strict_slashes=False)
def more_cards():
	my_deck = cards.get_deck()
	hand = []
	num = 1
	while num < 4:
		my_card = cards.get_card(my_deck)
		hand.append(my_card)
		num +=1
	return render_template("three_cards.html", hand = hand, title="Three card spread")


# get specific card
@app.route('/one-card/<card_url>')
def specific_card(card_url):
	my_deck = cards.get_deck()
	my_card = list(filter(lambda my_card: my_card['url'] == card_url, my_deck))[0]
	if my_card['sequence'] > 1 :
		previous_card_url = '/one-card/' + list(filter(lambda previous_card: previous_card['sequence'] == (my_card['sequence'] -1), my_deck))[0]['url']
	else :
		previous_card_url = '/tarot-study'
	if my_card['sequence'] < 78 :
		next_card_url = '/one-card/' + list(filter(lambda next_card: next_card['sequence'] == (my_card['sequence'] +1), my_deck))[0]['url']
	else :
		next_card_url = '/tarot-study'
	if my_card['cardtype'] == "major" :
		return render_template("specific_card.html",
								name = my_card['name'],
								title = my_card['name'],
								meaning = my_card['desc'],
								message = my_card['message'],
								reversed_meaning = my_card['rdesc'],
								golden_dawn = my_card['golden_dawn'],
								image = my_card['image'],
							    previous = previous_card_url,
							    next = next_card_url,
							    sequence = my_card['sequence'],
							    cardtype = my_card['cardtype'])
	else: 
		return render_template("specific_card.html",
								name = my_card['name'],
								title = my_card['name'],
								meaning = my_card['desc'],
								reversed_meaning = my_card['rdesc'],
								golden_dawn = my_card['golden_dawn'],
								image = my_card['image'],
							    previous = previous_card_url,
							    next = next_card_url,
							    sequence = my_card['sequence'],
							    cardtype = my_card['cardtype'])

# Tarocchi dell'Amore
LOVE_QUESTIONS = [
    {
        'id': 'future',
        'title': 'IL FUTURO DELLA RELAZIONE',
        'subtitle': 'Come si evolverà la relazione?'
    },
    {
        'id': 'feelings',
        'title': "M'AMA ... NON M'AMA",
        'subtitle': 'I sentimenti del partner'
    },
    {
        'id': 'return',
        'title': "TORNERA' DA ME?",
        'subtitle': "Ritorno d'amore"
    },
    {
        'id': 'crisis',
        'title': 'RELAZIONE IN CRISI',
        'subtitle': 'E\' proprio finita?'
    },
    {
        'id': 'angels',
        'title': 'GLI ANGELI DEL CUORE',
        'subtitle': 'Troverò l\'amore? E\' la persona giusta per me?'
    },
    {
        'id': 'advice',
        'title': "CONSIGLI D'AMORE",
        'subtitle': 'Come devo comportarmi con il mio partner per migliorare il nostro rapporto'
    },
    {
        'id': 'newmeet',
        'title': 'NUOVI INCONTRI E CONOSCENZE',
        'subtitle': 'Come andrà a finire?'
    }
]

@app.route('/tarocchi-amore', strict_slashes=False)
def love_tarot():
    return render_template('love_tarot.html', 
                         questions=LOVE_QUESTIONS,
                         title="Tarocchi dell'Amore")

@app.route('/tarocchi-amore/<question_id>', strict_slashes=False)
def love_reading(question_id):
    my_deck = cards.get_deck()
    drawn_card = cards.get_card(my_deck)
    reading = cards.get_love_reading(drawn_card, question_id)
    question = next((q for q in LOVE_QUESTIONS if q['id'] == question_id), None)
    
    return render_template('love_card.html',
                         card=drawn_card[0],
                         reversed=drawn_card[1],
                         reading=reading,
                         question=question,
                         title=question['title'])
    
# Tarocchi Si o No
@app.route('/tarocchi-si-no', strict_slashes=False)
def yesno_tarot():
    return render_template('yesno_tarot.html', 
                         title="Tarocchi Si o No")

@app.route('/tarocchi-si-no/risposta', strict_slashes=False)
def yesno_reading():
    my_deck = cards.get_deck()
    drawn_card = cards.get_card(my_deck)
    response = cards.get_yesno_reading(drawn_card)
    
    return render_template('yesno_card.html',
                         card=drawn_card[0],
                         reversed=drawn_card[1],
                         response=response,
                         title="Il Responso dei Tarocchi")
    
# Bologna Magica routes
@app.route('/bologna-magica')
def bologna_magica():
    return render_template('bologna-magica/index.html')

@app.route('/bologna-magica/percorsi/<path>')
def bologna_percorsi(path):
    return render_template(f'bologna-magica/percorsi/{path}.html')

@app.route('/bologna-magica/<path>')
def bologna_page(path):
    return render_template(f'bologna-magica/{path}.html')    