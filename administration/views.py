from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileForm, CampDetailsForm, DoctorForm, CampServiceForm, AppointmentForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from administration.models import profile, camp_details, doctor, camp_services, appointment
import json
from django.contrib.auth.models import User
from django.db.models import Max

# Create your views here.
@login_required
def home(request):
    camps = camp_details.objects.all()
    camp_total = camp_details.objects.all().count()
    total_users = User.objects.all().count()
    camp_active = camp_details.objects.filter(camp_register_active=True).count()
    camp_inactive = camp_details.objects.filter(camp_register_active=False).count()
    camp_data = [{'lat': camp.latitude, 'lng': camp.longitude, 'description': camp.description} for camp in camps]
    return render(request, 'home.html', {'camp_data': json.dumps(camp_data),'camp_total':camp_total,'total_users':total_users,'camp_active':camp_active,'camp_inactive':camp_inactive})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            subject = 'Welcome to Our Website!'
            message = 'Dear {},\n\nThank you for registering on our website. You are now able to log in.\n\nBest regards,\nThe Website Team'.format(user.username)
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])


            messages.success(request, 'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'register_form': form})

@login_required
def camp_organizer_request(request):
    submitted_profiles = profile.objects.filter(submitted_application=True, camp_register=False)
    return render(request, 'camp/camp_organizer_request.html', {'submitted_profiles': submitted_profiles})

@login_required
def camp_organizer_profile_detail(request,username):
    user_profile = get_object_or_404(profile, user_name__username=username)
    return render(request, 'camp/organizer_user_profile.html', {'user_profile': user_profile})

@login_required
def approve_application(request, username):
    # Retrieve the user's profile
    user_profile = get_object_or_404(profile, user_name__username=username)

    # Set camp_register to True
    user_profile.camp_register = True
    user_profile.save()

    # Send acknowledgment email to the user
    subject = 'Camp Registration Approval'
    message = 'Dear {},\n\nYour camp registration has been approved. Thank you for your registration.\n\nBest regards,\nThe Camp Registration Team'.format(user_profile.user_name.username)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_profile.user_name.email])

    # Redirect to a success page or another view
    return redirect('camp_organizer_request')

@login_required
def deny_application(request, username):
    # Retrieve the user's profile
    user_profile = get_object_or_404(profile, user_name__username=username)

    # Deny the application
    user_profile.camp_register = False
    user_profile.save()

    # Send notification email to the user
    subject = 'Camp Registration Denial'
    message = 'Dear {},\n\nWe regret to inform you that your camp registration has been denied.\n\nBest regards,\nThe Camp Registration Team'.format(user_profile.user_name.username)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_profile.user_name.email])

    # Redirect to a success page or another view
    return redirect('camp_organizer_request')


@login_required
def register_camp_org(request):
    user_profile = profile.objects.get(user_name=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            user_profile.submitted_application = True
            user_profile.save()

            user_email_subject = 'Camp Organizer Registration Submission Acknowledgement'
            user_email_message = 'Dear {},\n\nYour request for registering as a camp organizer has been received. We will review your application shortly.\n\nThank you for your interest.\n\nBest regards,\nThe Camp Registration Team'.format(request.user.username)
            send_mail(user_email_subject, user_email_message, settings.EMAIL_HOST_USER, [request.user.email])

            subject = 'New Camp Organizer Registration Request'
            message = 'User {} has requested for registering as a camp organizer. Please take appropriate action.'.format(request.user.username)
            from_email = settings.EMAIL_HOST_USER
            to_email = settings.SUPER_ADMIN_EMAIL
            send_mail(subject, message, from_email, [to_email])

            return redirect('camp_register')
    else:
        form = ProfileForm(instance=user_profile)
    
    submitted_application = user_profile.submitted_application
    camp_register = user_profile.camp_register
    return render(request, 'camp/camp_register.html', {'form': form, 'submitted_application': submitted_application, 'camp_register': camp_register})

@login_required
def user_camps(request):
    if request.user.is_superuser:
        # User is a super admin, retrieve all camp details
        user_camps = camp_details.objects.all()
    else:
        # User is not a super admin, retrieve camps created by this user
        user_camps = camp_details.objects.filter(createdby=request.user)
    
    return render(request, 'camp/all_camps_user.html', {'user_camps': user_camps})

@login_required
def create_camp_view(request):
    if request.method == 'POST':
        form = CampDetailsForm(request.POST)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.createdby = request.user
            camp.save()
            return redirect('my_camps')  # Redirect to camp details page
    else:
        form = CampDetailsForm()
    return render(request, 'camp/register_camp.html', {'form': form})

@login_required
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.user, request.POST)
        if form.is_valid():
            doctor = form.save()
            return redirect('list_user_doctors')  # Redirect to doctor detail page
    else:
        form = DoctorForm(request.user)
    
    return render(request, 'camp/add_doctor.html', {'form': form})

