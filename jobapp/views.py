from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
User = get_user_model()


def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        job_lists=[]
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'job_lists':job_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
    'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)

@cache_page(60 * 15)
def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    توفير إمكانية إنشاء إعلان وظيفة
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.is_published = True
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'تم نشر وظيفتك بنجاح! يرجى انتظار المراجعة.')
            return redirect(reverse("jobapp:single-job", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    توفير إمكانية عرض تفاصيل الوظيفة
    """
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id,job , 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        يمكن للمستخدم البحث عن الوظائف باستخدام حقول متعددة

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'تم التقدم للوظيفة بنجاح!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'لقد تقدمت لهذه الوظيفة مسبقاً!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'تم حذف إعلان الوظيفة بنجاح!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'تم إغلاق الوظيفة بنجاح!')
        except:
            messages.error(request, 'حدث خطأ ما!')
            
    return redirect('jobapp:dashboard')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'تم حذف الوظيفة المحفوظة بنجاح!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'تم حفظ الوظيفة بنجاح!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'لقد قمت بحفظ هذه الوظيفة مسبقاً!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    التعامل مع تحديث الوظيفة

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'تم تحديث إعلان الوظيفة بنجاح!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def accept_applicant_view(request, applicant_id):
    """
    قبول المتقدم وإرسال إشعار بالبريد الإلكتروني
    """
    try:
        # Get the applicant (which is actually a User)
        applicant = get_object_or_404(User, id=applicant_id)

        # Send acceptance email
        subject = 'تهانينا! تم قبولك في الوظيفة'
        message = f'''
        مرحبا {applicant.get_full_name}،

        نود أن نهنئك على قبولك في الوظيفة!

        لقد تم مراجعة طلبك وتقرر قبوله. سنتواصل معك قريباً لترتيب التفاصيل.

        مع خالص التحية،
        فريق التوظيف
        '''
        html_message = f'''
        <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c3e50;">تهانينا! تم قبولك في الوظيفة</h2>
            <p>مرحبا <strong>{applicant.get_full_name}</strong>،</p>
            <p>نود أن نهنئك على قبولك في الوظيفة!</p>
            <p>لقد تم مراجعة طلبك وتقرر قبوله. سنتواصل معك قريباً لترتيب التفاصيل.</p>
            <hr>
            <p style="color: #7f8c8d; font-size: 12px;">مع خالص التحية،<br>فريق التوظيف</p>
        </div>
        '''

        send_mail(
            subject,
            message,
            'wwohohoasas@gmail.com',  # From email
            [applicant.email],  # To email
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(request, f'تم قبول المتقدم {applicant.get_full_name} وإرسال إشعار بالبريد الإلكتروني!')
        return redirect('jobapp:applicant-details', id=applicant_id)

    except Exception as e:
        messages.error(request, f'حدث خطأ أثناء قبول المتقدم: {str(e)}')
        return redirect('jobapp:applicant-details', id=applicant_id)


@login_required(login_url=reverse_lazy('account:login'))
def email_communication_view(request, recipient_id=None):
    """
    التعامل مع التواصل عبر البريد الإلكتروني بين المستخدمين
    """
    recipient = None
    if recipient_id:
        recipient = get_object_or_404(User, id=recipient_id)

    if request.method == 'POST':
        form = EmailCommunicationForm(request.POST, sender=request.user, recipient=recipient)

        if form.is_valid():
            try:
                # Send email
                subject = form.cleaned_data['subject']
                title = form.cleaned_data['title']
                message = form.cleaned_data['message']

                # Create full email content
                full_message = f'''
                عنوان الرسالة: {title}

                {message}

                ---
                تاريخ الإرسال: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
                المرسل: {request.user.get_full_name} ({request.user.email})
                '''

                html_message = f'''
                <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h3 style="color: #2c3e50;">{title}</h3>
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        {message.replace(chr(10), '<br>')}
                    </div>
                    <hr>
                    <p style="color: #7f8c8d; font-size: 12px;">
                        تاريخ الإرسال: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                        المرسل: {request.user.get_full_name} ({request.user.email})
                    </p>
                </div>
                '''
    
                send_mail(
                    subject,
                    full_message,
                    'wwohohoasas@gmail.com',  # From email
                    [form.cleaned_data['recipient_email']],  # To email
                    html_message=html_message,
                    fail_silently=False,
                )


                messages.success(request, 'تم إرسال الرسالة بنجاح!')
                return redirect('jobapp:dashboard')

            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إرسال الرسالة: {str(e)}')
    else:
        form = EmailCommunicationForm(sender=request.user, recipient=recipient)

    context = {
        'form': form,
        'recipient': recipient
    }

    return render(request, 'jobapp/email-communication.html', context)
