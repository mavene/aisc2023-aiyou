from app import search_dict
from app.models import Review

from sgnlp.models.sentic_gcn import (
    SenticGCNBertTokenizer,
    SenticGCNBertEmbeddingConfig,
    SenticGCNBertEmbeddingModel,
    SenticGCNBertModel,
    SenticGCNBertPreprocessor,
    SenticGCNBertConfig,
    SenticGCNBertPostprocessor,
)

def inference(entities):

    entity_sentiment = {}

    # Load model
    config = SenticGCNBertConfig.from_pretrained(
        "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/config.json"
    )

    model = SenticGCNBertModel.from_pretrained(
        "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/pytorch_model.bin", config=config
    )

    # Create tokenizer
    tokenizer = SenticGCNBertTokenizer.from_pretrained("bert-base-uncased")
    # Create embedding model
    embed_config = SenticGCNBertEmbeddingConfig.from_pretrained("bert-base-uncased")
    embed_model = SenticGCNBertEmbeddingModel.from_pretrained("bert-base-uncased", config=embed_config)
    # Create preprocessor
    preprocessor = SenticGCNBertPreprocessor(
        tokenizer=tokenizer,
        embedding_model=embed_model,
        senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
        device="cpu",
    )

    # Create postprocessor
    postprocessor = SenticGCNBertPostprocessor()
    # label_dict = {
    #     "-1": "Negative",
    #     "0": "Neutral",
    #     "1": "Positive"
    # }

    for entity in entities:

        sentiment_template = {"Food": ["None", 0], 
                      "Service": ["None", 0], 
                      "Cleanliness": ["None", 0], 
                      "Price": ["None", 0], 
                      "Ambience": ["None", 0]}

        for area in sentiment_template.keys():
            reviews = {}
            
            # Find data
            for term in search_dict.terms[area]:
                search_term = "%{}%".format(term)
                relevant_reviews = Review.query.filter(Review.content.like(search_term), Review.entity_id.like(entity.id)).all()
                for hit in relevant_reviews:
                    if hit not in reviews.values():
                        if reviews.get(term):
                            reviews[term].append(hit)
                        else:
                            reviews[term] = [ hit ]
                    else:
                        continue

            # Prepare data
            input_batch = []
            if reviews:
                for aspect, sentences in reviews.items():
                    for sentence in sentences:
                        input_batch.append(
                        {
                            "aspects": aspect,
                            "sentence": sentence.content
                        }
                    )  

            # Perform inference
            if input_batch:
                try:
                    processed_inputs, processed_indices = preprocessor(input_batch)
                    outputs = model(processed_indices)
                except ValueError:
                    continue
    
                # Postprocessing
                dense_output = postprocessor(processed_inputs=processed_inputs, model_outputs=outputs)
                
                sentiment_sum = 0
                sentiment = ""
                for line in dense_output:
                    sentiment_sum = sum(line['labels'])

                if sentiment_sum > 5:
                    sentiment = "Good"
                elif sentiment_sum < 0:
                    sentiment = "Bad"
                else:
                    sentiment = "Neutral"
                    
                sentiment_template[area] = [sentiment, sentiment_sum]
        
        entity_sentiment[entity.id] = sentiment_template

    return entity_sentiment

# TODO: Figure out how to preload model bins so it doesn't load all the time
# TODO: Quick start guide and Landing Page
# TODO: Aggregate the 5 areas: Food, Service, Cleanliness, Price, Atmosphere
# TODO: Right is word cloud at top then, top 5 areas of Food, Service, Cleanliness, (3 will be big on top and 2 will be smaller below -> probably use templating)