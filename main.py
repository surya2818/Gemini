import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import google.generativeai as genai

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key='AIzaSyB4v74PmXcRPT33W5aVpROQBSqawQQC6hI')

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

async def start(update: Update, context: CallbackContext) -> None:
    await update.effective_chat.send_action(action="typing")
    message = '''> Hello👋 \!\! I am *Gemini*\, a ChatBot trained by _Google\'s DeepMind 🧿 AI team\._
    '''
    await update.message.reply_text(message, parse_mode='MarkdownV2')

async def handle_text_query(update: Update, context: CallbackContext) -> None:
    try:
        await update.effective_chat.send_action(action="typing")

        user_input = update.message.text
        # Use "gemini-pro" model for text-only input
        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)
        response = model.generate_content(user_input, stream=True)

        generated_text = ""
        generated_message = await update.message.reply_text("Generating response...")

        # Stream the response
        for chunk in response:
            generated_text += chunk.text
            await generated_message.edit_text(generated_text)

        # Parse logic: Replace '* ' with ' ' and '**' with '*'
        parsed_text = generated_text.replace('* ', ' ').replace('**', '*')+'🤖'
        await generated_message.edit_text(parsed_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error occurred while handling text query: {e}")
        await update.message.reply_text("🚫 An error occurred while processing your request.")

def main() -> None:
    application = Application.builder().token("6637558055:AAGjz-q8VVtM53VdAKjSZ_2hXjsujDkKces").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()