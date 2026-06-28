# -*- coding: utf-8 -*-
"""
Account Forms Module - نماذج الحساب
====================================

هذا الملف يحتوي على جميع نماذج (Forms) الخاصة بنظام الحسابات في بوابة الوظائف.
يتم استخدام Django Forms لإنشاء وتعديل حسابات الموظفين وأصحاب العمل.

Contains all account-related forms for the Job Portal system.
Uses Django Forms for creating and editing employee and employer accounts.

Author: Job Portal Development Team
Last Modified: 2024
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _  # لدعم الترجمة العربية

from account.models import User


class EmployeeRegistrationForm(UserCreationForm):
    """
    نموذج تسجيل الموظف - Employee Registration Form

    هذا النموذج يُستخدم لإنشاء حسابات جديدة للموظفين الباحثين عن عمل.
    يرث من UserCreationForm ويضيف حقل الجنس (gender) كحقل مطلوب.

    This form is used to create new accounts for employees seeking jobs.
    It inherits from UserCreationForm and adds gender field as required.
    """

    def __init__(self, *args, **kwargs):
        """
        تهيئة النموذج - Initialize the form

        تقوم هذه الدالة بتخصيص تسميات الحقول ونصوص المساعدة
        وإعدادات أخرى للنموذج.

        This function customizes field labels, help texts, and other
        form settings.
        """
        # استدعاء دالة التهيئة للنموذج الأب
        # Call parent form's __init__ method
        UserCreationForm.__init__(self, *args, **kwargs)

        # جعل حقل الجنس مطلوباً
        # Make gender field required
        self.fields['gender'].required = True

        # تخصيص تسميات الحقول باللغة العربية
        # Customize field labels in Arabic
        self.fields['first_name'].label = _("الاسم الأول :")
        self.fields['last_name'].label = _("الاسم الأخير :")
        self.fields['password1'].label = _("كلمة المرور :")
        self.fields['password2'].label = _("تأكيد كلمة المرور :")
        self.fields['email'].label = _("البريد الإلكتروني :")
        self.fields['gender'].label = _("الجنس :")

        # تخصيص نصوص المساعدة (placeholders) باللغة العربية
        # Customize placeholder texts in Arabic
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل الاسم الأول'),
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل الاسم الأخير'),
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': _('أدخل البريد الإلكتروني'),
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': _('أدخل كلمة المرور'),
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': _('أدخل تأكيد كلمة المرور'),
            }
        )

    class Meta:
        """
        إعدادات النموذج - Form Configuration

        تحدد هذه الكلاس النموذج المرتبط والحقول المطلوبة للنموذج.

        This class defines the associated model and required fields for the form.
        """
        model = User  # النموذج المرتبط - Associated model

        # الحقول المطلوبة للنموذج - Required fields for the form
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def clean_gender(self):
        """
        تنظيف وفحص حقل الجنس - Clean and validate gender field

        تتحقق هذه الدالة من أن حقل الجنس ليس فارغاً وتقوم بإرجاع القيمة المنظفة.

        This function validates that gender field is not empty and returns the cleaned value.
        """
        gender = self.cleaned_data.get('gender')
        if not gender:
            # رسالة خطأ باللغة العربية - Error message in Arabic
            raise forms.ValidationError(_("الجنس مطلوب"))
        return gender

    def save(self, commit=True):
        """
        حفظ المستخدم - Save the user

        تقوم هذه الدالة بحفظ المستخدم الجديد مع تحديد دوره كموظف.

        This function saves the new user with employee role specified.
        """
        # حفظ المستخدم دون الالتزام بالحفظ النهائي أولاً
        # Save user without final commit first
        user = UserCreationForm.save(self, commit=False)

        # تحديد دور المستخدم كموظف - Set user role as employee
        user.role = "employee"

        # الحفظ النهائي إذا كان مطلوباً - Final save if commit is True
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    """
    نموذج تسجيل صاحب العمل - Employer Registration Form

    هذا النموذج يُستخدم لإنشاء حسابات جديدة لأصحاب العمل الذين يريدون نشر الوظائف.
    يستخدم الاسم الأول لحفظ اسم الشركة والاسم الأخير لحفظ عنوان الشركة.

    This form is used to create new accounts for employers who want to post jobs.
    It uses first_name to store company name and last_name to store company address.
    """

    def __init__(self, *args, **kwargs):
        """
        تهيئة نموذج صاحب العمل - Initialize employer form

        تقوم هذه الدالة بتخصيص الحقول لتناسب متطلبات صاحب العمل
        وتستخدم الاسم الأول لاسم الشركة والاسم الأخير لعنوان الشركة.

        This function customizes fields for employer requirements
        using first_name for company name and last_name for company address.
        """
        # استدعاء دالة التهيئة للنموذج الأب
        # Call parent form's __init__ method
        UserCreationForm.__init__(self, *args, **kwargs)

        # جعل الحقول مطلوبة - Make fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # تخصيص تسميات الحقول باللغة العربية - Customize field labels in Arabic
        self.fields['first_name'].label = _("اسم الشركة")
        self.fields['last_name'].label = _("عنوان الشركة")
        self.fields['password1'].label = _("كلمة المرور")
        self.fields['password2'].label = _("تأكيد كلمة المرور")

        # تخصيص نصوص المساعدة باللغة العربية - Customize placeholders in Arabic
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل اسم الشركة'),
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل عنوان الشركة'),
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': _('أدخل البريد الإلكتروني'),
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': _('أدخل كلمة المرور'),
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': _('أدخل تأكيد كلمة المرور'),
            }
        )
    class Meta:
        """
        إعدادات نموذج صاحب العمل - Employer Form Configuration

        تحدد هذه الكلاس النموذج المرتبط والحقول المطلوبة لنموذج صاحب العمل.

        This class defines the associated model and required fields for employer form.
        """
        model = User  # النموذج المرتبط - Associated model

        # الحقول المطلوبة لنموذج صاحب العمل - Required fields for employer form
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """
        حفظ صاحب العمل - Save the employer

        تقوم هذه الدالة بحفظ المستخدم الجديد مع تحديد دوره كصاحب عمل.

        This function saves the new user with employer role specified.
        """
        # حفظ المستخدم دون الالتزام بالحفظ النهائي أولاً
        # Save user without final commit first
        user = UserCreationForm.save(self, commit=False)

        # تحديد دور المستخدم كصاحب عمل - Set user role as employer
        user.role = "employer"

        # الحفظ النهائي إذا كان مطلوباً - Final save if commit is True
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    نموذج تسجيل الدخول - User Login Form

    هذا النموذج يُستخدم لتسجيل دخول المستخدمين (الموظفين وأصحاب العمل)
    إلى نظام بوابة الوظائف. يتحقق من صحة البريد الإلكتروني وكلمة المرور.

    This form is used for user login (employees and employers) to the Job Portal system.
    It validates email and password credentials.
    """

    # حقل البريد الإلكتروني - Email field
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': _('البريد الإلكتروني'),
        })
    )

    # حقل كلمة المرور - Password field
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('كلمة المرور'),
        })
    )

    def clean(self, *args, **kwargs):
        """
        تنظيف وفحص بيانات تسجيل الدخول - Clean and validate login data

        تقوم هذه الدالة بالتحقق من صحة البريد الإلكتروني وكلمة المرور
        وتتحقق من وجود المستخدم وحالة حسابه.

        This function validates email and password, checks user existence
        and account status.
        """
        # الحصول على البيانات المدخلة - Get entered data
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # التحقق من وجود البريد الإلكتروني وكلمة المرور
        # Check if email and password are provided
        if email and password:
            # محاولة المصادقة - Try authentication
            self.user = authenticate(email=email, password=password)

            try:
                # البحث عن المستخدم في قاعدة البيانات - Find user in database
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # رسالة خطأ في حالة عدم وجود المستخدم - Error if user doesn't exist
                raise forms.ValidationError(_("المستخدم غير موجود"))

            # التحقق من صحة كلمة المرور - Check password validity
            if not user.check_password(password):
                # رسالة خطأ في حالة عدم تطابق كلمة المرور - Error if password doesn't match
                raise forms.ValidationError(_("كلمة المرور غير صحيحة"))

            # التحقق من حالة الحساب - Check account status
            if not user.is_active:
                # رسالة خطأ في حالة الحساب غير نشط - Error if account is not active
                raise forms.ValidationError(_("الحساب غير نشط"))

        # استدعاء دالة التنظيف للنموذج الأب - Call parent form's clean method
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        """
        الحصول على المستخدم - Get the user

        ترجع هذه الدالة كائن المستخدم بعد المصادقة الناجحة.

        This function returns the user object after successful authentication.
        """
        return self.user