@login_required
def list_doctors_for_user(request):
    # Get the current logged-in user
    user = request.user

    # Filter camps created by the user
    user_camps = camp_details.objects.filter(createdby=user)

    # Get all doctors associated with the user's camps
    doctors = doctor.objects.filter(camp_name__in=user_camps)

    return render(request, 'camp/doctor_list.html', {'doctors': doctors})

@login_required
def list_camp_services_for_user(request):
    # Get the current logged-in user
    user = request.user

    # Filter camps created by the user
    user_camps = camp_details.objects.filter(createdby=user)

    # Get all camp services associated with the user's camps
    camp_service = camp_services.objects.filter(camp_name__in=user_camps)

    return render(request, 'camp/camp_service_list.html', {'camp_services': camp_service})

@login_required
def create_camp_service(request):
    if request.method == 'POST':
        form = CampServiceForm(request.user, request.POST)
        if form.is_valid():
            camp_service = form.save()
            return redirect('list_user_camp_services')  # Redirect to camp service detail page
    else:
        form = CampServiceForm(request.user)
    
    return render(request, 'camp/camp_service_form.html', {'form': form})

@login_required
def camp_details_view(request, camp_id):
    # Retrieve the camp details object
    camp = get_object_or_404(camp_details, pk=camp_id)
    doctors = doctor.objects.filter(camp_name=camp)
    camp_service = camp_services.objects.filter(camp_name = camp)

    context = {
        'camp': camp,
        'doctors': doctors,
        'camp_ser': camp_service,
    }
    return render(request, 'camp/camp_detail.html', context)

@login_required
def camp_delete(request, pk):
    camp = get_object_or_404(camp_details, pk=pk)
    camp.delete()
    return redirect('my_camps')

@login_required
def all_camps(request):
    camps = camp_details.objects.filter(camp_register_active=True)
    user = request.user
    user_appointments = appointment.objects.filter(user_name=user)
    camp_appointments = {appointment.camp_name_id: appointment for appointment in user_appointments}

    context = {
        'camps': camps,
        'user_appointments': camp_appointments,
        'user': request.user,
    }
    return render(request, 'camp/all_camps.html', context)

@login_required
def register_appointment(request, camp_id):
    camp = get_object_or_404(camp_details, pk=camp_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_date = form.cleaned_data['appointment_date']

            # Validate appointment date against camp start and end dates
            if camp.start_date_time.date() and appointment_date < camp.start_date_time.date():
                messages.error(request, 'Appointment date cannot be before the start date of the camp.')
            elif camp.end_date_time.date() and appointment_date > camp.end_date_time.date():
                messages.error(request, 'Appointment date cannot be after the end date of the camp.')
            else:
                # Create appointment if date is valid
                appointment_obj = form.save(commit=False)
                appointment_obj.user_name = request.user
                appointment_obj.camp_name = camp
                max_token = appointment.objects.filter(camp_name=camp).aggregate(Max('token_no'))['token_no__max'] or 0
                appointment_obj.token_no = max_token + 1
                appointment_obj.save()
                # Send registration email or perform other actions
                messages.success(request, 'Appointment registered successfully.')
                return redirect('home')
        
    else:
        form = AppointmentForm()

    return render(request, 'camp/register_appointment.html', {'camp': camp, 'form': form})

def send_registration_email(appointment_obj):
    subject = 'Congratulations! You have registered for a camp'
    message = f'Hello {appointment_obj.user_name.username},\n\n'
    message += f'You have successfully registered for the camp "{appointment_obj.camp_name.camp_name}" '
    message += f'on {appointment_obj.appointment_date}.\n'
    message += f'Your Appointment id is: {appointment_obj.appointment_number}.\n'
    message += 'Enjoy your time at the camp!\n\n'
    message += 'Best regards,\nThe Camp Team'

    send_mail(subject, message, settings.EMAIL_HOST_USER, [appointment_obj.user_name.email])

def view_campregistration_details(request, camp_id, user):
    camp_detail = get_object_or_404(camp_details, pk=camp_id)
    user_detail = get_object_or_404(User, pk=user)
    appointments = get_object_or_404(appointment, camp_name = camp_detail, user_name=user_detail)
    return render(request,'camp/view_registration_details.html', {'camp_detail':camp_detail, 'user_detail':user_detail, 'appointments':appointments})