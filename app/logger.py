import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from config import cfg


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Форматтер логов"""

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


# дефолтный встроенный логгер
logger = logging.getLogger()
# куда писать логи (консоль)
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s")

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
# установка уровня логгирования
logger.setLevel(cfg.LOG_LEVEL)
