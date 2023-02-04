from app.models import Review, Entity
from app import search_dict

def relevant_hits(search_terms):
    processed_search_terms = search_terms.split(",")

    output = []

    for search_term in processed_search_terms:
        term = "%{}%".format(search_term)
        relevant_reviews_chunk = Review.query.filter(Review.content.like(term)).all()
        relevant_entities_chunk = [Entity.query.filter(Entity.id.like(past_review.entity_id)).all()[0] for past_review in relevant_reviews_chunk]
        named_entities_chunk = Entity.query.filter(Entity.name.like(term)).all()
        output = output + relevant_entities_chunk + named_entities_chunk
        print(named_entities_chunk)

    print(output)

    return list(set(output))

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