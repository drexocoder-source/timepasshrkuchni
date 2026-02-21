import io
import os

# Common imports for eval
import textwrap
import traceback
from contextlib import redirect_stdout

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from DazaiRobot import LOGGER, dispatcher
from DazaiRobot.modules.helper_funcs.chat_status import dev_plus

namespaces = {}


def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            "__builtins__": globals()["__builtins__"],
            "bot": bot,
            "effective_message": update.effective_message,
            "effective_user": update.effective_user,
            "effective_chat": update.effective_chat,
            "update": update,
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(f"IN: {update.effective_message.text} (user={user}, chat={chat})")


def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(chat_id=update.effective_chat.id, document=out_file)
    else:
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{msg}`",
            parse_mode=ParseMode.MARKDOWN,
        )


@dev_plus
def evaluate(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(eval, bot, update), bot, update)


@dev_plus
def execute(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(exec, bot, update), bot, update)


def cleanup_code(code):
    if code.startswith("```") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:-1])
    return code.strip("` \n")


def do(func, bot, update):
    log_input(update)

    content = update.message.text.split(" ", 1)
    if len(content) < 2:
        return "No code provided."

    body = cleanup_code(content[1])
    env = namespace_of(update.message.chat_id, update, bot)

    stdout = io.StringIO()

    # Try simple eval first
    try:
        result = eval(body, env)
        return result
    except SyntaxError:
        pass
    except Exception as e:
        return f"{e.__class__.__name__}: {e}"

    # If not eval-able, treat as exec
    to_compile = "def __func__():\n" + textwrap.indent(body, "    ")

    try:
        exec(to_compile, env)
    except Exception as e:
        return f"{e.__class__.__name__}: {e}"

    func = env["__func__"]

    try:
        with redirect_stdout(stdout):
            returned = func()
    except Exception:
        return stdout.getvalue() + traceback.format_exc()

    output = stdout.getvalue()

    if returned is not None:
        return output + str(returned)

    return output or "Done."
@dev_plus
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)


EVAL_HANDLER = CommandHandler(("e", "ev", "eva", "eval"), evaluate, run_async=True)
EXEC_HANDLER = CommandHandler(("x", "ex", "exe", "exec", "py"), execute, run_async=True)
CLEAR_HANDLER = CommandHandler("clearlocals", clear, run_async=True)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)

__mod_name__ = "Eᴠᴀʟ ᴍᴏᴅᴜʟᴇ"
