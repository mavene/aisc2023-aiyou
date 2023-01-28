from flask import render_template, request
from app import application, engine, sentic_bert
from app.models import Entity, Review

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', title='Landing Page (WIP)')

@application.route('/about-us')
def about_us():
    return render_template('about_us.html', title='OOPS')

@application.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_terms = request.form.get("search_terms")
        result = engine.relevant_hits(search_terms)
        sentiment_analysis = sentic_bert.inference([entity for entity in result.keys()])
        get_started = ""
    else:
        result = ""
        sentiment_analysis = ""
        get_started = "yep"
    return render_template('search.html', title='Search Results', search_hit=result, sentiments=sentiment_analysis, status=get_started)

# For testing purposes to check database entries
@application.route('/test_db', methods=['GET', 'POST'])
def test_db():
    entities = Entity.query.all()
    reviews = Review.query.all()
    return render_template('test_db.html', title='Testing testing 1 2 3',
        entities=entities, reviews=reviews)

@application.route('/<company_name>/details', methods=['GET', 'POST'])
def details(company_name):
    if request.method == "POST":
        entity = request.form.get("entity_id")
        print(entity)
        redirect_entity = Entity.query.filter(Entity.id.like(entity)).first()
        redirect_sentiment = request.form.get("sentiments")
        print(redirect_entity)
        print(redirect_sentiment)
    else:
        redirect_entity = ""
        redirect_sentiment = ""
    return render_template('details.html', entity=redirect_entity, sentiment=redirect_sentiment)