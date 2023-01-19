from app.models import Review
from app import search_dict

from sgnlp.models.sentic_gcn import (
    SenticGCNBertTokenizer,
    SenticGCNBertEmbeddingConfig,
    SenticGCNBertEmbeddingModel,
    SenticGCNBertModel,
    SenticGCNBertPreprocessor,
    SenticGCNBertConfig,
    SenticGCNBertPostprocessor,
)

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

def sentiment_analysis(search_terms):
    processed_search_terms = search_terms.split(",")
    past_reviews = Review.query.all()
    #print(past_reviews)
    past_reviews_dict = {r.content : r.entity_id for r in past_reviews}

    input_batch = []
    candidate = []
    output = []

    category_found = ""
    for search_term in processed_search_terms:
        relevant = False
        search_term.split()
        if len(search_term.split(" ")) > 1:
            for term in search_term.split(" "):
                #print(term)
                category_found = [ cat for cat in search_dict.terms if term.lower() in search_dict.terms[cat]]
        else:
            category_found = [ cat for cat in search_dict.terms if search_term.lower() in search_dict.terms[cat]]

        #print(category_found)
        for review in past_reviews_dict.keys():
        
            if search_term in review and category_found:
                relevant = True
                candidate.append({past_reviews_dict.get(review): category_found})
            if relevant:
                input_batch.append(
                        {
                            "aspects": processed_search_terms,
                            "sentence": review
                        }
                )
                relevant = False

        category_found = ""

    output = []

    if input_batch:
        try:
            processed_inputs, processed_indices = preprocessor(input_batch)
            print(processed_indices)
            outputs = model(processed_indices)
        except ValueError:
            output.append("Something went wrong :/")
            return output
    
        # Postprocessing
        dense_output = postprocessor(processed_inputs=processed_inputs, model_outputs=outputs)

        # Parsing output
        label_dict = {
            "-1": "Negative",
            "0": "Neutral",
            "1": "Positive"
        }

        for i, line in enumerate(dense_output):
            sub_output = ""
            output.append(f"Review for placeholder company using i var to find")
            review = " ".join(line['sentence'])
            output.append(f" '{review}' ")
            for idx, aspect in enumerate(line['aspects']):
                if len(aspect) == 1:
                    current_word = line['sentence'][aspect[0]].strip(",.(){}<>!?")
                else:
                    current_word = " ".join(line['sentence'][aspect[0]:aspect[-1]+1]).strip(",.(){}<>!?")
                sub_output = f"{current_word} - {label_dict[str(line['labels'][idx])]}"
                output.append(sub_output)
                sub_output = ""

    if len(output) < 1:
        output.append("No reviews found for your search :/")

    return output

# Overall - Model Stuff
# TODO: Figure out how to preload model bins so it doesn't load all the time
# DONE: Setup database for reviews and figure out retrieval

# HTML Stuff
# Landing page
# Done (left with CSS): Inherit Navbar Base - Home, About us, Get Started
# TODO: Quick start guide
# Search bar webpage
# DONE: Handle multi-word search terms
# TODO: Check if search term is capitalised or not (input sanitation)
# TODO: Aggregate the 5 areas: Food, Service, Cleanliness, Price, Atmosphere
# Company dashboard right is word cloud with top 5 areas of Food, Service, Cleanliness, (3 will be big on top and 2 will be smaller below -> probably use templating)
# TODO: Left is card
# TODO: Right is word cloud at top then, top 5 areas of Food, Service, Cleanliness, (3 will be big on top and 2 will be smaller below -> probably use templating)