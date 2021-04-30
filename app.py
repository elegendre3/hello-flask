#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path
import json

from flask import Flask, request, jsonify, render_template

# from gpt3 import parties
# from ner_spacy import predict
from logging_conf import setup

app = Flask(__name__, static_url_path='/static')

# init
base_path = Path("/base")
env_var = os.environ.get("MYVAR", "unset")

# try to set up headers as extra fields
# setup_logging(jsonformat=True, extra={'props': request.headers})

setup(json_enabled=False)
app_logger = logging.getLogger("ravnml")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

#
# @app.route('/v1/models/hello-world:predict', methods=['GET', 'POST'])
# def hello_world():
#     greeting_target = os.environ.get('GREETING_TARGET', 'World')
#     # app_logger.info(f'HEADERS: [{request.headers}]')
#     app_logger.info('This message should have extra header fields with it.', extra={'props': dict(request.headers)})
#     # Need to specify StreamHandler for these logs to show in the container. (always show in python app.py)
#     return 'Hello {}!\n'.format(greeting_target)
#
#
# @app.route('/v1/models/hello-world:headers', methods=['POST'])
# def hello_world_headers():
#     greeting_target = os.environ.get('GREETING_TARGET', 'World')
#
#     # setup_logger_from_flask("Host", "User-Agent", "Postman-Token")
#     request_logger = logging.getLogger(__name__)  # no effect it seems
#     request_logger.info('This message should have some header fields in it.')  # does not show
#     logging.info('This message should have some header fields in it.') # this shows
#
#     return 'Hello {}!\n'.format(greeting_target)
#
#
# @app.route('/v1/models/jsonify-request:predict', methods=['POST'])
# def to_json():
#     return jsonify(request.json)
#
#
# @app.route('/v1/models/static/partyextractor:predict', methods=['POST'])
# def partyextractor_gpt3_static():
#     prompt = 'as of the date of the last signature below, effective May 17, 2010 by and between ' \
#              'Elsinore Services, Inc., a Delaware corporation ("Client"), and FaceTime Strategy LLC, a ' \
#              'Virginia limited liability company ("FaceTime"), and provides as follows:'
#     # response = parties(prompt)
#     response = {"choices": [{"text": " my first party\n2. Second party here", "finish_reason": "blah blah reason"}]}
#     html_wrapper = """
#     <html>
#     <body>
#     <h1>{}</h1>
#     <p style="color:#3382FF";>{}</p>
#     <p>{}</p>
#     <p style="color:#3382FF";>{}</p>
#     <pre>{}</pre>
#     <p style="color:#99A1A7";>{}</p>
#     </body>
#     </html>
#     """
#
#     output = html_wrapper.format(
#         "Party Extraction",
#         'Parties Clause:',
#         prompt,
#         'What GPT3 thinks:',
#         '1.{}'.format(response["choices"][0]["text"]),
#         'Finish Reason: [{}]'.format(response["choices"][0]["finish_reason"])
#     )
#
#     return output
#
#
# @app.route('/v1/models/partyextractor:predict', methods=['POST'])
# def partyextractor_gpt3():
#     prompt = request.data.decode("utf-8")
#     app_logger.info("prompt")
#     app_logger.info(prompt)
#
#     response = parties(prompt)
#     # response = {"choices": [{"text": " my first party\n2. Second party here", "finish_reason": "blah blah reason"}]}
#
#     html_wrapper = """
#         <html>
#         <body>
#         <pre>{}</pre>
#         <p style="color:#99A1A7";>{}</p>
#         <br>
#         <br>
#         </body>
#         </html>
#         """
#
#     output = html_wrapper.format(
#         '1.{}'.format(response["choices"][0]["text"]),
#         'Finish Reason: [{}]'.format(response["choices"][0]["finish_reason"])
#     )
#
#     return jsonify({"parties": output})


@app.route('/v1/models/partyextractor:index', methods=['GET'])
def partyextractor_index():
    return render_template("partyextractor_index.html")


@app.route('/spacy/ner', methods=['GET'])
def ner():
    return render_template("ner.html")

#
# @app.route('/spacy/ner/predict', methods=['POST'])
# def ner_predict():
#     app_logger.info("NER Predict request received")
#
#     data = request.data.decode("utf-8")
#     text = json.loads(data)['text']
#     app_logger.info("Input: ")
#     app_logger.info(text)
#     return predict(text)


@app.route('/hackathon/', methods=['GET'])
@app.route('/hackathon/index', methods=['GET'])
def hackathon_index():
    app_logger.info("Hackathon Index Page")
    return render_template("hackathon_index.html")


@app.route('/hackathon/graph', methods=['GET'])
def hackathon_graph():
    app_logger.info("Hackathon Graph Page")
    return render_template("hackathon_graph.html")


@app.route('/hackathon/search', methods=['GET'])
def hackathon_search():
    app_logger.info("Hackathon Search Page")
    return render_template("hackathon_search.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
