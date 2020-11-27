# -*- coding: utf-8 -*-
"""
load up model and data for predictions
"""
import random
import json
import torch
# ryan - added os import from filepath handling
import os
# ryan - removed IntentHandler import
class modelStart:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # ryan - filepath reading
    filedir = os.path.dirname(os.path.realpath('../__file__'))
    filename = os.path.join(filedir, 'DataFiles/intents.json')
    with open(filename, 'r') as json_data:
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