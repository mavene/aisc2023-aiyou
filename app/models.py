from app import db, application
import pandas as pd
import os

# from app import login
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(UserMixin, db.Model):
# 	__tablename__ = 'user'
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(64), index=True, unique=True)
# 	password_hash = db.Column(db.String(128))
# 	review = db.relationship('Review', backref='from_user', 
# 								lazy='dynamic')

# 	def set_password(self, password):
# 		self.password_hash = generate_password_hash(password)

# 	def check_password(self, password):
# 		return check_password_hash(self.password_hash, password)

# 	def __repr__(self):
# 		return f'<User {self.username:}>'

# Parent
class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(255))
    review = db.relationship("Review", back_populates="entity")

# Child
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))
    entity = db.relationship("Entity", back_populates="review")
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship("User", back_populates="review")

    def __repr__(self):
        return f'{self.content}'

with application.app_context():
    db.create_all()
    
    csv_file = "prev_data.csv"
    filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + csv_file

    df = pd.read_csv(filename)

    for index, row in df.iterrows():
        new_entity = Entity(id=row['entity_id'], name=row['name'], address=row['address'])
        new_review = Review(id=row['review_id'], content=row['review'], entity_id=row['entity_id'])
        db.session.merge(new_entity)
        db.session.merge(new_review)
        db.session.commit()