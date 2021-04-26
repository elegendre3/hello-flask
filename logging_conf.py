from datetime import datetime
import json
import logging
import logging.config
from pathlib import Path
import sys
import re
import traceback

import json_logging
from yaml import safe_load as yaml_load

CONFIG_YML = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }},
    'loggers': {
        'component_logger': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}


def setup(json_enabled: bool, config_path: Path = None):
    tolog = []
    if json_enabled:
        json_logging.init_non_web(enable_json=True, custom_formatter=CustomJSONFormatter)
        tolog.append("Logging configured to JSON format.")
    else:
        if config_path:
            logging.config.dictConfig(yaml_load(config_path.open('r')))
        else:
            logging.config.dictConfig(CONFIG_YML)
            tolog.append("No config was found, using RAVNML default.")

    # Configure root logger
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(ContextFilter())
    logger.addHandler(handler)
    for m in tolog:
        logger.info(m)


def _get_ravnml_headers(*args):
    extra_fields = {}

    default_headers = {
        'action': "X-Action",
        'customerId': "X-Customer-Id",
        'modelId': "X-Model-Id",
        'projectId': "X-Project-Id",
        'userId': "X-User-Id",
        'requestId': "X-Request-Id",
        'runId': "X-Run-Id",
        'deploymentId': "X-Deployment-Id"
    }

    try:
        from flask import request

        for f in default_headers.keys():
            header_val = request.headers.get(default_headers[f], None)
            # Only adding a field if we can retrieve it
            if header_val:
                extra_fields[f] = header_val

        for f in args:
            if f not in default_headers:
                extra_val = request.headers.get(f, "NotFound")
                # Only adding a field if we can retrieve it
                if extra_val:
                    extra_fields[f] = extra_val

    except RuntimeError:
        # Outside of request context
        pass
    except ModuleNotFoundError:
        # missing dependency
        pass

    return extra_fields


def _get_ravnml_env_vars():
    import os

    prefix = 'ravnml_'
    pattern = '^{}(.+)'.format(prefix)

    extra_fields = {}

    env_vars = os.environ

    for v in env_vars:
        m = re.match(pattern, v)
        if m:
            extra_fields[m.groups()[0]] = env_vars[v]
    return extra_fields


class ContextFilter(logging.Filter):
    def filter(self, record):
        ravnml_headers = _get_ravnml_headers()
        ravnml_env_vars = _get_ravnml_env_vars()
        if hasattr(record, 'props'):
            record.props = {**record.props, **ravnml_headers, **ravnml_env_vars}
        else:
            record.props = {**ravnml_headers, **ravnml_env_vars}
        return True


class CustomJSONFormatter(logging.Formatter):
    """
    Customized logger
    """

    def __init__(self, extra_props: dict() = {}):
        super(CustomJSONFormatter).__init__()
        self.extra_props = extra_props

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {'python.exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = self._formatting_func(record)

        if record.exc_info or record.exc_text:
            json_log_object['data'].update(self.get_exc_fields(record))

        # Allows for passing extra fields
        if hasattr(record, 'props'):
            record.props.update(self.extra_props)
        else:
            record.props = self.extra_props
        json_log_object.update(record.props)

        return json.dumps(json_log_object)

    @staticmethod
    def _formatting_func(record):
        json_log_object = {
            "@timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "caller": record.filename + '::' + record.funcName
        }
        json_log_object['data'] = {
            "python.logger_name": record.name,
            "python.module": record.module,
            "python.funcName": record.funcName,
            "python.filename": record.filename,
            "python.lineno": record.lineno,
            "python.thread": record.threadName,
            "python.pid": record.process
        }
        return json_log_object


if __name__ == "__main__":
    setup(json_enabled=True)

    main_logger = logging.getLogger("ravnml")
    main_logger.debug("Test - ravnml")
    main_logger.info("Test - ravnml")
