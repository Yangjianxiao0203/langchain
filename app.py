from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break
from dotenv import load_dotenv
import logging

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process',methods=["POST"])
def process():
    name = request.form['name']
    description = request.form['description']
    logger.info(f"Name: {name}, Description: {description}")
    person_parser, pic = ice_break(name,description)
    display_json = jsonify({
        "summary":person_parser.summary,
        "facts":person_parser.facts,
        "interests":person_parser.topics_of_interest,
        "ice_breakers":person_parser.ice_breakers,
        "picture_url":pic
    })
    return display_json

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5001)