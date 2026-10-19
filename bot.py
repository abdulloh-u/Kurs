import os
import django
import telebot

# Django muhitini ulash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from courses.models import Course
from applications.models import Application
from applications.utils import send_telegram_notification

TOKEN = '8373580640:AAHJFoAyUM6qNjI_o_nqFDtIFPa03WW4bXw'
bot = telebot.TeleBot(TOKEN)

user_sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Assalomu alaykum! IT Shaharcha o'quv markazi botiga xush kelibsiz.\n\n"
        "Bot orqali o'quv markazimizga ariza topshirish uchun /ariza buyrug'ini bosing."
    )

@bot.message_handler(commands=['ariza'])
def ask_name(message):
    msg = bot.send_message(message.chat.id, "1️⃣ Ism va familiyangizni kiriting\n(Masalan: Alisher Valiyev):")
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    full_name = message.text.strip().split()
    first_name = full_name[0] if len(full_name) > 0 else "Noma'lum"
    last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ""
    
    user_sessions[message.chat.id] = {'first_name': first_name, 'last_name': last_name}
    
    courses = Course.objects.all()
    if not courses.exists():
        bot.send_message(message.chat.id, "Hozircha faol kurslar mavjud emas.")
        return

    course_list_text = "\n".join([f"<b>{c.id}</b>. {c.title} — <i>{c.price:.0f} so'm</i>" for c in courses])
    
    msg = bot.send_message(
        message.chat.id, 
        f"2️⃣ Quyidagi kurslardan birining <b>ID raqamini</b> yuboring:\n\n{course_list_text}",
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, process_course)

def process_course(message):
    chat_id = message.chat.id
    try:
        course_id = int(message.text.strip())
        course = Course.objects.get(id=course_id)
        
        if chat_id in user_sessions:
            user_sessions[chat_id]['course'] = course
        else:
            bot.send_message(chat_id, "Xatolik yuz berdi. Qaytadan /ariza buyrug'ini bosing.")
            return

        msg = bot.send_message(chat_id, "3️⃣ Telefon raqamingizni kiriting\n(Masalan: +998901234567):")
        bot.register_next_step_handler(msg, process_phone)
    except Exception:
        msg = bot.send_message(chat_id, "⚠️ Noto'g'ri ID kiritildi. Iltimos, kurs raqamini (ID) to'g'ri raqam shaklida yuboring:")
        bot.register_next_step_handler(message, process_course)

def process_phone(message):
    chat_id = message.chat.id
    phone_number = message.text.strip()
    
    if chat_id not in user_sessions:
        bot.send_message(chat_id, "Sesiya yakunlandi. Iltimos, /ariza buyrug'ini qaytadan bosing.")
        return

    user_sessions[chat_id]['phone_number'] = phone_number

    msg = bot.send_message(chat_id, "4️⃣ Yoshingizni kiriting (10 yoshdan 36 yoshgacha):\n(Masalan: 18)")
    bot.register_next_step_handler(msg, process_age)

def process_age(message):
    chat_id = message.chat.id
    try:
        age = int(message.text.strip())
    except ValueError:
        msg = bot.send_message(chat_id, "⚠️ Iltimos, yoshingizni faqat raqam bilan kiriting (Masalan: 18):")
        bot.register_next_step_handler(msg, process_age)
        return

    # 10 va 36 yosh oralig'ini tekshirish
    if age < 10 or age > 36:
        bot.send_message(
            chat_id, 
            "⚠️ <b>Afsuski, qabul faqat 10 yoshdan 36 yoshgacha bo'lgan o'quvchilar uchun ochiq.</b>\n\nArizangiz qabul qilinmadi.",
            parse_mode='HTML'
        )
        if chat_id in user_sessions:
            del user_sessions[chat_id]
        return

    if chat_id not in user_sessions:
        bot.send_message(chat_id, "Sesiya yakunlandi. Iltimos, /ariza buyrug'ini qaytadan bosing.")
        return

    session = user_sessions[chat_id]
    
    try:
        application = Application.objects.create(
            first_name=session['first_name'],
            last_name=session['last_name'],
            phone_number=session['phone_number'],
            course=session['course'],
            school_grade=age,
            comment=f"CHAT_ID:{chat_id}",
            status='new'
        )
        
        send_telegram_notification(application)
        
        del user_sessions[chat_id]
        
        bot.send_message(
            chat_id, 
            "✅ <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n\nTez orada Qabul bo'limimiz siz bilan bog'lanadi.",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.send_message(chat_id, f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    print("🚀 Telegram bot ishga tushdi va 10-36 yosh chegagasi bilan ishlashga tayyor...")
    bot.infinity_polling()
