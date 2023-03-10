from app import db, application, webscrape
import pandas as pd
import os
from unidecode import unidecode

# Parent
class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    category = db.Column(db.String(128))
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

review_idx = 1
entity_idx = 1
    
with application.app_context():
    db.create_all()

    results = webscrape.main()

    pictures = ["https://lh3.googleusercontent.com/p/AF1QipPIAJvO2Np7id53xElyDdGflAMeneeeGHsAMt7g=s1360-w1360-h1020",
                "https://lh3.googleusercontent.com/p/AF1QipPYDgdZsZqEWQxMIyKMoaMo66weVuMx2yvPa8Gq=s1360-w1360-h1020",
                "https://lh3.googleusercontent.com/p/AF1QipOEfMzmcx-OdyG9uYwVLm1xi1ufCMlkj3uLRDQm=s1360-w1360-h1020",
                "https://lh3.googleusercontent.com/p/AF1QipP7jtQ73xAj_zR7wPCGSEOvnnR32YdmRb1s9zz-=s680-w680-h510",
                "https://lh5.googleusercontent.com/p/AF1QipO3FQ_-wOJexLOretKSZ5W4dE4KqvL1MVCdgJ5i=w408-h272-k-no"]

    descriptions = ["Encik Tan marries local popular Chinese food with Halal ingredients and prepare them in Halal methods while still retaining the original flavour and taste of such food.",
                   "Buddy Hoagies has been operating our western grill restaurants since 2004 serving affordable and quality western cuisine for over 18 years.",
                   "Spize @ Bedok is the quintessential suburban supper place that defines late night dining. Nestled in the heartlands of the east in what is commonly known as Simpang Bedok , its ideally located to satisfy your midnight cravings!",
                   "Nestled in a charming shophouse along the trendy Tanjong Katong precinct, The Tipsy Cow stands out with its white neon signboard, chill atmosphere, and stellar Italian fare that keep diners coming back for more.",
                   "Take a seat at The Coffee Experience Bar and watch the barista craft your freshly siphoned brew or Chemex pour over. The outlet also offers nitro cold brew ??? cold brew coffee that is infused with nitrogen for a smoother taste and creamy foam top ??? on tap." ]

    for place in results[0]:
        df = pd.DataFrame.from_dict([place])
        new_entity = Entity(id=entity_idx, name=unidecode(df['name'].to_string(index=False)), description=descriptions[entity_idx-1], category=df['category'].to_string(index=False), address=df['address'].to_string(index=False), website=df['website'].to_string(index=False), contact=df['phone'].to_string(index=False), picture_url=pictures[entity_idx-1])
        db.session.merge(new_entity)

        for big_review in df['review']:
            for review in big_review:
                new_review = Review(id=review_idx, content=review, entity_id=entity_idx, author="Anonymous", date="2023")
                db.session.merge(new_review)
                review_idx += 1
        
        entity_idx += 1

    # Backup data as demonstration
    # csv_files = ["entity_data.csv", "review_data.csv"]
    # for csv in csv_files:
    #     filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + csv

    #     df = pd.read_csv(filename)

    #     for index, row in df.iterrows():
    #         if csv == "entity_data.csv":
    #             new_entity = Entity(id=row['entity_id'], name=row['name'], description=row['description'], address=row['address'], website=row['website'], contact=row['contact'], picture_url=row['picture_url'])
    #             db.session.merge(new_entity)
    #         elif csv == "review_data.csv":
    #             new_review = Review(id=row['review_id'], content=row['review'], entity_id=row['entity_id'], author=row['author'], date=row['date'])
    #             db.session.merge(new_review)
                     
    try:
        db.session.commit()
    except Exception:
        print("alert")
        pass