import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load the model and tokenizer (ensure the paths are correct)
model_path = os.path.join('custom_user', 'Ai', 'best_arabert_model')
tokenizer_path = os.path.join('custom_user', 'Ai', 'best_arabert_tokenizer')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Use the directory path for from_pretrained
ai = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
ai.to(device)
ai.eval()

def predict_responses(responses):
    if len(responses) < 2:
        raise ValueError('Not enough responses to process.')

    predictions = []

    # Iterate over responses in pairs
    for i in range(0, len(responses), 2):
        if i + 1 < len(responses):
            sentence1 = responses[i]
            sentence2 = responses[i + 1]
        else:
            break  # If there's an odd number of responses, break out of the loop

        encoding = tokenizer.encode_plus(
            sentence1,
            sentence2,
            add_special_tokens=True,
            max_length=180,
            return_token_type_ids=False,
            padding='max_length',
            truncation='longest_first',  # Change truncation strategy
            return_attention_mask=True,
            return_tensors='pt',
        )

        input_ids = encoding.get('input_ids')
        attention_mask = encoding.get('attention_mask')

        if input_ids is None or attention_mask is None:
            raise ValueError('Encoding input_ids or attention_mask is missing.')

        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)

        with torch.no_grad():
            outputs = ai(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            prediction = torch.argmax(logits, dim=1).cpu().numpy()[0]
            label_map = {0: "متحيز ضد الاسرائيليين", 1: "متحيز ضد الفلسطينيين", 2: "لا يوجد تحيز"}
            result = label_map.get(prediction, "Unknown")
            predictions.append(result)

    return predictions


# import os
# import torch
# from transformers import BertTokenizer, BertForSequenceClassification
# from collections import Counter

# # Load the model and tokenizer (ensure the paths are correct)
# model_path = os.path.join('custom_user', 'Ai', 'best_arabert_model')
# tokenizer_path = os.path.join('custom_user', 'Ai', 'best_arabert_tokenizer')
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # Use the directory path for from_pretrained
# ai = BertForSequenceClassification.from_pretrained(model_path)
# tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
# ai.to(device)
# ai.eval()

# def predict_responses(responses):
#     if len(responses) < 2:
#         raise ValueError('Not enough responses to process.')

#     predictions = []

#     # Iterate over responses in pairs
#     for i in range(0, len(responses), 2):
#         if i + 1 < len(responses):
#             sentence1 = responses[i]
#             sentence2 = responses[i + 1]
#         else:
#             break  # If there's an odd number of responses, break out of the loop

#         encoding = tokenizer.encode_plus(
#             sentence1,
#             sentence2,
#             add_special_tokens=True,
#             max_length=180,
#             return_token_type_ids=False,
#             padding='max_length',
#             truncation='longest_first',  # Change truncation strategy
#             return_attention_mask=True,
#             return_tensors='pt',
#         )

#         input_ids = encoding.get('input_ids')
#         attention_mask = encoding.get('attention_mask')

#         if input_ids is None or attention_mask is None:
#             raise ValueError('Encoding input_ids or attention_mask is missing.')

#         input_ids = input_ids.to(device)
#         attention_mask = attention_mask.to(device)

#         with torch.no_grad():
#             outputs = ai(input_ids, attention_mask=attention_mask)
#             logits = outputs.logits
#             prediction = torch.argmax(logits, dim=1).cpu().numpy()[0]
#             label_map = {0: "متحيز ضد الاسرائيليين", 1: "متحيز ضد الفلسطينيين", 2: "لا يوجد تحيز"}
#             result = label_map.get(prediction, "Unknown")
#             predictions.append(result)

#     return predictions

# def bias(predictions):
#     counter = Counter(predictions)
#     most_frequent = counter.most_common(1)[0]  # Get the most common label
#     print(f"result : {most_frequent[0]} with {most_frequent[1]} occurrences.")
