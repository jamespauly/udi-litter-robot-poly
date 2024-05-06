#!/usr/bin/env python3
"""
Polyglot v3 node server Daikin Interface
Copyright (C) 2021 James Paul
"""
import udi_interface
import sys

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER

from nodes import LitterRobotController
from nodes import LitterRobot4Node

if __name__ == "__main__":
    try:
        LOGGER.debug("Staring Litter Robot Interface")
        polyglot = udi_interface.Interface([LitterRobotController, LitterRobot4Node])
        polyglot.start()
        control = LitterRobotController(polyglot, 'controller', 'controller', 'Litter Robot Controller')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
        sys.exit(0)
