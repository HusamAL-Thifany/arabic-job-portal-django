# وثائق مشروع بوابة التوظيف - Job Portal Django Project

## نظرة عامة على المشروع
بوابة توظيف مبنية بـ Django 3.0 تدعم اللغة العربية بالكامل وتحتوي على نظام إدارة وظائف متكامل.

## 1. ملف الإعدادات - `job/settings.py`

### المعلومات الأساسية:
- **نوع المشروع:** Django 3.0
- **الغرض:** بوابة توظيف (Job Portal)
- **اللغة الافتراضية:** العربية (`LANGUAGE_CODE = 'ar'`)

### الأقسام الرئيسية:

#### الأمان والإعدادات الأساسية:
```python
SECRET_KEY = 'etdq)uvq=t0rc&ams5_ovn6w8bcwknjj0u97*(#n^(76x*+dr1'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'djobportal.herokuapp.com']
```

#### التطبيقات المثبتة:
```python
INSTALLED_APPS = [
    # تطبيقات Django الأساسية
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # تطبيقات المشروع
    'jobapp.apps.JobappConfig',      # تطبيق الوظائف
    'account.apps.AccountConfig',    # تطبيق الحسابات

    # تطبيقات خارجية
    'ckeditor',      # محرر نصوص
    'taggit',        # نظام العلامات
    'user_visit',    # تتبع زيارات المستخدمين
    'debug_toolbar', # شريط أدوات التطوير
]
```

#### قاعدة البيانات:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### الإعدادات الدولية:
```python
LANGUAGE_CODE = 'ar'  # اللغة العربية
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
```

#### الملفات الثابتة:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
```

#### نموذج المستخدم المخصص:
```python
AUTH_USER_MODEL = 'account.User'
```

#### إعدادات CKEditor:
```python
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'tabSpaces': 4,
    }
}
```

#### إعدادات البريد الإلكتروني:
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "wwohohoasas@gmail.com"
EMAIL_HOST_PASSWORD = "jfra ekst yywr ofsu"
```

## 2. تطبيق الوظائف - `jobapp/`

### 2.1 ملف النماذج - `jobapp/models.py`

#### الثوابت:
```python
JOB_TYPE = (
    ('1', _("Full time")),
    ('2', _("Part time")),
    ('3', _("Internship")),
)
```

#### نموذج Category (الفئات):
```python
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
```

#### نموذج Job (الوظائف):
```python
class Job(models.Model):
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
```

#### نموذج Applicant (المتقدمون):
```python
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
```

#### نموذج BookmarkJob (الوظائف المحفوظة):
```python
class BookmarkJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
```

### 2.2 ملف الصلاحيات - `jobapp/permission.py`

#### دالة user_is_employer:
```python
def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
```

#### دالة user_is_employee:
```python
def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
```

### 2.3 ملف النماذج - `jobapp/forms.py`

#### نموذج JobForm (إنشاء وظيفة):
```python
class JobForm(forms.ModelForm):
    # يحتوي على جميع حقول الوظيفة مع تخصيصات عربية
    # تسميات ورسائل مساعدة بالعربية
    # تحقق من صحة البيانات
```

#### نموذج JobApplyForm (التقدم للوظيفة):
```python
class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']
```

#### نموذج JobEditForm (تعديل الوظيفة):
```python
class JobEditForm(forms.ModelForm):
    # مشابه لـ JobForm لكن للتعديل
```

#### نموذج EmailCommunicationForm (التواصل بالبريد):
```python
class EmailCommunicationForm(forms.Form):
    title = forms.CharField(max_length=200)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
```

### 2.4 ملف العرض - `jobapp/views.py`

#### الدوال الرئيسية:

##### home_view:
- عرض الصفحة الرئيسية
- إحصائيات الوظائف والمستخدمين
- دعم AJAX للتحميل التدريجي

##### job_list_View:
- عرض قائمة الوظائف
- تخزين مؤقت لمدة 15 دقيقة
- ترقيم الصفحات

##### create_job_View:
- إنشاء وظيفة جديدة (لأصحاب العمل فقط)
- التحقق من صحة البيانات

##### single_job_view:
- عرض تفاصيل الوظيفة
- الوظائف المشابهة حسب العلامات

##### search_result_view:
- البحث في الوظائف
- معايير متعددة (العنوان، الموقع، النوع)

##### apply_job_view:
- التقدم للوظيفة (للموظفين فقط)
- منع التقدم المكرر