class EmployeeProfileEditForm(forms.ModelForm):
    """
    نموذج تعديل ملف الموظف - Employee Profile Edit Form

    هذا النموذج يُستخدم لتعديل المعلومات الشخصية للموظف مثل الاسم والجنس.
    يسمح بتحديث البيانات الأساسية لحساب الموظف.

    This form is used to edit employee personal information such as name and gender.
    It allows updating basic account information for employees.
    """

    def __init__(self, *args, **kwargs):
        """
        تهيئة نموذج تعديل الملف الشخصي - Initialize profile edit form

        تقوم هذه الدالة بتخصيص نصوص المساعدة للحقول
        وإعداد النموذج لتعديل بيانات الموظف.

        This function customizes placeholder texts for fields
        and sets up the form for employee data editing.
        """
        # استدعاء دالة التهيئة للنموذج الأب - Call parent form's __init__ method
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)

        # تخصيص نصوص المساعدة باللغة العربية - Customize placeholders in Arabic
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل الاسم الأول'),
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': _('أدخل الاسم الأخير'),
            }
        )

    class Meta:
        """
        إعدادات نموذج تعديل الملف الشخصي - Profile Edit Form Configuration

        تحدد هذه الكلاس النموذج المرتبط والحقول المتاحة للتعديل.

        This class defines the associated model and editable fields.
        """
        model = User  # النموذج المرتبط - Associated model

        # الحقول المتاحة للتعديل - Editable fields
        fields = ["first_name", "last_name", "gender"]
