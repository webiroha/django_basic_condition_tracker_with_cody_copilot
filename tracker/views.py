from django.shortcuts import render, redirect
from .forms import SupplementRecordForm
from .models import SupplementRecord

def supplement_record(request):
    if request.method == 'POST':
        form = SupplementRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplement_record')
    else:
        form = SupplementRecordForm()

    records = SupplementRecord.objects.all()
    return render(request, 'tracker/supplement_record.html', {
        'form': form,
        'records': records
    })
