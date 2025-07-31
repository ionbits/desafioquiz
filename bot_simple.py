from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
from langdetect import detect

BOT_TOKEN = '8349056540:AAHZTPt7X9X5bJLuOrD6ZYx6EyXAwpOPgs8'

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verificar se a mensagem e o texto existem
    if not update.message or not update.message.text:
        print("Mensagem sem texto, retornando")
        return
    
    text = update.message.text
    user = update.message.from_user
    user_name = user.first_name if user and user.first_name else "Usuário"
    
    print(f"Mensagem recebida de {user_name}: {text}")
    
    if not text.strip():
        print("Texto vazio, retornando")
        return

    try:
        lang = detect(text)
        print(f"Idioma detectado: {lang}")

        # Palavras-chave para detectar português
        portuguese_words = ['olá', 'oi', 'tchau', 'obrigado', 'obrigada', 'por favor', 'desculpa', 
                           'meu', 'minha', 'nome', 'sou', 'está', 'como', 'que', 'para', 'com', 
                           'não', 'sim', 'tudo', 'bem', 'muito', 'bom', 'dia', 'noite', 'tarde']
        
        # Palavras-chave para detectar inglês
        english_words = ['hello', 'hi', 'bye', 'thank you', 'thanks', 'please', 'sorry', 
                        'my', 'name', 'is', 'how', 'are', 'you', 'what', 'where', 'when',
                        'good', 'morning', 'evening', 'night', 'yes', 'no', 'very', 'nice',
                        'alright', 'okay', 'ok', 'the', 'and', 'but', 'with', 'from']
        
        text_lower = text.lower()
        has_portuguese = any(word in text_lower for word in portuguese_words)
        has_english = any(word in text_lower for word in english_words)
        
        # Decidir idioma baseado na detecção + palavras-chave
        if lang == 'pt' or has_portuguese or lang in ['es', 'it', 'ca', 'gl', 'fr']:
            translated = GoogleTranslator(source='pt', target='en').translate(text)
            print(f"Tradução PT->EN: {translated}")
            await update.message.reply_text(f"🇺🇸 {user_name} disse:\n{translated}")
        elif lang == 'en' or has_english:
            translated = GoogleTranslator(source='en', target='pt').translate(text)
            print(f"Tradução EN->PT: {translated}")
            await update.message.reply_text(f"🇧🇷 {user_name} said:\n{translated}")
        else:
            print(f"Idioma não suportado: {lang}, tentando português por padrão...")
            # Por padrão, tenta traduzir do português se não conseguir identificar
            translated = GoogleTranslator(source='pt', target='en').translate(text)
            print(f"Tradução PT->EN (padrão): {translated}")
            await update.message.reply_text(f"🇺🇸 {user_name} disse:\n{translated}")

    except Exception as e:
        print(f"Erro detalhado: {e}")
        await update.message.reply_text("Houve um erro ao traduzir sua mensagem.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_message))

print("Bot rodando...")
app.run_polling()