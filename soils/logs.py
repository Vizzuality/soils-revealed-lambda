import logging
import warnings
import sys
from colorlog import ColoredFormatter


def setup_logLevels(level: str = "DEBUG"):
    """Sets up logs level."""
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s[%(filename)s:%(lineno)d]: %(bold)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    root = logging.getLogger()
    root.setLevel(level)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARN)
    error_handler.setFormatter(formatter)
    root.addHandler(error_handler)

    output_handler = logging.StreamHandler(sys.stdout)
    output_handler.setLevel(level)
    output_handler.setFormatter(formatter)
    root.addHandler(output_handler)
    logging.getLogger("fastapi").setLevel(logging.ERROR)
    logging.getLogger("rasterio").setLevel(logging.ERROR)
    logging.getLogger("botocore").setLevel(logging.ERROR)
    logging.getLogger("uvicorn").setLevel(logging.ERROR)
    logging.getLogger("s3fs").setLevel(logging.ERROR)
    logging.getLogger("fsspec").setLevel(logging.ERROR)
    logging.getLogger("boto3").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("pyproj").setLevel(logging.ERROR)

    warnings.simplefilter(action="ignore", category=FutureWarning)
