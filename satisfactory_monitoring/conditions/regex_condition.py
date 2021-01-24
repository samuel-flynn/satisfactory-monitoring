import re
import logging

class regex_condition:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self, name, regex_str):
        self.name = name
        self.regex_pattern = re.compile(regex_str, re.IGNORECASE)

    def __str__(self):
        return f'{self.name}: (Regex rule: {self.regex_pattern.pattern})'

    def matches(self, line):
        match = self.regex_pattern.search(line)
        if match:
            self.__LOGGER.debug(f'Pattern {self.regex_pattern.pattern} matched line: {line}')
        return match is not None
