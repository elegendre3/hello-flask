#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

from my_app.logger.logging_conf import setup
from my_app.gpt3 import parties

# init
base_path = Path("/base")
env_var = os.environ.get("MYVAR", "unset")

setup(json_enabled=False)
app_logger = logging.getLogger(__name__)


def create_app(test_config=None, instance_path=None):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")

    @app.route('/hello-world:predict', methods=['GET', 'POST'])
    def hello_world():
        greeting_target = os.environ.get('GREETING_TARGET', 'World')
        # app_logger.info(f'HEADERS: [{request.headers}]')
        app_logger.info('Log message.')
        app_logger.info('This message should have extra headers fields. (json).', extra={'props': dict(request.headers)})
        # Need to specify StreamHandler for these logs to show in the container. (always show in python app.py)
        return 'Hello {}!\n'.format(greeting_target)

    @app.route('/v1/models/jsonify-request', methods=['POST'])
    def to_json():
        return jsonify(request.json)

    @app.route('/home', methods=['GET'])
    def home():
        app_logger.info('home endpoint')
        return render_template("home.html")

    @app.route('/reco', methods=['GET'])
    def reco():
        app_logger.info('reco endpoint')
        return render_template("recommendation.html")

    @app.route('/gpt', methods=['GET'])
    def gpt():
        app_logger.info('gpt endpoint')
        return render_template("gpt.html")

    @app.route('/gpt:predict', methods=['POST'])
    def partyextractor_gpt3():
        prompt = request.data.decode("utf-8")
        app_logger.info("prompt")
        app_logger.info(prompt)

        response = parties(prompt)
        # response = {"choices": [{"text": " my first party\n2. Second party here", "finish_reason": "blah blah reason"}]}

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

    return app