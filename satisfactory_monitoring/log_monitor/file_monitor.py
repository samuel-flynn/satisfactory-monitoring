import logging
import os
import asyncio

__SATISFACTORY_LOG_PATH_ENV_VAR = 'SATISFACTORY_LOG_PATH'
__WINDOWS_LOCALAPPDATA_ENV_VAR = 'LOCALAPPDATA'
__LOGGER = logging.getLogger(__name__)

async def open_watch(processors):

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
    try:
        while True:
            try:
                with open(log_path, 'rb') as log_file:
                    __LOGGER.info(f'Beginning watch on file: {log_path}')
                    current_position = 0
                    while True:
                        line = ''
                        while len(line) == 0 or line[-1] != '\n':

                            __check_for_rotation(log_file, current_position)

                            tail = log_file.readline()

                            if len(tail) == 0:
                                if not reached_tail_flag:
                                    __LOGGER.info('Reached log tail')
                                    reached_tail_flag = True
                                await asyncio.sleep(1)
                            else:
                                line += tail.decode('utf-8')
                            current_position = log_file.tell()
                        for processor in processors:
                            await processor.process_line(line.strip())
            except IOError as e:
                __LOGGER.info(f'IOError: {str(e)}')
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        __LOGGER.info(f'Terminating watch on {log_path}.')

def __check_for_rotation(log_file, current_position):

    # Seek to the end of the file and get the position
    log_file.seek(0, 2)
    end_position = log_file.tell()

    # If the end position is before our last known position, just go to the beginning. Otherwise, put the pointer back where it was
    if end_position < current_position:
        __LOGGER.debug(f'Seeking to beginning of log because end_position: {end_position} '
            f'< current_position: {current_position}')
        log_file.seek(0, 0)
    else:
        log_file.seek(current_position, 0)