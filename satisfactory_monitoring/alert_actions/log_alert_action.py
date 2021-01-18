import logging

class log_alert_action:
    __LOGGER = logging.getLogger(__name__)

    async def execute(self, alert_message):
        self.__LOGGER.info(alert_message)