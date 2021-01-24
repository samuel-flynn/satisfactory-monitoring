import asyncio
import os
import re

from satisfactory_monitoring.alert_actions.discord_alert_action import \
    discord_alert_action
from satisfactory_monitoring.alert_actions.log_alert_action import \
    log_alert_action
from satisfactory_monitoring.alert_processors.default_alert_processor import \
    default_alert_processor
from satisfactory_monitoring.alert_processors.idle_alert_processor import \
    idle_alert_processor
from satisfactory_monitoring.conditions.always_condition import \
    always_condition
from satisfactory_monitoring.conditions.regex_condition import regex_condition
from satisfactory_monitoring.line_processor.alerting_line_processor import \
    alerting_line_processor
from satisfactory_monitoring.line_processor.logging_line_processor import \
    logging_line_processor
from satisfactory_monitoring.log_monitor import file_monitor

__IDLE_ALERT_THRESHOLD_SECONDS = 300

__DISCORD_TOKEN_ENV_VARIABLE = 'DISCORD_TOKEN'

async def main():
    
    token = ''
    if __DISCORD_TOKEN_ENV_VARIABLE in os.environ:
        token = os.environ[__DISCORD_TOKEN_ENV_VARIABLE]
    else:
        raise EnvironmentError(f'Environment variable {__DISCORD_TOKEN_ENV_VARIABLE} is required.')

    loop = asyncio.get_running_loop()
    
    discord_action = discord_alert_action(token, 'SnakeyServer Monitoring', 'satisfactory')
    log_action = log_alert_action()

    with idle_alert_processor([log_action, discord_action], __IDLE_ALERT_THRESHOLD_SECONDS, loop) as crash_alert_processor:
        error_alert_processor = default_alert_processor([log_action, discord_action])

        connection_problem_condition = regex_condition('Server lost connection to matchmaking', re.escape('Warning: OSS: EOSSDK-LogHttp: Retry exhausted on https://api.epicgames.dev/matchmaking/'))
        server_start_condition = regex_condition('Server started', re.escape('LogGameState: Match State Changed from WaitingToStart to InProgress'))
        server_stop_condition = regex_condition('Server shutdown', re.escape('Closing by request'))

        line_processor = alerting_line_processor({crash_alert_processor : [always_condition()], error_alert_processor : [connection_problem_condition, server_start_condition, server_stop_condition]})
        discord_task = asyncio.create_task(discord_action.start())
        file_monitor_task = file_monitor.open_watch([line_processor])

        try:
            await asyncio.gather(discord_task, file_monitor_task)
        except KeyboardInterrupt:
            await discord_action.close()

if __name__ == '__main__':
    asyncio.run(main())
