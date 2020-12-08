from datetime import datetime
import json
import logging
import logging.config
from pathlib import Path
import traceback
from yaml import safe_load as yaml_load

import json_logging

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


def setup_logging(
        config_path: Path = None,
        jsonformat: bool = True,
):
    tolog = []  # backlog of messages to log when logger ready

    if config_path:
        try:
            logging.config.dictConfig(yaml_load(config_path.open('r')))
        except FileNotFoundError:
            raise FileNotFoundError(f'Could not find logging config file at [{config_path}].')
    else:
        logging.config.dictConfig(CONFIG_YML)
        tolog.append("No config passed, using default")

    METRIC_LEVELV_NUM = 50

    logging.addLevelName(METRIC_LEVELV_NUM, 'METRIC')

    def metric(self, message, *args, **kwargs):
        if self.isEnabledFor(METRIC_LEVELV_NUM):
            self._log(METRIC_LEVELV_NUM, message, args, **kwargs)

    logging.Logger.metric = metric

    if jsonformat:
        json_logging.init_non_web(enable_json=True, custom_formatter=CustomJSONFormatter,)
        tolog.append('Logging configured to JSON format.')
    else:
        tolog.append('Logging configured to string/stream format.')

    for msg in tolog:
        logging.info(msg)


class CustomJSONFormatter(logging.Formatter):
    """
    Customized logger
    """

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
        json_log_object = {
            "@timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
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
        if hasattr(record, 'props'):
            json_log_object['data'].update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object['data'].update(self.get_exc_fields(record))

        return json.dumps(json_log_object)
