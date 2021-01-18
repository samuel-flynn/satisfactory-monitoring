import logging

class alerting_line_processor:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self, processors_dict):
        self.processors_dict = processors_dict

    async def process_line(self, line):
        for processor in self.processors_dict:
            conditions = self.processors_dict[processor]
            matching_conditions = [match_condition for match_condition in conditions if match_condition.matches(line)]
            if len(matching_conditions) > 0:
                    await processor.alert(line, matching_conditions)
