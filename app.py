#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

from gpt3 import parties
from logging_conf import setup_logger, setup_logger_from_flask

app = Flask(__name__)

# init
base_path = Path("/base")
env_var = os.environ.get("MYVAR", "unset")

# try to set up headers as extra fields
# setup_logging(jsonformat=True, extra={'props': request.headers})
app_logger = setup_logger(__name__, jsonformat=False)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/v1/models/hello-world:predict', methods=['GET', 'POST'])
def hello_world():
    greeting_target = os.environ.get('GREETING_TARGET', 'World')
    # app_logger.info(f'HEADERS: [{request.headers}]')
    app_logger.info('This message should have extra header fields with it.', extra={'props': dict(request.headers)})
    # Need to specify StreamHandler for these logs to show in the container. (always show in python app.py)
    return 'Hello {}!\n'.format(greeting_target)


@app.route('/v1/models/hello-world:headers', methods=['POST'])
def hello_world_headers():
    greeting_target = os.environ.get('GREETING_TARGET', 'World')

    setup_logger_from_flask("Host", "User-Agent", "Postman-Token")
    request_logger = logging.getLogger(__name__)  # no effect it seems
    request_logger.info('This message should have some header fields in it.')  # does not show
    logging.info('This message should have some header fields in it.') # this shows

    return 'Hello {}!\n'.format(greeting_target)


@app.route('/v1/models/jsonify-request:predict', methods=['POST'])
def to_json():
    return jsonify(request.json)


@app.route('/v1/models/static/partyextractor:predict', methods=['POST'])
def partyextractor_gpt3_static():
    prompt = 'as of the date of the last signature below, effective May 17, 2010 by and between ' \
             'Elsinore Services, Inc., a Delaware corporation ("Client"), and FaceTime Strategy LLC, a ' \
             'Virginia limited liability company ("FaceTime"), and provides as follows:'
    # response = parties(prompt)
    response = {"choices": [{"text": " my first party\n2. Second party here", "finish_reason": "blah blah reason"}]}
    html_wrapper = """
    <html>
    <body>
    <h1>{}</h1>
    <p style="color:#3382FF";>{}</p>
    <p>{}</p>
    <p style="color:#3382FF";>{}</p>
    <pre>{}</pre>
    <p style="color:#99A1A7";>{}</p>
    </body>
    </html>
    """

    output = html_wrapper.format(
        "Party Extraction",
        'Parties Clause:',
        prompt,
        'What GPT3 thinks:',
        '1.{}'.format(response["choices"][0]["text"]),
        'Finish Reason: [{}]'.format(response["choices"][0]["finish_reason"])
    )

    return output


@app.route('/v1/models/partyextractor:predict', methods=['POST'])
def partyextractor_gpt3():
    prompt = request.data.decode("utf-8")
    app_logger.info("prompt")
    app_logger.info(prompt)

    # response = parties(prompt)
    response = {"choices": [{"text": " my first party\n2. Second party here", "finish_reason": "blah blah reason"}]}

    html_wrapper = """
        <html>
        <body>
        <pre>{}</pre>
        <p style="color:#99A1A7";>{}</p>
        <br>
        <br>
        </body>
        </html>
        """

    output = html_wrapper.format(
        '1.{}'.format(response["choices"][0]["text"]),
        'Finish Reason: [{}]'.format(response["choices"][0]["finish_reason"])
    )

    return jsonify({"parties": output})


@app.route('/v1/models/partyextractor:index', methods=['GET'])
def partyextractor_index():
    return render_template("partyextractor_index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
