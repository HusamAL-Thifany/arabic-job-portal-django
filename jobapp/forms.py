from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.utils.translation import gettext_lazy as _

from jobapp.models import *
from ckeditor.widgets import CKEditorWidget


    

class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = _("عنوان الوظيفة :")
        self.fields['location'].label = _("موقع الوظيفة :")
        self.fields['salary'].label = _("الراتب :")
        self.fields['description'].label = _("وصف الوظيفة :")
        self.fields['tags'].label = _("العلامات :")
        self.fields['last_date'].label = _("الموعد النهائي للتقديم :")
        self.fields['company_name'].label = _("اسم الشركة :")
        self.fields['url'].label = _("الموقع الإلكتروني :")


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': _('مثال : مطور برمجيات'),
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': _('مثال : السعودية'),
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': _('800 - 1200 دولار'),
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': _('استخدم فاصلة للفصل. مثال: بايثون، جافا سكريبت'),
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': _('YYYY-MM-DD'),

            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': _('اسم الشركة'),
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': _('https://example.com'),
            }
        )


    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError(_("نوع الوظيفة مطلوب"))
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError(_("التصنيف مطلوب"))
        return category


    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:

            job.save()
        return job




class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']




class JobEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = _("عنوان الوظيفة :")
        self.fields['location'].label = _("موقع الوظيفة :")
        self.fields['salary'].label = _("الراتب :")
        self.fields['description'].label = _("وصف الوظيفة :")
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = _("الموعد النهائي :")
        self.fields['company_name'].label = _("اسم الشركة :")
        self.fields['url'].label = _("الموقع الإلكتروني :")


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': _('مثال : مطور برمجيات'),
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': _('مثال : السعودية'),
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': _('800 - 1200 دولار'),
            }
        )
        # self.fields['tags'].widget.attrs.update(
        #     {
        #         'placeholder': 'Use comma separated. eg: Python, JavaScript ',
        #     }
        # )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': _('YYYY-MM-DD'),
            }
        )
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': _('اسم الشركة'),
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': _('https://example.com'),
            }
        )


        last_date = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': _('اسم الخدمة'),
                    'class' : 'datetimepicker1'
                }))

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError(_("نوع الوظيفة مطلوب"))
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError(_("التصنيف مطلوب"))
        return category


    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)

        if commit:
            job.save()
        return job


class EmailCommunicationForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        label=_("عنوان الرسالة"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('أدخل عنوان الرسالة')
        })
    )
    subject = forms.CharField(
        max_length=200,
        label=_("الموضوع"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('أدخل موضوع الرسالة')
        })
    )
    message = forms.CharField(
        label=_("الرسالة"),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': _('اكتب رسالتك هنا...')
        })
    )

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.recipient = kwargs.pop('recipient', None)
        super().__init__(*args, **kwargs)

        if self.sender:
            self.fields['sender_email'] = forms.CharField(
                initial=self.sender.email,
                label=_("المرسل"),
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                })
            )

        if self.recipient:
            self.fields['recipient_email'] = forms.CharField(
                initial=self.recipient.email,
                label=_("المستلم"),
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                })
            )
