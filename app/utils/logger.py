import logging

SENSITIVE_FIELDS = {"salary", "vacation_balance", "phone", "email", "sick_days"}


def mask_sensitive(data: dict) -> dict:
    return {k: "[MASKED]" if k in SENSITIVE_FIELDS else v for k, v in data.items()}


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
