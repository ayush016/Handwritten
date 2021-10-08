import flask
from flask import request, jsonify
import os
from flask import send_file
import handwrite
import argparse
import json

app = flask.Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/v1/submitText', methods=['POST'])
def setTextToConvert():
    print(request.json)


    if "text" in request.json:

        parser = argparse.ArgumentParser()
        parser.add_argument('--model', dest='model_path', type=str, default=os.path.join('pretrained', 'model-29'),help='(optional) DL model to use')
        parser.add_argument('--text', dest='text', type=str, help='Text to write',default=request.json["text"])
        parser.add_argument('--text-file', dest='file', type=str, default=None, help='Path to the input text file')
        parser.add_argument('--style', dest='style', type=int, default=0, help='Style of handwriting (1 to 7)')
        parser.add_argument('--bias', dest='bias', type=float, default=0.9,help='Bias in handwriting. More bias is more unclear handwriting (0.00 to 1.00)')
        parser.add_argument('--force', dest='force', action='store_true', default=False)
        parser.add_argument('--color', dest='color_text', type=str, default='0,0,150',help='Color of handwriting in RGB format')
        parser.add_argument('--output', dest='output', type=str, default='./handwritten.pdf',help='Output PDF file path and name')
        args = parser.parse_args()
        res = handwrite.textToHandWritting(args)
        return jsonify({'sucess': True,'key':res}), 201
    else:
         return jsonify({'sucess': False,'key':'Mandatory parameter text is missing'}), 201


@app.route('/downloadPdf',methods=['GET'])
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "handwritten.pdf"
    return send_file(path, as_attachment=True)

app.run(host="0.0.0.0")