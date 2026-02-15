import logging
from DazaiRobot.config import *

LOGGER = logging.getLogger("DazaiRobot")

# Role groups
DRAGONS = set()
DEV_USERS.add(int(OWNER_ID))
DEV_AND_MORE = DEV_USERS

DEMONS = set()
TIGERS = set()
WOLVES = set()
