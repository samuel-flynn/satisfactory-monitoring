import re

class always_condition:

    def __str__(self):
        return f'(Always True rule)'

    def matches(self, line):
        return True
