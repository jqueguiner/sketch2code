import os
import sys
import subprocess
import requests
import ssl
import random
import string
import json

from flask import jsonify
from flask import Flask
from flask import request
from flask import send_file
import traceback

from app_utils import blur
from app_utils import download
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import get_multi_model_bin

from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import numpy
from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable
from utils import *
from model import *
from inference.Compiler import *




try:  # Python 3.5+
    from http import HTTPStatus
except ImportError:
    try:  # Python 3
        from http import client as HTTPStatus
    except ImportError:  # Python 2
        import httplib as HTTPStatus


app = Flask(__name__)


@app.route("/process", methods=["POST"])
def process():

    input_path = generate_random_filename(upload_directory,"jpg")

    try:
        url = request.json["url"]

        download(url, input_path)

        image = resize_img(input_path)
        image = Variable(torch.FloatTensor([image]))

        predicted = '<START> '
        for di in range(9999):
            sequence = id_for_word(star_text)
            decoder_input = Variable(torch.LongTensor([sequence])).view(1,-1)
            features = encoder(image)
            outputs, hidden = decoder(features, decoder_input,hidden)
            topv, topi = outputs.data.topk(1)
            ni = topi[0][0][0]
            word = word_for_id(ni)
            if word is None:
                continue
            predicted += word + ' '
            star_text = word
            print(predicted)
            if word == '<END>':
                break
            compiler = Compiler('default')
            compiled_website = compiler.compile(predicted.split())

        return json.dumps(compiled_website), 200

    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400

    finally:
        clean_all([
            input_path
            ])


if __name__ == '__main__':
    global upload_directory, model_directory
    global encode, decoder, start_text, hidden

    upload_directory = 'upload/'
    create_directory(upload_directory)

    model_directory = 'model_weights/'
    create_directory(model_directory)

    encoder_file = 'encoder_resnet34_0.061650436371564865.pt'
    decoder_file = 'decoder_resnet34_0.061650436371564865.pt'


    model_url = "https://storage.gra.cloud.ovh.net/v1/AUTH_18b62333a540498882ff446ab602528b/pretrained-models/image/sketch2code/"

    get_model_bin(model_url + encoder_file, os.path.join(model_directory, encoder_file))
    get_model_bin(model_url + decoder_file, os.path.join(model_directory, decoder_file))

    encoder = torch.load(os.path.join(model_directory, encoder_file))
    decoder = torch.load(os.path.join(model_directory, decoder_file))

    star_text = '<START>'
    hidden = decoder.init_hidden()

    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)
