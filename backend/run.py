from models import *
import pickle
import urllib
from torchvision import transforms
import torch
from PIL import Image
from flask import request
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = '5ZN5zi!45QUsGG'



@app.route('/', methods=['GET'])
def home():
    return "Information retrieval"


@app.route('/', methods=['POST'])
def index():
    print("hello")
    input_image = Image.open(urllib.request.urlopen(request.json['url']))
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    model = torch.load('Data/best_classifier.pt', map_location='cpu')
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')
    with torch.no_grad():
        output = model(input_batch)
    with open("Data/food_labels.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top1_prob, top1_catid = torch.topk(probabilities, 1)

    print(categories[top1_catid[0]])
    return {"response": categories[top1_catid[0]]}
    


@app.route('/results', methods=['POST'])
def comparator():
    sentence_query = request.json['query']
    print(sentence_query)
   

    result = Results(file_obj, title_obj,
                     file_tf_idf_obj, title_tf_idf_obj)
    return {"data": result.getResults(sentence_query)}
if __name__ == '__main__':
	print("Loading Models ......")
	with open('Data/ProjectFile.obj', 'rb') as file_object:
		file_obj = pickle.load(file_object)

	print("Done(1/4)")
	with open('Data/ProjectTitle.obj', 'rb') as file_object:
		title_obj = pickle.load(file_object)
	print("Done(2/4)")
	with open('Data/TF_IDF_Calculated_File.obj', 'rb') as file_object:
		file_tf_idf_obj = pickle.load(file_object)
	print("Done(3/4)")
	with open('Data/TF_IDF_Calculated_Title.obj', 'rb') as file_object:
		title_tf_idf_obj = pickle.load(file_object)
	print("Done(4/4)")
	print(" Models Loaded")
	app.run(debug = True, port = '5000')