##### dashboard_view:
- لوحة تحكم المستخدم
- عرض الوظائف والمتقدمين حسب الدور

### 2.5 ملف الإدارة - `jobapp/admin.py`

#### تسجيل النماذج في لوحة التحكم:

##### ApplicantAdmin:
```python
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
```

##### JobAdmin:
```python
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')
```

##### BookmarkJobAdmin:
```python
class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
```

## 3. تطبيق الحسابات - `account/`

### 3.1 نموذج المستخدم - `account/models.py`

#### نموذج User:
```python
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=GENDER_TYPE, max_length=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
```

#### الثوابت:
```python
GENDER_TYPE = (
    ('M', "Male"),
    ('F', "Female"),
)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)
```

### 3.2 نماذج الحسابات - `account/forms.py`

#### EmployeeRegistrationForm:
- تسجيل الموظفين
- حقول: الاسم، البريد، كلمة المرور، الجنس
- تخصيصات عربية

#### EmployerRegistrationForm:
- تسجيل أصحاب العمل
- first_name: اسم الشركة
- last_name: عنوان الشركة

#### UserLoginForm:
- تسجيل الدخول
- التحقق من صحة البيانات

#### EmployeeProfileEditForm:
- تعديل الملف الشخصي
- تحديث البيانات الأساسية

## 4. المميزات الرئيسية للمشروع

### 4.1 دعم اللغة العربية:
- جميع النصوص والرسائل بالعربية
- دعم RTL (Right-to-Left)
- ترجمة شاملة للواجهة

### 4.2 نظام الأدوار:
- **Employer (صاحب العمل):**
  - نشر الوظائف
  - مراجعة المتقدمين
  - إدارة الوظائف

- **Employee (الموظف):**
  - البحث عن الوظائف
  - التقدم للوظائف
  - حفظ الوظائف المفضلة

### 4.3 نظام متقدم للوظائف:
- محرر نصوص متقدم (CKEditor)
- نظام العلامات (Tagging)
- تصنيف الوظائف
- بحث متقدم
- حفظ ومتابعة الوظائف

### 4.4 إدارة المحتوى:
- لوحة إدارة Django
- إدارة الوظائف والمستخدمين
- مراقبة النشاط

### 4.5 التواصل والإشعارات:
- نظام البريد الإلكتروني
- إشعارات القبول والرفض
- تواصل بين المستخدمين

## 5. التقنيات المستخدمة

### 5.1 Django وإضافاته:
- Django 3.0
- Django Admin
- Django Authentication
- Django Forms
- Django ORM

### 5.2 مكتبات خارجية:
- **CKEditor:** محرر نصوص متقدم
- **django-taggit:** نظام العلامات
- **user_visit:** تتبع زيارات المستخدمين
- **debug_toolbar:** أدوات التطوير

### 5.3 قاعدة البيانات:
- SQLite (للتطوير)
- دعم PostgreSQL (للإنتاج)

### 5.4 الواجهة الأمامية:
- Bootstrap 4
- CSS مخصص
- JavaScript للتفاعل
- AJAX للتحديث الديناميكي

## 6. كيفية التشغيل

### 6.1 متطلبات النظام:
```bash
pip install -r requirements.txt
```

### 6.2 إعداد قاعدة البيانات:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.3 إنشاء مستخدم إدارة:
```bash
python manage.py createsuperuser
```

### 6.4 تشغيل الخادم:
```bash
python manage.py runserver
```

## 7. الأمان والأداء

### 7.1 الأمان:
- تشفير كلمات المرور
- حماية CSRF
- التحقق من الصلاحيات
- منع الوصول غير المصرح

### 7.2 الأداء:
- تخزين مؤقت للوظائف
- ترقيم الصفحات
- تحسين قاعدة البيانات
- ضغط الملفات الثابتة

## 8. التطوير والصيانة

### 8.1 هيكل المشروع:
```
Job-Portal-Django-master/
├── account/           # تطبيق الحسابات
├── job/              # إعدادات المشروع
├── jobapp/           # تطبيق الوظائف
├── static/           # الملفات الثابتة
├── template/         # القوالب
└── screenshots/      # لقطات الشاشة
```

### 8.2 قاعدة البيانات:
- نماذج مرنة وقابلة للتوسع
- علاقات محسنة
- فهارس للأداء

### 8.3 الاختبار:
- اختبارات النماذج
- اختبارات العرض
- اختبارات النماذج

---

## المؤلف: فريق تطوير بوابة التوظيف
## الإصدار: 1.0
## تاريخ آخر تحديث: 2024
