from flask import render_template, request, redirect, url_for
from app import application, engine, sentic_bert, find_relevant, gen_cloud
from app.models import Entity, Review

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/about-us')
def about_us():
    return render_template('about_us.html')

@application.route('/get_started')
def get_started():
    return render_template('get_started.html')

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
    print(request.form)
    if 'new-search' in request.form:
        return redirect(url_for('search'), code=307)
    elif request.method == 'POST':
        detail = request.form.get("details").strip("[]")
        redirect_sentiment = [int(elem) for elem in detail.split(",")]
        redirect_entity = Entity.query.filter(Entity.name.like(company_name)).first()
        all_reviews = find_relevant.find_reviews(redirect_entity)
        text = [review.content for review_list in all_reviews.values() for review in review_list ]
        gen_cloud.generate(" ".join(text))
    else:
        redirect_entity = ""
        redirect_sentiment = ""
        all_reviews = ""
    return render_template('details.html', entity=redirect_entity, sentiment=redirect_sentiment, reviews=all_reviews)

@application.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')