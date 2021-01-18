import logging

class logging_line_processor:
    __LOGGER = logging.getLogger(__name__)

    async def process_line(self, line):
        self.__LOGGER.info(line)