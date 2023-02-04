from app import db, application, webscrape
import pandas as pd
import os

# Parent
class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    address = db.Column(db.String(255))
    website = db.Column(db.String(128))
    contact = db.Column(db.String(64))
    picture_url = db.Column(db.String(255))
    review = db.relationship("Review", back_populates="entity")

# Child
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    date = db.Column(db.String(255))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    entity = db.relationship("Entity", back_populates="review")
    
with application.app_context():
    db.create_all()

    csv_files = ["entity_data.csv", "review_data.csv"]
    for csv in csv_files:
        filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + csv

        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            if csv == "entity_data.csv":
                new_entity = Entity(id=row['entity_id'], name=row['name'], description=row['description'], address=row['address'], website=row['website'], contact=row['contact'], picture_url=row['picture_url'])
                db.session.merge(new_entity)
            elif csv == "review_data.csv":
                new_review = Review(id=row['review_id'], content=row['review'], entity_id=row['entity_id'], author=row['author'], date=row['date'])
                db.session.merge(new_review)
                     
    try:
        db.session.commit()
    except Exception:
        pass