

# maybe put this in a preloader so dont load twice when running twice
from sgnlp.models.emotion_entailment import (
    RecconEmotionEntailmentConfig,
    RecconEmotionEntailmentModel,
    RecconEmotionEntailmentTokenizer,
    RecconEmotionEntailmentPreprocessor,
    RecconEmotionEntailmentPostprocessor,
)

config = RecconEmotionEntailmentConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/config.json"
)
	
ml_model = RecconEmotionEntailmentModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/reccon_emotion_entailment/pytorch_model.bin",
    config=config,
)

tokenizer = RecconEmotionEntailmentTokenizer.from_pretrained("roberta-base")
preprocessor = RecconEmotionEntailmentPreprocessor(tokenizer)
postprocess = RecconEmotionEntailmentPostprocessor()

def emotion_entailment(text):

	print(text)

	# TODO: Appears upon clicking each company card for the 5 big areas
    
	input_batch = {
    "emotion": ["happiness", "happiness", "happiness", "happiness"],
    "target_utterance": [
        "Thank you very much .",
        "Thank you very much .",
        "Thank you very much .",
        "Thank you very much .",
    	],
    "evidence_utterance": [
        "It's very thoughtful of you to invite me to your wedding .",
        "How can I forget my old friend !",
        "My best wishes to you and the bride !",
        "Thank you very much .",
    	],
    "conversation_history": [
        "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
        "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
        "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
        "It's very thoughtful of you to invite me to your wedding . How can I forget my old friend ? My best wishes to you and the bride ! Thank you very much .",
    	],
	}
	input_dict = preprocessor(input_batch)
	raw_output = ml_model(**input_dict)
	output = postprocess(raw_output)
	return output
	# print(output)
	# [0, 1]

	