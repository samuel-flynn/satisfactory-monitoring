import re
import logging

class regex_rule:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self, regex_str):
        self.regex_pattern = re.compile(regex_str, re.IGNORECASE)

    def __str__(self):
        return f'(Regex rule: {self.regex_pattern.pattern})'

    def matches(self, line):
        match = self.regex_pattern.search(line)
        if match:
            self.__LOGGER.debug(f'Pattern {self.regex_pattern.pattern} matched line: {line}')
        return match is not None
