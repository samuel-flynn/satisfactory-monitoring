import logging

class log_alert_action:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self):
        pass

    def alert(self, line, matching_rules):
        rules_str = ','.join([str(rule) for rule in matching_rules])
        self.__LOGGER.info(f'Rules [{rules_str}] matched line {line}')