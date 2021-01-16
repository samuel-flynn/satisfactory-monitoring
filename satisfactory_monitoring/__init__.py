import json
import os
import logging
import logging.config

__VERSION__ = '0.0.1'
resources_dir = os.path.join(os.path.dirname(__file__), 'resources')

def setup_logging():
    with open(os.path.join(resources_dir, 'logging-config.json'), 'r') as fp:
        logging_config = json.load(fp)
        logging.config.dictConfig(logging_config)
    
    logging.getLogger().info('Logging initialized')

setup_logging()
