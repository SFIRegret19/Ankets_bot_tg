from telegram import ReplyKeyboardMarkup, Bot, Update, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, PollAnswerHandler
from credits_ankets_bor import bot_token
 
bot = Bot(token=bot_token)
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher
 
 
def poll(update, context):
    choices = ["4", "5", "3", "-4", "1000-7"]
    message = update.effective_message.reply_poll("Сколько будет 2 + 2?", choices, type=Poll.QUIZ, correct_option_id=0)
    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id,
            "message_id": message.message_id
        }
    }
    context.bot_data.update(payload)
 
def receive_poll_answer(update, context):
    answer = update.poll_answer
    poll_id = answer.poll_id

    context.bot_data[poll_id]["answers"] += 1

    if context.bot_data[poll_id]["answers"] == 3:
        context.bot.stop_poll(
            context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
        )



poll_handler = CommandHandler('poll', poll)
receive_poll_answer_handler = PollAnswerHandler(receive_poll_answer)
dispatcher.add_handler(poll_handler)
dispatcher.add_handler(receive_poll_answer_handler)



updater.start_polling()
updater.idle()