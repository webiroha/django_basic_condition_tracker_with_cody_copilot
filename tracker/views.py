from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SupplementRecordForm
from .models import SupplementRecord
from django.http import JsonResponse
import json
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import logging
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

logger = logging.getLogger('tracker')

@require_http_methods(["GET", "POST"])
@ratelimit(key='user_or_ip', rate='10/m')
@login_required
def supplement_record(request):
    """
    Handle supplement record creation and listing.

    GET: Display form and list of user's supplement records
    POST: Create new supplement record

    Requires authentication
    """
    if request.method == 'POST':
        form = SupplementRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, "Supplement record added successfully!")
            return redirect('supplement_record')
    else:
        form = SupplementRecordForm()
    records = SupplementRecord.objects.filter(user=request.user).order_by('-intake_datetime')
    return render(request, 'tracker/supplement_record.html', {
        'form': form,
        'records': records
    })

def choose_mode(request):
    if request.user.is_authenticated:
        return redirect('supplement_record')
    return redirect('login')

def edit_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id, user=request.user)  # Add user check
    if request.method == 'POST':
        form = SupplementRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('supplement_record')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupplementRecordForm(instance=record)

    return render(request, 'tracker/edit_record.html', {
        'form': form,
        'record': record
    })

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted successfully.')
        return redirect('supplement_record')

    return redirect('supplement_record')

@require_http_methods(["POST"])
@csrf_protect
@ratelimit(key='user_or_ip', rate='30/m')
def sync_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    local_records = data.get('records', [])
    if not isinstance(local_records, list):
        return JsonResponse({'error': 'Invalid records format'}, status=400)

    try:
        with transaction.atomic():
            for record in local_records:
                SupplementRecord.objects.create(
                    user=request.user,
                    supplement_name=record['supplement_name'],
                    intake_datetime=record['intake_datetime'],
                    amount=record['amount'],
                    local_id=record['id']
                )
    except KeyError as e:
        logger.error(f"Sync data error: {str(e)}")
        return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)

    return JsonResponse({'status': 'success'})

@ratelimit(key='ip', rate='5/m', method=['POST'])
def login_view(request):
    # Initialize counters
    max_attempts = 5
    failed_attempts = request.session.get('failed_attempts', 0)
    remaining_attempts = max_attempts - failed_attempts

    # Clear any existing messages
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['failed_attempts'] = 0
                return redirect('supplement_record')
            else:
                failed_attempts += 1
                request.session['failed_attempts'] = failed_attempts
                remaining_attempts = max_attempts - failed_attempts
                logger.warning(f"Failed login attempt for username: {username}")
                messages.error(request, "Invalid username or password.")
                return render(request, 'tracker/login.html', {
                    'form': form,
                    'failed_attempts': failed_attempts,
                    'remaining_attempts': remaining_attempts,
                    'max_attempts': max_attempts
                })
        else:
            failed_attempts += 1
            request.session['failed_attempts'] = failed_attempts
            remaining_attempts = max_attempts - failed_attempts
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        request.session['failed_attempts'] = 0

    return render(request, 'tracker/login.html', {
        'form': form,
        'failed_attempts': failed_attempts,
        'remaining_attempts': remaining_attempts,
        'max_attempts': max_attempts
    })

@ratelimit(key='ip', rate='3/m', method=['POST'])
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Supplement Tracker.")
            return redirect('supplement_record')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

def logout_view(request):
    # Clear messages before logout
    messages.get_messages(request).used = True
    logout(request)
    if 'failed_attempts' in request.session:
        del request.session['failed_attempts']
    return redirect('login')
