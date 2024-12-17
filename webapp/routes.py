# for the app routes
from webapp import app 
from flask import render_template, Response
# from flask_sitemapper import Sitemapper

# for the cards 
from webapp import cards
from webapp import sitemapper

# Constant for Domain URL
DOMAIN = "https://bolognamagica.com"

# Constants for Bologna Magica paths
BOLOGNA_PERCORSI = ['tarocchi', 'esoterico', 'alchemico']
BOLOGNA_PAGES = ['bologna-tarocchi', 'storia-misteri']

# Home Page
@sitemapper.include(changefreq="weekly", priority=1.0)
@app.route('/')
def index():
	return render_template("index.html")

## BOLOGNA MAGICA SECTION ##########
# Bologna Magica Main Hub
@sitemapper.include(changefreq="weekly", priority=0.9)
@app.route('/bologna-magica')
def bologna_magica():
    return render_template('bologna-magica/index.html')

# Bologna e i Tarocchi + Storia & Misteri (2 paths)
@app.route('/bologna-magica/<path>')
def bologna_page(path):
    return render_template(f'bologna-magica/{path}.html')

# Bologna Magica Percorsi (3 paths: tarocchi, esoterico, alchemico)
@app.route('/bologna-magica/percorsi/<path>')
def bologna_percorsi(path):
    return render_template(f'bologna-magica/percorsi/{path}.html')

## ABOUT US SECTION
@sitemapper.include(changefreq="monthly", priority=0.7)
@app.route('/about')
def about():
    return render_template('utils/about.html')

## TAROCCHI SECTION ##########
# Tarocchi dell'Amore Questions
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

# Tarocchi dell'Amore Start
@sitemapper.include(changefreq="weekly", priority=0.9)
@app.route('/tarocchi-amore', strict_slashes=False)
def love_tarot():
    return render_template('tarocchi/love_tarot.html', 
                         questions=LOVE_QUESTIONS)

# Tarocchi dell'Amore Solution
@app.route('/tarocchi-amore/<question_id>', strict_slashes=False)
def love_reading(question_id):
    my_deck = cards.get_deck()
    drawn_card = cards.get_card(my_deck)
    reading = cards.get_love_reading(drawn_card, question_id)
    question = next((q for q in LOVE_QUESTIONS if q['id'] == question_id), None)
    
    return render_template('tarocchi/love_card.html',
                         card=drawn_card[0],
                         reversed=drawn_card[1],
                         reading=reading,
                         question=question,
                         title=question['title'])

# Tarocchi Si o No Start
@sitemapper.include(changefreq="weekly", priority=0.9)
@app.route('/tarocchi-si-no', strict_slashes=False)
def yesno_tarot():
    return render_template('tarocchi/yesno_tarot.html')

# Tarocchi Si o No Solution
@app.route('/tarocchi-si-no/risposta', strict_slashes=False)
def yesno_reading():
    my_deck = cards.get_deck()
    drawn_card = cards.get_card(my_deck)
    response = cards.get_yesno_reading(drawn_card)
    
    return render_template('tarocchi/yesno_card.html',
                         card=drawn_card[0],
                         reversed=drawn_card[1],
                         response=response)

# Tarocchi One Card Start
@sitemapper.include(changefreq="weekly", priority=0.8)
@app.route('/one-card-tarot', strict_slashes=False)
def one_card_tarot():
    return render_template('tarocchi/one_card_tarot.html')

