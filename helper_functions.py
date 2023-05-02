import json
import logging


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def setup_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
)
