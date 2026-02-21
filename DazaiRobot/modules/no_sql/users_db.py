from DazaiRobot import dispatcher
from DazaiRobot.modules.no_sql import get_collection

USERS_DB = get_collection("USERS")
CHATS_DB = get_collection("CHATS")
CHAT_MEMBERS_DB = get_collection("CHAT_MEMBERS")


# ─────────────────────────────────────
# ✅ ENSURE BOT EXISTS IN DATABASE
# ─────────────────────────────────────
def ensure_bot_in_db():
    if dispatcher.bot:
        USERS_DB.update_one(
            {"_id": dispatcher.bot.id},
            {
                "$set": {
                    "username": dispatcher.bot.username,
                    "is_bot": True,
                }
            },
            upsert=True,
        )


# ─────────────────────────────────────
# ✅ UPDATE USER + CHAT + MEMBER ENTRY
# ─────────────────────────────────────
def update_user(user_id, username=None, chat_id=None, chat_name=None):

    if not user_id:
        return

    # Update User
    USERS_DB.update_one(
        {"_id": user_id},
        {
            "$set": {
                "username": username or "Unknown"
            }
        },
        upsert=True,
    )

    # If no chat info provided, stop here
    if not chat_id:
        return

    # Update Chat
    CHATS_DB.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "chat_name": chat_name or "Unknown"
            }
        },
        upsert=True,
    )

    # Ensure membership exists (no duplicates)
    if not CHAT_MEMBERS_DB.find_one({"chat_id": chat_id, "user_id": user_id}):
        CHAT_MEMBERS_DB.insert_one({
            "chat_id": chat_id,
            "user_id": user_id
        })


# ─────────────────────────────────────
# ✅ FETCH FUNCTIONS (SAFE RETURNS)
# ─────────────────────────────────────
def get_userid_by_name(username) -> list:
    if not username:
        return []
    return list(USERS_DB.find({"username": username}))


def get_name_by_userid(user_id) -> dict:
    if not user_id:
        return {}
    return USERS_DB.find_one({"_id": user_id}) or {}


def get_chat_members(chat_id) -> list:
    return list(CHAT_MEMBERS_DB.find({"chat_id": chat_id}))


def get_all_chats() -> list:
    return list(CHATS_DB.find())


def get_all_users() -> list:
    return list(USERS_DB.find())


# ─────────────────────────────────────
# ✅ COUNT FUNCTIONS (OPTIMIZED)
# ─────────────────────────────────────
def get_user_num_chats(user_id) -> int:
    return CHAT_MEMBERS_DB.count_documents({"user_id": user_id})


def get_user_com_chats(user_id) -> list:
    return list(CHAT_MEMBERS_DB.find({"user_id": user_id}))


def num_chats() -> int:
    return CHATS_DB.count_documents({})


def num_users() -> int:
    return USERS_DB.count_documents({})


# ─────────────────────────────────────
# ✅ REMOVE CHAT (WITH CLEANUP)
# ─────────────────────────────────────
def rem_chat(chat_id) -> None:
    CHATS_DB.delete_one({"chat_id": chat_id})
    CHAT_MEMBERS_DB.delete_many({"chat_id": chat_id})


# ─────────────────────────────────────
# ✅ MIGRATE CHAT (SUPERGROUP MIGRATION FIX)
# ─────────────────────────────────────
def migrate_chat(old_chat_id, new_chat_id) -> None:

    # Update Chat ID
    CHATS_DB.update_one(
        {"chat_id": old_chat_id},
        {"$set": {"chat_id": new_chat_id}}
    )

    # Update All Members
    CHAT_MEMBERS_DB.update_many(
        {"chat_id": old_chat_id},
        {"$set": {"chat_id": new_chat_id}}
    )


# ─────────────────────────────────────
# ✅ CREATE INDEXES (IMPORTANT FOR BIG BOTS)
# ─────────────────────────────────────
def create_indexes():
    USERS_DB.create_index("username")
    CHATS_DB.create_index("chat_id")
    CHAT_MEMBERS_DB.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )


# Initialize
ensure_bot_in_db()
create_indexes()