# Tarocchi One Card Solution
@app.route('/one-card', strict_slashes=False)
def one_card():
	my_deck = cards.get_deck()
	my_card = cards.get_card(my_deck)
	if my_card[0]['cardtype'] == "major" :
		return render_template("tarocchi/one_card.html",
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
		return render_template("tarocchi/one_card.html",
								name = my_card[0]['name'],
								title = my_card[0]['name'],
								rev = my_card[1],
								meaning = my_card[0]['desc'],
								reversed_meaning = my_card[0]['rdesc'],
								image = my_card[0]['image'],
								url = my_card[0]['url'],
								cardtype = my_card[0]['cardtype'])

# Tarocchi Three Cards Start
@sitemapper.include(changefreq="weekly", priority=0.8)
@app.route('/three-cards-tarot', strict_slashes=False)
def three_cards_tarot():
    return render_template('tarocchi/three_cards_tarot.html')

# Tarocchi Three Cards Solution
@app.route('/three-cards', strict_slashes=False)
def more_cards():
	my_deck = cards.get_deck()
	hand = []
	num = 1
	while num < 4:
		my_card = cards.get_card(my_deck)
		hand.append(my_card)
		num +=1
	return render_template("tarocchi/three_cards.html", hand = hand)

# Tarocchi Specific Card
@app.route('/one-card/<card_url>')
def specific_card(card_url):
    my_deck = cards.get_deck()
    my_card = list(filter(lambda my_card: my_card['url'] == card_url, my_deck))[0]
    
    if my_card['sequence'] > 1:
        prev_card = list(filter(lambda prev: prev['sequence'] == (my_card['sequence'] - 1), my_deck))[0]
        previous_card_url = f'/one-card/{prev_card["url"]}'
    else:
        previous_card_url = '/studia-i-tarocchi'
    
    if my_card['sequence'] < 78:
        next_card = list(filter(lambda next_card: next_card['sequence'] == (my_card['sequence'] + 1), my_deck))[0]
        next_card_url = f'/one-card/{next_card["url"]}'
    else:
        next_card_url = '/studia-i-tarocchi'

    return render_template("tarocchi/specific_card.html",
                         name=my_card['name'],
                         title=my_card['name'],
                         meaning=my_card['desc'],
                         message=my_card.get('message', ''),  # use .get() to handle non-major cards
                         reversed_meaning=my_card['rdesc'],
                         golden_dawn=my_card['golden_dawn'],
                         image=my_card['image'],
                         previous=previous_card_url,
                         next=next_card_url,
                         sequence=my_card['sequence'],
                         cardtype=my_card['cardtype'])
   
# Studia i Tarocchi
@sitemapper.include(changefreq="monthly", priority=0.8)
@app.route('/studia-i-tarocchi', strict_slashes=False)
def all_cards():
	return render_template("tarocchi/tarot_study.html")

# Reading List
@sitemapper.include(changefreq="monthly", priority=0.6)
@app.route('/letture-consigliate', strict_slashes=False)
def reading_list():
	return render_template("tarocchi/reading_list.html")
    
# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('utils/errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('utils/errors/500.html'), 500

# # Error 500 test route
# @app.route('/test-500')
# def test_500():
#     # Deliberately raise an exception
#     raise Exception("Test 500 error page")

# Cookies and Privacy
@sitemapper.include(changefreq="monthly", priority=0.6)
@app.route('/privacy')
def privacy():
    return render_template('utils/privacy.html')

@sitemapper.include(changefreq="monthly", priority=0.6)
@app.route('/cookies')
def cookies():
    return render_template('utils/cookies.html')

# Sitemap
@app.route('/sitemap.xml')
def sitemap():
    base_sitemap = sitemapper.generate()
    
    # Convert the base sitemap to string if it's not already
    if isinstance(base_sitemap, Response):
        base_sitemap = base_sitemap.get_data(as_text=True)
    
    # Generate dynamic URLs
    dynamic_urls = []
    
    # Add Bologna Magica percorsi URLs
    for path in BOLOGNA_PERCORSI:
        url = f"{DOMAIN}/bologna-magica/percorsi/{path}"
        dynamic_urls.append(f"""
    <url>
        <loc>{url}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
    
    # Add Bologna Magica pages URLs
    for path in BOLOGNA_PAGES:
        url = f"{DOMAIN}/bologna-magica/{path}"
        dynamic_urls.append(f"""
    <url>
        <loc>{url}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
    
    # Add all card URLs
    my_deck = cards.get_deck()
    for card in my_deck:
        url = f"{DOMAIN}/one-card/{card['url']}"
        dynamic_urls.append(f"""
    <url>
        <loc>{url}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>""")
    
    # # Add all love question URLs
    # for question in LOVE_QUESTIONS:
    #     url = f"{DOMAIN}/tarocchi-amore/{question['id']}"
    #     dynamic_urls.append(f"""
    # <url>
    #     <loc>{url}</loc>
    #     <changefreq>monthly</changefreq>
    #     <priority>0.7</priority>
    # </url>""") 
        
    # Insert dynamic URLs before closing tag
    if '</urlset>' in base_sitemap:
        final_sitemap = base_sitemap.replace('</urlset>', 
                                           ''.join(dynamic_urls) + '\n</urlset>')
    else:
        # If base sitemap is empty or malformed, create complete sitemap
        final_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(dynamic_urls)}
</urlset>"""
    
    return Response(final_sitemap, mimetype='application/xml')