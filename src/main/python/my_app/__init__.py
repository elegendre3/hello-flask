#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

from my_app.logger.logging_conf import setup

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

    return app