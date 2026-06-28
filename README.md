# Job Portal (Django)

بوابة توظيف مبنية بـ **Django** تدعم اللغة العربية (RTL) ونظام الأدوار (Employer/Employee).

## المميزات
- وظائف + بحث + تصفية
- Tagging و CKEditor
- نظام أدوار المستخدمين
- لوحة إدارة Django
- مراسلة بالبريد الإلكتروني

## المتطلبات
- Python

```bash
pip install -r requirements.txt
```

## إعدادات البيئة (مطلوب)
انسخ ملف الإعدادات:

```bash
copy .env.example .env
```

ثم عدّل القيم داخل `.env` (خصوصاً `SECRET_KEY` وبيانات البريد).

## قاعدة البيانات

```bash
python manage.py makemigrations
python manage.py migrate
```

## إنشاء مستخدم مدير
```bash
python manage.py createsuperuser
```

## تشغيل السيرفر
```bash
python manage.py runserver
```

ثم افتح: http://127.0.0.1:8000

## ملاحظات
- تم تجاهل ملفات مثل قواعد البيانات المحلية وملفات البيئة في `.gitignore`.
- لا ترفع ملفات `.env` أو أي أسرار على GitHub.

