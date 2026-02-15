import os

ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("TOKEN")
    OWNER_ID = int(os.environ.get("OWNER_ID"))

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", "True") == "True"
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", "False") == "True"
    CASH_API_KEY = os.environ.get("CASH_API_KEY")
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = os.environ.get("DEL_CMDS", "False") == "True"
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    INFOPIC = os.environ.get("INFOPIC", "True") == "True"
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")

    START_IMG = os.environ.get(
        "START_IMG",
        "https://telegra.ph/file/ad2b38da713ceb2f6085b.jpg"
    )

    STRICT_GBAN = os.environ.get("STRICT_GBAN", "True") == "True"
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "NexoraSupportchat")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TIME_API_KEY = os.environ.get("TIME_API_KEY")
    WORKERS = int(os.environ.get("WORKERS", 8))
    ARQ_API_URL = os.environ.get("ARQ_API_URL", "http://thearq.tech?")
    ARQ_API_KEY = os.environ.get(
        "ARQ_API_KEY",
        "FZPYYN-EKAYFK-RNPLEJ-DRVAPH-ARQ"
    )

    BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split() if x)
    DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split() if x)
    DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split() if x)
    DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split() if x)
    TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split() if x)
    WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split() if x)

else:
    from DazaiRobot.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    OWNER_ID = int(Config.OWNER_ID)

    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DB_URI = Config.DATABASE_URL
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    MONGO_DB_URI = Config.MONGO_DB_URI
    START_IMG = Config.START_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS
    ARQ_API_KEY = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL

    BL_CHATS = set(Config.BL_CHATS or [])
    DRAGONS = set(Config.DRAGONS or [])
    DEMONS = set(Config.DEMONS or [])
    TIGERS = set(Config.TIGERS or [])
    WOLVES = set(Config.WOLVES or [])
