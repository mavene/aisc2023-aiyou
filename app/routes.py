from flask import render_template, request
from app import application, sentic_bert
from app.models import Entity, Review

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', title='Review NLP Test Home')

@application.route('/about-us')
def about_us():
    return render_template('about_us.html', title='OOPS')

@application.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_terms = request.form.get("search_terms")
        # TODO: Modify so it retrieves model_id of relevant reviews and their attached sentiment
        result = sentic_bert.sentiment_analysis(search_terms)
    else:
        result = ""
    return render_template('search.html', title='Sentiments of Reviewers based on your search terms...', output=result)

# For testing purposes to check database entries
@application.route('/test_db', methods=['GET', 'POST'])
def test_db():
    entities = Entity.query.all()
    reviews = Review.query.all()
    return render_template('test_db.html', title='Testing testing 1 2 3',
        entities=entities, reviews=reviews)