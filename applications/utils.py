import requests
from django.conf import settings

def send_telegram_notification(application):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not token or not chat_id:
        return

    course_name = application.course.title if application.course else "Tanlanmagan"

    # Yangi ma'lumotlar (age va note) bo'yicha Telegram xabari formatlandi
    message = (
        f"🚨 <b>Yangi ariza kelib tushdi!</b>\n\n"
        f"👤 <b>Ism:</b> {application.first_name}\n"
        f"👥 <b>Familiya:</b> {application.last_name}\n"
        f"📞 <b>Telefon:</b> {application.phone}\n"
        f"🎂 <b>Yosh:</b> {application.age}\n"
        f"💻 <b>Kurs:</b> {course_name}\n"
        f"💬 <b>Izoh:</b> {application.note or 'Yo\'q'}\n"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Telegramga xabar yuborishda xatolik: {e}")