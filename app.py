#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify

from logging_conf import setup_logging

app = Flask(__name__)

# init
base_path = Path("/base")
env_var = os.environ.get("MYVAR", "unset")


setup_logging(jsonformat=True)
app_logger = logging.getLogger(__name__)


@app.route('/v1/models/hello-world:predict', methods=['GET', 'POST'])
def hello_world():
    greeting_target = os.environ.get('GREETING_TARGET', 'World')
    app_logger.info(f'HEADERS: [{request.headers}]')
    # Need to specify StreamHandler for these logs to show in the container. (always show in python app.py)
    return 'Hello {}!\n'.format(greeting_target)


@app.route('/v1/models/debug-request:predict', methods=['GET', 'POST'])
def debug_request():
    return request.get_data()


@app.route('/v1/models/jsonify-request:predict', methods=['POST'])
def to_json():
    return jsonify(request.json)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
