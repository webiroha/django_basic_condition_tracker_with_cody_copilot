from django.shortcuts import render, redirect, get_object_or_404
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

def delete_record(request, record_id):
    record = get_object_or_404(SupplementRecord, id=record_id)
    record.delete()
    return redirect('supplement_record')
