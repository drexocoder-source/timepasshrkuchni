from pyrate_limiter import (
    BucketFullException,
    Duration,
    Limiter,
    MemoryListBucket,
    RequestRate,
)

from telegram import Update
from telegram.ext import CommandHandler, Filters, MessageHandler, RegexHandler

import DazaiRobot.modules.sql.blacklistusers_sql as sql
from DazaiRobot import ALLOW_EXCL, DEMONS, DEV_USERS, DRAGONS, TIGERS, WOLVES


# ───────────────── COMMAND PREFIX ─────────────────
if ALLOW_EXCL:
    CMD_STARTERS = ("/", "!")
else:
    CMD_STARTERS = ("/",)


# ───────────────── ANTISPAM ─────────────────
class AntiSpam:
    def __init__(self):
        # ✅ FIXED: convert sets safely to list
        self.whitelist = (
            list(DEV_USERS)
            + list(DRAGONS)
            + list(WOLVES)
            + list(DEMONS)
            + list(TIGERS)
        )

        Duration.CUSTOM = 15  # 15 seconds

        self.sec_limit = RequestRate(6, Duration.CUSTOM)
        self.min_limit = RequestRate(20, Duration.MINUTE)
        self.hour_limit = RequestRate(100, Duration.HOUR)
        self.daily_limit = RequestRate(1000, Duration.DAY)

        self.limiter = Limiter(
            self.sec_limit,
            self.min_limit,
            self.hour_limit,
            self.daily_limit,
            bucket_class=MemoryListBucket,
        )

    def check_user(self, user):
        if user in self.whitelist:
            return False

        try:
            self.limiter.try_acquire(user)
            return False
        except BucketFullException:
            return True


SpamChecker = AntiSpam()
MessageHandlerChecker = AntiSpam()


# ───────────────── CUSTOM COMMAND HANDLER ─────────────────
class CustomCommandHandler(CommandHandler):
    def __init__(self, command, callback, admin_ok=False, allow_edit=False, **kwargs):
        super().__init__(command, callback, **kwargs)

        if allow_edit is False:
            self.filters &= ~(
                Filters.update.edited_message | Filters.update.edited_channel_post
            )

    def check_update(self, update):
        if isinstance(update, Update) and update.effective_message:
            message = update.effective_message

            try:
                user_id = update.effective_user.id
            except Exception:
                user_id = None

            if user_id and sql.is_user_blacklisted(user_id):
                return False

            if message.text and len(message.text) > 1:
                fst_word = message.text.split(None, 1)[0]

                if any(fst_word.startswith(start) for start in CMD_STARTERS):
                    args = message.text.split()[1:]
                    command = fst_word[1:].split("@")
                    command.append(message.bot.username)

                    if user_id == 1087968824:
                        user_id = update.effective_chat.id

                    if not (
                        command[0].lower() in self.command
                        and command[1].lower() == message.bot.username.lower()
                    ):
                        return None

                    if SpamChecker.check_user(user_id):
                        return None

                    filter_result = self.filters(update)
                    if filter_result:
                        return args, filter_result
                    else:
                        return False

    def handle_update(self, update, dispatcher, check_result, context=None):
        if context:
            self.collect_additional_context(context, update, dispatcher, check_result)
            return self.callback(update, context)
        else:
            optional_args = self.collect_optional_args(
                dispatcher, update, check_result
            )
            return self.callback(dispatcher.bot, update, **optional_args)

    def collect_additional_context(
        self, context, update, dispatcher, check_result
    ):
        if isinstance(check_result, bool):
            context.args = update.effective_message.text.split()[1:]
        else:
            context.args = check_result[0]
            if isinstance(check_result[1], dict):
                context.update(check_result[1])


# ───────────────── REGEX HANDLER ─────────────────
class CustomRegexHandler(RegexHandler):
    def __init__(self, pattern, callback, friendly="", **kwargs):
        super().__init__(pattern, callback, **kwargs)


# ───────────────── MESSAGE HANDLER ─────────────────
class CustomMessageHandler(MessageHandler):
    def __init__(self, filters, callback, friendly="", allow_edit=False, **kwargs):
        super().__init__(filters, callback, **kwargs)

        if allow_edit is False:
            self.filters &= ~(
                Filters.update.edited_message | Filters.update.edited_channel_post
            )
