#! /usr/bin/env python

'''
    PURPOSE: Determine which executable to run and then passes all arguments
             through to the appropriate script.

    PROJECT: Land Satellites Data Systems Science Research and Development
             (LSRD) at the USGS EROS

    LICENSE: NASA Open Source Agreement 1.3

    AUTHOR: ngenetzky@usgs.gov

    NOTES:
        This script does not have its own help message and will just return the
            help from underlying executables where appropriate.
        If this script has a required argument then only the usage for that
            argument will be shown if that argument is not included.
        All output from the underlying script will be given to the logger as an
            info message.
'''

import os
import sys
import logging
import commands


class ExecuteError(Exception):
    '''Raised when command in execute_cmd returns with error'''

    def __init__(self, message, *args):
        self.message = message
        Exception.__init__(self, message, *args)


def execute_cmd(cmd_string):
    '''Execute a command line and return the terminal output

    Raises:
        ExecuteError (Stdout/Stderr)

    Returns:
        output:The stdout and/or stderr from the executed command.
    '''

    (status, output) = commands.getstatusoutput(cmd_string)

    if status < 0:
        message = ('Application terminated by signal [{0}]'
                   .format(cmd_string))
        if len(output) > 0:
            message = ' Stdout/Stderr is: '.join([message, output])
        raise ExecuteError(message)

    if status != 0:
        message = 'Application failed to execute [{0}]'.format(cmd_string)
        if len(output) > 0:
            message = ' Stdout/Stderr is: '.join([message, output])
        raise ExecuteError(message)

    if os.WEXITSTATUS(status) != 0:
        message = ('Application [{0}] returned error code [{1}]'
                   .format(cmd_string, os.WEXITSTATUS(status)))
        if len(output) > 0:
            message = ' Stdout/Stderr is: '.join([message, output])
        raise ExecuteError(message)

    return output


def get_science_application_name():
    '''Returns name of executable that needs to be called'''

    return 'spectral_indices'


def main():
    '''Determines executable, and calls it with all input arguments '''

    # Setup the default logger format and level.  Log to STDOUT.
    logging.basicConfig(format=('%(asctime)s.%(msecs)03d %(process)d'
                                ' %(levelname)-8s'
                                ' %(filename)s:%(lineno)d:'
                                '%(funcName)s -- %(message)s'),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        stream=sys.stdout)

    # Get the logger
    logger = logging.getLogger(__name__)

    # Get the science application
    cmd = [get_science_application_name()]

    # Pass all arguments through to the science application
    cmd.extend(sys.argv[1:])

    # Convert the list to a string
    cmd_string = ' '.join(cmd)
    try:
        logger.info(' '.join(['EXECUTING SCIENCE APPLICATION:',
                              cmd_string]))
        output = execute_cmd(cmd_string)

        if len(output) > 0:
            logger.info('\n{0}'.format(output))
    except ExecuteError:
        logger.exception('Error running {0}.'
                         'Processing will terminate.'
                         .format(os.path.basename(__file__)))
        raise  # Re-raise so exception message will be shown.

if __name__ == '__main__':
    main()
