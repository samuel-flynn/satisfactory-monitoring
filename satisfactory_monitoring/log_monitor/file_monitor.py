import logging
import os
import asyncio

__SATISFACTORY_LOG_PATH_ENV_VAR = 'SATISFACTORY_LOG_PATH'
__WINDOWS_LOCALAPPDATA_ENV_VAR = 'LOCALAPPDATA'

async def open_watch(processors):

    logger = logging.getLogger(__name__)

    log_path = ''
    if __SATISFACTORY_LOG_PATH_ENV_VAR in os.environ:
        log_path = os.environ[__SATISFACTORY_LOG_PATH_ENV_VAR]
    elif __WINDOWS_LOCALAPPDATA_ENV_VAR in os.environ:
        log_path = os.path.join(os.environ[__WINDOWS_LOCALAPPDATA_ENV_VAR], 'FactoryGame', 'Saved', 'Logs', 'FactoryGame.log')
    else:
        raise EnvironmentError(f'Unable to determine Satisfactory log location. Please set environment variable {__SATISFACTORY_LOG_PATH_ENV_VAR} to the location of FactoryGame.log')
    
    if not os.path.isfile(log_path):
        raise EnvironmentError(f'Unable to find file {log_path}. Please set environment variable {__SATISFACTORY_LOG_PATH_ENV_VAR} to the location of FactoryGame.log')

    reached_tail_flag = False
    
    # Source: https://stackoverflow.com/a/11909303
    with open(log_path) as log_file:
        try:
            logger.info(f'Beginning watch on file: {log_path}')
            while True:
                line = ''
                while len(line) == 0 or line[-1] != '\n':
                    tail = log_file.readline()
                    if tail == '':
                        if not reached_tail_flag:
                            logger.info('Reached log tail')
                            reached_tail_flag = True
                        await asyncio.sleep(1)
                    else:
                        line += tail
                for processor in processors:
                    await processor.process_line(line.strip())
        except KeyboardInterrupt:
            logger.info(f'Terminating watch on {log_path}.')