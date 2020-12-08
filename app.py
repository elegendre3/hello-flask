#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from flask import Flask, request, jsonify

from logging_conf import setup_logging, setup_logging_from_flask

app = Flask(__name__)

# init
base_path = Path("/base")
env_var = os.environ.get("MYVAR", "unset")

# try to set up headers as extra fields
# setup_logging(jsonformat=True, extra={'props': request.headers})
setup_logging(jsonformat=True)
app_logger = logging.getLogger(__name__)


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

    setup_logging_from_flask("Host", "User-Agent", "Postman-Token")
    request_logger = logging.getLogger(__name__)  # no effect it seems
    request_logger.info('This message should have some header fields in it.')  # does not show
    logging.info('This message should have some header fields in it.') # this shows

    return 'Hello {}!\n'.format(greeting_target)


@app.route('/v1/models/jsonify-request:predict', methods=['POST'])
def to_json():
    return jsonify(request.json)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
