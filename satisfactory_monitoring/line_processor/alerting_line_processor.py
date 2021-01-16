import logging

class alerting_line_processor:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self, match_rules, alert_actions):
        self.match_rules = match_rules
        self.alert_actions = alert_actions

    def process_line(self, line):
        matching_rules = [match_rule for match_rule in self.match_rules if match_rule.matches(line)]
        if len(matching_rules) > 0:
            for alert_action in self.alert_actions:
                alert_action.alert(line, matching_rules)
