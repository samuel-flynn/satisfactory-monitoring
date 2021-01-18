class default_alert_processor:
    
    def __init__(self, actions):
        self.actions = actions

    async def alert(self, line, matching_rules):
        matching_rules_str = (str(rule) for rule in matching_rules)
        alert_message = f'Alert: [{",".join(matching_rules_str)}] matched: {line}'
        for action in self.actions:
            await action.execute(alert_message)
