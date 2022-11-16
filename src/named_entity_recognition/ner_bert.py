from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import torch
import os

TEXT = "My name is Wolfgang and I live in Berlin"

def ner_using_bert(text):
    '''
    This function take path of document_image as input and predicts the document types
    INPUT :  String
    Output : String

    '''
    try:

        tokenizer = torch.load("artifacts/pre-trained-models/ner_bert/bert-base-NER-token.pt")
        model = torch.load("artifacts/pre-trained-models/ner_bert/bert-base-NER-model.pt")
        print("bert_model loaded successfully from local storage")
        
    except:
        os.makedirs("artifacts/pre-trained-models/ner_bert", exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        

        torch.save(tokenizer,"artifacts/pre-trained-models/ner_bert/bert-base-NER-token.pt")
        torch.save(model,"artifacts/pre-trained-models/ner_bert/bert-base-NER-model.pt")
        print("bert_model loaded successfully from huggingface and saved to local storage")

    nlp = pipeline("ner", model=model, tokenizer=tokenizer)

    #example = "My name is Wolfgang and I live in Berlin"
    ner_results = nlp(text)
    print(ner_results)

    return ner_results

if __name__ == "__main__":
     ner_using_bert(text = TEXT)
    