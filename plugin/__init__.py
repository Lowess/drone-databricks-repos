#!/usr/bin/env python
"""Drone plugin package."""

import os
import sys

import logging
import coloredlogs

FORMAT = "%(asctime)-15s - [%(levelname)s] - %(message)s"

logging.basicConfig(format=FORMAT, stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class DroneCli:
    """DroneCli helper to parse variables from Drone builds."""

    def __init__(self):
        """Create a DroneCli."""
        self._buildargs = os.environ

    def get(self, key, default=None):
        """Helper to retrieve Drone build vars safely."""
        if default is None:
            try:
                return self._buildargs[key]
            except KeyError as e:
                logger.error("The variable {} is mandatory but undefined".format(e))
                sys.exit(1)
        else:
            return self._buildargs.get(key, default)


# Instanciate the Drone cli
dronecli = DroneCli()

# Final logger setup
coloredlogs.install(
    level=dronecli.get("PLUGIN_LOG", "INFO"), fmt=FORMAT, logger=logger, isatty=True
)
