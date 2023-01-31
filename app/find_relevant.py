from app import search_dict
from app.models import Review

def find_reviews(entity):

    areas_of_focus = {"Food": [], "Service": [], "Cleanliness": [], "Price": [], "Ambience": []}

    for area in areas_of_focus.keys():
            
        # Find data
        for term in search_dict.terms[area]:
            search_term = "%{}%".format(term)
            relevant_reviews = Review.query.filter(Review.content.like(search_term), Review.entity_id.like(entity.id)).all()
            for hit in relevant_reviews:
                if hit not in areas_of_focus[area]:
                    areas_of_focus[area].append(hit)
                else:
                    continue

    return areas_of_focus