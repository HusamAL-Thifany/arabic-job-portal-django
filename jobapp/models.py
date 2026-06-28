from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
User = get_user_model()


from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


JOB_TYPE = (
    ('1', _("Full time")),
    ('2', _("Part time")),
    ('3', _("Internship")),
)

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    

class Job(models.Model):

    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    description = RichTextField(verbose_name=_("Description"))
    tags = TaggableManager(verbose_name=_("Tags"))
    location = models.CharField(max_length=300, verbose_name=_("Location"))
    job_type = models.CharField(choices=JOB_TYPE, max_length=1, verbose_name=_("Job Type"))
    category = models.ForeignKey(Category,related_name='Category', on_delete=models.CASCADE, verbose_name=_("Category"))
    salary = models.CharField(max_length=30, blank=True, verbose_name=_("Salary"))
    company_name = models.CharField(max_length=300, verbose_name=_("Company Name"))
    company_description = RichTextField(blank=True, null=True, verbose_name=_("Company Description"))
    url = models.URLField(max_length=200, verbose_name=_("URL"))
    last_date = models.DateField(verbose_name=_("Last Date"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Published"))
    is_closed = models.BooleanField(default=False, verbose_name=_("Is Closed"))
    timestamp = models.DateTimeField(auto_now=True, verbose_name=_("Timestamp"))


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

 

class Applicant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name=_("Job"))
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_("Timestamp"))


    def __str__(self):
        return self.job.title

    class Meta:
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")


  

class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name=_("Job"))
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_("Timestamp"))


    def __str__(self):
        return self.job.title

    class Meta:
        verbose_name = _("Bookmarked Job")
        verbose_name_plural = _("Bookmarked Jobs")
