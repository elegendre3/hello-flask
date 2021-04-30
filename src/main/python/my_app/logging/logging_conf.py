from datetime import datetime
import json
import logging
import logging.config
from pathlib import Path
import sys
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


def setup_logger(
        name: str,
        config_path: Path = None,
        jsonformat: bool = True,
        extra: dict() = {"props": {}},
) -> logging.Logger:
    """
    Sets up logging configuration according to RAVNML standards (default) or to a yaml config file (arg: config_path).
    Default format will be JSON - set jsonformat=False for string/stream format.
    Argument "extras" allows to pass extra fields to the logger, using the "extra" mechanism enabled by json-logging.
    Format: extra={"props": {"extra_field_1": "value1", ...}}. Will raise Exception if "props" is absent.
    Ignored if jsonformat=False.
    """
    tolog = []  # backlog of messages to log when logger ready

    if jsonformat:
        tolog.append('Logging configured to JSON format.')
        # Need to wrap CustomJSONFormatter because it has a special configuration
        # and we need to pass the class constructor, not an instance
        try:
            extra["props"]
        except KeyError as e:
            raise KeyError(str(e) + 'Needs to be of the format: extra={"props": {"extra_field_1": "value1", ...}}')
        #
        custom_json_formatter = CustomJSONFormatter(extra["props"])

        class JsonFormatter(logging.Formatter):
            def format(self, record):
                return custom_json_formatter.format(record)

        json_logging.init_non_web(enable_json=True, custom_formatter=JsonFormatter, )

        logger = logging.getLogger(name)
        # removing pre-existing handlers (this can happen when using seldoncore framework)
        while len(logger.handlers) > 0:
            logger.removeHandler(logger.handlers[0])
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(sys.stdout))

    else:
        tolog.append('Logging configured to string/stream format.')

        if config_path:
            try:
                logging.config.dictConfig(yaml_load(config_path.open('r')))
            except FileNotFoundError:
                raise FileNotFoundError('Could not find logging config file at [{}].'.format(config_path))
        else:
            logging.config.dictConfig(CONFIG_YML)
            tolog.append("No config passed, using RAVNML default")

        METRIC_LEVELV_NUM = 50

        logging.addLevelName(METRIC_LEVELV_NUM, 'METRIC')

        def metric(self, message, *args, **kwargs):
            if self.isEnabledFor(METRIC_LEVELV_NUM):
                self._log(METRIC_LEVELV_NUM, message, args, **kwargs)

        logging.Logger.metric = metric

        logger = logging.getLogger(name)

    for msg in tolog:
        logger.info(msg)

    return logger


def setup_logger_from_flask(name: str, *args) -> logging.Logger:
    """
    Seldon Core uses flask as http server.
    This function allows to initialize the logger with some of the headers as extra fields.
    """
    tolog = []
    extra_fields = {"props": {}}

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
                extra_fields["props"][f] = header_val
            else:
                tolog.append(f'Could not find header [{default_headers[f]}].')

        for f in args:
            if f not in default_headers:
                extra_val = request.headers.get(f, "NotFound")
                # Only adding a field if we can retrieve it
                if extra_val:
                    extra_fields["props"][f] = extra_val
                else:
                    tolog.append(f'Could not find header [{f}].')

        tolog.append(f'Successfully retrieved headers [{list(extra_fields["props"].keys())}].')

    except ModuleNotFoundError:
        tolog.extend([
            'flask package not installed.',
            'Could not retrieve any header information.',
            'Using default Json logger with no extra fields.',
        ])
    except RuntimeError:
        tolog.extend([
            'This was called outside of Request Context.',
            'Needs an active HTTP Request.',
            'Using default Json logger with no extra fields.',
        ])

    logger = setup_logger(name, jsonformat=True, extra=extra_fields)
    for m in tolog:
        logger.info(m)

    return logger


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
