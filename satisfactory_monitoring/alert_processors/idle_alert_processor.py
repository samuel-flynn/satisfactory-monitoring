import threading

class idle_alert_processor:

    def __init__(self, actions, idle_time_seconds):
        self.actions = actions
        self.idle_time_seconds = idle_time_seconds
        self.timer = threading.Timer(self.idle_time_seconds, self.__idle_action)

    def __idle_action(self):
        alert_message = f'Alert: It\'s been {self.idle_time_seconds} since last log message. Did the server crash?'
        for action in self.actions:
            action.execute(alert_message)
    
    async def alert(self, line, matching_rules):
        """We are alerting if we recieve no messages in {self.idle_time_seconds}, so just reset the timer when we do get one."""

        self.timer.cancel()
        self.timer = threading.Timer(self.idle_time_seconds, self.__idle_action)
        self.timer.start()

    def __enter__(self):
        self.timer.start()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.timer.cancel()