from app.models import Review, Entity

def relevant_hits(search_terms):
    processed_search_terms = search_terms.split(",")

    output = {}

    for search_term in processed_search_terms:
        term = "%{}%".format(search_term)
        relevant_reviews = Review.query.filter(Review.content.like(term)).all()
        relevant_entities = [Entity.query.filter(Entity.id.like(past_review.entity_id)).all()[0] for past_review in relevant_reviews]

    for i in range(0, len(relevant_entities)):
        if i == 0:
            prev_entity = relevant_entities[i]
            output[relevant_entities[i]] = [ relevant_reviews[i] ]
        else:
            current_entity = relevant_entities[i]
            if prev_entity == current_entity:
                output[prev_entity].append(relevant_reviews[i])
            else:
                output[current_entity] = [ relevant_reviews[i] ]
            prev_entity = current_entity
    
    return output