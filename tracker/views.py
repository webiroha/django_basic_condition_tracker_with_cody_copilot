from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SupplementRecordForm
from .models import SupplementRecord
from django.http import JsonResponse
import json

def supplement_record(request):
    if not (request.user.is_authenticated or request.session.get('is_guest')):
        return redirect('choose_mode')

    if request.method == 'POST':
        form = SupplementRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            if request.user.is_authenticated:
                record.user = request.user
            record.save()
            return redirect('supplement_record')
    else:
        form = SupplementRecordForm()

    if request.user.is_authenticated:
        records = SupplementRecord.objects.filter(user=request.user)
    else:
        records = SupplementRecord.objects.filter(user=None)

    return render(request, 'tracker/supplement_record.html', {
        'form': form,
        'records': records
    })

def choose_mode(request):
    # If user is already logged in, redirect to supplement record page
    if request.user.is_authenticated:
        return redirect('supplement_record')

    # If user is in guest mode, redirect to supplement record page
    if request.session.get('is_guest'):
        return redirect('supplement_record')

    if request.method == 'POST':
        if 'guest' in request.POST:
            request.session['is_guest'] = True
            return redirect('supplement_record')
        elif 'login' in request.POST:
            return redirect('login')

    return render(request, 'tracker/choose_mode.html')

def edit_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id)
    if request.method == 'POST':
        form = SupplementRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('supplement_record')
    else:
        form = SupplementRecordForm(instance=record)

    return render(request, 'tracker/edit_record.html', {
        'form': form,
        'record': record
    })

def delete_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id)
    record.delete()
    return redirect('supplement_record')

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
