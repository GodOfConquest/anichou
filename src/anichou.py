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

from AniChou import settings
from AniChou.config import BaseConfig
from AniChou.services import Manager




## FIRST RUN STUFF

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
    import AniChou.gtkctl
    gui = AniChou.gtkctl.guictl(service, cfg)
else:
    print 'no-gui option set'


print 'Shutting down, bye bye..'
