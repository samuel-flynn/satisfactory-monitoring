from satisfactory_monitoring.line_processor.logging_line_processor import logging_line_processor
from satisfactory_monitoring.line_processor.alerting_line_processor import alerting_line_processor
from satisfactory_monitoring.log_monitor import file_monitor
from satisfactory_monitoring.alert_actions.discord_alert_action import discord_alert_action
from satisfactory_monitoring.alert_actions.log_alert_action import log_alert_action
from satisfactory_monitoring.line_processor.alerting.regex_rule import regex_rule

def main():
    log_processor = logging_line_processor()
    discord_alert = discord_alert_action()
    log_alert = log_alert_action()
    shutdown_regex_rule = regex_rule(r'shut[^ ]* down')


    alert_processor = alerting_line_processor([shutdown_regex_rule], [discord_alert, log_alert])
    file_monitor.open_watch([alert_processor])

if __name__ == '__main__':
    main()