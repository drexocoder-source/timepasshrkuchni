import logging
import glob
from os.path import basename, dirname, isfile
from DazaiRobot.config import LOAD, NO_LOAD

LOGGER = logging.getLogger(__name__)

def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f)
        and f.endswith(".py")
        and not f.endswith("__init__.py")
    ]

    if LOAD:
        if not all(mod in all_modules for mod in LOAD):
            LOGGER.error("Invalid LOAD names detected. Quitting...")
            quit(1)

        all_modules = sorted(set(all_modules) - set(LOAD))
        to_load = list(all_modules) + LOAD
    else:
        to_load = all_modules

    if NO_LOAD:
        LOGGER.info("Not loading: %s", NO_LOAD)
        to_load = [mod for mod in to_load if mod not in NO_LOAD]

    return to_load


ALL_MODULES = __list_all_modules()

LOGGER.info("Modules to load: %s", ALL_MODULES)

__all__ = ALL_MODULES + ["ALL_MODULES"]
