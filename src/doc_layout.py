from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch

IMG_PATH = "uploads\download.jpg"

def doc_layout(img_path):
    '''
    This function take path of document_image as input and predicts the document types
    INPUT :  String
    Output : String

    '''
    path_to_image = img_path
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
    try:
        feature_extractor = torch.load("artifacts/pre-trained-models/dit-base-feature_extractor-rvlcdip.pt")
        model = torch.load("artifacts/pre-trained-models/dit-base-model-rvlcdip.pt")
        print("model loaded successfully from local storage")
    except:
        feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        torch.save(feature_extractor,"artifacts/pre-trained-models/dit-base-feature_extractor-rvlcdip.pt")

        model = AutoModelForImageClassification.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        torch.save(model,"artifacts/pre-trained-models/dit-base-model-rvlcdip.pt")

        print("model loaded successfully from huggingface and saved to local storage")
    finally:
        doc_layout(IMG_PATH, feature_extractor, model)