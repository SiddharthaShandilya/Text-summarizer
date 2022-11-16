from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
import os

IMG_PATH = "uploads\download.jpg"

def doc_layout(IMG_PATH):
    '''
    This function take path of document_image as input and predicts the document types
    INPUT :  String
    Output : String

    '''
    try:

        feature_extractor = torch.load("artifacts/pre-trained-models/doc_layout/dit-base-feature_extractor-rvlcdip.pt")
        model = torch.load("artifacts/pre-trained-models/doc_layout/dit-base-model-rvlcdip.pt")
        print("feature_extractor_model loaded successfully from local storage")
        
    except:
        os.makedirs("artifacts/pre-trained-models/doc_layout", exist_ok=True)
        feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        model = AutoModelForImageClassification.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        

        torch.save(feature_extractor,"artifacts/pre-trained-models/doc_layout/dit-base-feature_extractor-rvlcdip.pt")
        torch.save(model,"artifacts/pre-trained-models/doc_layout/dit-base-model-rvlcdip.pt")
        print("feature_extractor_model loaded successfully from huggingface and saved to local storage")

    path_to_image = IMG_PATH
    #Open image with PIL
    image = Image.open(path_to_image).convert("RGB")
    # prepare image for model (resize + normalize)
    inputs = feature_extractor(image, return_tensors="pt")

    # forward pass
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # model predicts one of the 16 RVL-CDIP classes
    predicted_class_idx = logits.argmax(-1).item()
    print ("Predicted class:", model.config.id2label[predicted_class_idx])
    return model.config.id2label[predicted_class_idx]

if __name__ == "__main__":
     doc_layout(IMG_PATH)
    