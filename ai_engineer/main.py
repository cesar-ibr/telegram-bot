import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

tg_bot_token = os.getenv("TG_BOT_TOKEN")
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [{
  "role": "system",
  "content": "You are a helpful assistant that answers questions."
}]

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
  messages.append({"role": "user", "content": update.message.text})
  completion = openai.chat.completions.create(model="gpt-4o-mini",
                                              messages=messages)
  completion_answer = completion.choices[0].message
  messages.append(completion_answer)

  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=completion_answer.content)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="I'm a bot, please talk to me!")
  
def start_bot() :
  application = ApplicationBuilder().token(tg_bot_token).build()
  start_handler = CommandHandler('start', start)
  chat_handler = CommandHandler('chat', chat)

  application.add_handler(start_handler)
  application.add_handler(chat_handler)
  
  application.run_polling()


if __name__ == '__main__':
  start_bot()
