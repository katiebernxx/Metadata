''' Ranking emotions expressed in the scripts'''

from transformers import pipeline
from transformers import AutoTokenizer

def split_script(script_text, max_tokens=450):
    # Load a pre-trained tokenizer and tokenize the text
    tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
    tokens = tokenizer.encode(script_text, add_special_tokens=False)

    # Split the tokens into chunks
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]

    # Decode each chunk back to text
    chunked_texts = [tokenizer.decode(chunk, clean_up_tokenization_spaces=True) for chunk in chunks]

    return chunked_texts

def extract_emotions(chunk):
    # Load a pre-trained emotion detection model
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

    # Perform emotion detection
    emotions = emotion_classifier(chunk)

    # Aggregate and rank emotions
    emotion_scores = {emotion['label']: emotion['score'] for emotion in emotions[0]}
    extracted_emotions = sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)

    return extracted_emotions

def rank_emotions(script_text, num_to_display = 4, verbose = False):
    chunks = split_script(script_text)
    aggregated_scores = {}

    for chunk in chunks:
        chunk_emotions = extract_emotions(chunk)
        
        for emotion, score in chunk_emotions:
            if emotion in aggregated_scores:
                aggregated_scores[emotion] += score
            else:
                aggregated_scores[emotion] = score

    # Rank the aggregated emotions
    final_ranked_emotions = sorted(aggregated_scores.items(), key=lambda item: item[1], reverse=True)

    if verbose:
        print("Final Ranked Emotions:", final_ranked_emotions)

    return final_ranked_emotions[:num_to_display]