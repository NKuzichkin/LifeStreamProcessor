#!flask/bin/python
from flask import Flask, jsonify, request, redirect
import numpy as np
import urllib.request
import os
import TorchvisionMaskRCnn as tv

if not os.path.exists('upload_image'):
    os.makedirs('upload_image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload_image'

tv.init()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg': 'home'})

@app.route('/api/process-objects', methods=['POST'])
def process_objects():
    # check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file:
		filiname = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(filiname)
		output = tv.run(filiname)
		resp = jsonify(output)
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

if __name__ == '__main__':
    app.run(debug=False)