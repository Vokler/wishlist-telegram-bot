from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

REPLY_KEYBOARD = [
    ['Title', 'Link'],
    ['Image'],
    ['Done'],
]

MARKUP = ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True)


def facts_to_str(user_data) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    text = str(
        'Let\'s add a new wish to your list!\n'
        'Tell me more about your dream?'
    )
    update.message.reply_text(text, reply_markup=MARKUP)

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Yes, let\'s input {text.lower()} for your wish!')

    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    text = str(
        'Neat! Just so you know, this is what you already told me:\n'
        f'{facts_to_str(user_data)}\n'
        'You can tell me more or change your opinion on something.'
    )
    update.message.reply_text(text, reply_markup=MARKUP)

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    text = str(
        'Your new wish looks like:\n'
        f'{facts_to_str(user_data)}\n'
        'I have saved this info but you can edit it at any time.'
    )
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    user_data.clear()
    return ConversationHandler.END


new_wish_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('new_wish', start)],
    states={
        CHOOSING: [
            MessageHandler(
                Filters.regex('^(Title|Link|Image)$'), regular_choice
            ),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
)
