import requests
from django.conf import settings

def send_telegram_notification(application):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not token or not chat_id:
        return False # Sozlanmagan bo'lsa xatolik keltirib chiqarmaydi
    
    message = (
        f"🚀 **Yangi Ariza - IT Shaharcha!**\n\n"
        f"👤 **O'quvchi:** {application.first_name} {application.last_name}\n"
        f"🏫 **Sinf:** {application.school_grade}-sinf\n"
        f"📞 **Telefon:** {application.phone_number}\n"
        f"💻 **Kurs:** {application.course.title}\n"
        f"💬 **Izoh:** {application.comment or 'Mavjud emas'}\n"
        f"📅 **Vaqti:** {application.created_at.strftime('%Y-%m-%d %H:%M')}"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception:
        return False