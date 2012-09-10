#!/usr/bin/env python
# =========================================================================== #
# Name:    anichou.py
# Purpose: AnimeCollecor application starup script
#          Will be installed as executable by the setup script
#          Loads configuration and runs main routine.
#
# Copyright (c) 2009 Sebastian Bartos
# Copyright (c) 2009 Andre 'Necrotex' Peiffer
# Copyright (c) 2012 Sir Anthony
#
# License: GPL v3, see COPYING file for details
# =========================================================================== #

import os
import logging.config

from AniChou import settings
from AniChou.config import BaseConfig
from AniChou.services import Manager
from AniChou import gui

try:
    logging.config.dictConfig(settings.LOG_CONFIG)
except AttributeError:
    #python < 2.7
    import ConfigParser
    logging.config.fileConfig(settings.LOG_CONFIG_PATH)
    fileHandler = logging.handlers.RotatingFileHandler(
        settings.LOG_PATH, mode='a', maxBytes=10000, backupCount=5)
    logger = logging.getLogger('root')
    logger.addHandler(fileHandler)
    fileHandler.setFormatter(logging.Formatter(
        settings.LOG_ERROR_FORMAT, settings.LOG_ERROR_DATE))



# Check for AniChou home path existence
# Create it if not existient
if not os.path.isdir(settings.USER_PATH):
    os.mkdir(settings.USER_PATH)


# Run command line option parser and configuration parser
cfg = BaseConfig()

service = Manager(config=cfg)

## RUN THE APPLICATION
if cfg.startup.get('gui'):
    ## ONLY RUN GUI IF CLI OPTION NOT SET ##
    gui.Qt(service, cfg)
    #import AniChou.gtkctl
    #gui = AniChou.gtkctl.guictl(service, cfg)
else:
    logging.warn('no-gui option set')

logging.info('Shutting down, bye bye..')
