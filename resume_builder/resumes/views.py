from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

# Razorpay setup (optional)
client = None
if not getattr(settings, 'DISABLE_PAYMENT', True):
    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    except AttributeError:
        pass  # Razorpay keys not set yet

def create_resume(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Extract education list of (degree, institution, year)
        education = list(zip(
            request.POST.getlist('education_degree[]'),
            request.POST.getlist('education_institution[]'),
            request.POST.getlist('education_year[]')
        ))

        # Extract experience list of (title, company, duration, description)
        experience = list(zip(
            request.POST.getlist('experience_title[]'),
            request.POST.getlist('experience_company[]'),
            request.POST.getlist('experience_duration[]'),
            request.POST.getlist('experience_description[]')
        ))

        # Extract skills list
        skills = request.POST.getlist('skills_item[]')

        # Store data as JSON
        data = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'education': education,
            'experience': experience,
            'skills': skills,
        }

        resume = Resume.objects.create(data=data)
        return redirect('preview_resume', uuid=resume.uuid)

    return render(request, 'resumes/create.html')

def preview_resume(request, uuid):
    resume = get_object_or_404(Resume, uuid=uuid)
    payment_order = None
    if settings.DISABLE_PAYMENT:
        resume.is_paid = True
        resume.save()
    return render(request, 'resumes/preview.html', {
        'resume': resume,
        'payment_order': payment_order,
        'RAZORPAY_KEY_ID': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        'DISABLE_PAYMENT': getattr(settings, 'DISABLE_PAYMENT', True),
    })

@csrf_exempt
def payment_success(request, uuid):
    resume = get_object_or_404(Resume, uuid=uuid)
    resume.is_paid = True
    resume.save()
    return redirect('download_pdf', uuid=uuid)

# def download_pdf(request, uuid):
#     resume = get_object_or_404(Resume, uuid=uuid)
#     if not resume.is_paid:
#         return HttpResponse("Payment required.", status=403)

#     html = render_to_string('resumes/pdf_template.html', {'resume': resume})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=\"resume_{uuid}.pdf\"'
#     weasyprint.HTML(string=html).write_pdf(response)
#     return response

def download_pdf(request, uuid):
    resume = get_object_or_404(Resume, uuid=uuid)
    if not resume.is_paid:
        return HttpResponse("Payment required.", status=403)

    # Copy and clean data to prevent polluting original
    cleaned_data = dict(resume.data)

    # Remove empty skills/certs
    cleaned_data['skills'] = [s for s in cleaned_data.get('skills', []) if s and s.strip()]
    cleaned_data['certificates'] = [c for c in cleaned_data.get('certificates', []) if c and c.strip()]
    cleaned_data['experience'] = [e for e in cleaned_data.get('experience', []) if any(e)]
    cleaned_data['education'] = [e for e in cleaned_data.get('education', []) if any(e)]

    html = render_to_string('resumes/pdf_template.html', {
        'resume': {
            'data': cleaned_data,
            'uuid': resume.uuid,
            'is_paid': True
        }
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{uuid}.pdf"'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import ResumeForm
# from .models import Resume
# import uuid
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint

# client = None
# if not getattr(settings, 'DISABLE_PAYMENT', True):
#     try:
#         import razorpay
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     except AttributeError:
#         pass  # Razorpay keys not set yet

# def create_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST)
#         if form.is_valid():
#             resume = Resume.objects.create(data=form.cleaned_data)
#             return redirect('preview_resume', uuid=resume.uuid)
#     else:
#         form = ResumeForm()
#     return render(request, 'resumes/create.html', {'form': form})

# def preview_resume(request, uuid):
#     resume = get_object_or_404(Resume, uuid=uuid)
#     payment_order = None
#     if settings.DISABLE_PAYMENT:
#         resume.is_paid = True
#         resume.save()
#     return render(request, 'resumes/preview.html', {'resume': resume, 'payment_order': payment_order, 'RAZORPAY_KEY_ID': getattr(settings, 'RAZORPAY_KEY_ID', '')})

# @csrf_exempt
# def payment_success(request, uuid):
#     resume = get_object_or_404(Resume, uuid=uuid)
#     resume.is_paid = True
#     resume.save()
#     return redirect('download_pdf', uuid=uuid)

# def download_pdf(request, uuid):
#     resume = get_object_or_404(Resume, uuid=uuid)
#     if not resume.is_paid:
#         return HttpResponse("Payment required.", status=403)

#     html = render_to_string('resumes/pdf_template.html', {'resume': resume})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="resume_{uuid}.pdf"'
#     weasyprint.HTML(string=html).write_pdf(response)
#     return response