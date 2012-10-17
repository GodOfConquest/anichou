#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

# Load logging system
import logging
try:
    from logging.config import dictConfig
except ImportError:
    from AniChou.dictconfig import dictConfig
from AniChou import settings
dictConfig(settings.LOG_CONFIG)

import os, sys
from AniChou import gui
from AniChou.config import BaseConfig
from AniChou.services import ServiceManager
from AniChou.tracker import tracker

# Check for AniChou home path existence
# Create it if not existient
if not os.path.isdir(settings.USER_PATH):
    os.mkdir(settings.USER_PATH)


# Run command line option parser and configuration parser
cfg = BaseConfig()
tracker.set_config(cfg)
ServiceManager.setConfig(cfg)

## RUN THE APPLICATION
if cfg.startup.get('gui'):
    ## ONLY RUN GUI IF CLI OPTION NOT SET ##
    with ServiceManager as service:
        gui.Qt(service, cfg)
else:
    logging.warn('no-gui option set')

logging.info('Shutting down, bye bye..')

try:
    tracker.stop()
except RuntimeError:
    pass

sys.exit(0)
