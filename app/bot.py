import hashlib
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    text = inline_query.query or "echo"
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f"Result {text!r}",
        input_message_content=input_content,
    )

    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Please send the URL and description in the following format: URL DESCRIPTION\n Example: \nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ:: Never click here:: Hey check this 🙂",
        disable_web_page_preview=True,
    )


@dp.message_handler()
async def handle_message(message: Message):
    # Split the message text into the URL and description
    parts = message.text.split("::")
    if len(parts) == 3:
        url = parts[0]
        description = parts[1]
        msgtext = parts[2]

        # Create the inline button
        button = InlineKeyboardButton(text=description, url=url)
        keyboard = InlineKeyboardMarkup().add(button)

        # Send the message with the inline button
        await bot.send_message(message.chat.id, msgtext, reply_markup=keyboard)
    else:
        # The message is not in the correct format
        await bot.send_message(
            message.chat.id,
            "Please send the URL and description in the following format: URL:: BUTTONTEXT:: MSGTEXT",
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
