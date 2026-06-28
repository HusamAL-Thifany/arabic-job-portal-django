# العلاقات بين الجداول في قاعدة البيانات

## 9.1 نظرة عامة على العلاقات
المشروع يستخدم Django ORM لإدارة قاعدة البيانات مع عدة أنواع من العلاقات:

## 9.2 العلاقات المباشرة (Foreign Keys)

### 1. علاقة المستخدم بالوظائف:
```python
# في نموذج Job
user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
```
- **العلاقة:** One-to-Many (واحد إلى متعدد)
- **الوصف:** كل وظيفة تنتمي لمستخدم واحد (صاحب العمل)
- **السلوك عند الحذف:** CASCADE (حذف الوظائف عند حذف المستخدم)
- **الوصول العكسي:** `user.job_set.all()` أو `user.User.all()`

### 2. علاقة الفئة بالوظائف:
```python
# في نموذج Job
category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
```
- **العلاقة:** Many-to-One (متعدد إلى واحد)
- **الوصف:** كل وظيفة تنتمي لفئة واحدة
- **السلوك عند الحذف:** CASCADE
- **الوصول العكسي:** `category.job_set.all()` أو `category.Category.all()`

### 3. علاقة المستخدم بالطلبات:
```python
# في نموذج Applicant
user = models.ForeignKey(User, on_delete=models.CASCADE)
job = models.ForeignKey(Job, on_delete=models.CASCADE)
```
- **العلاقة:** Many-to-Many عبر جدول وسيط
- **الوصف:** كل مستخدم يمكنه التقدم لعدة وظائف
- **السلوك عند الحذف:** CASCADE

### 4. علاقة المستخدم بالوظائف المحفوظة:
```python
# في نموذج BookmarkJob
user = models.ForeignKey(User, on_delete=models.CASCADE)
job = models.ForeignKey(Job, on_delete=models.CASCADE)
```
- **العلاقة:** Many-to-Many عبر جدول وسيط
- **الوصف:** كل مستخدم يمكنه حفظ عدة وظائف

## 9.3 العلاقات العكسية (Reverse Relations)

### من نموذج User:
```python
# الوظائف التي نشرها المستخدم
user.job_set.all()  # أو user.User.all() بسبب related_name='User'

# طلبات التقدم للمستخدم
user.applicant_set.all()

# الوظائف المحفوظة للمستخدم
user.bookmarkjob_set.all()
```

### من نموذج Job:
```python
# المتقدمون للوظيفة
job.applicant_set.all()

# المستخدمون الذين حفظوا الوظيفة
job.bookmarkjob_set.all()
```

### من نموذج Category:
```python
# الوظائف في هذه الفئة
category.job_set.all()  # أو category.Category.all()
```

## 9.4 أمثلة على الاستعلامات المعقدة

### استعلامات متداخلة:
```python
# جميع الوظائف لمستخدم معين مع الفئات
jobs = Job.objects.filter(user=user).select_related('category', 'user')

# جميع المتقدمين لوظيفة معينة مع بيانات المستخدمين
applicants = Applicant.objects.filter(job=job).select_related('user')
```

### استعلامات مع الشروط:
```python
# الوظائف المنشورة والمفتوحة فقط
active_jobs = Job.objects.filter(
    is_published=True,
    is_closed=False
).select_related('user', 'category')

# المتقدمون للوظائف في فئة معينة
applicants_in_category = Applicant.objects.filter(
    job__category=category
).select_related('user', 'job')
```

## 9.5 العلاقات الخاصة

### نظام العلامات (Tagging):
```python
# في نموذج Job
tags = TaggableManager()

# أمثلة على الاستخدام:
# البحث عن وظائف تحتوي على علامة معينة
jobs_with_python = Job.objects.filter(tags__name__in=["Python"])

# الوظائف المشابهة حسب العلامات
similar_jobs = job.tags.similar_objects()
```

### محرر النصوص المنسقة:
```python
# في نموذج Job
description = RichTextField()
company_description = RichTextField(blank=True, null=True)
```

## 9.6 رسم بياني للعلاقات

```
User (المستخدمين)
├── Job (الوظائف) [One-to-Many]
│   ├── Category (الفئات) [Many-to-One]
│   ├── Applicant (المتقدمون) [Many-to-Many عبر جدول وسيط]
│   └── BookmarkJob (المحفوظات) [Many-to-Many عبر جدول وسيط]
│
Category (الفئات)
└── Job (الوظائف) [One-to-Many]

Job (الوظائف)
├── User (المستخدمين) [Many-to-One]
├── Category (الفئات) [Many-to-One]
├── Applicant (المتقدمون) [One-to-Many]
└── BookmarkJob (المحفوظات) [One-to-Many]
```

## 9.7 جداول قاعدة البيانات الناتجة

### الجداول الرئيسية:
1. **account_user** - بيانات المستخدمين
2. **jobapp_category** - فئات الوظائف
3. **jobapp_job** - الوظائف
4. **jobapp_applicant** - طلبات التقدم
5. **jobapp_bookmarkjob** - الوظائف المحفوظة

### جداول Django الإضافية:
- **taggit_tag** - العلامات
- **taggit_taggeditem** - ربط العلامات بالمحتوى
- **auth_permissions** - الصلاحيات
- **django_content_type** - أنواع المحتوى

## 9.8 أمثلة على استخدام العلاقات في Views

### في dashboard_view:
```python
# لأصحاب العمل - الوظائف الخاصة بهم
jobs = Job.objects.filter(user=request.user.id)

# عدد المتقدمين لكل وظيفة
for job in jobs:
    count = Applicant.objects.filter(job=job.id).count()
    total_applicants[job.id] = count
```

### في search_result_view:
```python
# البحث بالعنوان أو اسم الشركة
job_list = job_list.filter(title__icontains=job_title_or_company_name) | \
           job_list.filter(company_name__icontains=job_title_or_company_name)

# البحث بالموقع
job_list = job_list.filter(location__icontains=location)
```

## 9.9 تحسينات الأداء للعلاقات

### Select Related:
```python
# تحميل البيانات المرتبطة مع الاستعلام الرئيسي
jobs = Job.objects.select_related('user', 'category').all()
```

### Prefetch Related:
```python
# تحميل العلاقات المتعددة مسبقاً
jobs = Job.objects.prefetch_related('applicant_set', 'bookmarkjob_set').all()
```

### تجنب N+1 Queries:
```python
# بدلاً من:
for job in jobs:
    print(job.user.first_name)  # استعلام منفصل لكل وظيفة

# استخدم:
jobs = Job.objects.select_related('user').all()
for job in jobs:
    print(job.user.first_name)  # بيانات محملة مسبقاً
```

هذا النظام من العلاقات يوفر مرونة عالية في إدارة البيانات ويسهل عمليات البحث والتصفية المعقدة.
