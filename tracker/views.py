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

@require_http_methods(["POST"])
@login_required
@csrf_protect
def delete_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id, user=request.user)  # Add user check
    record.delete()
    messages.success(request, "Record deleted successfully!")
    return redirect('supplement_record')

@csrf_protect
def sync_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    data = json.loads(request.body)
    local_records = data.get('records', [])

    for record in local_records:
        SupplementRecord.objects.create(
            user=request.user,
            supplement_name=record['supplement_name'],
            intake_datetime=record['intake_datetime'],
            amount=record['amount'],
            local_id=record['id']
        )

    return JsonResponse({'status': 'success'})

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('supplement_record')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('supplement_record')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})
