# -*- coding: utf-8 -*-
"""
load up model and data for predictions
"""
import random
import json
import torch
import IntentHandler
class modelStart:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)
    
    FILE = "data.pth"
    data = torch.load(FILE)
    
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    
    model = IntentHandler.Model.NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()