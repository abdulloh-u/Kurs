# 💻 IT Shaharcha — O‘quv Markazi Platformasi

Farg‘ona viloyati, Toshloq tumanidagi **IT Shaharcha** zamonaviy o‘quv markazi uchun yaratilgan veb-platforma.

Platforma orqali foydalanuvchilar kurslarni ko‘rishi, onlayn ariza yuborishi va arizalar holatini boshqarish mumkin. Ma’muriyat uchun alohida boshqaruv paneli ham mavjud.

## 🚀 Asosiy imkoniyatlar

- 📚 O‘quv kurslari ro‘yxati va tavsiflari.
- 📝 Onlayn ro‘yxatdan o‘tish va kurslarga ariza yuborish.
- 👤 Ariza topshiruvchilarning ma’lumotlarini saqlash.
- 🎯 Yosh bo‘yicha tekshiruv: 10–36 yosh.
- 📊 Admin Dashboard orqali arizalarni boshqarish.
- 🔄 Ariza holatini yangilash.
- 🤖 Telegram bot orqali xabarnomalar yuborish.
- 📥 Arizalarni CSV formatida eksport qilish.
- 📱 Telefon, planshet va kompyuterga moslashuvchan dizayn.
- 🔐 Django autentifikatsiyasi va admin paneli.

## 🛠 Texnologiyalar

| Texnologiya | Vazifasi |
|---|---|
| Python | Asosiy dasturlash tili |
| Django | Backend va veb-platforma |
| SQLite | Ma’lumotlar bazasi |
| HTML5 | Sahifalar tuzilishi |
| CSS3 | Dizayn va bezaklar |
| Bootstrap 5 | Moslashuvchan interfeys |
| JavaScript | Interaktiv funksiyalar |
| Font Awesome 6 | Ikonkalar |
| SweetAlert2 | Interaktiv bildirishnomalar |
| Requests | Telegram Bot API bilan aloqa |

## 📋 Talablar

- Python 3.10 yoki undan yuqori.
- pip paket menejeri.
- VS Code yoki boshqa kod muharriri.
- Terminal.
- Internet aloqasi — Telegram xabarnomalari va tashqi resurslar uchun.

## 📁 Loyiha tuzilishi

```text
it_shaharcha/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── applications/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── utils.py
│   ├── urls.py
│   └── views.py
│
├── courses/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── apply.html
│   └── applications/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
├── .env
├── .gitignore
├── requirements.txt
├── manage.py
├── db.sqlite3
└── README.md
```

**Eslatma:** Bu namunaviy tuzilma. Papka va fayllar loyihangda mavjud bo‘lmasa, ularni o‘zing yaratishing kerak. `db.sqlite3` esa migratsiyadan so‘ng hosil bo‘lishi mumkin.

## 📦 1. Loyihani tayyorlash

Terminalda loyiha papkasiga kir:

```bash
cd ~/Music/it_shaharcha
```

Virtual muhit yarat:

```bash
python3 -m venv venv
```

Virtual muhitni faollashtir:

```bash
source venv/bin/activate
```

Faollashgandan so‘ng terminal boshida `(venv)` yozuvi ko‘rinadi.

## 📚 2. Kerakli kutubxonalarni o‘rnatish

Avval pip dasturini yangila:

```bash
python -m pip install --upgrade pip
```

`requirements.txt` mavjud bo‘lsa:

```bash
pip install -r requirements.txt
```

Agar ushbu fayl hali yaratilmagan bo‘lsa:

```bash
pip install "Django>=4.2,<5.0" requests
```

### requirements.txt

Quyidagi kutubxonalar ushbu loyihaning boshlang‘ich talablarini tashkil qiladi:

```text
Django>=4.2,<5.0
requests>=2.31
```

Faylni saqlagandan keyin kutubxonalarni quyidagicha o‘rnatish mumkin:

```bash
pip install -r requirements.txt
```

**Muhim:** Agar loyihangda qo‘shimcha Python kutubxonalari ishlatilsa, ularni ham `requirements.txt` fayliga kiritish kerak. Django versiyasi va boshqa paketlarni amaldagi loyihaga mos tanla.

## ⚙️ 3. Django sozlamalarini tekshirish

Loyiha asosiy sozlamalari `core/settings.py` faylida joylashgan.

`INSTALLED_APPS` ichida mavjud ilovalar kiritilgan bo‘lishi kerak:

```python
INSTALLED_APPS = [
    # Django standart ilovalari
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Loyiha ilovalari
    "accounts",
    "applications",
    "courses",
]
```

Bu kodni mavjud sozlamalaringni tekshirmasdan butunlay almashtirma. Agar ilovalar allaqachon kiritilgan bo‘lsa, ularni takrorlama.

## 🗄️ 4. Ma’lumotlar bazasini tayyorlash

Terminalda quyidagi buyruqlarni bajar:

```bash
python manage.py check
```

So‘ng:

```bash
python manage.py makemigrations
python manage.py migrate
```

Migratsiyalar muvaffaqiyatli bajarilgach, ma’lumotlar bazasi